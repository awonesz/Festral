import disnake
from disnake.ext import commands


class Listeners(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(title='🩶 Festral | Неизвестно', description='Здравствуй, юный волшебник, скорее всего ты неправильно написал команду.', colour=0x2B2933)
            embed.set_footer(text='➡️ Если ты уверен, что ты все написал правильно, будь добр отпиши aevuum!')
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Бот запущен')


def setup(client):
    client.add_cog(Listeners(client))