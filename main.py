import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv, dotenv_values

intents = disnake.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('F.'), intents=intents, status=disnake.Status.idle)
client.remove_command('help')

load_dotenv()

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(embed=disnake.Embed(title="Успешно!", description=f'Вы успешно загрузили cog {extension}', colour=0x2B2933))


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(embed=disnake.Embed(title="Успешно!", description=f'Вы успешно выгрузили cog {extension}', colour=0x2B2933))


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.send(embed=disnake.Embed(title="Успешно!", description=f'Вы успешно перезагрузили cog {extension}', colour=0x2B2933))

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))