import sqlite3 as sqlite_library

database = sqlite_library.connect(database="./rav_kav_db.sqlite")
cursor = database.cursor()
create_table_cards = '''CREATE TABLE IF NOT EXISTS cards
                (card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT,
                code_contract INT,
                wallet INT);
                '''
cursor.execute(create_table_cards)

create_table_contracts = '''CREATE TABLE IF NOT EXISTS contracts
                (code_contract INTEGER PRIMARY KEY AUTOINCREMENT,
                name_contract TEXT,
                price INT)
                '''
cursor.execute(create_table_contracts)


def add_contract(cont_name, cont_price):
    cursor.execute("INSERT OR REPLACE INTO contracts "
                   "(name_contract, price) VALUES (?, ?)",
                   (cont_name, cont_price))
    database.commit()


add_contract('NONE', 0)
add_contract('NORTH', 25)
add_contract('CENTER', 40)
add_contract('SOUTH', 30)
