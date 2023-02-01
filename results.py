import pymysql
import matplotlib.pyplot as plt
import numpy as np

connection = pymysql.connect(host="db-buf-02.sparkedhost.us",autocommit=True ,port=3306, user="u75662_RNokPhakPC", passwd="v4RL73jqIfS^1lkMc@mZrZkE", db="s75662_NNN")
cursor = connection.cursor()

def dead_count(day):
        sql = ""
        for i in range(int(day)):
            if i + 1 == int(day):
                sql += f'November{i + 1:02d} = 1' 
            else:
                sql += f'November{i + 1:02d} = 1 OR '
        # print(f'DEAD SQL {sql}')
        return (cursor.execute(f'SELECT * FROM NNN WHERE {sql}'))

def alive_count(day):
    sql = ""
    for i in range(int(day)):
        if i + 1 == int(day):
            sql += f'November{i + 1:02d} = 0' 
        else:
            sql += f'November{i + 1:02d} = 0 AND '
    # print(f'ALIVE SQL {sql}')
    return (cursor.execute(f'SELECT user_name FROM NNN WHERE {sql}'))

def everyday_dead_count(day):
    sql = ""
    for i in range(int(day)):
        if i + 1 == int(day):
            sql += f'November{i + 1:02d} = 1' 
        else:
            sql += f'November{i + 1:02d} = 1 AND '
    print(f'DEAD SQL {sql}')
    return (cursor.execute(f'SELECT * FROM NNN WHERE {sql}'))

def dead_alive_plot(alive, dead):
    plt.plot(alive, color='g')
    plt.plot(dead, color='r')
    plt.xticks(np.arange(len(alive)), np.arange(1, len(alive) + 1))
    plt.yticks(np.arange(0, 210, 10))
    plt.legend(['啊', '啊'], prop={'size': 20})
    plt.title('啊和啊人數隨著日數的變化\n', fontsize=30)
    plt.xlabel('日數', fontsize=18)
    plt.ylabel('人數', fontsize=18)
    plt.grid()
    plt.show()
    

def get_dead_alive_account():
    alive = []
    dead = []
    for i in range(1, 31):
    # print(f"DAY {i}: DEAD: {dead_count(i)} ALIVE: {alive_count(i)}")
        alive.append(alive_count(i))
        dead.append(dead_count(i))
    return alive, dead

def get_database():
    cursor.execute("SELECT * FROM NNN")
    return cursor.fetchall()

# alive, dead = get_dead_alive_account()
# alive = [172, 113, 100, 91, 79, 67, 61, 59, 56, 52, 43, 39, 37, 36, 34, 29, 29, 29, 26, 26, 26, 25, 25, 25, 23, 23]
# dead = [60, 74, 84, 93, 114, 127, 137, 138, 142, 147, 152, 158, 160, 161, 164, 169, 172, 172, 173, 174, 175, 177, 177, 180, 183, 184]

survivor = alive_count(30)
print(cursor.fetchall())
# plt.rcParams['font.sans-serif'] = ['SimHei'] # Or any other Chinese characters
# dead_alive_plot(alive, dead)
# print(everyday_dead_count(30))

# # print(get_database()[0])
# total_alive_count = []
# total_dead_count = []
# db = get_database()
# for days in range(1, 31):
#     total_alive = 0
#     total_dead = 0
#     for person in db:
#         dead_count = 0
#         alive_count = 0
#         for data in person[1:-1]:
#             if data == 0:
#                 alive_count += 1
#             elif data == 1:
#                 dead_count += 1
#         if alive_count == days:
#             total_alive += 1
#         if dead_count == days:
#             total_dead += 1
#     total_alive_count.append(total_alive)
#     total_dead_count.append(total_dead)
#     # print(f"DAY{days} TOTAL ALIVE: {total_alive}    TOTAL DEAD: {total_dead}")
# print(total_alive_count)
# print((total_dead_count))

# # dead_count = [49, 19, 18, 10, 11, 6, 6, 5, 3, 5, 3, 3, 2, 5, 1, 3, 5, 1, 3, 6, 0, 0, 0, 0, 3, 2, 5, 2, 6, 8]
# # alive_count = [56, 20, 11, 5, 11, 3, 3, 3, 4, 10, 10, 5, 4, 1, 1, 4, 1, 4, 4, 2, 2, 3, 4, 3, 3, 1, 2, 3, 11, 19]
# y_pos = np.arange(30)
# bar_width = 0.35
# plt.bar(y_pos, total_dead_count, bar_width, alpha=0.8, label='死', color='r')
# plt.bar(y_pos + bar_width, total_alive_count, bar_width, alpha=0.8, label='生', color='g')
# plt.xticks(y_pos + bar_width - 0.2, (1, 2, 3, 4, 5, 6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30))
# plt.yticks(np.arange(0, 60, 2))
# plt.legend(prop={'size': 20})
# plt.title('啊和啊的日數分佈\n記錄有多少人是啊了n天和啊了n天\n', fontsize=30)
# plt.xlabel('日數', fontsize=18)
# plt.ylabel('人數', fontsize=18)
# plt.grid()
# plt.show()