from dis import code_info
import connect_employee as CtoDB
import fdb
import work_with_image as wwi
import random
import inn
import datetime
from datetime import timedelta
import experiments.exp_faker as fake
import re
import classification_natasha as classification_natasha
import numpy as np
import faker_generate as faker
import change.blur as blur


def generate_sql_query_UPDATE(name_table,field,id_name,id):    
    """ Подготавливает запрос в зависимости от количества ключей
        name_table - название таблицы
        field - название поля
        id_name - список названий полей, содержащий primory key
        id - соответственно названия ключей    
    """
    sql_insert_blob_query = f"""UPDATE "{name_table}" SET "{field}" = ? WHERE"""
    if len(id_name)==len(id):        
        sql_insert_blob_query+=f""" "{id_name[0][0]}" = '{id[0]}'"""
        for i in range(1,len(id_name)):
            sql_insert_blob_query+=f""" and "{id_name[i][0]}" = '{id[i]}'"""
        return sql_insert_blob_query
    else:
        print("Error when entering the primary key")
        exit      
def insert_names(cur,connect,name_table,field_first_name,field_second_name,count_of_insert,field_id_name="ID"):
    """ Нужна для создания полей в таблице PERSONAL_DATE
        cur - База данных;
        name_table - название таблицы;
        field - название полей, которые используются;
        field_first_name - название поля с именем;
        field_second_name - название поля с фамилией;
        count_of_insert - количество добавлений"""
    #stroka="select \""+field+"\" from \""+name_table+"\""
    stroka="select * from \""+name_table+"\""
    print(stroka)
    cur.execute(stroka)
    wenera = cur.fetchall()
    len_gen=len(wenera)

    for i in range(len_gen+1,len_gen+count_of_insert+1):
        print(i)
        # INSERT INTO "PERSONAL_DATE" ("ID", "FIRST_NAME", "SECOND_NAME") 
        # VALUES ('2', 'Алекс', 'Мерсер');
        sql_insert_blob_query = "INSERT INTO \""+name_table+"\" (\""+field_id_name+"\",\""+field_first_name+"\",\""+field_second_name+"\") VALUES (?, ?, ?)" 
        print(sql_insert_blob_query)
        val = (i,fake.generate_first_name('ru_RU'),fake.generate_last_name('ru_RU'))
        #print(sql_insert_blob_query)
        result = cur.execute(sql_insert_blob_query,val)
        connection.commit()
def generate_sql_query_SELECT(name_table,field,id_name,id):    
    """ Подготавливает запрос в зависимости от количества ключей
        name_table - название таблицы
        field - название поля
        id_name - список названий полей, содержащий primory key
        id - соответственно названия ключей    
    """ 
    #f"""Select  "{field}" from "{name_table}" WHERE"""
    sql_insert_blob_query = "Select  \""+field+"\" from \""+name_table+"\" WHERE"
    if len(id_name)==len(id):
        sql_insert_blob_query+=" \""+id_name[0][0]+"\" = \'"+str(id[0])+'\''
        for i in range(1,len(id_name)):
            sql_insert_blob_query+=" and \""+id_name[i][0]+"\" = \'"+str(id[i])+'\''
        #print(sql_insert_blob_query)
        # print(sql_insert_blob_query)
        return sql_insert_blob_query
    else:
        print("Error when entering the primary key")
        exit  
def update_field(cur,connect,name_table,field,id_name,id,data):
    """ cur - база данных;
        name_table - название таблицы;
        field - название поля;
        id_name - лист с названиями таблиц, содержащих "первичный ключ"
        id - номера "первичных ключей"
        data - дата-заменитель
    """
    try:
        sql_insert_blob_query = generate_sql_query_UPDATE(name_table=name_table,field=field,id_name=id_name,id=id)
        # print(sql_insert_blob_query,data)
        val = (data,)
        # print(sql_insert_blob_query,val)
        result = cur.execute(sql_insert_blob_query,val)
        connect.commit()
    except:
        print("Ошибка изменения поля")
        
        """"""
def work_with_picture(cur,connect,name_table,field,id_list,id_name_list,photo="/home/alex/anonymizer/RAM/1.jpeg"):
    """
    cur - подключенная база данных;
    name_table - имя таблиы;
    field - имя поля;
    id_name_list - список имен полей первичного ключа
    id_list - первичный ключ    
    """  
    try:
        for id in id_list:
            sql_fetch_blob_query = generate_sql_query_SELECT(name_table=name_table, field=field, id_name=id_name_list, id=id)
            # print(sql_fetch_blob_query)
            cur.execute(sql_fetch_blob_query)
            record = cur.fetchall()
            # print(record)

            for row in record:
                image = row[0]
                if image is None:
                    continue
                wwi.write_file(image, photo)
                blur.blur_image(photo)
                empPicture = wwi.convertToBinaryData(photo)
                update_field(cur=cur,connect=connect,
            name_table=name_table,field=field,
            id_name=id_name_list,id=id,data=empPicture)


    except:
        print("поле не хранит изображение")
    
def select_table_names(cur):
    """ Возвращает названия таблиц;
        cur - база данных;"""
    cur.execute(
    'select RDB$RELATION_NAME from RDB$RELATIONS '
    'where (RDB$SYSTEM_FLAG = 0) AND (RDB$RELATION_TYPE = 0) '
    'order by RDB$RELATION_NAME ')
    return cur.fetchall()
def select_field_names(cur,connect,name_table):
    """Выдает все названия полей из таблицы
        cur - подключенная база данных;
        name_table - название таблицы.
    """
    cur.execute(
        f"""
    select RDB$FIELD_NAME from RDB$RELATION_FIELDS 
    where RDB$RELATION_NAME = '{name_table}'""")
    return cur.fetchall()
def select_primory_key(cur,connect,name_table):
    """ Выдает primory_key для названной таблицы
        cur - база данных;
        name_table - название таблицы;    
    """
    cur.execute(f"""
        SELECT s.RDB$FIELD_NAME 
        FROM RDB$RELATION_CONSTRAINTS r 
        NATURAL JOIN RDB$INDEX_SEGMENTS s 
        WHERE r.rdb$constraint_type='PRIMARY KEY' 
        AND r.rdb$relation_name='{name_table}' 
        ORDER BY s.RDB$FIELD_POSITION""")
    return cur.fetchall()
def select_important_relations(cur,connect,name_table):
    """
    Находит все важные компаненты таблицы:
    Уникальные значения, foreign and primory key
    cur - соединенная база данных;
    name_table - название таблицы
    """
    cur.execute(
    f"""SELECT DISTINCT s.RDB$FIELD_NAME
        FROM RDB$RELATION_CONSTRAINTS r
        NATURAL JOIN RDB$INDEX_SEGMENTS s
            WHERE r.rdb$relation_name=   '{name_table}'                                            
        ORDER BY s.RDB$FIELD_POSITION""")
    return cur.fetchall()
def UPDATE_FLAG(cur,connect,name_table,field):
    """ Проверяет, является ли поле вычисляемым
    cur - подключенная база данных;
    name_table - имя таблиы;
    field - имя поля.    
    """
    #print(name_table,field)
    cur.execute(
    f"""select 
    rel.RDB$UPDATE_FLAG
    from  RDB$RELATION_FIELDS rel
    where rel.RDB$RELATION_NAME='{name_table}'
    and rel.RDB$FIELD_NAME = '{field}'
    """)
    result=cur.fetchall()[0][0]
    #print(result)
    if result==1:
        return False
    else: return True
def work_with_number(cur,connect,name_table,field,id_list,id_name_list):
    check=np.array([0,0,0])
    """        
        0 - номер телефона(вычисляет исключительно русские номера)
        1 - инн
        2 - кредитная карта
    """
    for id in id_list:
        # print("id_name_list",id_name_list)
        # print("id",id)
        # print("field",field)
        # try:

            cur.execute(generate_sql_query_SELECT(name_table=name_table,field=field,id_name=id_name_list,id=id))
            text=cur.fetchall()
            # print(text)
            if text[0][0] is None:
                continue
            # print(text)
            text = str(text[0][0])
            check[0]+=classification_natasha.if_phone(text)

            check[1]+=inn.inn_check(text)
            check[2]+=classification_natasha.lunh_controling(text)
    check=check/len(id_list)
    if check[2]>0.65:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_credit_card)
    elif   check[1]>0.8:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=inn.inn_gen)
    
    elif check[0]>0.8:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_phone)
    
            #print(cur.fetchall())


def work_with_text(cur,connect,name_table,field,id_list,id_name_list):
    """
    cur - подключенная база данных;
    name_table - имя таблиы;
    field - имя поля;
    id_name_list - список имен полей первичного ключа
    id_list - первичный ключ    
    """
    check=np.array([0,0,0,0,0,0,0,0,0,0,0])
    """
        0 - имя
        1 - отчество
        2 - фамилия
        3 - наличие другого местоположения помимо улицы
        4 - улица
        5 - дата
        6 - деньги
        7 - емаил
        8 - номер телефона(вычисляет исключительно русские номера)
        9 - инн
        10 - кредитная карта
    """
    for id in id_list:
        # print("id_name_list",id_name_list)
        # print("id",id)
        # print("field",field)
        try:

            cur.execute(generate_sql_query_SELECT(name_table=name_table,field=field,id_name=id_name_list,id=id))
            text=cur.fetchall()
            # print(text)
            if text[0][0] is None:
                continue
            # print(text)
            for i in range(len(result:=classification_natasha.classifity_text(text[0][0]))):
                check[i]+=result[i]
            #print(cur.fetchall())
        except:
            print("Невозможно опознать тип поля")
            return 0
    # print(check)
    check=check/len(id_list)
    # print(check)
    if  check[7]>0.8:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_email)
    elif   check[9]>0.8:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=inn.inn_gen)
    elif   check[4]>0.8:
        if check[3]>0.8:
            generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_address)
        else:
            generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_street_address)
    # elif check[5]>0.8:
    #     """"""
    elif check[10]>0.65:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_credit_card)

    elif check[8]>0.8:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_phone)
    elif check[0]>0.8:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_first_name)
    elif check[2]>0.7:
        generate_new_data(cur=cur,connect=connect,name_table=name_table,field=field,id_name_list=id_name_list,generator=faker.generate_last_name)
        # except Exception: 

        #     print("Недопустимое значение",Exception)
        #     return
def get_id_primary_key(cur,name_table,primory_key,threshold=None):
    """ Выдает все значения ключей
        cur - подключенная база данных
        name_table - название таблицы - str
        primory_key - список полей первичного ключа - [(x1,),(x2,)....]
    
    """
    stroka=""
    if threshold is not None:
        stroka=f"""select first {threshold} "{primory_key[0][0]}" """
    else:
        stroka=f"""select "{primory_key[0][0]}" """
    # pr_key=[primory_key[0][0]]
    for key in range(1,len(primory_key)):
        # print(primory_key[key][0])
        stroka+=", \""+primory_key[key][0]+"\" "
        # pr_key.append(primory_key[key][0])
    stroka+="from \""+name_table+"\""
    cur.execute(stroka)
    return cur.fetchall()
def generate_new_data(cur,connect,name_table,field,id_name_list,generator):
    """
    генерирует данные с помощью занесенной функии и заносит их в базу данных.
    cur - подключенная база данных;
    name_table - имя таблиы;
    field - имя поля;
    id_name_list - список имен полей первичного ключа
    id_list - первичный ключ  
    generator - способ генерации новой информации     
    """
    wenera = get_id_primary_key(cur=cur ,name_table=name_table,primory_key=id_name_list)
    # wenera = cur.fetchall()
    for i in wenera:
        # print(name_table,field,id_name_list,i)
        update_field(cur=cur,connect=connect,name_table=name_table,field=field,id_name=id_name_list,id=i,data=generator())

    #print(wenera)






def work_with_date(cur,connect,name_table,field,id_list,id_name_list):
    """
    cur - подключенная база данных;
    name_table - имя таблиы;
    field - имя поля;
    id_name_list - список имен полей первичного ключа
    id_list - первичный ключ    
    """
    for id in id_list:
        cur.execute(generate_sql_query_SELECT(name_table=name_table,field=field,id_name=id_name_list,id=id))
        date=cur.fetchall()[0][0]
        if type(date)==datetime.date or type(date)==datetime.datetime:
            add_date=timedelta(days=random.randint(-30,30))
            date+=add_date
            update_field(cur=cur,connect=connect,
            name_table=name_table,field=field,
            id_name=id_name_list,id=id,data=date)

    
    """def change_date(cur,connect,name_table,field,name_id,id):
    stroka="select \""+field+"\" from \""+name_table+"\" where \""+name_id+"\"="+id
    print(stroka)
    cur.execute(stroka)
    date=cur.fetchall()[0][0]
    wenera=type(date)
    if type(date)==datetime.date or type(date)==datetime.datetime:
        add_date=timedelta(days=random.randint(-30,30))
        date+=add_date
        update_field(cur,connect,name_table,field,name_id,id,date)
    else:
        print("Неверный тип данных")
"""


def update_fields(cur,connect,name_table,field_list,method_generation=[]):
    """ Анонимизирует базу данных.
        cur - база данных;
        name_table - название таблицы;
        field_list - список полей таблицы;
        method_generation - список методов - не используется  
    """
    primory_key=select_primory_key(cur=cur,connect=connect,name_table=name_table)
    # print(primory_key,name_table)
    stroka=f"""select FIRST 100 "{primory_key[0][0]}" """
    pr_key=[primory_key[0][0]]
    for key in range(1,len(primory_key)):
        # print(primory_key[key][0])
        stroka+=", \""+primory_key[key][0]+"\" "
        pr_key.append(primory_key[key][0])
    stroka+="from \""+name_table+"\""
    # print(stroka)
    cur.execute(stroka)
    wenera = cur.fetchall()
    # print(field_list)

    for field in field_list:   
        print(field)
        if    UPDATE_FLAG(cur,connect,name_table,field[0]):
            print("Найдено вычисляемое поле")
            continue
        info = select_information_about_table(cur=cur,connect=connect,name_table=name_table,field=field[0])[0][3]
        info = re.sub(r"\s+", "", info)
        # print(info)
        if info=='INTEGER' or info=='LONG' or info=='INT64' or info=='SHORT':
            print("Числовое поле")
            work_with_number(cur=cur,connect=connect,name_table=name_table,field=field[0],id_list=wenera,id_name_list=primory_key)
        elif info=='TEXT' or info=='VARYING':
            print("Текстовое поле")
            work_with_text(cur=cur,connect=connect,name_table=name_table,field=field[0],id_list=wenera,id_name_list=primory_key)

        elif info=='DATE' or info=='TIMESTAMP':
            print("Поле даты")
            work_with_date(cur=cur,connect=connect,name_table=name_table,field=field[0],id_list=wenera,id_name_list=primory_key)
        elif info=='BLOB':
            print("Поле массива двоичных данных") 
            work_with_picture(cur=cur,connect=connect,name_table=name_table,field=field[0],id_list=wenera,id_name_list=primory_key)

def select_information_about_table(cur,connect,name_table,field):
    """
    Получает информацию о таблице
    cur - подключенная база данных;
    name_table - имя таблиы;
    field - имя поля.   
    """
    cur.execute(
        f"""select R.RDB$FIELD_NAME, F.RDB$FIELD_LENGTH, F.RDB$FIELD_TYPE, t.rdb$type_name--,
        --R.RDB$NULL_FLAG, r.RDB$UPDATE_FLAG
        from RDB$FIELDS F, RDB$RELATION_FIELDS R, rdb$types t
        where
        (F.RDB$FIELD_NAME = R.RDB$FIELD_SOURCE)
        and (R.RDB$SYSTEM_FLAG = 0)
        and f.rdb$field_type = t.rdb$type
        and t.rdb$field_name = 'RDB$FIELD_TYPE'
        AND (RDB$RELATION_NAME = '{name_table}')
        AND (R.RDB$FIELD_NAME = '{field}')""")
    return cur.fetchall()

def change_of_database(cur,connect,table_names=None):
    """
    функция изменения базы данных.
    cur - подключенная база данных
    """
    if table_names is None:
        table_names=select_table_names(cur)
    # print(table_names)
    for table in table_names:
        fields_name=select_field_names(cur,connect,table[0])
        important_relat=select_important_relations(cur,connect,table[0])
        for text in important_relat:
            fields_name.remove(text)
        # print(fields_name)
        update_fields(cur,connect,table[0],fields_name)
        # print("--------------------------------------------")

#date_db=0
if __name__ == "__main__":    
    cursor,connection  = CtoDB.connect_to_bd('/home/alex/anonymizer/BDstorage/name_storage.fdb')
    # cursor,connection  = CtoDB.connect_to_bd('/home/alex/anonymizer/BDstorage/employee.fdb')   
    change_of_database(cursor,connection)
    # change_of_database(cursor,connection,[("PYTHON_EMPLOYEE",)])
    # generate_new_data(cur=cursor,connect=connection,name_table="SEC",field="EMAIL",id_name_list=[("id",)],generator=faker.generate_last_name)
    # generate_new_data(cur=cursor,connect=connection,name_table="foreign_names",field="EMAIL",id_name_list=[("id",)],generator=faker.generate_email)
    # generate_new_data(cur=cursor,connect=connection,name_table="foreign_names",field="SECOND_NAME",id_name_list=[("id",)],generator=faker.generate_last_name)
    # generate_new_data(
 
