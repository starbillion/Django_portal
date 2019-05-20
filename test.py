# import pymysql
#
# database = pymysql.connect(host='localhost', user='root', password='', db='portal')
# cursor = database.cursor()
#
# file = open("Mission_Lavels_All.txt", "r")
# cnt = 0;
# for line in file:
#     cnt = cnt + 1
#     print (line.split(',')[0])
#     if cnt % 2 == 0:
#         level_record = (cnt, line.split(',')[0], line.split(',')[1],False,0)
#     else:
#         level_record = (cnt, line.split(',')[0], line.split(',')[1], True, 0)
#     query_insert_level = """INSERT INTO farm_level(id, level, comment, hidden, raid) VALUES(%s,%s,%s,%s,%s)"""
#     cursor.execute(query_insert_level, level_record)
#     database.commit()

