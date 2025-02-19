import disnake
from disnake.ext import commands
from config import ROLE_ADMIN, EMBED_COLOR
import sqlite3


class SetEndurance(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='set_endurance', description='Вызовите эту команду, дабы установить выносливость персонажу')
    @commands.has_any_role(ROLE_ADMIN[0], ROLE_ADMIN[1])
    async def set_endurance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.Param(name='имя', description='Имя персонажа'),
        max_endurance: int = commands.Param(name='максимальная', description='Установите максимальную выносливость', default=None),
        endurance: int = commands.Param(name='выносливость', description='Установите выносливость персонажу', default=None)
    ):
        if not max_endurance and not endurance:
            embed = disnake.Embed(
                title="Festral | Ошибка",
                description="Вы должны указать хотя бы одно из значений: `максимальная` или `выносливость`.",
                color=EMBED_COLOR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        with sqlite3.connect('character.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT endurance, max_endurance FROM character WHERE name = ?", (name,))
            result = cursor.fetchone()

            if not result:
                embed = disnake.Embed(
                    title="<:7382no:1227261658485883002> Festral | Ошибка",
                    description=f"Персонаж с именем `{name}` не найден в базе данных.",
                    color=EMBED_COLOR
                )
                await inter.response.send_message(embed=embed, ephemeral=True)
                return

            current_endurance, current_max_endurance = result
            if max_endurance is not None:
                if max_endurance < 0:
                    embed = disnake.Embed(
                        title="<:7382no:1227261658485883002> Festral | Ошибка",
                        description="Максимальная выносливость не может быть меньше 0.",
                        color=EMBED_COLOR
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

                current_max_endurance = max_endurance

            if endurance is not None:
                if endurance < 0:
                    embed = disnake.Embed(
                        title="<:7382no:1227261658485883002> Festral | Ошибка",
                        description="Текущая выносливость не может быть меньше 0.",
                        color=EMBED_COLOR
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return
                if endurance > current_max_endurance:
                    endurance = current_max_endurance

                current_endurance = endurance
            cursor.execute(
                "UPDATE character SET endurance = ?, max_endurance = ? WHERE name = ?",
                (current_endurance, current_max_endurance, name)
            )
            db.commit()
            embed = disnake.Embed(
                title="<:7057checkmark:1227245983616991262> Festral | Успешно",
                description=f"Выносливость персонажа `{name}` успешно обновлена.\n"
                            f"<:idle:1199756934526533652> Текущая выносливость: {current_endurance}\n"
                            f"<:idle:1199756934526533652> Максимальная выносливость: {current_max_endurance}",
                color=EMBED_COLOR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(SetEndurance(client))