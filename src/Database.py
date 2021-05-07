import sqlite3 as sql
import numpy as np
import os

database_name = 'result.db'

def open_database(db_name):
   database_path = os.path.abspath(os.getcwd())
   database_path = database_path.replace('src', 'db')
   db = sql.connect(database_path +'\\' + db_name)
   my_cursor = db.cursor()
   return db, my_cursor

def create_table(db_name, table_name, header, type):
   db, my_cursor = open_database(db_name)                                           #open database
   column_names = ' REAL, '.join(header)                                                 #header dizisi sütun ismi olmaya uygun hale getirildi

   command = "CREATE TABLE IF NOT EXISTS "+'['+ type + table_name + ']' + " (Filename TEXT PRIMARY KEY, "+ column_names + " REAL)"             #Comp_Db_GTZAN_function_Coiflet_Degree_3

   my_cursor.execute(command)
   db.close()

def add_values_to_table(db_name, table_name, file_name, col_names, matrix, type):
   db, my_cursor = open_database(db_name)                                                       #dinamik sütun için    #sütun sayısına bakılarak
                                                                                                # soru işareti koyup değeri ekliyoruz
   real = np.array(matrix).real
   imag = np.array(matrix).imag

   command = 'INSERT INTO '  + '[' + type + table_name + ']' + ' (Filename, ' + ', '.join(col_names) + ') VALUES (' + "'"  + file_name + "', " +  ','.join(['?'] * ((len(col_names)))) + ')'

   if type == "":
      my_cursor.execute(command, real)
   else:
      my_cursor.execute(command, imag)

   db.commit()
   db.close()

def delete_row(db_name, table_name, file_name, type):
   db, my_cursor = open_database(db_name)
   command = 'DELETE FROM '  + '['+ type + table_name + ']' + ' WHERE Filename = ' + "'" + file_name + "'"
   my_cursor.execute(command)
   db.commit()
   db.close()

def read_from_table(db_name, table_name):
   db, my_cursor = open_database(db_name)
   my_cursor.execute("SELECT * FROM " + '[' + table_name + ']')
   rows = my_cursor.fetchall()
   return rows

def get_table_names(db_name):
   db, my_cursor = open_database(db_name)
   my_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

   db_tables = my_cursor.fetchall()

   my_cursor.close()
   db.close()

   tables = []
   for table in db_tables :
      tables.append(str(table).split("'")[1])
   return tables

