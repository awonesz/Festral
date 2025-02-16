import disnake
from disnake.ext import commands
import sqlite3
import Paginator

db = sqlite3.connect('character.db')
cursor = db.cursor()

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='profiles', description='Выведите весь список профелей на сервере')
    async def profiles(self, ctx):
        


def setup(client):
    client.add_cog(Character(client))