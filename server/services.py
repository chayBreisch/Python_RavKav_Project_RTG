import sqlite3 as sqlite_library

database = sqlite_library.connect(database="./rav_kav_db.sqlite")
cursor = database.cursor()


def check_valid_card(value, name):
    """
    Generic function for Checking in SQL server if the card number given appears and valid.
    :param value: The value to change the variable to
    :param name: generic variable name to change to
    :return:
    """
    cursor.execute(f"SELECT * FROM cards WHERE {name} = {value}")
    all_contract = cursor.fetchall()
    return all_contract


def create_card(user_id, contract, wallet):
    """
    A function to create a new card
    :param user_id: number of user id
    :param contract: name of contract
    :param wallet: sum of wallet
    :return: the card id of the new card
    """
    cursor.execute("SELECT * FROM contracts WHERE name_contract =  ?", (contract,))
    contract_code = cursor.fetchall()[0][0]
    cursor.execute("INSERT OR REPLACE INTO cards (user_id, code_contract, wallet) VALUES (?,?,?)"
                   , (user_id, contract_code, wallet))
    database.commit()
    cursor.execute("SELECT card_id FROM cards WHERE user_id = ?", (user_id,))
    card_id = cursor.fetchall()[0][0]
    return card_id


def get_data_card(card_id):
    """
    A function to get the data of a card
    :param card_id: number of card id
    :return: the data of the card
    """
    cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,))
    data_card = cursor.fetchall()
    if not data_card:
        return -1
    cursor.execute("SELECT * FROM contracts WHERE code_contract = ?", (data_card[0][2],))
    name_cont = cursor.fetchall()
    return [data_card[0][0], name_cont[0][1], data_card[0][3]]


def pay_ride(card_id, destination):
    """
    A function to pay of a ride
    :param card_id: number of card id
    :param destination: The destination of the ride
    :return: -1 if fails
    """
    if not check_valid_card(card_id, 'card_id'):
        return -1
    cursor.execute("SELECT * FROM contracts WHERE name_contract = ?", (destination,))
    contracts = cursor.fetchall()
    if contracts is None:
        return -1
    cursor.execute("SELECT code_contract FROM cards WHERE card_id = ?", (card_id,))
    current_contract = cursor.fetchall()
    if current_contract is None:
        return -1
    if contracts[0][0] == current_contract[0][0]:
        return "Card already has the desired contract. No payment required."
    # Update the contract for the given card_id
    cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,))
    wallet = cursor.fetchall()[0][3]
    if wallet - contracts[0][2] < 0:
        return -1
    # Perform payment if the contract is different
    if destination != "NONE":
        cursor.execute("UPDATE cards SET wallet = wallet - ? WHERE card_id = ?", (contracts[0][2], card_id))
    database.commit()


def fill_wallet(card_id, wallet_sum):
    """
    A function to fill the wallet of the card
    :param card_id: number of card id
    :param wallet_sum: sum of wallet to fill
    :return: -1 if fails
    """
    if not check_valid_card(card_id, 'card_id'):
        return -1
    cursor.execute("UPDATE cards SET wallet = wallet + ? WHERE card_id = ?", (wallet_sum, card_id))
    database.commit()


def change_contract(card_id, new_contract):
    """
    A function to change the contract of the card
    :param card_id: number of card id
    :param new_contract: name of contract change to
    :return: -1 if fails
    """
    if not check_valid_card(card_id, 'card_id'):
        return -1
    cursor.execute("SELECT * FROM contracts WHERE name_contract = ?", (new_contract, ))
    all_contracts = cursor.fetchall()
    if not all_contracts:
        return -1
    new_code_contract = all_contracts[0][0]
    cursor.execute("UPDATE cards SET code_contract = ? WHERE card_id = ?", (new_code_contract, card_id))
    database.commit()
