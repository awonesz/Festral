import disnake
from disnake.ext import commands
from config import EMBED_COLOR


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='help', description='Вызовите эту команду, дабы узнать все команды доступные в боте!')
    async def help(self, inter):
        embed = disnake.Embed(title='Festral | Помощь', description='## <:xmas_snow_flake:1205471954908487710> Слэш команды \n >>> <:5581hotpinkstar:1227183441775169569> __/add_characters__ - "добавить профиль персонажа" \n <:5581hotpinkstar:1227183441775169569> __/delete_characters__ - "удалить профиль персонажа" \n  <:5581hotpinkstar:1227183441775169569> /profiles - вывести профиль персонажей (после вызова команды написать имя нужного профиля и он откроет его полную версию)', colour=EMBED_COLOR)
        embed.add_field(name='Заклинания', value='>>> <:5581hotpinkstar:1227183441775169569> /add_spells - добавить заклинание \n <:5581hotpinkstar:1227183441775169569> /delete_spells - удалить заклинание ')
        await inter.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Help(client))