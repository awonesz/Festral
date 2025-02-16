import disnake
from disnake.ext import commands
import sqlite3
import asyncio

db = sqlite3.connect('character.db')
cursor = db.cursor()

FACULTY_EMOJIS = {
    "Гриффиндор": "🦁",
    "Слизерин": "🐍",
    "Пуффендуй": "🦡",
    "Когтевран": "🦅" 
}

class PaginationView(disnake.ui.View):
    current_page : int = 1
    sep : int = 5

    def __init__(self, author_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id = author_id  # Идентификатор пользователя, вызвавшего команду

    async def send(self, inter: disnake.Interaction):
        await inter.response.send_message(view=self)
        self.message = await inter.original_message()
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        total_page = (len(self.data) + self.sep - 1) // self.sep
        embed = disnake.Embed(title="🪄 Профили Персонажей", colour=0x2B2933)
        for item in data:
            name = item[1]
            age = item[2]
            faculty = item[3]
            emoji = FACULTY_EMOJIS.get(faculty)
            embed.add_field(name=f'{name}, *{age}*', value=f"{emoji} {faculty}", inline=False)
        embed.set_footer(text=f'Страница {self.current_page} из {total_page}')
        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        total_page = (len(self.data) + self.sep - 1) // self.sep
        if self.current_page == 1:
            self.prev_button.disabled = True
            self.prev_button.style = disnake.ButtonStyle.gray
        else: 
            self.prev_button.disabled = False
            self.prev_button.style = disnake.ButtonStyle.primary
        if self.current_page == total_page:
            self.next_button.disabled = True
            self.next_button.style = disnake.ButtonStyle.gray
        else: 
            self.next_button.disabled = False
            self.next_button.style = disnake.ButtonStyle.primary

    def get_current_page_data(self):
        from_item = (self.current_page - 1) * self.sep
        until_item = self.current_page * self.sep
        return self.data[from_item:until_item]

    @disnake.ui.button(label="⬅️", style=disnake.ButtonStyle.primary)
    async def prev_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Вам недоступно это действие.", ephemeral=True)
            return
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @disnake.ui.button(label="➡️", style=disnake.ButtonStyle.primary)
    async def next_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Вам недоступно это действие.", ephemeral=True)
            return
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())


class Character(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='profiles', description='Выведите весь список профилей на сервере')
    async def profiles(self, inter: disnake.ApplicationCommandInteraction):
        cursor.execute('SELECT * FROM character')
        data = cursor.fetchall()
        pagination_view = PaginationView(author_id=inter.author.id, timeout=None)
        pagination_view.data = data
        await pagination_view.send(inter)

        def check(m: disnake.Message):
            return m.author.id == inter.author.id and m.channel.id == inter.channel.id

        try:
            message = await self.client.wait_for("message", check=check, timeout=60.0)
            character_name = message.content.strip()

            cursor.execute('SELECT * FROM character WHERE name = ?', (character_name,))
            character = cursor.fetchone()

            if character:
                name, age, faculty, picture = character[1], character[2], character[3], character[4]
                emoji = FACULTY_EMOJIS.get(faculty)
                embed = disnake.Embed(
                    title=f"🪄 Festral | Профиль",
                    description=f"**Имя:** {name} \n **Возраст:** {age}\n**Факультет:** {emoji} {faculty}",
                    inline=True,
                    colour=0x2B2933,
                )
                embed.set_thumbnail(picture)
                await pagination_view.message.edit(embed=embed, view=None)
            else:
                await inter.followup.send(f"Персонаж с именем `{character_name}` не найден.", ephemeral=True)

        except asyncio.TimeoutError:
            await inter.followup.send("Время ожидания истекло. Попробуйте снова.", ephemeral=True)


def setup(client):
    client.add_cog(Character(client))