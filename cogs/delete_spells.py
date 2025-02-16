import disnake
import json
import os
from disnake.ext import commands
from config import ROLE_ADMIN, EMBED_COLOR

class DeleteSpells(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='delete_spells', description='Удалите заклинание')
    @commands.has_any_role(ROLE_ADMIN[0], ROLE_ADMIN[1])
    async def remove_spell(
        self,
        inter: disnake.ApplicationCommandInteraction,
        spell_name: str = commands.Param(name='заклинание', description="Введите имя заклинания для удаления")
    ):
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
        initial_length = len(data)
        data = [spell for spell in data if spell['name'] != spell_name]

        if len(data) < initial_length:
            with open('spells.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            embed = disnake.Embed(
                title="🪄 Festral | Успешно",
                description=f"Заклинание __{spell_name}__ было успешно удалено.",
                colour=EMBED_COLOR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(
                title="🪄 Festral | Ошибка",
                description=f"Заклинание __{spell_name}__ не найдено.",
                colour=disnake.Colour.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

def setup(client):
    client.add_cog(DeleteSpells(client))