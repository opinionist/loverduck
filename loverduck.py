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
client = commands.Bot(command_prefix='$', intents=intents, help_command = None)
conn = sqlite3.connect('DateBase.db')
cursor = conn.cursor()

rd_allowed = True #random명렁어를 제어하는거
st_allowed = False #start new명령어를 제어하는거
en_allowed = False #end명령어를 제어하는거(real 제외)
lk_allowed = False #start like명령어를 제어하는거

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
    
@client.command(aliases=["메뉴얼","도움말","mn","manual"],name='help')#명령어에 대해서 설명해주는 명령어
async def helpasdf(x, *, message=None):
    if message is None:
        await x.author.send("명령어들을 알려드립니다.```java\n1.in\n2.out\n3.random\n4.end\n5.start\n6.list\n7.replace\n8.displace\n9.coin\n10.profile\n11.gamble(만드는 중...)\n12.auction(만드는 중...)```")
        await x.author.send("```ansi\n명령어들은 각각 영어 발음, 영어 약어, 영어 의미(한글)로 사용할 수 있습니다.\n명령어에 대하여 좀 더 자세하게 알고싶다면 [1m$메뉴얼 / $도움말 / $help / $mn +'명령어'[0m로 확인하세요\nex) $메뉴얼 인 / $도움말 퇴장 / $help end / $mn st```")
    elif(message == "in" or message == "인" or message == "참가"):
        await x.author.send("```ansi\n이 명령어는 게임에 참가하는 명령어입니다.\n같은 명령어 = [4;1m인[0m [4;1m참가[0m [4;1min[0m```")
    elif(message == "out" or message == "아웃" or message == "퇴장"):
        await x.author.send("```ansi\n이 명령어는 참가한 게임에서 퇴장하는 명령어입니다.\n같은 명령어 = [4;1m아웃[0m [4;1m퇴장[0m [4;1mout[0m```")
    elif(message == "end" or message == "종료" or message =="엔드"):
        await x.author.send("```ansi\n이 명령어는 누가 이겼는지를 입력받아 coin을 지급하는 명령어입니다.\n내전을 완전히 끝냈을 땐 [1m$end real[0m 명령어를 사용해주 세요\n같은 명령어 = [4;1m엔드[0m [4;1m종료[0m [4;1mend[0m```")
    elif(message == "random" or message == "섞기" or message == "랜덤" or message == "rd"):
        await x.author.send("```ansi\n이 명령어는 팀을 섞은 후 통화방을 나누는 명령어입니다.\n같은 명령어 = [4;1m랜덤[0m [4;1m섞기[0m [4;1mrandom[0m [4;1mrd[0m```")
    elif(message == "replace" or message == "rpl" or message == "포함" or message == "리플레이스"):
        await x.author.send("```ansi\n이 명령어는 플레이어를 대신 참가시키는 명령어입니다.\n같은 명령어 = [4;1m리플레이스[0m [4;1m포함[0m [4;1mreplace[0m [4;1mrep[0m\n[1;31m매우[0m [1;31m중요!![0m [1;31m이[0m [1;31m명령어를[0m [1;31m악용할시[0m [1;31m이[0m [1;31m봇을[0m [1;31m사용할[0m [1;31m수[0m [1;31m없을[0m [1;31m수도[0m [1;31m있습니다!!![0m```")
    elif(message == "list" or message == "리스트" or message == "ls" or message == "인원"):
        await x.author.send("```ansi\n이 명령어는 현재 팀을 출력해주는 명령어입니다.\n같은 명령어 = [4;1m리스트[0m [4;1m인원[0m [4;1mlist[0m [4;1mls[0m```")
    elif(message == "displace" or message == "dsp" or message =="제외" or message == "디스플레이스"):
        await x.author.send("```ansi\n이 명령어는 플레이어를 대신 제외시키는 명령어입니다.\n같은 명령어 = [4;1m디스플레이스[0m [4;1m제외[0m [4;1mdisplace[0m [4;1mdip[0m\n[1;31m매우[0m [1;31m중요!![0m [1;31m이[0m [1;31m명령어를[0m [1;31m악용할시[0m [1;31m이[0m [1;31m봇을[0m [1;31m사용할[0m [1;31m수[0m [1;31m없을[0m [1;31m수도[0m [1;31m있습니다!!![0m```")
    elif(message == "coin" or message == "ci" or message =="코인"):
        await x.author.send("```ansi\n이 명령어는 현재 당신의 코인들을 알려주는 명령업니다.\n코인은 내전을 하시면 늘어나고 [4;1m도박[0m을 하시면 늘거나 줄어들 수 있습니다.\n코인은 나중에 [4;1m경매[0m를 할때 사용이 가능하십니다.\n같은 명령어 = [4;1m코인[0m [4;1mcoin[0m [4;1mci[0m```")
    elif(message == "gamble" or message == "gb" or message == "겜블" or message == "도박"):
        await x.author.send("```ansi\n이 명령어는 코인을 사용해 러시안 룰렛을 하는 여러가지 추가 명령이 있는 명령업니다.\n아이디어:[4;1m최주찬[0m\n추가 명령어를 보고싶다면 [4;1m$gb[0m를 치시면 됩니다.\n주의:도박중독은 [4;1m1336[0m\n같은 명령어 = [4;1m겜블[0m [4;1m도박[0m [4;1mgamble[0m [4;1mgb[0m```")
    elif(message == "auction" or message == "경매" or message == "옥션" or message == "at"):
        await x.author.send("```ansi\n이 명령어는 경매를 통해 자신이 원하는 사람을 자신의 내전 팀으로 옮기는 여러가지 명령어를 가진 명령어입니다.\n이 명령어에 자세하게 알고싶다면 [4;1m$auction[0m을 사용해 확인하세요.\n같은 명령어 = [4;1m옥션[0m [4;1m경매[0m [4;1mauction[0m [4;1mat[0m```")
    elif(message == "start" or  message == "st" or message == "스타트" or message =="시작"):
        await x.author.send("```ansi\n이 명령어는 간단하게 팀에 있는 사람수에 비례해 참가한 사람에게 coin을 지급하는 명령어입니다.\n같은 명령어 = [4;1m스타트[0m [4;1m시작[0m [4;1mstart[0m [4;1mst[0m```")
    elif(message == "프로필" or message == "prf" or message == "profile"):
        await x.author.send("```ansi\n이 명령어는 사용자의 프로필을 확인 및 수정하는 명령어입니다.\n같은 명령어 = [4;1m프로필[0m [4;1mprofile[0m [4;1mprf[0m```")
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

@client.command(aliases=["종료", "엔드"], name="end")#참가한 인원을 초기화시키는 명령어
async def endasdf(x,*,message=None):
    global rd_allowed
    global st_allowed
    global en_allowed
    global lk_allowed
    
    team(team="team_one")
    team_one = cursor.fetchall()
    team(team="team_two")
    team_two = cursor.fetchall()
    
    if message is None:
        await x.author.send("```ansi\n이 명령어는 이긴팀의 번호를 써 이긴팀에게 더 많은 [1;4mcoin[0m을 제공하거나 팀들을 초기화하는 명령어입니다.\nend의 명령어 : [1;4mone[0m [1;4mtwo[0m [1;4mreal[0m \n[1;4mone[0m은 1팀이 [1;4mtwo[0m는 2팀이 이겼을때 사용하시면 됩니다. \n같은 명령어 : [1;4mone[0m [1;4m일[0m [1;4m원[0m / [1;4mtwo[0m [1;4m이[0m [1;4m투[0m ex) $end 일 / $end 2\n[1;4mreal[0m은 내전이 끝났을때 사용하시면 됩니다. \n같은 명령어 : [1;4mreal[0m [1;4m정말[0m [1;4mra[0m [1;4m리얼[0m ex) $end 리얼```")
    elif(message == "real" or message =="ra" or message == "정말" or message == "리얼"):
        cursor.execute('DELETE FROM team')
        cursor.execute('DELETE FROM team_one')
        cursor.execute('DELETE FROM team_two')
        commit()
        rd_allowed = True
        st_allowed = False
        en_allowed = False
        lk_allowed = False
        await x.send("데이터베이스가 초기화 되었습니다.")
    elif (message == "1" or message == "one" or message == "일" or message == "원"):
        if(st_allowed):
            en_allowed = False
            st_allowed = False
            rd_allowed = True
            
            cursor.execute('SELECT ID FROM team_one')
            teamer_one = [record[0] for record in cursor.fetchall()]
            for user_id in teamer_one:
                cursor.execute('UPDATE fight SET coin = coin + ? WHERE ID = ?', (len(team_one)*60,user_id,))
                commit()
            
            cursor.execute('SELECT ID FROM team_two')
            teamer_two = [record[0] for record in cursor.fetchall()]
            for user_id in teamer_two:
                cursor.execute('UPDATE fight SET coin = coin + ? WHERE ID = ?', (len(team_two)*20,user_id,))
                commit()
                
            await x.send("1팀이 승리했습니다")
        else:
            await x.send("start명령어를 사용해야 가능합니다.")
    elif (message == "2" or message == "이" or message == "two" or message == "투"):
        if(st_allowed):
            en_allowed = False
            st_allowed = False
            rd_allowed = True
            
            cursor.execute('SELECT ID FROM team_two')
            teamer_two = [record[0] for record in cursor.fetchall()]
            
            for user_id in teamer_two:
                cursor.execute('UPDATE fight SET coin = coin + ? WHERE ID = ?', (len(team_two)*60,user_id,))
                commit()
            
            cursor.execute('SELECT ID FROM team_one')
            teamer_one = [record[0] for record in cursor.fetchall()]
            
            for user_id in teamer_one:
                cursor.execute('UPDATE fight SET coin = coin + ? WHERE ID = ?', (len(team_one)*20,user_id,))
                commit()
                
            await x.send("2팀이 승리했습니다.")
        else:
            await x.send("start명령어를 사용해야 가능합니다.")
    else:
        await x.send("명령어 형식이 잘못되었거나 지금 팀에 아무도 없습니다.")

@client.command(aliases=["포함", "rpl", "리플레이스"],name='replace')#플레이어를 포함시키는 명령어
async def rplasdf(ctx, *, message=None):  
    global en_allowed
    if message is None:
        await ctx.author.send("```이 명령어는 남을 대신 추가시키는 명령어입니다. ex) $replace @귀차니즘 러덕```")
    elif message[1] != "@":
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

@client.command(aliases=["dsp", "제외", "디스플레이스"],name='displace')#플레이어를 제외시키는 명령어
async def dipasdf(x, *, message=None):
    if message is None:
        await x.author.send("```이 명령어는 남을 대신 추가시키는 명령어입니다. ex) $displace @귀차니즘 러덕```")
    elif message[1] != "@":
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
        cursor.execute('SELECT * FROM team_one')
        team_one_data = cursor.fetchall()
        cursor.execute('SELECT * FROM team_two')
        team_two_data = cursor.fetchall()

        team_one_members = '\n'.join([data[0] for data in team_one_data])
        team_two_members = '\n'.join([data[0] for data in team_two_data])
        
        cursor.execute('SELECT ID FROM team_one')
        toI = cursor.fetchall()
        cursor.execute('SELECT ID FROM team_two')
        ttI = cursor.fetchall()
        
        
        
        await ctx.send(f'```ansi\n[1;31mTeam 1[0m [1;31;4m\n{team_one_members}[0m```')
        await ctx.send(f'```ansi\n[1;34mTeam 2[0m [1;34;4m\n{team_two_members}[0m```')
        all_voice_channels = ctx.guild.voice_channels
            
        for voice_channel in all_voice_channels:
            for member in voice_channel.members :
                member_ID = member.id
                for i in range(5):
                    toI[i] = toI[i]
                    ttI[i] = ttI[i]
                    if member_ID in toI[i] :
                        target_channel = discord.utils.get(all_voice_channels, name="귀찮지만 내전은 하고 싶은 방")
                        if target_channel:
                            await member.move_to(target_channel)
                    elif member_ID in ttI[i] :
                        target_channel = discord.utils.get(all_voice_channels, name="귀찮지만 내전은 하고 싶은 방2")
                        if target_channel:
                            await member.move_to(target_channel)
    else:
        await ctx.send("end명령어를 사용해 주세요.")

@client.command(aliases=["시작","st","스타트"], name="start")
async def stasdf(x,*,message=None):
    global rd_allowed
    global st_allowed
    global lk_allowed
    global en_allowed
    cursor.execute('SELECT ID FROM team')
    teamer = [record[0] for record in cursor.fetchall()]
    
    if message is None:
        await x.author.send("```ansi\n이 명령어는 플레이를 하는 사람에게 coin을 주기위한 명령어입니다.\nstart의 명령어 : [1;4mnew[0m or [1;4msame[0m가 있습니다.\n[1;4mnew[0m는 [1m팀이 rd로 인해 달라졌을때 사용하시면 됩니다.\n같은 명령어 : [1;4mnew[0m [1;4m새팀[0m [1;4m뉴[0m ex) $start 새팀\n[1;4msame[0m는 [1m저번 팀이랑 비슷할 때 사용하면 됩니다.\n같은 명령어 : [1;4msame[0m [1;4m같은팀[0m [1;4msm[0m [1;4m샘[0m ex) $start sm```")
    elif(message == 'new' or message == '뉴' or message == '새팀'):
        if(en_allowed):
            if(st_allowed):
                await x.send("end명령어를 사용하세요.")
            else:
                if len(teamer) % 2 == 0:
                    await x.send("지금 팀으로 시작합니다.")
                    rd_allowed = False
                    st_allowed = True
                    lk_allowed = True
                    for user_id in teamer:
                        cursor.execute('UPDATE fight SET coin = coin + ? WHERE ID = ?', (len(teamer)/2*100,user_id))
                        commit()
                else:
                    await x.send("사람 수가 안 맞습니다.")
        else:
            await x.send("random명령어를 사용하세요.")
            
    elif(message == 'same' or message == "샘" or message == "sm" or message == "같은팀"):
        if(lk_allowed):
            if(st_allowed):
                await x.send("end명령어를 사용하세요.")
            else:
                await x.send("지금 팀으로 시작합니다.")
                rd_allowed = False
                st_allowed = True
                for user_id in teamer:
                    cursor.execute('UPDATE fight SET coin = coin + ? WHERE ID = ?', (len(teamer)/2*100,user_id))
                    commit()
        else:
            await x.send("전에 있던 팀이 없습니다.")
    else:
        await x.author.send("없는 명령어입니다.")
        
@client.command(aliases=["코인","ci"],name="coin")#코인을 출력해주는 명령어
async def coinasdf(ctx):
    user_id = str(ctx.author.id)
    user = ctx.author.display_name
    cursor.execute('SELECT coin FROM fight WHERE ID = ?', (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        await ctx.author.send("게임에 참가한 적이 없습니다.")
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
        await ctx.author.send("```ansi\n이 명령어는 나의 프로필을 확인 및 수정하는 명령어입니다.\nprofile의 명령어 : [1;4mcheck[0m or [1;4mposition[0m or [1;4msubposition[0m or [1;4mintro[0m가 있습니다.\n[1;4mcheck[0m : 자신의 프로필을 확일할 때 사용할 수 있습니다. \n같은 명령어 : [1;4mcheck[0m [1;4m확인[0m [1;4mcc[0m [1;4m체크[0m ex) $profile cc\n[1;4mposition[0m : 자신의 주라인을 바꿀 때 사용할 수 있습니다.\n같은 명령어 : [1;4mposition[0m [1;4m포지션[0m [1;4mpst[0m ex) $profile pst\n[1;4msubposition[0m : 자신이 부라인을 바꿀 때 사용할 수 있습니다.\n같은 명령어 : [1;4msubposition[0m [1;4m서브포지션[0m [1;4msbp[0m ex) $profile sbp\n[1;4mintro[0m : 자신을 소개할 때 사용할 수 있습니다.\n같은 명령어 : [1;4mintro[0m [1;4m자기소개[0m [1;4mitr[0m [1;4m인트로[0m ex) $profile itr```")
    elif (message == "check" or message == "cc" or message == "확인" or message == "체크"):
        await ctx.send(f"```이름 : {user_profile[0][0]}\n티어 : {user_profile[0][1]}\n주라인 : {user_profile[0][4]}\n부라인 : {user_profile[0][5]}\n자기소개 : {user_profile[0][6]}```")
    elif (message == "position" or message == "pst" or message == "포지션" or message == "주라인"):
        await ctx.author.send("주로 가는 라인을 바꿉니다. 주로가는 / 희망하는 라인을 입력해 주세요.")
        while True:
            user_message = await client.wait_for('message', check=lambda m: m.author == ctx.author)
            if (user_message.content[0] == "$"):
                await ctx.author.send("명령어는 불가능합니다.")
                break
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
                break
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
                break
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
                info_str = f"이름: {info[0]} / 티어: {info[1]} Tire \nMP: {info[4]} / SP: {info[5]} / intro: {info[6]}\n"
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
            tire_group_info.append("```존재하지 않습니다.```")
            tire_groups[i] = tire_group_info
            
    for i in range(1, 6):
        await ctx.author.send("\n".join(tire_groups[i]))

@client.event #에러가 뜨면 출력해주는 명령어
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound, ):
        await ctx.send("```ansi\n[31;1m잘못된[0m [31;1m명령입니다.[0m```")

@client.event
async def on_message(message):
    blacklist = []
    if message.author.id in blacklist:
        return  # 블랙리스트에 있는 사용자는 봇 명령을 무시
    await client.process_commands(message)

loverduck_token = os.getenv('LOVERDUCK')
client.run(loverduck_token)