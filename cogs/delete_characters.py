import disnake
from disnake.ext import commands
import sqlite3

db = sqlite3.connect('character.db')
cursor = db.cursor()

class DeleteCharacter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='delete_characters', description='Удалите персонажа из базу данных')
    @commands.has_any_role(1197999786217971804, 1198222492943269898)
    async def add_character(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.Param(name="имя", description="Введите имя персонажа"),
    ):
        embed = disnake.Embed(title='🪄 Успешно', description='Вы успешно удалили персонажа из БД!', colour=0x2B2933)
        try:
            cursor.execute("DELETE FROM character WHERE name = (?)", (name,))
            db.commit()
            await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"Ошибка при удалении персонажа: {e}")
        finally:
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(DeleteCharacter(client))