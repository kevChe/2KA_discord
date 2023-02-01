import pymysql

def change_money(cursor, id, value):
    print(value, id)
    cursor.execute(f'UPDATE `cardboard` SET cardboards = cardboards + {value} WHERE id = {id}')