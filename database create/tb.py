import sqlite3

tes = sqlite3.connect("test.db", isolation_level = None)
tet = tes.cursor()
tet.execute("CREATE TABLE IF NOT EXISTS fight (name TEXT, tire REAL DEFAULT 0, point REAL DEFAULT 0, coin INTEGER DEFAULT 500, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
tet.execute("CREATE TABLE IF NOT EXISTS team_one(name TEXT, tire REAL, point REAL, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
tet.execute("CREATE TABLE IF NOT EXISTS team_two(name TEXT, tire REAL, point REAL, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
tet.execute("CREATE TABLE IF NOT EXISTS team(name TEXT, tire REAL, point REAL, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")
tet.execute("CREATE TABLE IF NOT EXISTS gamble (name TEXT, coin INTEGER DEFAULT 0, money INTEGER DEFAULT 0, ID INTEGER NOT NULL, dividend INTEGER DEFAULT 0, num INTEGER)")
tet.execute("CREATE TABLE IF NOT EXISTS auction (name TEXT, tire REAL DEFAULT 0, point REAL DEFAULT 0, coin INTEGER DEFAULT 500, position TEXT DEFAULT '미정', subposition TEXT DEFAULT '미정', intro TEXT DEFAULT '미정')")