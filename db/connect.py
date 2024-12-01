import pymssql

def db_init():
    conn = pymssql.connect(host='sql12.freesqldatabase.com',
                        user='sql12748566',
                        password='bksyrWbIkG',
                        database='sql12748566',
                        port=3306,
                        tds_version='7.0')

    return conn