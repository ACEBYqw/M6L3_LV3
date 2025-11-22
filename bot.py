# bot.py
import discord, asyncio
from discord.ext import commands
from discord.ui import Select, View
from config import DISCORD_TOKEN
from logic import youtube_search
from reminders import save_reminder, start_reminders
from quiz import QUIZ_QUESTIONS, save_score

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CLASSES = ["8.sınıf","9.sınıf","10.sınıf","11.sınıf","12.sınıf"]

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")
    bot.loop.create_task(start_reminders(bot))

# Sınıf ve konu seçimi
@bot.command()
async def sinif(ctx):
    options = [discord.SelectOption(label=c) for c in CLASSES]
    select = Select(placeholder="Sınıf seçin", options=options)

    async def callback(interaction):
        selected_class = select.values[0]
        await interaction.response.send_message(f"Seçilen sınıf: {selected_class}")

        topics = list(QUIZ_QUESTIONS[selected_class].keys())
        topic_options = [discord.SelectOption(label=t) for t in topics]
        topic_select = Select(placeholder="Konu seçin", options=topic_options)

        async def topic_callback(inter2):
            topic = topic_select.values[0]
            await inter2.response.send_message(f"Konu seçildi: {topic}")

            # Video arama ve embed
            videos = youtube_search(f"{selected_class} {topic} konu anlatımı")
            embed = discord.Embed(title=f"{selected_class} - {topic} Videolar", color=0x00ff00)
            for v in videos:
                embed.add_field(name=v["title"], value=f"[Videoyu izle]({v['url']})", inline=False)
                embed.set_thumbnail(url=v["thumbnail"])
            await inter2.followup.send(embed=embed)

        topic_select.callback = topic_callback
        view2 = View()
        view2.add_item(topic_select)
        await ctx.send("Konu seçiniz:", view=view2)

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send("Sınıf seçiniz:", view=view)

# Hatırlatma
@bot.command()
async def hatirlat(ctx, delay_seconds: int, *, text: str):
    save_reminder(ctx.author.id, text, delay_seconds)
    await ctx.send(f"Hatırlatma ayarlandı: {text} ({delay_seconds} saniye sonra)")

# Quiz
@bot.command()
async def quiz(ctx, sinif: str, konu: str):
    if sinif not in QUIZ_QUESTIONS or konu not in QUIZ_QUESTIONS[sinif]:
        await ctx.send("Yanlış sınıf veya konu girdiniz!")
        return

    questions = QUIZ_QUESTIONS[sinif][konu]
    score = 0
    for q in questions:
        options_text = "\n".join([f"{i+1}. {opt}" for i,opt in enumerate(q["options"])])
        embed = discord.Embed(title=q["question"], description=options_text, color=0x3498db)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.content in [str(i+1) for i in range(len(q["options"]))]

        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            answer_idx = int(msg.content)-1
            if q["options"][answer_idx] == q["answer"]:
                await ctx.send("✅ Doğru!")
                score += 1
            else:
                await ctx.send(f"❌ Yanlış! Doğru cevap: {q['answer']}")
        except:
            await ctx.send(f"⏰ Süre doldu! Doğru cevap: {q['answer']}")

    save_score(ctx.author.id, score)
    await ctx.send(f"🏆 Quiz tamamlandı! Toplam puanınız: {score}")

bot.run(DISCORD_TOKEN)
