# // MYSQL DATABASE CONNECTOR
import mysql.connector

# // IMPORT AUTO CURSOR CLOSING
from contextlib import closing

# CONNECT TO THE "MySQL Database" FUNCTION
# ////////////////////////////////////////////
def _connect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="main"
    )
    return db

# // CREATING DATABASE VARIABLES
# ////////////////////////////////
db = _connect()

class SQL():
    def __init__(self):
        pass
        #cur = db.cursor(buffered=True)
        #cur.execute(f"DROP TABLE bans")
        #cur.execute(f"DROP TABLE maps")
        #cur.execute(f"DROP TABLE matches")
        #cur.execute(f"DROP TABLE settings")
        #cur.execute(f"DROP TABLE users")


        # // USERS TABLE
        #cur.execute("CREATE TABLE users (guild_id BIGINT, user_id BIGINT, user_name VARCHAR(50), elo int, wins int, loss int, id int PRIMARY KEY AUTO_INCREMENT)")

        # // SETTINGS TABLE
        #cur.execute("CREATE TABLE settings (guild_id BIGINT, reg_role BIGINT, map_pick_phase VARCHAR(10), match_categories VARCHAR(10), team_pick_phase VARCHAR(10), queue_channel BIGINT, reg_channel BIGINT, win_elo int, loss_elo int, match_logs BIGINT, party_size INT, id int PRIMARY KEY AUTO_INCREMENT)")

        # // MATCHES TABLE
        #cur.execute("CREATE TABLE matches (guild_id BIGINT, match_id int, map VARCHAR(50), orange_cap VARCHAR(50), orange_team VARCHAR(200), blue_cap VARCHAR(50), blue_team VARCHAR(200), status VARCHAR(50), winners VARCHAR(50), id int PRIMARY KEY AUTO_INCREMENT)")

        # // MAPS TABLES
        #cur.execute("CREATE TABLE maps (guild_id BIGINT, map_list VARCHAR(50), id int PRIMARY KEY AUTO_INCREMENT)")

        # // BANS TABLE
        #cur.execute("CREATE TABLE bans (guild_id BIGINT, user_id BIGINT, length BIGINT, reason VARCHAR(50), banned_by VARCHAR(50), id int PRIMARY KEY AUTO_INCREMENT)")


    # // CHECK IF A VALUE IN A TABLE EXISTS
    # ////////////////////////////////////////
    async def exists(self, command):
        global db
        try:
            with closing(db.cursor(buffered=True)) as cur:
                cur.execute(command)
                if cur.fetchone() is None:
                    return False # // Doesn't exist
                return True # // Does exist
        except mysql.connector.Error:
            db.close()
            db = _connect()

    # // RETURNS A SINGLE LIST FROM THE SELECTED TABLE
    # /////////////////////////////////////////////////
    async def select(self, command):
        global db
        try:
            cur = db.cursor(buffered=True)
            if await self.exists(command):
                cur.execute(command)
                return list(cur.fetchall()[0])
            return None
        except mysql.connector.Error:
            db.close()
            db = _connect()

    # // RETURNS MULTIPLE LISTS FROM THE SELECTED TABLE
    # ///////////////////////////////////////////////////
    async def select_all(self, command):
        global db
        try:
            with closing(db.cursor(buffered=True)) as cur:
                cur.execute(command)
                return list(cur.fetchall())
        except mysql.connector.Error:
            db.close()
            db = _connect()

    # // EXECUTE A SEPERATE COMMAND
    # /////////////////////////////////////
    async def execute(self, command):
        global db
        try:
            with closing(db.cursor(buffered=True)) as cur:
                cur.execute(command)
                db.commit()
        except mysql.connector.Error:
            db.close()
            db = _connect()