class DB():
    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()

    @property
    def cursor(self):
        return self.c
    
    @cursor.setter
    def cursor(self, value):
        self.c = value

    def create_database(self, name):
        self.c.execute(f"CREATE DATABASE {name}")

    def create_table(self, name, columns):
        # Check if table exists, if not, create table
        self.c.execute(f"SHOW TABLES LIKE '{name}'")
        if not self.c.fetchone():
            self.c.execute(f"CREATE TABLE {name} ({columns})")

    def insert(self, table, columns, values):
        if "None" in values:
            values = values.replace("None", "NULL")
        self.c.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

    def addColumn(self, table, columnName, dataType):
        self.c.execute(f"ALTER TABLE {table} ADD {columnName} {dataType}")

    def select(self, table, columns):
        self.c.execute(f"SELECT {columns} FROM {table}")
        return self.c.fetchall()
    
    def update(self, table, columns, values, condition):
        self.c.execute(f"UPDATE {table} SET {columns} = {values} WHERE {condition}")

    def delete(self, table, condition):
        self.c.execute(f"DELETE FROM {table} WHERE {condition}")

    def drop(self, table):
        self.c.execute(f"DROP TABLE {table}")