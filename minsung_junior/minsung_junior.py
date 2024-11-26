import discord
import random
import asyncio
import sqlite3
from itertools import combinations
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="%", intents=intents, help_command = None)
        self.command_in_use = False

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands have been synced!")
client = MyBot()

conn = sqlite3.connect('Test.db')
cursor = conn.cursor()

def fightfind(user):
    cursor.execute("SELECT * FROM fight WHERE ID = ?", (user,))
    
def teamfind(team,user):
    cursor.execute(f"SELECT * FROM {team} WHERE ID = ?", (user,))

def commit():
    conn.commit()
    
def team(team):
    cursor.execute(f"SELECT * FROM {team}")

def fight():
    cursor.execute("SELECT * FROM fight")

@client.tree.command(name="help",description="메뉴얼 도움말 help hl mn menu")#명령어에 대해서 설명해주는 명령어
async def helpasdf(interaction: discord.Interaction, value: str = ""):
    if not value:
        await interaction.response.send_message("명령어들을 알려드립니다.```java\n1.in\n2.out\n3.random\n6.list\n7.replace\n8.displace\n9.coin\n10.gamble\n11.auction(만드는 중...)\n12.profile```", ephemeral=True)
        await interaction.response.send_message("```ansi\n명령어들은 각각 한글, 영어(줄임말) 영어의미로 할 수 있습니다.\n명령어에 대하여 좀 더 자세하게 알고싶다면 [1m$메뉴얼 / $도움말 / $help / $hl +'명령어'[0m로 확인하세요\nex) $메뉴얼 인 / $도움말 퇴장 / $help rd / $mn tire```", ephemeral=True)
    elif(value == "in" or value == "인" or value == "참가"):
        await interaction.response.send_message("```ansi\n이 명령어는 게임에 참가하는 명령어입니다.\n같은 명령어 = [4;1m인[0m [4;1m참가[0m [4;1min[0m```",ephemeral=True)
    elif(value == "out" or value == "아웃" or value == "퇴장"):
        await interaction.response.send_message("```ansi\n이 명령어는 참가한 게임에서 퇴장하는 명령어입니다.\n같은 명령어 = [4;1m아웃[0m [4;1m퇴장[0m [4;1mout[0m```",ephemeral=True)
    elif(value == "random" or value == "섞기" or value == "랜덤" or value == "rd"):
        await interaction.response.send_message("```ansi\n이 명령어는 팀을 섞은 후 통화방을 나누는 명령어입니다.\n같은 명령어 = [4;1m랜덤[0m [4;1m섞기[0m [4;1mrandom[0m [4;1mrd[0m```",ephemeral=True)
    elif(value == "replace" or value == "rep" or value == "포함" or value == "리플레이스"):
        await interaction.response.send_message("```ansi\n이 명령어는 플레이어를 대신 참가시키는 명령어입니다.\n같은 명령어 = [4;1m리플레이스[0m [4;1m포함[0m [4;1mreplace[0m [4;1mrep[0m\n[1;31m매우[0m [1;31m중요!![0m [1;31m이[0m [1;31m명령어를[0m [1;31m악용할시[0m [1;31m이[0m [1;31m봇을[0m [1;31m사용할[0m [1;31m수[0m [1;31m없을[0m [1;31m수도[0m [1;31m있습니다!!![0m```",ephemeral=True)
    elif(value == "list" or value == "리스트" or value == "ls" or value == "인원"):
        await interaction.response.send_message("```ansi\n이 명령어는 현재 팀을 출력해주는 명령어입니다.\n같은 명령어 = [4;1m리스트[0m [4;1m인원[0m [4;1mlist[0m [4;1mls[0m```")
    elif(value == "displace" or value == "dis" or value =="제외" or value == "디스플레이스"):
        await interaction.response.send_message("```ansi\n이 명령어는 플레이어를 대신 제외시키는 명령어입니다.\n같은 명령어 = [4;1m디스플레이스[0m [4;1m제외[0m [4;1mdisplace[0m [4;1mdip[0m\n[1;31m매우[0m [1;31m중요!![0m [1;31m이[0m [1;31m명령어를[0m [1;31m악용할시[0m [1;31m이[0m [1;31m봇을[0m [1;31m사용할[0m [1;31m수[0m [1;31m없을[0m [1;31m수도[0m [1;31m있습니다!!![0m```",ephemeral=True)
    elif(value == "coin" or value == "ci" or value =="코인"):
        await interaction.response.send_message("```ansi\n이 명령어는 현재 당신의 코인들을 알려주는 명령업니다.\n코인은 내전을 하시면 늘어나고 [4;1m도박[0m을 하시면 늘거나 줄어들 수 있습니다.\n코인은 나중에 [4;1m경매[0m를 할때 사용이 가능하십니다.\n같은 명령어 = [4;1m코인[0m [4;1mcoin[0m [4;1mci[0m```",ephemeral=True)
    elif(value == "gamble" or value == "gb" or value == "겜블" or value == "도박"):
        await interaction.response.send_message("```ansi\n이 명령어는 코인을 사용해 러시안 룰렛을 하는 여러가지 추가 명령이 있는 명령업니다.\n아이디어:[4;1m최주찬[0m\n추가 명령어를 보고싶다면 [4;1m$gb[0m를 치시면 됩니다.\n주의:도박중독은 [4;1m1336[0m\n같은 명령어 = [4;1m겜블[0m [4;1m도박[0m [4;1mgamble[0m [4;1mgb[0m```",ephemeral=True)
    elif(value == "auction" or value == "경매" or value == "옥션" or value == "at"):
        await interaction.response.send_message("```ansi\n이 명령어는 경매를 통해 자신이 원하는 사람을 자신의 내전 팀으로 옮기는 여러가지 명령어를 가진 명령어입니다.\n이 명령어에 자세하게 알고싶다면 [4;1m$auction[0m을 사용해 확인하세요.\n같은 명령어 = [4;1m옥션[0m [4;1m경매[0m [4;1mauction[0m [4;1mat[0m```",ephemeral=True)
    elif(value == "프로필" or value == "prf" or value == "profile"):
        await interaction.response.send_message("```ansi\n이 명령어는 자신의 개인프로필을 확인 및 수정하는 명령어 입니다\n같은 명령어 = 프로필 prf proflie```",ephemeral=True)
    elif(value == "tire" or value == "티어" or value == "tr"):
        await interaction.response.send_message("```ansi\n이 명령어는 러버덕의 모든 사람들의 티어를 출력하는 명령어 입니다.\n같은 명령어 = 티어 tr tire```",ephemeral=True)
    else:
        await interaction.response.send_message("```ansi\n[31;1m존재하지 않는 명령어입니다.[0m```",ephemeral=True)

@client.tree.command(name="in", description="인 참가")
async def in_game(interaction: discord.Interaction):
    user = interaction.user
    users = user.display_name
    user_id = str(user.id)

    fightfind(user=user_id)
    existing_fighter = cursor.fetchone()

    teamfind(user=user_id,team="team")
    existing_team = cursor.fetchone()

    if existing_fighter is None:
        cursor.execute(f'INSERT INTO fight (name,ID) VALUES (?,?)', (users,user_id,))
        commit()

    if existing_team:
        await interaction.response.send_message(f'**{users}**님은 이미 게임에 참가한 상태입니다!')
    else:
        cursor.execute('INSERT INTO team (name, tire, point, position, subposition, intro, ID) SELECT name, COALESCE(tire, 0), COALESCE(point, 0),COALESCE(position, "미정"),COALESCE(subposition, "미정"),COALESCE(intro, "미정") , COALESCE(ID, 0) FROM fight WHERE ID = ?', (user_id,))
        commit()
        await interaction.response.send_message(f'**{users}**님이 게임에 참가했습니다.')

@client.tree.command(name="out", description="아웃 퇴장")#게임에 퇴장하는 명령어
async def outasdf(interaction: discord.Interaction):
    user = interaction.user
    users = user.display_name
    user_id = str(user.id)

    teamfind(user=user_id,team="team")
    out_fighter = cursor.fetchone()
    
    if out_fighter:
        cursor.execute('DELETE FROM team WHERE ID = ?', (user_id,))
        commit()
        await interaction.response.send_message(f'**{users}**님이 게임에서 퇴장하였습니다.')
    else:
        await interaction.response.send_message(f'**{users}**님은 게임에 참여해 있지 않습니다.') 

@client.tree.command(name='replace', description="rep 리플레이스 포함")
async def repasdf(interaction: discord.Interaction, mention: discord.Member):  
        user_id = mention.id
        user_nickname = mention.display_name

        fightfind(user=user_id)
        replace_fighter = cursor.fetchone()
            
        teamfind(user=user_id, team="team")
        existing_team = cursor.fetchone()
            
        if not replace_fighter:
            cursor.execute('INSERT INTO fight (name,ID) VALUES (?,?)', (user_nickname,user_id,))
            commit()
                
        if existing_team:
            await interaction.response.send_message(f'**{user_nickname}**님은 이미 게임에 참가한 상태입니다!',ephemeral=True)
        else:
            cursor.execute('INSERT INTO team (name, tire, point, position, subposition, intro, ID) SELECT name, tire, point, position, subposition, intro, ID FROM fight WHERE ID = ?', (user_id,))
            commit()
            await interaction.response.send_message(f"**{user_nickname}**님을 게임에 추가합니다.")

@client.tree.command(name='displace', description="dis 디스플레이스 퇴장")
async def displace(interaction: discord.Interaction, mention: discord.Member):

    nickname = mention.display_name
    user_id = mention.id
    teamfind(user=user_id, team="team")
    displace_fighter = cursor.fetchone()
        
    if  displace_fighter:
        cursor.execute('DELETE FROM team WHERE ID = ?', (user_id,))
        commit()
        await interaction.response.send_message(f'**{nickname}**님이 게임에서 퇴장하였습니다.')
    else:
        await interaction.response.send_message(f"**{nickname}**님은 게임에 참여해 있지 않습니다.",ephemeral=True)

@client.tree.command(name='list',description="리스트 ls 인원")#게임에 참가한 사람들을 출력해주는 명령어
async def list_fuction(interaction: discord.Interaction):
    team(team="team")
    fighters = cursor.fetchall()
    
    if not fighters:
        await interaction.response.send_message("지금 참가한 사람이 없습니다.",ephemeral=True)
    else:
        await interaction.response.send_message("지금 게임에 참가한 사람들을 출력합니다")
        fighter_list = '\n'.join([f'<@{team[6]}>' for team in fighters])
        await interaction.followup.send(f'***_player list_***')
        await interaction.followup.send(f'\n{fighter_list}')

@client.tree.command(description="rd 랜덤 섞기", name='random')  # 플레이어를 섞는 명령어
@app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id))
async def rdasdf(interaction: discord.Interaction):
    
        team(team="team")
        fighter = cursor.fetchall()
        
        cursor.execute('DELETE FROM team_one')
        cursor.execute('DELETE FROM team_two')
        commit()
            
        if len(fighter) <= 1 or len(fighter) % 2 == 1 or len(fighter) > 10:
            await interaction.response.send_message("팀의 인원이 1명이거나 10명 이상 혹은 플레이어가 홀수라 명령어를 실행할 수 없습니다.",ephemeral=True)
            return
        
        min_diff = float('inf')
        
        teamer = [(data[0], data[2], data[6]) for data in fighter]
        random.shuffle(teamer)
        final_group1, final_group2 = [], []

        for comb in combinations(range(len(teamer)), len(teamer) // 2):
            group1 = [(teamer[i]) for i in comb]
            group2 = [(teamer[i]) for i in range(len(teamer)) if i not in comb]

            sum_team1 = sum(point_id[1] for point_id in group1)
            sum_team2 = sum(point_id[1] for point_id in group2)
            diff = abs(sum_team1 - sum_team2)

            if diff < min_diff:
                min_diff = diff
                final_group1 = group1
                final_group2 = group2
                
        user_id1 = [data[2] for data in final_group1]
        user_id2 = [data[2] for data in final_group2]
        for data in fighter:
            if data[6] in user_id1:
                cursor.execute('INSERT INTO team_one (name, tire, point, position, subposition, intro, ID) VALUES(?,?,?,?,?,?,?)', data,)
                commit()
            elif data[6] in user_id2:
                cursor.execute('INSERT INTO team_two (name, tire, point, position, subposition, intro, ID) VALUES(?,?,?,?,?,?,?)', data,)
                commit()
        cursor.execute('SELECT name FROM team_one')
        team_one_data = cursor.fetchall()
        cursor.execute('SELECT name FROM team_two')
        team_two_data = cursor.fetchall()

        team_one_members = '\n'.join([data[0] for data in team_one_data])
        team_two_members = '\n'.join([data[0] for data in team_two_data])
        await interaction.response.send_message('팀을 나누겠습니다.')
        await interaction.followup.send(f'```ansi\n[1;31mTeam 1[0m [1;31;4m\n{team_one_members}[0m```')
        await interaction.followup.send(f'```ansi\n[1;34mTeam 2[0m [1;34;4m\n{team_two_members}[0m```')
        all_voice_channels = interaction.guild.voice_channels
            
        for voice_channel in all_voice_channels:
            for member in voice_channel.members:
                member_id = member.id
                if (member_id,) in team_one_data:
                    target_channel = discord.utils.get(all_voice_channels, name="귀찮지만 내전은 하고 싶은 방")
                    if target_channel: 
                        await member.move_to(target_channel)
                elif (member_id,) in team_two_data:
                    target_channel = discord.utils.get(all_voice_channels, name="귀찮지만 내전은 하고 싶은 방2")
                    if target_channel:
                        await member.move_to(target_channel)

@client.tree.error
async def on_error(interaction: discord.Interaction, error: Exception):
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        await interaction.response.send_message(f"쿨타임입니다. 잠시 후 다시 시도해주세요.", ephemeral=True)

@client.tree.command(description="코인 ci",name="coin")#코인을 출력해주는 명령어
async def coinasdf(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user = interaction.user.display_name
    cursor.execute('SELECT coin FROM fight WHERE ID = ?', (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        await interaction.response.send_message("게임에 참가한 적이 없습니다.",ephemeral=True)
    else:
        your_coin = result[0]
        await interaction.response.send_message(f"{user}님의 코인: {your_coin}coin",ephemeral=True) 
        
class ProfileButton(View):
    line = ""
    async def process_interaction(self, interaction: discord.Interaction, value: str):
        user = interaction.user
        users = user.display_name
        self.line = value 
        self.stop() 

    @discord.ui.button(label="TOP", style=discord.ButtonStyle.primary)
    async def button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, "TOP")

    @discord.ui.button(label="JG", style=discord.ButtonStyle.primary)
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, "JG")
    
    @discord.ui.button(label="MID", style=discord.ButtonStyle.primary)
    async def button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, "MID")

    @discord.ui.button(label="AD", style=discord.ButtonStyle.primary)
    async def button_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, "AD")
    
    @discord.ui.button(label="SUP", style=discord.ButtonStyle.primary)
    async def button_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, "SUP")

class ProfileModal(Modal):
    def __init__(self):
        super().__init__(title="자기소개")
        self.content_input = TextInput(label="내용", placeholder="자신을 소개하세요", required=False)
        self.add_item(self.content_input)
        
    async def on_submit(self, interaction: discord.Interaction):
        user_profile = self.content_input.value
        await interaction.response.send_message(f"확인되었습니다.", ephemeral=True)

class RiotModal(Modal):
    def __init__(self):
        super().__init__(title="Riot")
        self.riot_input = TextInput(label="이름", placeholder="플레이어 이름을 적으세요.", required=True)
        self.add_item(self.riot_input)
        self.tag_input = TextInput(label="Tag", placeholder="KR1", max_length=5,required=True)
        self.add_item(self.tag_input)
        
    async def on_submit(self, interaction: discord.Interaction):
        player_name = self.riot_input.value
        game_tag = self.tag_input.value
        await interaction.response.send_message(f"확인되었습니다.", ephemeral=True)

@client.tree.command(description="프로필 prf", name="profile")
async def prfasdf(interaction: discord.Interaction, value : str = ""):
    user_id = str(interaction.user.id)
    fightfind(user=user_id)
    user_profile = cursor.fetchone()
    if value == "":
        await interaction.response.send_message("```ansi\n이 명령어는 나의 프로필을 확인 및 수정하는 명령어입니다.\nprofile의 명령어 : [1;4mcheck[0m or [1;4mposition[0m or [1;4msubposition[0m or [1;4mintro[0m가 있습니다.\n[1;4mcheck[0m : 자신의 프로필을 확일할 때 사용할 수 있습니다.\n[1;4mposition[0m : 자신의 주라인을 바꿀 때 사용할 수 있습니다.\n[1;4msubposition[0m : 자신이 부라인을 바꿀 때 사용할 수 있습니다.\n[1;4mintro[0m : 자신을 소개할 때 사용할 수 있습니다.```",ephemeral=True)
    elif (value == "check" or value == "chk" or value == "확인" or value == "체크"):
        await interaction.response.send_message(f"이름 : {user_profile[0]}\n티어 : {user_profile[1]}\n주라인 : {user_profile[4]}\n부라인 : {user_profile[5]}\n자기소개 : {user_profile[6]}",ephemeral=True)
    elif (value == "position" or value == "pst" or value == "포지션" or value == "주라인"):
        view = ProfileButton()
        message = await interaction.response.send_message("주로 가는 라인을 바꿉니다. 주로가는 / 희망하는 라인을 선택해 주세요.",view=view, ephemeral=True)
        view.message = message
        await view.wait()
        line = view.line
        cursor.execute(f'UPDATE fight SET position = ? WHERE ID = ?',(line, user_id,))
        commit()
        await interaction.followup.send("확인되었습니다.",ephemeral=True)
    elif (value == "subposition" or value == "sub" or value == "서브포지션" or value == "부라인"):
        view = ProfileButton()
        message = await interaction.response.send_message("보조로 가는 라인을 바꿉니다. 보조로가는 / 희망하는 라인을 선택해 주세요.",view = view,ephemeral=True)
        view.message = message
        await view.wait()
        line = view.line
        cursor.execute(f'UPDATE fight SET subposition = ? WHERE ID = ?',(line, user_id,))
        commit()
        await interaction.followup.send("확인되었습니다.",ephemeral=True)
    elif (value == "intro" or value == "itr" or value == "인트로" or value == "자기소개"):
        modal = ProfileModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        content = modal.content_input.value
        cursor.execute(f'UPDATE fight SET intro = ? WHERE ID = ?',(content, user_id,))
        commit()
    elif (value == "riot" or value == "라이엇" or value == "ri"):
        modal = RiotModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        player_name = modal.riot_input.value
        tag = modal.tag_input.value
        tag = tag.replace('#','')
        cursor.execute(f"UPDATE fight SET riot = ?, tag = ? WHERE ID = ?",(player_name, tag,user_id,))
        commit()
    else:
        await interaction.response.send_message("잘못된 명령어입니다.",ephemeral=True)

@client.tree.command(description="티어 tr", name="tire")
@app_commands.checks.cooldown(1, 3.0, key=lambda i: (i.guild_id))
async def tire(interaction: discord.Interaction):
    await interaction.response.send_message("현재 러버덕의 모든 사람들의 티어를 알려드리겠습니다.",ephemeral=True)

    tire_groups = {}

    for i in range(1, 6):
        cursor.execute(f'SELECT * FROM fight WHERE tire - {i} < 1 and tire - {i} >= 0 ORDER BY tire')
        tire_group = cursor.fetchall()

        if tire_group:
            tire_group_info = []
            tire_group_info.append("```ansi\n")
            if i == 1:
                tire_group_info.append(f"[1;31m{i}Tire")
            if i == 2:
                tire_group_info.append(f"[1;34m{i}Tire")
            if i == 3:
                tire_group_info.append(f"[1;36m{i}Tire")
            if i == 4:
                tire_group_info.append(f"[1;33m{i}Tire")
            if i == 5:
                tire_group_info.append(f"[1;30m{i}Tire")
                
            for info in tire_group:
                info_str = f"이름: {info[0]} / 티어: {info[1]} Tire \n MP: {info[4]} / SP: {info[5]} / intro: {info[6]}\n"
                tire_group_info.append(info_str)
            tire_group_info.append("```")
            tire_groups[i] = tire_group_info
        else:
            tire_group_info = []
            tire_group_info.append("```ansi\n")
            if i == 1:
                tire_group_info.append(f"[1;31m{i}Tire")
            if i == 2:
                tire_group_info.append(f"[1;34m{i}Tire")
            if i == 3:
                tire_group_info.append(f"[1;36m{i}Tire")
            if i == 4:
                tire_group_info.append(f"[1;33m{i}Tire")
            if i == 5:
                tire_group_info.append(f"[1;30m{i}Tire")
            tire_group_info.append("존재하지 않습니다.```")
            tire_groups[i] = tire_group_info
    for i in range(1, 6):
        await interaction.followup.send("\n".join(tire_groups[i]),ephemeral=True)
            
class GambleModal(Modal):
    your_money = 0
    def __init__(self):
        super().__init__(title="배팅")
        self.money_input = TextInput(label="금액", placeholder="배팅할 금액을 알려주십시오.", required=False)
        self.add_item(self.money_input)
        
    async def on_submit(self, interaction: discord.Interaction):
        users = str(interaction.user.id)
        user_name = interaction.user.display_name
        user_money = self.money_input.value
        try:
            int_value = int(self.money_input.value)
            if int_value < 1:
                raise ValueError("금액은 1 이상이어야 합니다.")
            if int_value > self.your_money:
                raise ValueError("금액이 부족합니다.")
            await interaction.response.send_message(f"{user_name}님이 {user_money}만큼 배팅힙니다.")

        except ValueError as e:
            if (str(e) == "금액은 1 이상이어야 합니다." or str(e) == "금액이 부족합니다."):
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"{str(e)}", ephemeral=True)
            else:
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"숫자만 가능합니다.", ephemeral=True)

class ShootView(View):
    number = 0
    limit = 0
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    @discord.ui.button(label="선택", style=discord.ButtonStyle.red)
    async def enter_name_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (interaction.user.id == self.owner):
            modal = ShootModal(self)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("당신은 선택받은 자가 아닙니다.",ephemeral=True)

class ShootModal(Modal):
    def __init__(self, shootview: ShootView):
        super().__init__(title="선택")
        self.shootview = shootview
        self.choice_input = TextInput(label="선택", placeholder="선택할 플레이어의 번호를 입력하세요.", required=True)
        self.add_item(self.choice_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            int_value = int(self.choice_input.value)
            if (int_value < 1 or int_value > self.shootview.limit):
                raise ValueError("플레이어의 번호는 범위 안에 있어야 합니다.")
            user = interaction.user
            users = user.display_name
            self.shootview.number = int_value
            await interaction.response.send_message(f"{int_value}번 플레이어를 {users}님이 쏘기 시작합니다...")
            await self.shootview.disable_all_items()
            self.shootview.stop()

        except ValueError as e:
            if str(e) == "플레이어의 번호는 범위 안에 있어야 합니다.":
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"{str(e)}", ephemeral=True)
            else:
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"숫자만 가능합니다.", ephemeral=True)

@client.tree.command(description = "도박 겜블 gb",name="gamble")
async def gb(interaction: discord.Interaction, value : str = ""):
    user = interaction.user
    users = str(interaction.user.id)
    user_name = user.display_name
    cursor.execute("SELECT coin FROM fight WHERE ID = ?", (users,))
    money =  cursor.fetchone()[0]
    
    if money is None:
        await interaction.response.send_message("아에 참가한 적이 없습니다 $in을 치세요.",ephemeral=True)
    elif money == 0:
        await interaction.response.send_message("돈이 없습니다.",ephemeral=True)
    else:
        if value == "":
            await interaction.response.send_message("```java\n명령어의 종류 \n1.in : 게임에 참가하는 명령업니다.\n같은 명령어 : in / 인 / 참가\n2.out : 게임에 퇴장하는 명령업니다.\n같은 명령어 : out / 아웃 / 퇴장\n3.money : 게임에 걸린 돈들을 보는 명령어입니다.\n같은 명령어 :  money / mn / 머니 / 판돈\n4.bet : 게임에 돈을 거는 명령업니다.\n같은 명령어 : bet / 배팅 / 걸기\n5.list : 지금 도박에 참여한 사람들을 확인하는 명령업니다.\n같은 명령어 : list / ls / 리스트 / 인원\n6.start : 러시안 룰렛을 시작하는 명령업니다.\n같은 명령어 : start / st / 스타트 / 시작```",ephemeral=True)

        elif (value == "in" or value == "참가" or value == "인"): #참가하는 명령어
            cursor.execute('SELECT * FROM gamble WHERE ID = ?', (users,))
            player = cursor.fetchone()
            if player:
                await interaction.response.send_message("이미 참가되어 있습니다.",ephemeral=True)
            else:
                cursor.execute('INSERT INTO gamble (name,coin,ID) values(?,?,?)', (user_name,money,users,))
                commit()
                cursor.execute("SELECT COUNT(*) FROM gamble")
                num = cursor.fetchone()
                cursor.execute('UPDATE gamble SET num = ? WHERE ID = ?',(num[0],users,))
                commit()
                await interaction.response.send_message(f"러시안 룰렛에 **{user_name}**님이 참가합니다.")
                
        elif (value == "out" or value == "아웃" or value == "퇴장"):#게임에서 나가는 명령어
            cursor.execute('SELECT * FROM gamble WHERE ID = ?', (users,))
            out_fighter = cursor.fetchone()
    
            if out_fighter:
                cursor.execute('DELETE FROM gamble WHERE ID = ?', (users,))
                commit()
                await interaction.response.send_message(f'**{user_name}**님이 게임에서 이탈합니다.')
            else:
                await interaction.response.send_message(f'참여하지 않는 사람은 나가실 수 없습니다.',ephemeral=True) 
                
        elif (value == "money" or value == "mn" or value == "판돈" or value == "머니"):#게임의 판돈을 보는 명령어
            cursor.execute('SELECT SUM(money) FROM gamble')
            game_money = cursor.fetchone()
            
            if game_money[0] == 0:
                await interaction.response.send_message("걸린 돈이 없습니다.",ephemeral=True)
            else:
                await interaction.response.send_message(f"이 한 게임의 판돈 : {game_money[0]}",ephemeral=True)
                
        elif (value == "bet" or value == "걸기" or value == "배팅"):#게임에 돈을 거는 명령어
            cursor.execute('SELECT coin FROM gamble WHERE ID = ?', (users,))
            your_money = cursor.fetchone()[0]
            modal = GambleModal()
            await interaction.response.send_modal(modal)
            modal.your_money = your_money
            await modal.wait()
            bet_money = modal.money_input.value

            cursor.execute('UPDATE gamble SET money = money + ? WHERE ID = ?', (bet_money, users,))
            cursor.execute('UPDATE gamble SET coin = coin - ? WHERE ID = ?', (bet_money, users,))
            cursor.execute('UPDATE gamble SET dividend = (SELECT SUM(money) FROM gamble)')
            cursor.execute("UPDATE fight SET coin = coin - ? WHERE ID = ?",(bet_money,users,))
            commit()

            cursor.execute('SELECT coin FROM gamble WHERE ID = ?', (users,))
            change = cursor.fetchone()[0]
            await interaction.followup.send(f"{user_name}님의 남은 돈 : {change}",ephemeral=True)

        elif (value == "list" or value == "ls" or value == "리스트" or value == "인원"):#게임에 참가한 사람들 보여주기
            cursor.execute('SELECT ID , num FROM gamble')
            mamber = cursor.fetchall()
            
            gamble_mm = '\n'.join([f'***{data[1]}***. <@{data[0]}>' for data in mamber])
            await interaction.response.send_message(f"***게임에 참가한 사람들*** \n{gamble_mm}")
        
        elif (value == "start" or value == "st" or value == "시작" or value == "스타트"):  # 도박 시작
            cursor.execute('SELECT * FROM gamble')
            members = cursor.fetchall()
            num = len(members)
            if client.command_in_use :
                await interaction.response.send_message("이미 러시안 룰렛이 시작되었습니다. 끝날 때까지 기다려주세요.", ephemeral=True)
                return


            if num is None:
                await interaction.response.send_message("참가한 사람이 없습니다.",ephemeral=True)
            elif num > 1:
                client.command_in_use = True
                await interaction.response.send_message(f"참가한 인원 {num}명\n게임을 시작하겠습니다.")
                
                while (num != 1):
                    unluck = random.randrange(1, 6)
                    circle = True
                    cursor.execute('SELECT ID, num FROM gamble')
                    member = cursor.fetchall()
                    gamble_mm = '\n'.join([f'***{data[1]}***. <@{data[0]}>' for data in member])
                    await interaction.followup.send(f"***게임에 참여한 사람들*** \n{gamble_mm}")

                    own = random.choice(member)
                    await interaction.followup.send(f"<@{own[0]}>님이 총을 쥐었습니다.")
                    check = own[0]
                    while(circle):
                        view = ShootView()
                        message = await interaction.channel.send(view=view)

                        view.message = message
                        view.owner = check
                        view.limit = num

                        await view.wait()

                        number = view.number
                        cursor.execute("SELECT * FROM gamble WHERE num = ?", (number,))
                        check = cursor.fetchone()[3]

                        if check is None:
                            await interaction.followup.send("그 플레이어는 쏠 수 없습니다.")
                        else:
                            unluck = unluck - 1
                            if unluck <= 1:
                                circle = False
                                num = num - 1
                                await interaction.followup.send(f"<@{check}>님은 선택받은 사람이 아니였습니다.")
                                cursor.execute("SELECT ID,money FROM gamble WHERE num = ?",(number,))
                                loser = cursor.fetchone()
                                cursor.execute("UPDATE fight SET coin = coin - ? WHERE ID = ?",(loser[1],loser[0],))
                                cursor.execute("DELETE FROM gamble WHERE num = ?",(number,))
                                commit()
                            else:
                                await interaction.followup.send(f"총의 주인은 이제 <@{check}>님 입니다.")
                                cursor.execute('SELECT ID, num FROM gamble')
                                member = cursor.fetchall()
                                gamble_mm = '\n'.join([f'***{data[1]}***. <@{data[0]}>' for data in member])
                                await interaction.followup.send(f"***게임에 참여한 사람들*** \n{gamble_mm}")

                cursor.execute("SELECT ID,dividend FROM gamble")
                last = cursor.fetchone()
                await interaction.followup.send(f"<@{last[0]}>님이 최후의 생존자 입니다.")
                cursor.execute("UPDATE fight SET coin = coin + ? WHERE ID = ?",(last[1],last[0],))
                cursor.execute("DELETE FROM gamble")
                commit()
                client.command_in_use = False
            else:
                await interaction.response.send_message("혼자서는 게임을 못 합니다.",ephemeral=True)
        else:
            await interaction.response.send_message("잘못된 명령어",ephemeral=True)
#----------------------------------------------------------------------------------------------------------------------------
class AuctionView(View):
    money = 5
    name = ""

    def __init__(self,timeout: float = 10):
        super().__init__(timeout=timeout)
    
    async def on_timeout(self) -> None:
        await self.disable_all_items()

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    def reset_timeout(self):
        self.timeout = 10

    async def process_interaction(self, interaction: discord.Interaction, value: int):
        self.money += value
        user = interaction.user
        users = user.display_name
        self.name = users
        await interaction.response.send_message(f"입찰 금액 : {self.money} - {users}")

    @discord.ui.button(label="+5", style=discord.ButtonStyle.primary)
    async def button_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, 5)

    @discord.ui.button(label="+10", style=discord.ButtonStyle.primary)
    async def button_10(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, 10)

    @discord.ui.button(label="+50", style=discord.ButtonStyle.primary)
    async def button_50(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, 50)

    @discord.ui.button(label="+100", style=discord.ButtonStyle.primary)
    async def button_100(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_interaction(interaction, 100)
    
    @discord.ui.button(label="입찰", style=discord.ButtonStyle.primary)
    async def enter_name_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = NameInputModal(self)
        await interaction.response.send_modal(modal)

class NameInputModal(Modal):
    def __init__(self, auction_view: AuctionView):
        super().__init__(title="입찰")
        self.auction_view = auction_view
        self.money_input = TextInput(label="금액", placeholder="입찰 금액을 입력하세요", required=True)
        self.add_item(self.money_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            int_value = int(self.money_input.value)
            if int_value < 1:
                raise ValueError("금액은 1 이상이어야 합니다.")
            user = interaction.user
            users = user.display_name
            self.name = users
            self.auction_view.money += int_value
            self.auction_view.reset_timeout()
            self.auction_view.name = users
            await interaction.response.send_message(f"입찰 금액 : {self.auction_view.money} - {users}")

        except ValueError as e:
            if str(e) == "금액은 1 이상이어야 합니다.":
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"{str(e)}", ephemeral=True)
            else:
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"숫자만 가능합니다.", ephemeral=True)

button = True
@client.tree.command(name="auction",description="옥션 경매 auc" )
async def auction(interaction: discord.Interaction, value : str = ""):
    user = interaction.user
    user_id = str(interaction.user.id)
    user_name = user.display_name
    fightfind(user = user_id)
    player = cursor.fetchone()[0]
    global button

    team(team = team)
    team_count = len(cursor.fetchall())
    team(team = auction)
    auction_count = len(cursor.fetchall())

    if(value == "in" or value == "참가" or value == "인"):
        if(auction_count >= 2):
            await interaction.response.send_message("경매에 참여하실 수 없습니다.",ephemeral=True)
            return
        
        cursor.execute("SELECT * FROM auction WHERE ID = ?",(user_id,))
        check = cursor.fetchone()[0]
        if(check is not None):
            await interaction.response.send_message(f"{user_name}님은 이미 경매에 참가했습니다.",ephemeral=True)
        else:
            await interaction.response.send_message(f"{user_name}님이 경매에 참가합니다.")
            cursor.execute("INSERT INTO auction values(?,?,?,?,?,?)",(player[0],player[1],player[2],player[4],player[5],player[6],player[7],player[8],player[9]))
            cursor.execute("DELETE FROM team WHERE ID = ?"(user_id,))
            commit()

    if(value == "start" or value == "st" or value == "시작" or value == "스타트"):
        if not (button):
            await interaction.response.send_message("실행하실 수 없습니다.",ephemeral=True)
            return
        if (team_count > 8 or team_count % 2 == 1):
            await interaction.response.send_message("대기열에 있는 사람의 수가 이상합니다.",ephemeral=True)
            return
        if (auction_count >= 2 or auction_count % 2 == 1):
            await interaction.response.send_message("경매에 참여한 사람의 수가 이상합니다.",ephemeral=True)
            return
        
        cursor.execute("SELECT * FROM team")
        checklist = cursor.fetchall()
        button = False
        
        await interaction.response.send_message("경매가 시작되었습니다!")

        for check in checklist:
            embed = discord.Embed(
                title=f"{check[0]}",
                description=f"{check[1]}",
                color=discord.Color.blurple()
            )

            embed.set_thumbnail(url="https://i.namu.wiki/i/zmaUOORwV8b4zdqU7YshHxBknjVqo2OpijLShyYW6f61rBNh_2KzJtjNZxqJ6phjdSX87S9jTR5e9Avg7pt3vQ.webp")
            embed.add_field(name="Main Position",value=f"{check[3]}", inline=False)
            embed.add_field(name="Sub Position", value=f"{check[4]}", inline=True)
            embed.set_footer(text=f"{check[5]}")

            view = AuctionView()
            message = await interaction.channel.send(view=view,embed=embed)
            view.message = message
            await view.wait()
        
            if(view.name == ""):
                await interaction.followup.send("유찰되었습니다.")
                await asyncio.sleep(1)
            else :
                await interaction.followup.send(f"경매 종료! 의 가격은 {view.money}")
                await asyncio.sleep(1)
        
        button = True


@client.tree.command(name="embed")
async def embed_with_button(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(interaction.user.id)
    user_name = user.display_name
    view = AuctionView()
    cursor.execute("SELECT * FROM team WHERE ID = ?",(user_id,))
    check = cursor.fetchone()
    embed = discord.Embed(
        title=f"{check[0]}",
        description=f"{check[1]}",
        color=discord.Color.blurple()
    )

    embed.set_thumbnail(url="https://i.namu.wiki/i/zmaUOORwV8b4zdqU7YshHxBknjVqo2OpijLShyYW6f61rBNh_2KzJtjNZxqJ6phjdSX87S9jTR5e9Avg7pt3vQ.webp")
    embed.add_field(name="Main Position",value=f"{check[3]}", inline=False)
    embed.add_field(name="Sub Position", value=f"{check[4]}", inline=True)
    embed.set_footer(text=f"{check[5]}")
    await interaction.response.send_message("test")
    message = await interaction.channel.send(embed=embed,view=view)
    view.message = message


minsung_junior = os.getenv('MINSUNGJUNIOR')
client.run(minsung_junior)