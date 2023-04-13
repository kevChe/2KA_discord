import pymysql
import discord
import time

def update_cardboards(cursor, id, value):
    print(f"CHANGE MONEY FOR {id}")
    try:
        cursor.execute(f'UPDATE `cardboard` SET cardboards = {value} WHERE id = {id}')
        return True
    except Exception:
        print(f"{Exception}")
        new_account(cursor, id)
        return False

def get_cardboards(cursor, id):
    try:
        cursor.execute(f'SELECT cardboards FROM cardboard WHERE id = {id}')
        # print(cursor.fetchone()[0])
        return cursor.fetchone()[0]
    except TypeError:
        # print(f"{id}并沒有任何紙皮")
        new_account(cursor, id)
        return 1000

def new_account(cursor, id):
    print(f'Creating new account for {id}')
    cursor.execute(f'INSERT INTO `cardboard` (`id`, `cardboards`) VALUES ({id}, 1000)')
