import mysql.connector

__cnx = None

def get_sql_connection_cursor():
  print("Opening mysql connection")
  global __cnx

  if __cnx is None:
    __cnx = mysql.connector.connect(user='root', password='Mihir2701', database='transport')

  return __cnx

