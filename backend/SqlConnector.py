import cx_Oracle

def get_connection():
    cursor = cx_Oracle.connect(user="d.rangaraju",password="3cbfrLvxQ7YtmdNjTFYVeoaK",dsn="oracle.cise.ufl.edu/ORCL")
    return cursor


