import disnake
from disnake.ext import commands
from config import EMBED_COLOR


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='help', description='Вызовите эту команду, дабы узнать все команды доступные в боте!')
    async def help(self, inter):
        embed = disnake.Embed(title='Festral | Помощь', description='## 🧾 Слэш команды \n >>> ➡️ __/add_characters__ - "добавить профиль персонажа" \n ➡️ __/delete_characters__ - "удалить профиль персонажа" \n /profiles - вывести профиль персонажей (после вызова команды написать имя нужного профиля и он откроет его полную версию)', colour=EMBED_COLOR)
        await inter.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Help(client))