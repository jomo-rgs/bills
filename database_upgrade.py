import data
import sqlite3

import datetime as dt
NOW = f"{dt.datetime.now():%c}"

# This change supports the following functionality:
#   1. Due date offset: Set the month ofset on an account due date.
#   2. Auto Pay: Automatically set the bill to paid for an account.
#   3. Auto Confirm: Automatically set the bill to confirmed for an account.
#   4. Create the DATABASE_VERSION settings value. This is the first time we 
#      are using this table. Using the create_db() to accomplish this task.
def v1(log):
        
        log.write(NOW + "v1 Update Started.\n")
        data.create_db() # Don't worry, This will only create tables that don't exits.

        log.write("Attempting Database Connection.\n")
        conn = sqlite3.connect(data.get_db_file())

        log.write("Generating Cursor.\n")
        sql_cursor = conn.cursor()

        log.write("Updating Account Table Field due_dom_offset\n")
        sql_cursor.execute("""    
            ALTER TABLE account ADD COLUMN due_dom_offset INTEGER DEFAULT 0;
        """)

        log.write("Updating Account Table Field auto_pay\n")
        sql_cursor.execute("""    
            ALTER TABLE account ADD COLUMN auto_pay INTEGER DEFAULT 0;
        """)

        log.write("Updating Account Table Field auto_confirm\n")
        sql_cursor.execute("""    
            ALTER TABLE account ADD COLUMN auto_confirm INTEGER DEFAULT 0;                   
        """)

        log.write("Commit and Close Database\n")
        conn.commit()
        conn.close()

        log.write("Updating Database Version\n")
        data.save_setting(key='DATABASE_VERSION', value='1')

        log.write("Version 1 update complete...\n\n")

def upgrade():

    try: 

        log = open("database_upgrade.log", "a")
        log.write(NOW + "Starting Upgrade\n")

        if data.does_table_exist("settings"):
            database_version = data.get_setting("DATABASE_VERSION")
            if database_version == None:
                database_version = 0    
        else:
            database_version = 0 

        if database_version == 0:
            v1(log)

    except Exception as e :
        log.write("Upgrade failed\n")
        log.write(f"Error: {str(e)}\n")
    finally:
        pass