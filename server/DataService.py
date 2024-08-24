import sqlite3
import os.path


class DataService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "DataBase.db")

    def create_tables(self):
        with sqlite3.connect(self.db_path) as db:
            curs = db.cursor()
            curs.execute(
                """ CREATE TABLE IF NOT EXISTS "AdminUsers" (
                            "key" INTEGER PRIMARY KEY AUTOINCREMENT ,
                            "username"	text NOT NULL UNIQUE,
                            "password"	text NOT NULL
                            );"""
            )
            db.commit()
            curs.execute(
                """CREATE TABLE IF NOT EXISTS MonitorUsers (
                            "key" INTEGER PRIMARY KEY AUTOINCREMENT ,
                            "name"	TEXT NOT NULL,
                            "ip"	TEXT NOT NULL,
                            "adminKey" INTEGER NOT NULL
                            );"""
            )
            db.commit()

    def addAdminUser(self, username, password):
        with sqlite3.connect(self.db_path) as db:
            try:
                curs = db.cursor()
                if username in curs.execute("SELECT username FROM adminUsers"):
                    print("didnt find sql")
                    return False

                curs.execute(
                    "INSERT INTO adminUsers VALUES (NULL , ?, ? )", [username, password]
                )
                db.commit()
                return True
            except Exception as e:
                print("sql error")
                return False

    def add_monitor_user(self, ip, name, admin_key):
        with sqlite3.connect(self.db_path) as db:

            curs = db.cursor()
            curs.execute(
                "INSERT INTO MonitorUsers VALUES (NULL, ?, ?, ?) " " RETURNING key",
                [name, ip, admin_key],
            )
            row = curs.fetchone()
            (inserted_id,) = row if row else None
            db.commit()
            return [inserted_id, name, ip, admin_key]

    def GetAllAdminUsers(self):
        with sqlite3.connect(self.db_path) as db:
            curs = db.cursor()
            curs.execute("SELECT * FROM adminUsers")
            rows = curs.fetchall()

        return rows

    def GetAllMonitorUsers(self):
        with sqlite3.connect(self.db_path) as db:

            curs = db.cursor()

            curs.execute("SELECT * FROM 'MonitorUsers' ")
            rows = curs.fetchall()

        return rows

    def get_monitor_list_by_admin_key(self, adminKey):
        with sqlite3.connect(self.db_path) as db:
            curs = db.cursor()

            curs.execute(
                """SELECT * FROM MonitorUsers WHERE MonitorUsers.adminKey = ? """,
                [adminKey],
            )
            rows = curs.fetchall()
        return rows

    def check_login(self, username, password):
        with sqlite3.connect(self.db_path) as db:
            curs = db.cursor()

            curs.execute(
                """SELECT * FROM AdminUsers WHERE AdminUsers.username = ? AND AdminUsers.password = ? """,
                [username, password],
            )
            rows = curs.fetchall()

        if len(rows) == 0:
            return None
        else:
            return rows[0]

    def delete_monitor_by_key(self, key):
        with sqlite3.connect(self.db_path) as db:
            curs = db.cursor()
            curs.execute("delete from MonitorUsers where MonitorUsers.key = (?)", [key])
            db.commit()
