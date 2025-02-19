import disnake
from disnake.ext import commands
import json
import os
from config import ROLE_ADMIN, EMBED_COLOR

class AddSpells(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='add_spells', description='Добавить заклинание')
    @commands.has_any_role(ROLE_ADMIN[0], ROLE_ADMIN[1])
    async def add_spels(
        self,
        inter: disnake.ApplicationCommandInteraction,
        spells: str = commands.Param(name='заклинание', description="Добавьте заклинание"),
        coef: float = commands.Param(name='коэффециент', description="Внесите коэффициент")
    ):
        new_spell = {
            'name': spells,
            'coefficient': coef
        }

        if os.path.exists('spells.json'):
            with open('spells.json', 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        data.append(new_spell)

        with open('spells.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        embed = disnake.Embed(
            title="<:7057checkmark:1227245983616991262> Festral | Успешно",
            description=f"Вы успешно добавили заклинание __{spells}__ с коэффициентом __{coef}__",
            colour=EMBED_COLOR
        )
        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(client):
    client.add_cog(AddSpells(client))