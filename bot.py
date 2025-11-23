import discord, asyncio
from discord.ext import commands
from discord.ui import Select, View
from config import DISCORD_TOKEN
from logic import youtube_search_comprehensive 
from reminders import save_reminder, start_reminders
from quiz import QUIZ_QUESTIONS, save_score

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CLASSES = list(QUIZ_QUESTIONS.keys()) 

@bot.event
async def on_ready():
    print(f"🤖 Bot olarak giriş yapıldı: {bot.user}")
    bot.loop.create_task(start_reminders(bot))

@bot.command()
async def sinif(ctx):
    options = [discord.SelectOption(label=c) for c in CLASSES]
    select = Select(placeholder="Sınıf seçin", options=options)

    async def callback(interaction):
        selected_class = select.values[0]
        await interaction.response.send_message(f"Seçilen sınıf: **{selected_class}**")

        lessons = list(QUIZ_QUESTIONS[selected_class].keys())
        lesson_options = [discord.SelectOption(label=t) for t in lessons]
        lesson_select = Select(placeholder="Ders seçin", options=lesson_options)

        async def lesson_callback(interaction_lesson):
            selected_lesson_name = lesson_select.values[0]
            
            quiz_topic_questions = QUIZ_QUESTIONS[selected_class][selected_lesson_name]
            all_unit_names = [q['question'] for q in quiz_topic_questions]
            
            await interaction_lesson.response.send_message(
                f"Arama başlatılıyor: **{selected_class} {selected_lesson_name}** dersinin **{len(all_unit_names)}** ana ünitesi ve **Genel Tekrar** videosu aranıyor...", 
                ephemeral=True
            )

            videos = youtube_search_comprehensive(selected_class, selected_lesson_name, all_unit_names)
            
            if videos:
                embed = discord.Embed(
                    title=f"📹 {selected_class} {selected_lesson_name} Kapsamlı Konu Anlatım Listesi",
                    description=f"Toplam **{len(videos)}** video bulundu (Konular + Genel Tekrar)",
                    color=0x3498db # Mavi renk
                )
                
                for i, video in enumerate(videos):
                    embed.add_field(name=f"**{i+1}. {video['title']}**", 
                                    value=f"[[Videoyu İzle]]({video['url']})", 
                                    inline=False)
                
                await interaction_lesson.followup.send(embed=embed)
            else:
                await interaction_lesson.followup.send("Üzgünüm, aradığınız konularla ilgili video bulunamadı veya bir hata oluştu.")
        
        lesson_select.callback = lesson_callback
        lesson_view = View().add_item(lesson_select)
        await interaction.followup.send("Ders seçin:", view=lesson_view)

    select.callback = callback
    view = View().add_item(select)
    await ctx.send("Sınıf seçiniz:", view=view)

@bot.command()
async def hatirlat(ctx, delay_seconds: int, *, text: str):
    """Belirtilen süre sonunda kullanıcıya özel mesaj yoluyla hatırlatma gönderir."""
    save_reminder(ctx.author.id, text, delay_seconds)
    await ctx.send(f"⏰ Hatırlatma ayarlandı: **{text}** ({delay_seconds} saniye sonra)")

@bot.command()
async def quiz(ctx, sinif: str, konu: str):
    """Belirtilen sınıf ve dersten quiz başlatır ve tüm soruları sorar."""
    if sinif not in QUIZ_QUESTIONS or konu not in QUIZ_QUESTIONS[sinif]:
        available_lessons = ", ".join(QUIZ_QUESTIONS.get(sinif, {}).keys())
        error_msg = f"❌ Yanlış sınıf veya ders girdiniz! '{sinif}' sınıfı için geçerli dersler: **{available_lessons}**"
        if not available_lessons:
             error_msg = "❌ Yanlış sınıf girdiniz! Lütfen geçerli bir sınıf girin (örn: 8.sınıf, 9.sınıf)."
        await ctx.send(error_msg)
        return

    questions = QUIZ_QUESTIONS[sinif][konu]
    score = 0
    total_questions = len(questions)
    
    await ctx.send(f"**📚 {sinif} - {konu} Quizi Başlıyor!** Toplam **{total_questions}** soru.")
    for q in questions:
        options_text = "\n".join([f"{i+1}. {opt}" for i,opt in enumerate(q["options"])])
        
        embed = discord.Embed(title=f"❓ Soru: {q['question']}", description=options_text, color=0xe67e22)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.content in [str(i+1) for i in range(len(q["options"]))]
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            answer_idx = int(msg.content)-1
            
            if q["options"][answer_idx] == q["answer"]:
                await ctx.send("✅ **Doğru!**")
                score += 1
            else:
                await ctx.send(f"❌ **Yanlış!** Doğru cevap: **{q['answer']}**")
        except asyncio.TimeoutError:
            await ctx.send("⌛ Süreniz doldu! Bu soruya puan alamadınız.")

    save_score(ctx.author.id, score)
    await ctx.send(f"🏆 **Quiz tamamlandı!** Toplam puanınız: **{score} / {total_questions}**")

bot.run(DISCORD_TOKEN)
