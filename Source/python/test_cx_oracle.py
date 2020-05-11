import cx_Oracle
import sqlalchemy
# dsn = cx_Oracle.makedsn('192.168.1.5', 1521, r'XE')
# db = cx_Oracle.connect('dvirhaberman', 'dvirhpass', dsn)
# print(db.version)

conn_string =f"oracle+cx_oracle://dvirhaberman:dvirhpass@192.168.1.5:1521/dvirhaberman"

eng = sqlalchemy.create_engine(conn_string)

conn = eng.connect()