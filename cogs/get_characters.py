import disnake
from disnake.ext import commands
import sqlite3
import asyncio
from config import EMBED_COLOR, FACULTY_EMOJI, ROLE_ADMIN

db = sqlite3.connect('character.db')
cursor = db.cursor()

def get_relationship_progress(relationships: int) -> str:
    filled = '■' * (relationships // 10)
    empty = '▢' * (10 - (relationships // 10))
    return f"{filled}{empty} {relationships}%"


class ProfileView(disnake.ui.View):
    def __init__(self, author_id: int, character_name: str, member_roles: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id = author_id
        self.character_name = character_name
        self.member_roles = member_roles
        
        if any(role.id in {ROLE_ADMIN[0], ROLE_ADMIN[1]} for role in self.member_roles):
            self.add_rel.disabled = False
            self.subtract_relationship.disabled = False
        else:
            self.add_rel.disabled = True
            self.subtract_relationship.disabled = True


    @disnake.ui.button(label='🟢 Добавить +10', style=disnake.ButtonStyle.success)
    async def add_rel(self, button: disnake.ui.Button, inter: disnake.Interaction):
        if not any(role.id in [ROLE_ADMIN[0], ROLE_ADMIN[1]] for role in inter.author.roles):
            embed = disnake.Embed(
                title="❌ Festral | Ошибка",
                description="У вас нет необходимых ролей для выполнения этого действия.",
                color=EMBED_COLOR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        cursor.execute('SELECT * FROM character WHERE name = ?', (self.character_name,))
        character = cursor.fetchone()
        if character:
            cursor.execute('UPDATE character SET relationships = relationships + 10 WHERE id = ?', (character[0],))
            db.commit()
            await self.update_profile(inter)

    @disnake.ui.button(label="🔴 Вычесть -10", style=disnake.ButtonStyle.danger)
    async def subtract_relationship(self, button: disnake.ui.Button, inter: disnake.Interaction):
        if not any(role.id in [ROLE_ADMIN[0], ROLE_ADMIN[1]] for role in inter.author.roles):
            embed = disnake.Embed(
                title="❌ Festral | Ошибка",
                description="У вас нет необходимых ролей для выполнения этого действия.",
                color=EMBED_COLOR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        cursor.execute('SELECT * FROM character WHERE name = ?', (self.character_name,))
        character = cursor.fetchone()
        if character:
            cursor.execute('UPDATE character SET relationships = relationships - 10 WHERE id = ?', (character[0],))
            db.commit()
            await self.update_profile(inter)

    async def update_profile(self, inter: disnake.Interaction):
        cursor.execute("SELECT * FROM character WHERE name = ?", (self.character_name,))
        character = cursor.fetchone()
        if character:
            name, age, faculty, picture, relationships, endurance = character[1], character[2], character[3], character[4], character[5], character[6]
            emoji = FACULTY_EMOJI.get(faculty)
            relationship_progress = get_relationship_progress(int(relationships))
            check_picture = str(picture)
            if check_picture.startswith('https://cdn.discordapp.com/'):                                                                                                                    
                embed = disnake.Embed(title=f"🪄 Festral | Профиль", description=f"**Имя:** {name} \n **Возраст:** {age}\n**Факультет:** {emoji} {faculty}", colour=EMBED_COLOR,)
                embed.set_thumbnail(picture)
                embed.add_field(name="Показатели", value=f'> __Отношения с палочкой:__ \n *{relationship_progress}* \n > __Выносливость:__ \n *{endurance} единиц*', inline=True)
            else:
                embed = disnake.Embed(title=f"🪄 Festral | Профиль", description=f"**Имя:** {name} \n **Возраст:** {age}\n**Факультет:** {emoji} {faculty} \n **Описание внешности:** {check_picture}", colour=EMBED_COLOR,)
                embed.add_field(name="Показатели", value=f'> __Отношения с палочкой:__ \n *{relationship_progress}* \n > __Выносливость:__ \n *{endurance} единиц*', inline=True)
            await inter.response.edit_message(embed=embed, view=self)


class PaginationView(disnake.ui.View):
    current_page: int = 1
    sep: int = 5

    def __init__(self, author_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_id = author_id

    async def send(self, inter: disnake.Interaction):
        await inter.response.send_message(view=self)
        self.message = await inter.original_message()
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        total_page = (len(self.data) + self.sep - 1) // self.sep
        embed = disnake.Embed(title="🪄 Festral | Профили Персонажей", colour=EMBED_COLOR)
        for item in data:
            name = item[1]
            age = item[2]
            faculty = item[3]
            emoji = FACULTY_EMOJI.get(faculty)
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
    async def prev_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        if inter.user.id != self.author_id:
            await inter.response.send_message("Вам недоступно это действие.", ephemeral=True)
            return
        await inter.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @disnake.ui.button(label="➡️", style=disnake.ButtonStyle.primary)
    async def next_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        if inter.user.id != self.author_id:
            await inter.response.send_message("Вам недоступно это действие.", ephemeral=True)
            return
        await inter.response.defer()
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
            await message.delete()

            cursor.execute('SELECT * FROM character WHERE name = ?', (character_name,))
            character = cursor.fetchone()

            if character:
                name, age, faculty, picture, relationships, endurance = character[1], character[2], character[3], character[4], character[5], character[6]
                emoji = FACULTY_EMOJI.get(faculty)
                relationship_progress = get_relationship_progress(int(relationships))
                check_pucture = str(picture)
                member_roles = inter.author.roles
                view = ProfileView(inter.author.id, character_name, member_roles)
                if check_pucture.startswith('https'):
                    embed = disnake.Embed(
                    title=f"🪄 Festral | Профиль",
                    description=f"**Имя:** {name} \n **Возраст:** {age}\n**Факультет:** {emoji} {faculty}",
                    colour=EMBED_COLOR,
                )
                    embed.add_field(name="Показатели", value=f'> __Отношения с палочкой:__ \n *{relationship_progress}* \n > __Выносливость:__ \n *{endurance} единиц*', inline=True)
                    embed.set_thumbnail(picture)
                elif check_pucture.strip():
                    embed = disnake.Embed(
                    title=f"🪄 Festral | Профиль",
                    description=f"**Имя:** {name} \n **Возраст:** {age}\n**Факультет:** {emoji} {faculty}",
                    colour=EMBED_COLOR,
                )
                    embed.add_field(name="Показатели", value=f'> __Отношения с палочкой:__ \n *{relationship_progress}* \n > __Выносливость:__ \n *{endurance} единиц*', inline=True)
                else:
                    embed = disnake.Embed(
                    title=f"🪄 Festral | Профиль",
                    description=f"**Имя:** {name} \n **Возраст:** {age}\n**Факультет:** {emoji} {faculty} \n **Описание внешности:** {picture}",
                    colour=EMBED_COLOR,
                )
                    embed.add_field(name="Показатели", value=f'> __Отношения с палочкой:__ \n *{relationship_progress}* \n > __Выносливость:__ \n *{endurance} единиц*', inline=True)
                await pagination_view.message.edit(embed=embed, view=view)
            else:
                await inter.followup.send(f"Персонаж с именем `{character_name}` не найден.", ephemeral=True)

        except asyncio.TimeoutError:
            await inter.followup.send("Время ожидания истекло. Попробуйте снова.", ephemeral=True)


def setup(client):
    client.add_cog(Character(client))