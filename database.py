import sqlite3
import time
import GETAPI


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute('''DROP TABLE IF EXISTS parks''')
        self.c.execute('''DROP TABLE IF EXISTS rides''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS parks
                     (id text primary key, `name` text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS rides
                     (`name` text, 
                     park_id text, 
                     `time` text,
                     wait_time integer, 
                     status text, 
                     primary key (`name`, park_id, `time`))''')
        self.conn.commit()

    def insert_park(self, park_id, park_name):
        self.c.execute("INSERT INTO parks VALUES (?, ?)", (park_id, park_name))
        self.conn.commit()

    def insert_ride(self, park_id, rides_name, time, wait_time, status):
        self.c.execute("INSERT INTO rides VALUES (?, ?, ?, ?, ?)", (rides_name, park_id, time, wait_time, status))
        self.conn.commit()

    def auto_update(self):
        while True:
            api = GETAPI.API()
            parks = api.get_parks()
            if parks == 0:
                continue
            for park in parks:
                self.insert_park(parks[park], park)
                attractions, closed = api.get_park(park)
                if attractions == 0:
                    continue
                for ride in attractions:
                    self.insert_ride(parks[park], ride, time.strftime("%H:%M:%S"), attractions[ride], "OPEN")
                time.sleep(1)  # Sleep 1 second
            self.conn.commit()
            time.sleep(60 * 5)  # Sleep for 5 minutes


db = DataBase()
db.auto_update()
