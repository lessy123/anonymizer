import fdb
from firebird.driver import connect

import fdb
# con = fdb.create_database("create database '/home/alex/work/test.fdb' user 'sysdba' password 'masterkey'")
con = fdb.create_database("create database '/opt/RedDatabase/examples/mydatabase/test.fdb' user 'sysdba' password 'masterkey'")
print("Hello")

# _req = "";
# _req += " CREATE DATABASE 'localhost:/home/alex/work/test.fdb' "
# _req += " page_size 8192 "
# _req += " user 'SYSDBA' "
# _req += " password 'masterkey' "
# _req += " DEFAULT CHARACTER SET UTF8 ";

# con = fdb.create_database( _req );

# # ---------

# con = fdb.connect(host='localhost', database='/home/alex/work/test.fdb', user='SYSDBA', password='fobar', charset='UTF8');




# f = open('/home/alex/Документы/masterkey', 'r')
# print(f.read(10))

# con = fdb.connect(host='localhost', database='/opt/RedDatabase/examples/empbuild/employee.fdb', user='SYSDBA', password='masterkey', charset='UTF8');
# #con = fdb.connect(host='127.0.0.1', database='/opt/RedDatabase/examples/empbuild/employee.fdb', user='sysdba', password='masterkey')



# from firebird.driver import driver_config
# driver_config.server_defaults.host.value = 'localhost'
# con = connect('/home/alex/Документы/employee.fdb', user='sysdba', password='masterkey')

# con = connect('/opt/RedDatabase/examples/empbuild/employee.fdb', user='sysdba', password='masterkey')
# con = connect('employee.fdb', user='SYSDBA', password='masterkey')
# con = connect('/opt/RedDatabase/examples/empbuild/employee.fdb', 
#        user='SYSDBA', password='masterkey')
# # con = fdb.connect(
# #     host='bison', database='/opt/RedDatabase/examples/empbuild/employee.fdb',
# #     user='SYSDBA', password='masterkey'
# #   )
# # Create a Cursor object that operates in the context of Connection con:
# cur = con.cursor()

# # Execute the SELECT statement:
# cur.execute("select * from languages order by year_released")

# # Retrieve all rows as a sequence and print that sequence:
# print (cur.fetchall())