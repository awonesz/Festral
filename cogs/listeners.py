import disnake
from disnake.ext import commands
import sqlite3
from config import EMBED_COLOR


class Listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect('character.db')
        self.cursor = self.db.cursor()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(title='🩶 Festral | Неизвестно', description='Здравствуй, юный волшебник, скорее всего ты неправильно написал команду.', colour=EMBED_COLOR)
            embed.set_footer(text='➡️ Если ты уверен, что ты все написал правильно, будь добр отпиши aevuum!')
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def character_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = disnake.Embed(
            title="❌ Festral | Ошибка",
            description="У вас нет необходимых ролей для выполнения этой команды.",
            color=EMBED_COLOR
        )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def rel_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, sqlite3.IntegrityError):
            embed = disnake.Embed(
            title="❌ Festral | Ошибка",
            description="Вы не можете задать значение ниже 0 или выше 100",
            color=EMBED_COLOR
        )
            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Бот запущен')
        self._ensure_table_exists()
        
    def _ensure_table_exists(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS character (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                faculty TEXT NOT NULL,
                picture TEXT NOT NULL,
                relationships INTEGER NOT NULL DEFAULT 50 CHECK (relationships >= 0 AND relationships <= 100),
                endurance INTEGER NOT NULL DEFAULT 100 CHECK (endurance >= 0 AND endurance <= 100),
                items TEXT 
            )
        ''')
        self.db.commit()

def setup(client):
    client.add_cog(Listeners(client))