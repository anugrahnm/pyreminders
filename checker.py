from datetime import date, timedelta
import os

import asyncio
import psycopg2
import telegram
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")




class Checker():
    def __init__(self):
        self.connect()
        self.create_table()



    def connect(self):
        try:    
            with psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
                ) as self.connection_obj:

                print("Connected to PostgreSQL")
        except psycopg2.Error as e:
            print(e)

    def create_table(self):
        self.cursor_obj = self.connection_obj.cursor()
        table_creation_query = """
            CREATE TABLE IF NOT EXISTS REMINDERS (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                reminder_name VARCHAR(255) NOT NULL,
                due_date DATE NOT NULL
            );
        """

        self.cursor_obj.execute(table_creation_query)

        print("Table is Ready!")

    def check_due_date(self):
        check_due_date_query = """
            SELECT * FROM REMINDERS
            WHERE due_date = %s OR due_date = %s
        """

        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.date_today = today.strftime("%d/%m/%Y")
        self.date_tomorrow = tomorrow.strftime("%d/%m/%Y")

        self.cursor_obj.execute(check_due_date_query, (self.date_today, self.date_tomorrow,))

        self.rows = self.cursor_obj.fetchall()



        

    async def send_telegram_alert(self):
        bot = telegram.Bot(TOKEN)
        for row in self.rows:
            if row[2] == self.date_today:
                day = "TODAY"
            elif row[2] == self.date_tomorrow:
                day = "TOMORROW"
            else:
                print("Error: Wrong Date Fetched!")
            async with bot:
                await bot.send_message(text=f"REMINDER DUE {day}!: \n \nID: {row[0]}, Reminder Name: {row[1]}, Due Date: {row[2]}", chat_id=CHAT_ID)
       

        

        

async def main():
    check = Checker()
    check.check_due_date()
    await check.send_telegram_alert()
    

if __name__ == "__main__":
    asyncio.run(main())