import fdb
import connect_employee as CtoDB
import sql_query as sql
import blur as blur

class perfecr():
    def new_file(self):
        self.x=1


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        if type(data).__name__=="BlobReader":
            file.write(data.read())
        else:
            file.write(data)


def readBLOB(cursor,connection,table,field,emp_id, photo):
    if __name__=='__main__':
        print("Reading BLOB data from python_employee table")
    try:
        # print(field,table,emp_id)
        sql_fetch_blob_query = "SELECT "+field+" from "+table+" where id = "+emp_id
        # print(sql_fetch_blob_query)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            # print("Id = ", row[0], )
            # print("Name = ", row[1])
            image = row[0]
            print("Storing employee image on disk \n")
            write_file(image, photo)
    except:
        print("Failed to read BLOB data from Firebird table")
    # finally:
    #     if __name__=='__main__':
    #         cursor.close()
    #         connection.close()
    #         print("Firebird connection is closed")

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(cursor,connection, table,emp_id, name, photo):
    if __name__=='__main__':
        print("Inserting BLOB into python_employee table")
    try:
        sql_insert_blob_query = """ INSERT INTO """+table+"""
                          (id, "name", photo) VALUES (?,?,?)"""
        empPicture = convertToBinaryData(photo)
        print(type(empPicture))
        insert_blob_tuple = (emp_id, name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        if __name__=='__main__': 
            print("Image and file inserted successfully as a BLOB into python_employee table", result)
    except fdb.connector.Error as error:
        print("Failed inserting BLOB data into Firebird table {}".format(error))
    # finally:
    #     if __name__=='__main__':    
    #         cursor.close()
    #         connection.close()
    #         print("Firebird connection is closed")

def updateBLOB(cursor,connection,table,field ,emp_id, photo):
    if __name__=='__main__':
        print("Inserting BLOB into python_employee table")
    try:
        #print(cursor)
        empPicture = convertToBinaryData(photo)
        sql_insert_blob_query = "UPDATE "+table+" SET "+field+" = ? WHERE id = ?" 
        val = (empPicture,int(emp_id))
        #print(sql_insert_blob_query)
        result = cursor.execute(sql_insert_blob_query,val)
        connection.commit() #updata database
        if __name__=='__main__':
            print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except:
        print("Failed inserting BLOB data into Firebird table")
    # finally:
    #     # if connection.is_connected():
    #     if __name__=='__main__':
    #         cursor.close()
    #         connection.close()            
    #         print("Firebird connection is closed")

#insertBLOB(2, "Eric", "/home/alex/picture/birth_certificate.png")
#insertBLOB(3, "Scott", "/home/alex/picture/passport.png")
# #readBLOB(1, "/home/alex/picture/passport.jpg")


if __name__ == "__main__":    
    cursor,connection = CtoDB.connect_to_bd('/home/alex/anonymizer/BDstorage/name_storage.fdb')
    path = "/home/alex/anonymizer/RAM/1.jpeg"
    readBLOB(cursor,connection,"PYTHON_EMPLOYEE","photo","1", path)
    blur.blur_image(path)
    updateBLOB(cursor,connection,"python_employee","photo","1", path)
    # readBLOB(cursor,connection,"MYPICTURES","PICTURE","1", path)
    # blur.blur_image(path)
    # updateBLOB(cursor,connection,"MYPICTURES","PICTURE","1", path)
    