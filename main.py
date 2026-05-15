import datetime
from textwrap import dedent
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")



class Reminders():
    def __init__(self):
        self.connect()
        self.create_table()

        self.options = None
        self.add_data = [()]
        
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
            INSERT INTO REMINDERS (reminder_name, due_date) VALUES (%s,%s)
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

                self.add_data.append((option1_add_reminder_name  ,  option1_add_due_date))

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
        while True:
            try:
                self.edit_id = int(input("What is the ID of the reminder that you want to edit?: ") )
                self.update_or_delete = int(input(dedent("""
                Select One:
                1: Edit Reminder
                2: Delete Reminder
                3: Go Back
                """)))
                
                match self.update_or_delete:
                    case 1:
                        self.update_reminder()
                        break
                    case 2:
                        self.delete_reminder()
                        print(f"Deleted Reminder {self.edit_id}")
                        break
                    case 3:
                        break

                print("") 
            except ValueError as e:
                print(e)
                continue

        



    def update_reminder(self):

        update_name_due_date_query = """
        UPDATE REMINDERS
        SET reminder_name = %s, due_date = %s
        WHERE id = %s
        """
        update_name_only_query = """
        UPDATE REMINDERS
        SET reminder_name = %s
        WHERE id = %s
        """
        update_due_date_only_query = """
        UPDATE REMINDERS
        SET due_date = %s
        WHERE id = %s
        """


        print("Enter new values below. Press Enter to skip and keep it the same.")
        try:
            update_name = input("Reminder Name: ")
            new_date = input("Due Date (dd/mm/yyyy): ")
            
            if not update_name:
                update_name = None

            if new_date:
                dd_str, mm_str, yyyy_str = new_date.split("/")
                dd = int(dd_str)
                mm = int(mm_str)
                yyyy = int(yyyy_str)
                update_due_date = datetime.date(yyyy, mm, dd).strftime("%d/%m/%Y")

            else:
                update_due_date = None

            

            try:
                if update_name and update_due_date:
                    self.cursor_obj.execute(update_name_due_date_query, (update_name, update_due_date, self.edit_id ))
                    self.connection_obj.commit()
                    print(f"Reminder {self.edit_id} has been updated!")
                elif update_name and not update_due_date:
                    self.cursor_obj.execute(update_name_only_query, (update_name, self.edit_id ))
                    self.connection_obj.commit()   
                    print(f"Reminder {self.edit_id} has been updated!")
                elif update_due_date and not update_name:
                    self.cursor_obj.execute(update_due_date_only_query, (update_due_date, self.edit_id ))
                    self.connection_obj.commit() 
                    print(f"Reminder {self.edit_id} has been updated!")  
                else:
                    print(f"Reminder remains unchanged.")
                
            except psycopg2.Error as e:
                print(e)


            
        except ValueError as e:
            print(str(e))



    def delete_reminder(self):

        delete_reminder_query = "DELETE FROM REMINDERS WHERE id = %s"
        try:
            self.cursor_obj.execute(delete_reminder_query, (self.edit_id, ))
            self.connection_obj.commit()
        except ValueError as e:
            print(e)

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
