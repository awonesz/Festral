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
                relationships TEXT NOT NULL DEFAULT 50,
                endurance TEXT NOT NULL DEFAULT 100,
                items TEXT 
            )
        ''')
        self.db.commit()

def setup(client):
    client.add_cog(Listeners(client))