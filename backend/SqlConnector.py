import cx_Oracle

def get_connection():
    cursor = cx_Oracle.connect(user="d.rangaraju",password="3cbfrLvxQ7YtmdNjTFYVeoaK",dsn="oracle.cise.ufl.edu/ORCL")
    return cursor

def get_connection2():
    cursor = cx_Oracle.connect(user="vyasdishant",password="tlGQDuBUhZH7QpW2qBeKRr27",dsn="oracle.cise.ufl.edu/ORCL")
    return cursor

def get_connection3():
    cursor = cx_Oracle.connect(user="kbudham",password="pTi0gREbUqoycBaopoLzPni0",dsn="oracle.cise.ufl.edu/ORCL")
    return cursor

def get_connection4():
    cursor = cx_Oracle.connect(user="thumsib",password="xT7U6OIIKz404w1VCOt3fZWe",dsn="oracle.cise.ufl.edu/ORCL")
    return cursor