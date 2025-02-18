import disnake
from disnake.ext import commands
from config import ROLE_ADMIN, EMBED_COLOR
import apsw

with apsw.Connection('character.db') as db:
    cursor = db.cursor()

class DeleteCharacter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='delete_characters', description='Удалите персонажа из базу данных')
    @commands.has_any_role(ROLE_ADMIN[0], ROLE_ADMIN[1])
    async def del_character(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.Param(name="имя", description="Введите имя персонажа"),
    ):
        embed = disnake.Embed(title='🪄 Festral | Успешно', description='Вы успешно удалили персонажа из БД!', colour=EMBED_COLOR)
        try:
            cursor.execute("DELETE FROM character WHERE name = (?)", (name,))
            db.commit()
            await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"Ошибка при удалении персонажа: {e}")

def setup(client):
    client.add_cog(DeleteCharacter(client))