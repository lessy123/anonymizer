import fdb

def connect_to_bd(name_db='/opt/RedDatabase/examples/empbuild/employee.fdb',connect='localhost',
                    user_name='SYSDBA',password_db='masterkey',charset_db='UTF8'):
    try:
        con = fdb.connect(host=connect, database=name_db, user=user_name, password=password_db, charset=charset_db);
        print("База успешно подключена")        
        return con.cursor(),con,True
    except Exception:      
        print("Ошибка, не удалось подключиться к базе данных")
        return 0,0,False

#con = fdb.connect(host='localhost', database='/opt/RedDatabase/examples/empbuild/employee.fdb', user='SYSDBA', password='masterkey', charset='UTF8');
if __name__ == "__main__":    
    cur = connect_to_bd('/home/alex/anonymizer/BDstorage/employee.fdb')
    # Execute the SELECT statement:
    cur.execute('select * from "COUNTRY"')
    country=cur.fetchall()
    print(len(country))
    print(country[0])
    print(country[0][0])
    cur.execute(
    'select RDB$FIELD_NAME from RDB$RELATION_FIELDS '
    'where RDB$RELATION_NAME = \'JOB\'')
    print(cur.fetchall())
# cur.execute(
# 'select RDB$RELATION_NAME from RDB$RELATIONS '
# 'where (RDB$SYSTEM_FLAG = 0) AND (RDB$RELATION_TYPE = 0) '
# 'order by RDB$RELATION_NAME ')
# print(cur.fetchall())