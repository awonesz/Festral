import disnake
from disnake.ext import commands
import sqlite3

db = sqlite3.connect('character.db')
cursor = db.cursor()

class AddCharacter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='add_characters', description='Добавьте персонажа в базу данных')
    @commands.has_any_role(1197999786217971804, 1198222492943269898)
    async def add_character(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.Param(name="имя", description="Введите имя персонажа"),
        age: int = commands.Param(name="возраст", description="Введите возраст персонажа (цифрами)"),
        faculty: str = commands.Param(name="факультет", description="Выберите факультет персонажа", choices=["Гриффиндор", "Слизерин", "Пуффендуй", "Когтевран"]),
        picture: str = commands.Param(name='внешность', description='Добавьте внешность персонажу, нажмите правой кнопкой мыши по арту и "скопировать ссылку"')
    ):
        embed = disnake.Embed(title='🪄 Успешно', description='Вы успешно добавили персонажа в БД!', colour=0x2B2933)
        try:
            cursor.execute("INSERT INTO character (name, age, faculty, picture) VALUES (?, ?, ?, ?)", (name, age, faculty, picture))
            db.commit()
            await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"Ошибка при добавлении персонажа: {e}")
        cursor.close()
        db.close()

def setup(client):
    client.add_cog(AddCharacter(client))