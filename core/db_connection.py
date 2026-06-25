import mysql.connector
import config

class DBConnection:
    """
    Manages raw connection lifecycles to the fitlog_nutrition_db instance.
    Implements a Context Manager interface for safe resource allocation.
    """
    def __init__(self):
        self.config = {
            'host': config.DB_HOST,
            'user': config.DB_USER,
            'password': config.DB_PASSWORD,
            'database': config.DB_NAME
        }
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Opens a resource pipe to MySQL when entering a 'with' block."""
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor, self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically releases database sockets upon code block termination."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()