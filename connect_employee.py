import fdb

con = fdb.connect(host='localhost', database='/opt/RedDatabase/examples/empbuild/employee.fdb', user='SYSDBA', password='masterkey', charset='UTF8');


# Create a Cursor object that operates in the context of Connection con:
cur = con.cursor()
# Execute the SELECT statement:
cur.execute("select * from COUNTRY")

# Retrieve all rows as a sequence and print that sequence:
print(cur.fetchall())

cur.execute(
'select RDB$RELATION_NAME from RDB$RELATIONS '
'where (RDB$SYSTEM_FLAG = 0) AND (RDB$RELATION_TYPE = 0) '
'order by RDB$RELATION_NAME ')
print(cur.fetchall())