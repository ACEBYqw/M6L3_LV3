import discord, asyncio, re
from discord.ext import commands
from discord.ui import Select, View, Button
from config import DISCORD_TOKEN
from logic import youtube_search_comprehensive, youtube_search_single, save_videos, get_saved_videos, delete_saved_video 
from reminders import save_reminder, start_reminders, get_remaining_reminders, delete_reminder
from quiz import QUIZ_QUESTIONS, save_score, get_top_scores
from datetime import datetime

EMBED_COLOR = 0x3498db
ERROR_COLOR = 0xe74c3c

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CLASSES = list(QUIZ_QUESTIONS.keys()) 

class CustomHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="📚 Akıllı Öğrenme Asistanı Komut Rehberi",
            description="Komut ön eki: `!`",
            color=EMBED_COLOR,
            timestamp=datetime.now()
        )
        embed.add_field(name="✨ !anasayfa / !giriş", value="Botun ana ekranını ve temel işlevlerini gösterir.", inline=False)
        embed.add_field(name="📚 !sinif", value="Sınıf ve ders seçimi yaparak konuya özel **YouTube videolarını** listeler.", inline=False)
        embed.add_field(name="❓ !quiz [sınıf] [konu]", value="Örnek: `!quiz 8.sınıf Matematik`. Çoktan seçmeli test başlatır.", inline=False)
        embed.add_field(name="⏰ !hatirlat [süre] [mesaj]", value="Örnek: `!hatirlat 2h Kimya çalış`. Hatırlatma kurar.", inline=False)
        embed.add_field(name="🏅 !skor", value="En iyi quiz skorlarını listeler.", inline=False)
        embed.add_field(name="🔎 !ara [sorgu]", value="Direkt olarak bir arama yaparak **YouTube videosu** önerir.", inline=False)
        embed.add_field(name="🗑️ !video_sil [index]", value="Kaydedilen son arama videolarını siler.", inline=False)
        embed.add_field(name="❌ !hatirlatma_sil [index]", value="Ayarlanan aktif hatırlatmalardan birini siler.", inline=False)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text="Geliştirme: Yapay Zeka Destekli Öğrenme | İyi Çalışmalar!")
        
        await self.get_destination().send(embed=embed)

bot.help_command = CustomHelp()


@bot.event
async def on_ready():
    print(f"✅ Bot olarak giriş yapıldı: {bot.user}")
    print(f"🔥 Başlatma Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!yardim | !anasayfa"))
    bot.loop.create_task(start_reminders(bot))

@bot.command(name="anasayfa", aliases=["giriş", "başlangıç"])
async def anasayfa(ctx):
    class HomeView(View):
        def __init__(self, ctx_author):
            super().__init__(timeout=60)
            self.ctx_author = ctx_author
        
        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            if interaction.user != self.ctx_author:
                await interaction.response.send_message("Bu etkileşimi sadece komutu başlatan kullanıcı kullanabilir.", ephemeral=True)
                return False
            return True

        @discord.ui.button(label="Tüm Komutlar (!yardim)", style=discord.ButtonStyle.primary, custom_id="help_button", emoji="❓")
        async def help_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(content="Yardım ekranı yükleniyor...", embed=None, view=None)
            await bot.help_command.send_bot_help(bot.cogs)
            
        @discord.ui.button(label="Sınıf Seçimi (!sinif)", style=discord.ButtonStyle.success, custom_id="class_button", emoji="📚")
        async def class_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(content="Sınıf seçimi başlatılıyor...", embed=None, view=None)
            await sinif(ctx)

    embed = discord.Embed(
        title="✨ Akıllı Öğrenme Asistanı Bot'a Hoş Geldiniz! ✨",
        description="Merhaba! Ben ders çalışma ve öğrenme süreçlerini destekleyen asistanınızım.\n\n`!yardim` ile tüm komutları görebilirsiniz.",
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    embed.set_author(name=f"{bot.user.name}", icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url="https://i.imgur.com/k9vY9nE.png") 
    embed.set_footer(text="Geliştirme: Yapay Zeka Destekli Öğrenme | İyi Çalışmalar!")

    await ctx.send(embed=embed, view=HomeView(ctx.author))



@bot.command()
async def sinif(ctx):
    options = [discord.SelectOption(label=c) for c in CLASSES]
    select = Select(placeholder="Sınıf seçin", options=options, custom_id="class_select")
    
    embed = discord.Embed(title="📚 Hangi Sınıf?", description="Lütfen aşağıdaki menüden sınıfı seçin.", color=EMBED_COLOR)

    async def callback(interaction):
        if interaction.user != ctx.author:
             await interaction.response.send_message("Bu menüyü sadece komutu başlatan kullanıcı kullanabilir.", ephemeral=True)
             return
             
        selected_class = select.values[0]
        lessons = list(QUIZ_QUESTIONS[selected_class].keys())
        lesson_options = [discord.SelectOption(label=t) for t in lessons]
        lesson_select = Select(placeholder="Ders seçin", options=lesson_options, custom_id="lesson_select")

        async def lesson_callback(interaction_lesson):
            if interaction_lesson.user != ctx.author:
                 await interaction_lesson.response.send_message("Bu menüyü sadece komutu başlatan kullanıcı kullanabilir.", ephemeral=True)
                 return
                 
            selected_lesson_name = lesson_select.values[0]
            await interaction_lesson.response.send_message(f"Seçilen ders: **{selected_lesson_name}**. Konu anlatımları aranıyor...", ephemeral=True)

            topic_names = list(QUIZ_QUESTIONS[selected_class][selected_lesson_name].keys()) if isinstance(QUIZ_QUESTIONS[selected_class][selected_lesson_name], dict) else [q["question"] for q in QUIZ_QUESTIONS[selected_class][selected_lesson_name]]
            
            videos = youtube_search_comprehensive(selected_class, selected_lesson_name, topic_names)
            
            if not videos:
                error_embed = discord.Embed(title="❌ Video Bulunamadı", description="Bu konu için video önerisi bulunamadı.", color=ERROR_COLOR)
                await ctx.send(embed=error_embed)
                return

            video_list = "\n".join([f"**{i+1}.** **[{v['title']}]({v['url']})**" for i, v in enumerate(videos)])
            
            result_embed = discord.Embed(
                title=f"🎬 {selected_class} - {selected_lesson_name} Konu Anlatımları",
                description=f"İşte konulara özel **{len(videos)}** adet YouTube video önerisi.",
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            result_embed.add_field(name="Video Listesi", value=video_list, inline=False)
            if videos[0].get("thumbnail"):
                result_embed.set_thumbnail(url=videos[0]["thumbnail"])
            
            await ctx.send(embed=result_embed)
            await interaction_lesson.edit_original_response(content=f"Seçim tamamlandı: **{selected_class} - {selected_lesson_name}**.", view=None)

        lesson_select.callback = lesson_callback
        lesson_view = View().add_item(lesson_select)
        
        await interaction.response.edit_message(embed=embed.set_footer(text=f"Sınıf: {selected_class}"), content="Şimdi bir ders seçin:", view=lesson_view)

    select.callback = callback
    view = View().add_item(select)
    
    await ctx.send(embed=embed, view=view)

@bot.command()
async def ara(ctx, *, query):
    await ctx.send(f"🔍 **{query}** için arama yapılıyor...")
    results = youtube_search_single(query, max_results=5) 
    
    if not results:
        embed = discord.Embed(title="❌ Video Bulunamadı", description=f"**{query}** sorgusuna uygun video bulunamadı.", color=ERROR_COLOR)
        await ctx.send(embed=embed)
        return

    save_videos(query, results)
    
    embed = discord.Embed(
        title=f"🎬 Arama Sonuçları: {query}",
        description=f"İşte **{len(results)}** adet video önerisi:",
        color=EMBED_COLOR,
        timestamp=datetime.now()
    )
    video_list = "\n".join([f"**{i+1}.** **[{video['title']}]({video['url']})**" for i, video in enumerate(results)])
    
    if results[0].get("thumbnail"):
        embed.set_thumbnail(url=results[0]["thumbnail"])
        
    embed.add_field(name="Video Listesi", value=video_list, inline=False)
    embed.set_footer(text="Bu sonuçlar kaydedilmiştir. İstenirse !video_sil [index] komutu ile silebilirsiniz.")

    await ctx.send(embed=embed)

@bot.command(name="skor")
async def quiz_skor(ctx):
    top_scores = get_top_scores()
    
    embed = discord.Embed(
        title="🏆 En İyi Quiz Skorları",
        description="Öğrencilerimizin en yüksek başarımları:",
        color=0xf1c40f,
        timestamp=datetime.now()
    )
    
    if not top_scores:
        embed.add_field(name="Kayıt Yok", value="Henüz kimse quiz çözmemiş.", inline=False)
    else:
        rank_text = ""
        for i, (user_id, score) in enumerate(top_scores[:10]):
            try:
                user = await bot.fetch_user(user_id)
                username = user.name
            except:
                username = f"Kullanıcı ID: {user_id}"
                
            rank_text += f"**#{i+1}** - **{username}**: {score} Puan\n"
        
        embed.add_field(name="Liderlik Tablosu", value=rank_text, inline=False)
        embed.set_thumbnail(url=bot.user.avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def quiz(ctx, sinif: str, konu: str):
    if sinif not in QUIZ_QUESTIONS or konu not in QUIZ_QUESTIONS[sinif]:
        available_lessons = ", ".join(QUIZ_QUESTIONS.get(sinif, {}).keys())
        error_msg = f"❌ Yanlış sınıf/konu. Geçerli dersler: **{available_lessons}**"
        if not available_lessons: error_msg = "❌ Yanlış sınıf girdiniz! Lütfen geçerli bir sınıf girin."
        
        error_embed = discord.Embed(title="Hata: Quiz Başlatılamadı", description=error_msg, color=ERROR_COLOR)
        await ctx.send(embed=error_embed)
        return

    questions = QUIZ_QUESTIONS[sinif][konu]
    score = 0
    total_questions = len(questions)
    
    await ctx.send(f"**📚 {sinif} - {konu} Quizi Başlıyor!** Toplam **{total_questions}** soru.")
    
    for q in questions:
        options_text = "\n".join([f"{i+1}. {opt}" for i,opt in enumerate(q["options"])])
        
        embed = discord.Embed(title=f"❓ Soru: {q['question']}", description=options_text, color=EMBED_COLOR)
        embed.set_footer(text=f"Kullanıcı: {ctx.author.name} | Cevaplamak için 30 saniyeniz var.")
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.content in [str(i+1) for i in range(len(q["options"]))]
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            answer_idx = int(msg.content)-1
            
            if q["options"][answer_idx] == q["answer"]:
                await ctx.send("✅ **Doğru!** (+10 Puan)")
                score += 10
            else:
                await ctx.send(f"❌ **Yanlış!** Doğru cevap: **{q['answer']}**")
                
        except asyncio.TimeoutError:
            await ctx.send(f"⌛ Süre doldu! Doğru cevap: **{q['answer']}**")
            
        await asyncio.sleep(1)
        
    final_embed = discord.Embed(
        title="🎉 Quiz Bitti! Sonuçlar:",
        description=f"Toplam **{total_questions}** sorudan **{score}** puan topladın!",
        color=0x2ecc71 if score > (total_questions*10/2) else 0xf1c40f
    )
    save_score(str(ctx.author.id), score)
    await ctx.send(embed=final_embed)

@bot.command()
async def hatirlat(ctx, delay: str, *, message: str):
    match = re.match(r"(\d+)([smh])", delay, re.IGNORECASE)
    if not match:
        error_embed = discord.Embed(
            title="Hata: Geçersiz Süre Formatı",
            description="Örn: `!hatirlat 30m Kimya çalış` (s/m/h).",
            color=ERROR_COLOR
        )
        await ctx.send(embed=error_embed)
        return

    amount, unit = match.groups()
    amount = int(amount)
    
    delay_seconds = 0
    time_unit = ""

    if unit.lower() == 's': delay_seconds = amount; time_unit = "saniye"
    elif unit.lower() == 'm': delay_seconds = amount * 60; time_unit = "dakika"
    elif unit.lower() == 'h': delay_seconds = amount * 3600; time_unit = "saat"
    
    save_reminder(str(ctx.author.id), message, delay_seconds)
    
    confirm_embed = discord.Embed(
        title="✅ Hatırlatma Kuruldu!",
        description=f"⏰ **{amount} {time_unit}** sonra size hatırlatılacak: **{message}**",
        color=0x2ecc71
    )
    confirm_embed.set_footer(text=f"Kuruluş zamanı: {datetime.now()}")
    await ctx.send(embed=confirm_embed)

@bot.command()
async def video_sil(ctx, index: int):
    success = delete_saved_video(index)
    if success:
        await ctx.send(f"🗑️ **{index}.** sıradaki video kaydı silindi.")
    else:
        await ctx.send("❌ Hata: Geçersiz video indeksi veya hiç kaydedilmiş video yok.")

@bot.command()
async def hatirlatma_sil(ctx, index: int):
    reminders = get_remaining_reminders()
    user_reminders = [r for r in reminders if str(r["user_id"]) == str(ctx.author.id)]
    
    if 0 < index <= len(user_reminders):
        reminder_to_delete = user_reminders[index - 1]
        try:
             delete_reminder(reminder_to_delete)
             await ctx.send(f"❌ **{index}.** sıradaki hatırlatmanız silindi: **{reminder_to_delete['text']}**.")
        except Exception as e:
             await ctx.send(f"❌ Hata: Silinirken sorun oluştu.")
    else:
        await ctx.send("❌ Hata: Geçersiz hatırlatma indeksi.")


if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("HATA: DISCORD_TOKEN config.py dosyasında tanımlı değil.")
