import discord
from discord.ext import commands
from collections import defaultdict

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


user_scores = defaultdict(int)
user_current_question = defaultdict(int)
user_in_quiz = defaultdict(bool)



class Question:
    """Tek doğru cevaplı soru"""
    def __init__(self, text, answers, correct):
        self.text = text
        self.answers = answers
        self.correct = correct
        self.image = None

    def is_correct(self, answer):
        return answer == self.correct


class MultiAnswerQuestion(Question):
    """Çoklu doğru cevaplı soru (inheritance kullanıldı)"""
    def __init__(self, text, answers, correct_list):
        super().__init__(text, answers, None)
        self.correct_list = correct_list

    def is_correct(self, answer):
        return answer in self.correct_list


class ImageQuestion(Question):
    """Resimli soru"""
    def __init__(self, text, answers, correct, image_url):
        super().__init__(text, answers, correct)
        self.image = image_url



questions = [
    Question("2 + 2 kaçtır?", ["3", "4", "5"], "4"),
    MultiAnswerQuestion("Hangileri memelidir?", ["Tavuk", "İnek", "Köpek"], ["İnek", "Köpek"]),
    ImageQuestion("Bu Pokémon hangisidir?", ["Pikachu", "Charmander", "Bulbasaur"], "Pikachu",
                  "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png")
]




class AnswerView(discord.ui.View):
    def __init__(self, question, user_id):
        super().__init__(timeout=None)
        self.question = question
        self.user_id = user_id

        for ans in question.answers:
            self.add_item(AnswerButton(ans))


class AnswerButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        q_index = user_current_question[interaction.user.id]
        question = questions[q_index]

        # Tek basış sonrası tüm tuşlar disable!
        for item in self.view.children:
            item.disabled = True
        await interaction.response.edit_message(view=self.view)

        # Cevap doğru mu?
        if question.is_correct(self.label):
            user_scores[interaction.user.id] += 1
            await interaction.followup.send("✔ Doğru cevap!", ephemeral=True)
        else:
            await interaction.followup.send("❌ Yanlış!", ephemeral=True)

        # Sonraki soru
        user_current_question[interaction.user.id] += 1

        if user_current_question[interaction.user.id] >= len(questions):
            score = user_scores[interaction.user.id]
            await interaction.followup.send(f"🏁 Quiz bitti! Skorun: **{score}**")
            user_in_quiz[interaction.user.id] = False
            return

        # Sıradaki soruyu göster
        await send_question(interaction.channel, interaction.user.id)


async def send_question(channel, user_id):
    q_index = user_current_question[user_id]
    question = questions[q_index]

    embed = discord.Embed(title=f"Soru {q_index+1}", description=question.text)

    if question.image:
        embed.set_image(url=question.image)

    await channel.send(embed=embed, view=AnswerView(question, user_id))



@bot.command()
async def start(ctx):
    user_id = ctx.author.id

    # Kullanıcı zaten quizdeyse -> resetle
    if user_in_quiz[user_id]:
        await ctx.send("🔁 Quiz yeniden başlatılıyor! Puanların sıfırlandı.")
        user_scores[user_id] = 0
        user_current_question[user_id] = 0
    else:
        await ctx.send("🎮 Quiz başlıyor!")
        user_in_quiz[user_id] = True
        user_scores[user_id] = 0
        user_current_question[user_id] = 0

    await send_question(ctx.channel, user_id)


bot.run("BOT_TOKEN")
