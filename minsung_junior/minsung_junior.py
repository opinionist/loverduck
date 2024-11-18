import discord
import random
import asyncio
import sqlite3
from itertools import combinations
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='%', intents=intents, help_command = None)
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
    
@client.command(aliases=["메뉴얼", "hl","도움말",""],name='help')#명령어에 대해서 설명해주는 명령어
async def helpasdf(x, *, message=None):
    if message is None:
        await x.author.send("명령어들을 알려드립니다.```java\n1.in\n2.out\n3.random\n6.list\n7.replace\n8.displace\n9.coin(만드는 중...)\n10.gamble(만드는 중...)\n11.auction(만드는 중...)\n12.profile(만드는 중...)```")
        await x.author.send("```ansi\n명령어들은 각각 한글, 영어(줄임말) 영어의미로 할 수 있습니다.\n명령어에 대하여 좀 더 자세하게 알고싶다면 [1m$메뉴얼 / $도움말 / $help / $hl +'명령어'[0m로 확인하세요\nex) $메뉴얼 인 / $도움말 퇴장 / $help rd / $mu tire```")
    elif(message == "in" or message == "인" or message == "참가"):
        await x.author.send("```ansi\n이 명령어는 게임에 참가하는 명령어입니다.\n같은 명령어 = [4;1m인[0m [4;1m참가[0m [4;1min[0m```")
    elif(message == "out" or message == "아웃" or message == "퇴장"):
        await x.author.send("```ansi\n이 명령어는 참가한 게임에서 퇴장하는 명령어입니다.\n같은 명령어 = [4;1m아웃[0m [4;1m퇴장[0m [4;1mout[0m```")
    elif(message == "random" or message == "섞기" or message == "랜덤" or message == "rd"):
        await x.author.send("```ansi\n이 명령어는 팀을 섞은 후 통화방을 나누는 명령어입니다.\n같은 명령어 = [4;1m랜덤[0m [4;1m섞기[0m [4;1mrandom[0m [4;1mrd[0m```")
    elif(message == "replace" or message == "rep" or message == "포함" or message == "리플레이스"):
        await x.author.send("```ansi\n이 명령어는 플레이어를 대신 참가시키는 명령어입니다.\n같은 명령어 = [4;1m리플레이스[0m [4;1m포함[0m [4;1mreplace[0m [4;1mrep[0m\n[1;31m매우[0m [1;31m중요!![0m [1;31m이[0m [1;31m명령어를[0m [1;31m악용할시[0m [1;31m이[0m [1;31m봇을[0m [1;31m사용할[0m [1;31m수[0m [1;31m없을[0m [1;31m수도[0m [1;31m있습니다!!![0m```")
    elif(message == "list" or message == "리스트" or message == "ls" or message == "인원"):
        await x.author.send("```ansi\n이 명령어는 현재 팀을 출력해주는 명령어입니다.\n같은 명령어 = [4;1m리스트[0m [4;1m인원[0m [4;1mlist[0m [4;1mls[0m```")
    elif(message == "displace" or message == "dis" or message =="제외" or message == "디스플레이스"):
        await x.author.send("```ansi\n이 명령어는 플레이어를 대신 제외시키는 명령어입니다.\n같은 명령어 = [4;1m디스플레이스[0m [4;1m제외[0m [4;1mdisplace[0m [4;1mdip[0m\n[1;31m매우[0m [1;31m중요!![0m [1;31m이[0m [1;31m명령어를[0m [1;31m악용할시[0m [1;31m이[0m [1;31m봇을[0m [1;31m사용할[0m [1;31m수[0m [1;31m없을[0m [1;31m수도[0m [1;31m있습니다!!![0m```")
    elif(message == "coin" or message == "ci" or message =="코인"):
        await x.author.send("```ansi\n이 명령어는 현재 당신의 코인들을 알려주는 명령업니다.\n코인은 내전을 하시면 늘어나고 [4;1m도박[0m을 하시면 늘거나 줄어들 수 있습니다.\n코인은 나중에 [4;1m경매[0m를 할때 사용이 가능하십니다.\n같은 명령어 = [4;1m코인[0m [4;1mcoin[0m [4;1mci[0m```")
    elif(message == "gamble" or message == "gb" or message == "겜블" or message == "도박"):
        await x.author.send("```ansi\n이 명령어는 코인을 사용해 러시안 룰렛을 하는 여러가지 추가 명령이 있는 명령업니다.\n아이디어:[4;1m최주찬[0m\n추가 명령어를 보고싶다면 [4;1m$gb[0m를 치시면 됩니다.\n주의:도박중독은 [4;1m1336[0m\n같은 명령어 = [4;1m겜블[0m [4;1m도박[0m [4;1mgamble[0m [4;1mgb[0m```")
    elif(message == "auction" or message == "경매" or message == "옥션" or message == "at"):
        await x.author.send("```ansi\n이 명령어는 경매를 통해 자신이 원하는 사람을 자신의 내전 팀으로 옮기는 여러가지 명령어를 가진 명령어입니다.\n이 명령어에 자세하게 알고싶다면 [4;1m$auction[0m을 사용해 확인하세요.\n같은 명령어 = [4;1m옥션[0m [4;1m경매[0m [4;1mauction[0m [4;1mat[0m```")
    elif(message == "프로필" or message == "prf" or message == "profile"):
        await x.author.send("```ansi\n이 명령어는 자신의 개인프로필을 확인 및 수정하는 명령어 입니다\n같은 명령어 = 프로필 prf proflie```")
    elif(message == "tire" or message == "티어" or message == "tr"):
        await x.author.send("```ansi\n이 명령어는 러버덕의 모든 사람들의 티어를 출력하는 명령어 입니다.\n같은 명령어 = 티어 tr tire```")
    else:
        await x.author.send("```ansi\n[31;1m존재하지 않는 명령어입니다.[0m```")

@client.command(aliases=["인", "참가"], name="in")  # 게임에 참가하는 명령어
async def inasdf(ctx):
    global en_allowed
    users = ctx.author.display_name
    user_id = str(ctx.author.id)

    fightfind(user=user_id)
    existing_fighter = cursor.fetchone()

    teamfind(user=user_id,team="team")
    existing_team = cursor.fetchone()

    if existing_fighter is None:
        cursor.execute(f'INSERT INTO fight (name,ID) VALUES (?,?)', (users,user_id,))
        commit()

    if existing_team:
        await ctx.send(f'**{users}**님은 이미 게임에 참가한 상태입니다!')
    else:
        cursor.execute('INSERT INTO team (name, tire, point, position, subposition, intro, ID) SELECT name, COALESCE(tire, 0), COALESCE(point, 0),COALESCE(position, "미정"),COALESCE(subposition, "미정"),COALESCE(intro, "미정") , COALESCE(ID, 0) FROM fight WHERE ID = ?', (user_id,))
        commit()
        await ctx.send(f'**{users}**님이 게임에 참가했습니다.')
        en_allowed = False

@client.command(aliases=["아웃", "퇴장"], name="out")#게임에 퇴장하는 명령어
async def outasdf(ctx):
    users = ctx.author.display_name
    user_id = str(ctx.author.id)

    teamfind(user=user_id,team="team")
    out_fighter = cursor.fetchone()
    
    if out_fighter:
        cursor.execute('DELETE FROM team WHERE ID = ?', (user_id,))
        commit()
        await ctx.send(f'**{users}**님이 게임에서 퇴장하였습니다.')
    else:
        await ctx.send(f'**{users}**님은 게임에 참여해 있지 않습니다.') 

@client.command(aliases=["포함", "rep", "리플레이스"],name='replace')#플레이어를 포함시키는 명령어
async def repasdf(ctx, *, message=None):  
    global en_allowed
    if message is None or message[1] != "@":
        await ctx.send("명령어의 형식이 잘못되었습니다. 올바른 형식은 `$replace @{플레이어}` 입니다.")
    else:
        user = ctx.message.mentions[0]
        user_id = user.id
        user_nickname = user.display_name

        fightfind(user=user_id)
        replace_fighter = cursor.fetchone()
        
        teamfind(user=user_id, team="team")
        existing_team = cursor.fetchone()
        
        if not replace_fighter:
            cursor.execute('INSERT INTO fight (name,ID) VALUES (?,?)', (user_nickname,user_id,))
            commit()
            
        if existing_team:
            await ctx.send(f'**{user_nickname}**님은 이미 게임에 참가한 상태입니다!')
        else:
            cursor.execute('INSERT INTO team (name, tire, point, position, subposition, intro, ID) SELECT name, tire, point, position, subposition, intro, ID FROM fight WHERE ID = ?', (user_id,))
            commit()
            await ctx.send(f"**{user_nickname}**님을 게임에 추가합니다.")
            en_allowed = False

@client.command(aliases=["dis", "제외", "디스플레이스"],name='displace')#플레이어를 제외시키는 명령어
async def dipasdf(x, *, message=None):
    if message is None or message[1] != "@":
        await x.send("명령어의 형식이 잘못되었습니다. 올바른 형식은 '$displace @{플레이어}' 입니다.")
    else:
        user = x.message.mentions[0]
        nickname = user.display_name
        user_id = user.id
        teamfind(user=user_id, team="team")
        displace_fighter = cursor.fetchone()
        
        if  displace_fighter:
            cursor.execute('DELETE FROM team WHERE ID = ?', (user_id,))
            commit()
            await x.send(f'**{nickname}**님이 게임에서 퇴장하였습니다.')
        else:
            await x.send(f"**{nickname}**님은 게임에 참여해 있지 않습니다.")

@client.command(aliases = ["리스트" , "ls"],name='list')#게임에 참가한 사람들을 출력해주는 명령어
async def lsasdf(x):
    team(team="team")
    fighters = cursor.fetchall()
    
    if not fighters:
        await x.send("지금 참가한 사람이 없습니다.")
    else:
        await x.send("지금 게임에 참가한 사람들을 출력합니다")
        fighter_list = '\n'.join([f'<@{team[6]}>' for team in fighters])
        await x.send(f'***_player list_***')
        await x.send(f'\n{fighter_list}')

@client.command(aliases=["rd", "랜덤", "섞기"], name='random')  # 플레이어를 섞는 명령어
@commands.cooldown(1, 3, commands.BucketType.default)
async def rdasdf(ctx):
    global rd_allowed
    global en_allowed
    global lk_allowed
    
    if rd_allowed:
        team(team="team")
        fighter = cursor.fetchall()
        en_allowed = True
        lk_allowed = False
        
        cursor.execute('DELETE FROM team_one')
        cursor.execute('DELETE FROM team_two')
        commit()
            
        if len(fighter) <= 1 or len(fighter) % 2 == 1 or len(fighter) > 10:
            await ctx.send("팀의 인원이 1명이거나 10명 이상 혹은 플레이어가 홀수라 명령어를 실행할 수 없습니다.")
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

        await ctx.send(f'```ansi\n[1;31mTeam 1[0m [1;31;4m\n{team_one_members}[0m```')
        await ctx.send(f'```ansi\n[1;34mTeam 2[0m [1;34;4m\n{team_two_members}[0m```')
        all_voice_channels = ctx.guild.voice_channels
            
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
    else:
        await ctx.send("end명령어를 사용해 주세요.")

        
@client.command(aliases=["코인","ci"],name="coin")#코인을 출력해주는 명령어
async def coinasdf(ctx):
    user_id = str(ctx.author.id)
    user = ctx.author.display_name
    cursor.execute('SELECT coin FROM fight WHERE ID = ?', (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        await ctx.author.send("게임에 참가한 적이 없네요?")
    else:
        your_coin = result[0]
        await ctx.author.send(f"{user}님의 코인: {your_coin}coin") 
        
@client.command(aliases=["프로필", "prf"], name="profile")
async def prfasdf(ctx,*,message = None):
    user_id = str(ctx.author.id)
    fightfind(user=user_id)
    user_profile = cursor.fetchall()
    commit()
    if message is None:
        await ctx.author.send("```ansi\n이 명령어는 나의 프로필을 확인 및 수정하는 명령어입니다.\nprofile의 명령어 : [1;4mcheck[0m or [1;4mposition[0m or [1;4msubposition[0m or [1;4mintro[0m가 있습니다.\n[1;4mcheck[0m : 자신의 프로필을 확일할 때 사용할 수 있습니다.\n[1;4mposition[0m : 자신의 주라인을 바꿀 때 사용할 수 있습니다.\n[1;4msubposition[0m : 자신이 부라인을 바꿀 때 사용할 수 있습니다.\n[1;4mintro[0m : 자신을 소개할 때 사용할 수 있습니다.```")
    elif (message == "check" or message == "chk" or message == "확인" or message == "체크"):
        await ctx.author.send(f"이름 : {user_profile[0][0]}\n티어 : {user_profile[0][1]}\n주라인 : {user_profile[0][4]}\n부라인 : {user_profile[0][5]}\n자기소개 : {user_profile[0][6]}")
    elif (message == "position" or message == "pst" or message == "포지션" or message == "주라인"):
        await ctx.author.send("주로 가는 라인을 바꿉니다. 주로가는 / 희망하는 라인을 입력해 주세요.")
        while True:
            user_message = await client.wait_for('message', check=lambda m: m.author == ctx.author)
            if (user_message.content[0] == "$"):
                await ctx.author.send("명령어는 불가능합니다.")
                continue
            else:
                cursor.execute(f'UPDATE fight SET position = ? WHERE ID = ?',(user_message.content, user_id,))
                commit()
                await ctx.author.send("확인되었습니다.")
                break
    elif (message == "subposition" or message == "sub" or message == "서브포지션" or message == "부라인"):
        await ctx.author.send("보조로 가는 라인을 바꿉니다. 보조로가는 / 희망하는 라인을 입력해 주세요.")
        while True:
            user_message = await client.wait_for('message', check=lambda m: m.author == ctx.author)
            if (user_message.content[0] == "$"):
                await ctx.author.send("명령어는 불가능합니다.")
                continue
            else:
                cursor.execute(f'UPDATE fight SET subposition = ? WHERE ID = ?',(user_message.content, user_id,))
                commit()
                await ctx.author.send("확인되었습니다.")
                break
    elif (message == "intro" or message == "itr" or message == "인트로" or message == "자기소개"):
        await ctx.author.send("자신을 마음껏 표현해주세요.")
        while True:
            user_message = await client.wait_for('message', check=lambda m: m.author == ctx.author)
            if (user_message.content[0] == "$"):
                await ctx.author.send("명령어는 불가능합니다.")
                continue
            else:
                cursor.execute(f'UPDATE fight SET intro = ? WHERE ID = ?',(user_message.content, user_id,))
                commit()
                await ctx.author.send("확인되었습니다.")
                break
    else:
        await ctx.author.send("잘못된 명령어입니다.")

@client.command(aliases=["티어", "tr"], name="tire")
@commands.cooldown(1, 3, commands.BucketType.default)
async def tire(ctx):
    await ctx.author.send("현재 러버덕의 모든 사람들의 티어를 알려드리겠습니다.")

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
        await ctx.author.send("\n".join(tire_groups[i]))
            
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["도박","겜블","gb"],name="gamble")
async def gb(ctx, *, message=None):
    users = ctx.author.display_name
    cursor.execute("SELECT coin FROM fight WHERE name = ?", (users,))
    money =  cursor.fetchone()
    
    if money is None:
        await ctx.send("아에 참가한 적이 없습니다 $in을 치세요.")
    elif money[0] == 0:
        await ctx.send("돈이 없습니다.")
    else:
        if message is None:
            await ctx.author.send("```java\n명령어의 종류 \n1.in : 게임에 참가하는 명령업니다.\n같은 명령어 : in / 인 / 참가\n2.out : 게임에 퇴장하는 명령업니다.\n같은 명령어 : out / 아웃 / 퇴장\n3.money : 게임에 걸린 돈들을 보는 명령어입니다.\n같은 명령어 :  money / mn / 머니 / 판돈\n4.bet : 게임에 돈을 거는 명령업니다.\n같은 명령어 : bet / 배팅 / 걸기\n5.list : 지금 도박에 참여한 사람들을 확인하는 명령업니다.\n같은 명령어 : list / ls / 리스트 / 인원\n6.start : 러시안 룰렛을 시작하는 명령업니다.\n같은 명령어 : start / st / 스타트 / 시작```")
        elif (message == "in" or message == "참가" or message == "인"): #참가하는 명령어
            cursor.execute('SELECT * FROM gamble WHERE name = ?', (users,))
            player = cursor.fetchone()
            if player:
                await ctx.send("이미 참가되어 있습니다.")
            else:
                await ctx.send(f"러시안 룰렛에 **{users}**님이 참가합니다.")
                cursor.execute('INSERT INTO gamble (name,coin) values(?,?)', (users,money))
                commit()
                
        elif (message == "out" or message == "아웃" or message == "퇴장"):#게임에서 나가는 명령어
            cursor.execute('SELECT * FROM gamble WHERE name = ?', (users,))
            out_fighter = cursor.fetchone()
    
            if out_fighter:
                cursor.execute('DELETE FROM gamble WHERE name = ?', (users,))
                commit()
                await ctx.send(f'**{users}**님이 게임에서 이탈합니다..??')
            else:
                await ctx.send(f'참여하지 않는 사람은 나가실 수 없습니다.**{users}**') 
                
        elif (message == "money" or message == "mn" or message == "판돈" or message == "머니"):#게임의 판돈을 보는 명령어
            cursor.execute('SELECT SUM(money) FROM gamble')
            game_money = cursor.fetchone()
            
            if game_money[0] == 0:
                await ctx.send("걸린 돈이 없습니다.")
            else:
                await ctx.send(f"이 한 게임의 판돈 : {game_money[0]}")
                
        elif (message == "bet" or message == "걸기" or message == "배팅"):#게임에 돈을 거는 명령어
            await ctx.send("얼마를 걸겁니까?")

            def check(message):
                return message.author == ctx.author
            try:
                bet_message = await client.wait_for("message", check=check, timeout=10)
                bet_amount = bet_message.content

                if not bet_amount.isdigit():
                    await ctx.send("숫자여야 합니다.")
                else:
                    bet_amount = int(bet_amount)
                    cursor.execute('SELECT coin FROM gamble WHERE name = ?', (users,))
                    your_money = cursor.fetchone()[0]

                    if bet_amount > your_money:
                        await ctx.send("자본이 부족합니다.")
                    elif bet_amount <= 0:
                        await ctx.send("0 또는 음수는 불가능합니다.")
                    else:
                        await ctx.send(f"배팅 금액: **{bet_amount}**coin")
                        cursor.execute('UPDATE gamble SET coin = ? WHERE name = ?', (your_money - bet_amount, users,))
                        commit()
                        cursor.execute('SELECT money FROM gamble WHERE name = ?', (users,))
                        your_bet = cursor.fetchone()
                        cursor.execute('UPDATE gamble SET money = ? WHERE name = ?', (your_bet[0]+bet_amount, users,))
                        commit()
                        await ctx.send(f"**{users}**님의 남은 코인: **{your_money - bet_amount}**coin")
            except asyncio.TimeoutError:
                await ctx.send("시간이 초과되었습니다. 베팅이 취소되었습니다.")
                
        elif (message == "list" or message == "ls" or message == "리스트" or message == "인원"):#게임에 참가한 사람들 보여주기
            cursor.execute('SELECT name FROM gamble')
            mamber = cursor.fetchall()
            
            gamble_mm = '\n'.join([data[0] for data in mamber])
            await ctx.send(f"```게임에 참여한 사람들 \n{gamble_mm}```")
        
        elif (message == "start" or message == "st" or message == "시작" or message == "스타트"):  # 도박 시작
            cursor.execute('SELECT * FROM gamble')
            members = cursor.fetchall()
            num = len(members)

            if num is None:
                await ctx.send("참가한 사람이 없습니다.")
            elif num > 1:
                persent = num
                await ctx.send(f"참가한 인원 {num}명\n게임을 시작하겠습니다.")
                own = random.choice(members)
                while True:
                    await ctx.send(f"{own[0]}님? 누구를 쏘실건가요?")
                    def cheak(message):
                        return message.author == own[0]
                    try:
                        gb_msg = await client.wait_for("message", check=cheak, timeout=10)
                        gb_am = gb_msg.content
                        gb_kl = gb_am.replace('@', '')
                        unluck = random.randrange(1, persent)
                        luck = random.randrange(1, persent)
                        if (unluck == luck):
                            await ctx.send(f"{gb_kl}님이 사망하셨습니다. 아쉬워라")
                            persent = 7
                        else:
                            persent -= 1
                            await ctx.send(f"{gb_kl}님이 살아남으셨습니다. 남은 확률{persent}분의 1")
                            own[0] = gb_kl
                        cursor.execute('SELECT * FROM gamble')
                        surviber = cursor.fetchall()
                        if (len(surviber) == 1):
                            await ctx.send(f"축하합니다. {surviber[0]}님 당신은 살아남으셨습니다.")
                    except asyncio.TimeoutError:
                        if (unluck == luck):
                            await ctx.send(f"{own}님이 자신을 쐈고 그 결과는 참혹했습니다.")
                            persent = 7
                        else:
                            await ctx.send(f"{own}님이 살아남으셨습니다.")
                            persent -= 1
                    if (serve == 1):
                        break
                return  # 게임 종료 후 더 이상 진행하지 않도록 리턴
            else:
                await ctx.author.send("혼자서는 게임을 못 합니다.")
        else:#오타나 다른거 치면 나오는 에러 잡는거
            await ctx.send("잘못된 명령어")
#러시안 룰렛 이건 나중에 업데이트 할것. 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
@client.command(aliases=["at","경매","옥션"],name="auction")
async def atasdf(x,*,message = None):
    users = x.author.display_name
    team(team="team")
    atlist = cursor.fetchall()
    
    if message is None:
        await x.author.send("```이 명령어는 플래이어들을 선발하는 명령어입니다.```")
    elif(message == "리더" or message == "leader" or message == "ldr" or message == "지도자"):
            if len(atlist) / 2 > 1 and len(atlist) % 2 == 0:
                team(team="team_one")
                tolist = cursor.fetchone()
                team(team="team_two")
                twlist = cursor.fetchone()
                if(tolist is None):
                    await x.send(f"{users}님이 1팀의 리더입니다.")
                    cursor.execute('INSERT INTO team_one (name, tire, point) SELECT name, COALESCE(tire, 0), COALESCE(point, 0) FROM team WHERE name = ?', (users,))
                    commit()
                elif(twlist is None):
                    teamfind(team="team_one",user=users)
                    toli = cursor.fetchone()
                    if(toli):
                        await x.send("당신은 이미 1팀의 리더입니다.")
                    else:
                        await x.send(f"{users}님이 2팀의 리더입니다.")
                        cursor.execute('INSERT INTO team_two (name, tire, point) SELECT name, COALESCE(tire, 0), COALESCE(point, 0) FROM team WHERE name = ?', (users,))
                        commit()
                else:
                    await x.send("이미 모든 팀의 리더가 있습니다.")
            else:
                await x.send("내전에 참가한 사람이 부족하거나 홀수입니다.")
                
    elif(message == "start" or message == "시작" or message == "st" or message == "시작"):
        cursor.execute("DELETE FROM auction")
        commit()
        if len(atlist) / 2 > 1 and len(atlist) % 2 == 0:
            team(team="team")
            tlist = cursor.fetchall()
            team(team="team_one")
            tolist = cursor.fetchone()
            team(team="team_two")
            twlist = cursor.fetchone()
            if(tolist is None or twlist is None):
                await x.send("팀에 리더가 부족합니다.")
            else:
                for team_info in tlist:
                    cursor.execute("INSERT INTO auction (name, tire, point, position, subposition, intro, ID) VALUES (?, ?, ?, ?, ?, ?, ?)", team_info)
                    commit()
                cursor.execute("DELETE FROM auction WHERE name = ?",(tolist[0],))
                cursor.execute("DELETE FROM auction WHERE name = ?",(twlist[0],))
                commit()
                cursor.execute("SELECT * FROM auction")
                atls = cursor.fetchall()
                await x.send("경매를 시작합니다.")
                
                for atmem in atls:
                    cursor.execute("SELECT coin FROM fight WHERE name = ?",(tolist[0],))
                    ldr1coin = cursor.fetchone()
                    cursor.execute("SLEECT coin FROM fight WHERE name = ?"(twlist[0],))
                    ldr2coin = cursor.fetchone()
                    await x.send(f"이름 : {atmem[0]}\n티어 : {atmem[1]}\n주라인 : {atmem[3]}\n부라인 : {atmem[4]}\n자기소개 : {atmem[5]}")
                    bttl1 = 0
                    bttl2 = 0
                    while True:
                        def check(message):
                            return message.author == tolist[0] or message.author == twlist[0]
                        try:
                            bet_message = await client.wait_for("message", check=check, timeout=10)
                            bet_amount = bet_message.content

                            if not bet_amount.isdigit():
                                await x.send("숫자여야 합니다.")
                            else:
                                if(message.author == tolist[0]):
                                    bttl1 = bttl1 + bet_amount
                                    if(bet_amount <= ldr1coin or ldr1coin - bttl1 > 0):
                                        await x.send(f"```ansi\nn[1;31m{atmem[0]} : {bet_amount}n[0m```")
                                        await x.author.send(f"사용 가능한 코인 : {ldr1coin-bttl1}")
                                    else:
                                        await x.send("돈이 부족합니다.")
                                if(message.author == twlist[0]):
                                    bttl2 = bttl2 + bet_amount
                                    if(bet_amount <= ldr2coin or ldr2coin - bttl2 > 0):
                                        await x.send(f"```ansi\nn[1;34m{atmem[0]} : {bet_amount}n[0m```")
                                        await x.author.send(f"사용 가능한 코인 : {ldr2coin-bttl2}")
                                    else:
                                        await x.send("돈이 부족합니다.")
                        except asyncio.TimeoutError:
                            cursor.execute("UPDATE fight SET coin")
                            commit() 
        else:
            await x.send("내전에 참가한 사림이 부족하거나 홀수입니다.")
    else:
        await x.author.send("잘못된 명령어입니다.")

@client.event#에러가 뜨면 출력해주는 명령어
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound, ):
        await ctx.send("잘못된 명령입니다.")
        
@client.event#블랙리스트
async def on_message(message):
    blacklist = [640894329942719850]
    if message.author.id in blacklist:
        return  # 블랙리스트에 있는 사용자는 봇 명령을 무시
    await client.process_commands(message)
        


minsung_junior = os.getenv('MINSUNGJUNIOR')
client.run(minsung_junior)