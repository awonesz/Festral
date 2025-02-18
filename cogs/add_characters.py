import disnake
from disnake.ext import commands
import sqlite3
from config import ROLE_ADMIN, EMBED_COLOR

with sqlite3.connect('character.db') as db:
    cursor = db.cursor()

class AddCharacter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='add_characters', description='Добавьте персонажа в базу данных')
    @commands.has_any_role(ROLE_ADMIN[0], ROLE_ADMIN[1])
    async def add_character(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.Param(name="имя", description="Введите имя персонажа"),
        age: int = commands.Param(name="возраст", description="Введите возраст персонажа (цифрами)"),
        faculty: str = commands.Param(name="факультет", description="Выберите факультет персонажа", choices=["Гриффиндор", "Слизерин", "Пуффендуй", "Когтевран", "Не имеет"]),
        picture: str = commands.Param(name='внешность', description='Добавьте внешность персонажу, нажмите правой кнопкой мыши по арту и "скопировать ссылку".'),
        teacher: str = commands.Param(name='преподаватель', description='Выберите является ли персонаж преподавателем', choices=['Да', 'Нет'])
    ):
        is_teacher = teacher == "Да"

        embed = disnake.Embed(title='🪄 Успешно', description='Вы успешно добавили персонажа в БД!', colour=EMBED_COLOR)
        try:
            cursor.execute("INSERT INTO character (name, age, faculty, picture, teacher) VALUES (?, ?, ?, ?, ?)", 
                        (name, age, faculty, picture, is_teacher))
            db.commit()
            await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"Ошибка при добавлении персонажа: {e}")

def setup(client):
    client.add_cog(AddCharacter(client))