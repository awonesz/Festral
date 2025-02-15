import disnake
from disnake.ext import commands
import sqlite3


db = sqlite3.connect('character.db')
cursor = db.cursor()


query = """
CREATE TABLE IF NOT EXISTS character(
    id INTEGER PRIMARY KEY,
    name VARCHAR(30),
    age INTEGER,
    faculty VARCHAR(10)
)
"""
cursor.executescript(query)

class AddCharacter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='add_characters', description='Добавьте персонажа в базу данных')
    @commands.has_any_role(1197999786217971804, 1198222492943269898)
    async def add_character(self, inter, name, age, faculty):
        embed = disnake.Embed(title='Успешно', description='Вы успешно добавили персонажа в БД', colour=0x2B2933)
        embed_error = disnake.Embed(title='Ошибка', description='По какой-то причине вы не смогли добавить персонажа в БД.', colour=0x2B2933)
        try:
            cursor.execute("""INSERT INTO character(name, age, faculty)""", [name, age, faculty])
            db.commit()
        except:
            await inter.response.send_message(embed=embed_error, ephemeral=True)
        finally:
            await inter.response.send_message(embed=embed, ephemeral=True)


cursor.close()
db.close()

def setup(client):
    client.add_cog(AddCharacter(client))