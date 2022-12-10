import psycopg2
from config import *

try:
    connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
                "SELECT version();"
            )
        print(f"Server version: {cursor.fetchone()}")


    def create_table_found_users():
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS found_users(
            id serial,
            first_name varchar (30) NOT NULL,
            last_name varchar (30) NOT NULL,
            vk_id varchar (50) NOT NULL PRIMARY KEY,
            vk_link varchar (50));""")
        print('[INFO] Table found_users is created successfully.')


    def create_table_seen_users():
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar (50) PRIMARY KEY); """)


        print('[INFO] Table seen_users is created successfully.')



    def insert_data_found_users(first_name, last_name, vk_id, vk_link):
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO found_users (first_name, last_name, vk_id, vk_link)
              VALUES ('{first_name}', '{last_name}', '{vk_id}', '{vk_link}')
              ON CONFLICT (vk_id) DO NOTHING;""")


    def insert_data_seen_users(vk_id):
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO seen_users(vk_id)
              VALUES ('{vk_id}')""")


    def drop_found_users():
        with connection.cursor() as cursor:
            cursor.execute("""
            DROP TABLE IF EXISTS found_users CASCADE;""")


    def select_unseen(offset):
        with connection.cursor() as cursor:
            cursor.execute(
                    f"""SELECT 
                found_users.vk_id,
                found_users.first_name, 
                found_users.last_name, 
                found_users.vk_link
                FROM found_users 
                WHERE vk_id NOT IN (SELECT vk_id FROM seen_users)
                OFFSET '{offset}';""")
            return cursor.fetchone()


    def drop_seen_users():
        with connection.cursor() as cursor:
            cursor.execute("""
        DROP TABLE IF EXISTS seen_users CASCADE;""")


    def create_db():
        # drop_found_users()
        # drop_seen_users()
        create_table_found_users()
        create_table_seen_users()


    #
except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL, _ex")
# finally:
#     if connection:
#         connection.close()
#         print("[INFO] PostgreSQL connection closed")

# if __name__ == '__main__':
#     create_db()
