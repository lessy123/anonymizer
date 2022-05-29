import fdb
import connect_employee as CtoDB
import sql_query as sql



# x="dth"
# s=(x,)
# print(s)
s=False
while(not s):
    print("Введите расположение базы данных")
    path=input()
    cursor,connection,s  = CtoDB.connect_to_bd(path)
print("Желаете анонимизировать всю базу данных?(Да/Нет)")
select=input()
if select=="Да" or select=="Yes" or select=="Д" or select=="Y" or select=="1":
    sql.change_of_database(cursor,connection)
else:
    print("Введите, сколько таблиц вы желаете изменить")
    table_name=[]
    n=input()
    for i in range(int(n)):
        print(f"""Введите, название таблицы под номером: {i+1}""")
        name_table=input()
        table_name.append((name_table,))
    sql.change_of_database(cursor,connection,table_name)







# cursor,connection  = CtoDB.connect_to_bd('/home/alex/anonymizer/BDstorage/name_storage.fdb')

# sql.change_of_database(cursor,connection)

# connection.commit()#update to database

# cursor.close()      
# connection.close()