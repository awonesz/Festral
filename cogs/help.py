import disnake
from disnake.ext import commands
from config import EMBED_COLOR


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='help', description='Вызовите эту команду, дабы узнать все команды доступные в боте!')
    async def help(self, inter):
        embed = disnake.Embed(title='Festral | Помощь', description='## <:8586slashcommand:1227257608180596819> Слэш команды \n >>> <:5581hotpinkstar:1227183441775169569> /add_characters - "добавить профиль персонажа" \n <:5581hotpinkstar:1227183441775169569> /delete_characters - "удалить профиль персонажа" \n  <:5581hotpinkstar:1227183441775169569> /profiles - "вывести профиль персонажей (после вызова команды написать имя нужного профиля и он откроет его полную версию)"', colour=EMBED_COLOR)
        embed.add_field(name='Заклинания', value='>>> <:5581hotpinkstar:1227183441775169569> /add_spells - "добавить заклинание" \n <:5581hotpinkstar:1227183441775169569> /delete_spells - "удалить заклинание" ')
        await inter.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Help(client))