import datetime
import sqlite3
from textwrap import dedent



class Reminders():
    def __init__(self):
        self.connect()
        self.create_table()

        self.options = None
        self.add_data = [()]
        
    def connect(self):
        try:    
            with sqlite3.connect('reminders.db') as self.connection_obj:
                print("Connected to SQLite")
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        self.cursor_obj = self.connection_obj.cursor()
        table_creation_query = """
            CREATE  TABLE IF NOT EXISTS REMINDERS (
                id INTEGER PRIMARY KEY,
                reminder_name VARCHAR(255) NOT NULL,
                due_date DATE NOT NULL 
            );
        """

        self.cursor_obj.execute(table_creation_query)

        print("Table is Ready!")

    def user_options(self):
        while True:
            try:
                self.options = int(input(dedent(
                """
                    Select an option number:
                    1: Add a Reminder.
                    2: Show Reminders.
                    3: Edit Reminders.
                    4: Quit

                """)))
                print("")

                match self.options:
                    case 1:
                        self.get_reminder()
                    case 2:
                        self.show_reminder()
                    case 3:
                        self.edit_reminder()
                    case 4:
                        print("Thank You!")
                        break
                    case _:
                        print("Only 1-4 is allowed as input, Try Again!")
            except ValueError:
                print("Invalid Input, Try Again!")


    def add_reminder(self):
        add_reminder_query = """
            INSERT INTO REMINDERS (id, reminder_name, due_date) VALUES (?,?,?)
        """
        self.cursor_obj.executemany(add_reminder_query, self.add_data)
        self.connection_obj.commit()
        print("Reminder Added!")

    def get_reminder(self):
        while True:
            try:
                self.add_data = []
                option1_add_reminder_name = str(input("Reminder Name: "))
                date = input("Date (dd/mm/yyyy) in Numbers: ")
                dd_str, mm_str, yyyy_str = date.split("/")
                dd = int(dd_str)
                mm = int(mm_str)
                yyyy = int(yyyy_str)

                option1_add_due_date = datetime.date(yyyy, mm, dd).strftime("%d/%m/%Y")

                self.add_data.append((None, option1_add_reminder_name  ,  option1_add_due_date))

                self.add_reminder()
                break

            except ValueError as e:
                print(str(e))
        

    def show_reminder(self):
        self.cursor_obj.execute("SELECT * FROM REMINDERS")
        rows = self.cursor_obj.fetchall()

        print('\nAll Reminders:')
        for row in rows:
            print(f"ID: {row[0]}, Reminder Name: {row[1]}, Due Date: {row[2]}")
            
    def edit_reminder(self):
        pass
    def close_connection(self):
        self.connection_obj.close()
    
    



def main():
    reminders = Reminders()
    reminders.user_options()
    reminders.close_connection()
    # reminders.connect()
    # reminders.create_table()

if __name__ == "__main__":
    main()
