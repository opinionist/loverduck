import sqlite3

con = sqlite3.connect("DateBase.db", isolation_level = None)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS fight (name TEXT, tire REAL DEFAULT 0, point REAL DEFAULT 0, coin INTEGER DEFAULT 500, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
cur.execute("CREATE TABLE IF NOT EXISTS team_one(name TEXT, tire REAL, point REAL, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
cur.execute("CREATE TABLE IF NOT EXISTS team_two(name TEXT, tire REAL, point REAL, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
cur.execute("CREATE TABLE IF NOT EXISTS team(name TEXT, tire REAL, point REAL, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
cur.execute("CREATE TABLE IF NOT EXISTS gamble (name TEXT, coin INTEGER DEFAULT 0, money INTEGER DEFAULT 0, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)")
cur.execute("CREATE TABLE IF NOT EXISTS auction (name TEXT, tire REAL, point REAL, payment INTEGER DEFAULT 0, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")

com = sqlite3.connect("sub.db", isolation_level= None)
cmr = com.cursor()
cmr.execute("CREATE TABLE IF NOT EXISTS copy (name TEXT, tire REAL DEFAULT 0, point REAL DEFAULT 0, coin INTEGER DEFAULT 500, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")

#이거는 fight.db라는 데이터에 sub.db 데이터를 옮기는 명령어
# cmr.execute('SELECT * FROM copy')
# copy_data = cmr.fetchall()

# for row in copy_data:
#     cur.execute('INSERT INTO fight (name, tire, point, coin, position, subposition, intro, ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', row)    
# con.commit()

# 이거는 sub.db라는 데이터에 fight.db 데이터를 옮기는 명령어
# cur.execute('SELECT * FROM fight')
# data = cur.fetchall()

# for row in data:
#     cmr.execute('INSERT INTO copy (name, tire, point, coin, position, subposition, intro, ID) VALUES (?,?,?,?,?,?,?,?)', row)
# com.commit()