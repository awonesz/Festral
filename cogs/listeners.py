import disnake
from disnake.ext import commands, tasks
import sqlite3
from config import EMBED_COLOR, CATEGORIES_RP
import json
import os


def load_spells():
    if os.path.exists('spells.json'):
        with open('spells.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


class Listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect('character.db')
        self.cursor = self.db.cursor()
        self.restore_endurance.start()

    @tasks.loop(minutes=10)
    async def restore_endurance(self):
        self.cursor.execute('UPDATE character SET endurance = endurance + 10 WHERE endurance < 100')
        self.db.commit()

    @restore_endurance.before_loop
    async def before_restore_endurance(self):
        await self.client.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.client.user:
            return
        if not message.author.bot:
            return
        if message.channel.category_id not in CATEGORIES_RP:
            return
        spells = load_spells()
        content = message.content.lower()
        found_spells = []
        for spell in spells:
            if spell['name'].lower() in content:
                found_spells.append(spell)

        if found_spells:
            bot_name = message.author.name
            self.cursor.execute('SELECT endurance FROM character WHERE name = ?', (bot_name,))
            result = self.cursor.fetchone()

            if result:
                endurance = result[0]
                for spell in found_spells:
                    endurance -= spell['coefficient']
                    if endurance < 0:
                        endurance = 0
                self.cursor.execute('UPDATE character SET endurance = ? WHERE name = ?', (endurance, bot_name))
                self.db.commit()
                spell_list = "\n".join([f"**{spell['name']}**" for spell in found_spells])
                if spell_list != 0: 
                    embed = disnake.Embed(title=f"{message.author.name} использовал заклинания {spell_list}", colour=EMBED_COLOR)
                    embed.set_footer(text=f'Выносливость: {str(endurance)[:4]}')
                    await message.channel.send(embed=embed)
                else:
                    embed = disnake.Embed(title=f'{message.author.name} использовал заклинание {spell_list}', colour=EMBED_COLOR)
                    embed.set_footer(text=f'Выносливость: {str(endurance)[:4]}')
                    await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(
                title='🩶 Festral | Неизвестно',
                description='Здравствуй, юный волшебник, скорее всего ты неправильно написал команду.',
                colour=EMBED_COLOR
            )
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
        self._character_ensure_table_exists()

    def _character_ensure_table_exists(self):
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