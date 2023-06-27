import mysql.connector

class MySQLClass:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(host="", user="", password="", database="")
        return self.conn
    
    def close(self):
        if self.conn:
            self.conn.close()

    def execute_select_query(self, query):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    
    def execute_other_query(self, query):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
            self.close()
            return True
        except mysql.connector.Error:
            return False