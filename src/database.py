import pysqlite3 as sqlite3
import sqlite_vss
import os
from tkinter import Tk, filedialog
import subprocess

root = Tk()
root.withdraw()

class NonSavedDatabaseError(Exception):
    #Exception levée quand l'utilisateur annule la sauvegarde de la base
    pass

class Database:
    def __init__(self, path = ""):
        self.path = path
        self.name = os.path.splitext(self.path)[0]
        try:
            self.conn = sqlite3.connect(self.path)
            self.conn.enable_load_extension(True)
            sqlite_vss.load(self.conn)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to {self.name}.db: {e}")
    
    @classmethod
    def initiate(cls, path): 
        try:
            instance = cls(path)
        except Exception as e:
            print(e)
            return None
        history_attributes = [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "role TEXT", 
            "content TEXT", 
            "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
        ]
        embeddings_attributes = ["embedding(384)"]
        embeddings_message_attributes = [
            "embedding_rowid INTEGER", 
            "message_id INTEGER", 
            "FOREIGN KEY(message_id) REFERENCES history(id)"
        ]
        instance.history = Table("history", history_attributes, path, instance.cursor)
        instance.embeddings = Virtual_Table("embeddings", embeddings_attributes, path, instance.cursor)
        instance.embeddings_message = Table("embeddings_message", embeddings_message_attributes, path, instance.cursor)
        
        instance.history.create()
        instance.embeddings.create()
        instance.embeddings_message.create()
        return instance
    
    def create(self):
        try:
            path = filedialog.asksaveasfilename(
                title="Create database",
                defaultextension=".db",
                filetypes=[("SQLite Database", "*.db")]
            )
            if path:
                print(f"Database successfully created at: {path}")
            else:
                raise NonSavedDatabaseError("Database not saved!")
            return self.initiate(path)
        except Exception as e:
            print(f"Database not created: {e}")
            return None
    
    @classmethod
    def open_existing(cls):
        try:
            path = filedialog.askopenfilename(
                title = "choose your database", 
                filetypes=[("SQLite Database", "*.db")]
            )
            instance = cls(path)
            return instance
        except Exception as e:
            print(e)
            return None
    
    def request(self, tables: list = None, fields = None, conditions = None, values = None):
        result = {}
        for table in tables:
            table_fields = fields.get(table.name) if fields else None
            table_conditions = conditions.get(table.name, "") if conditions else ""
            table_values = values.get(table.name, ()) if values else ()
            
            result[table.name] = table.select(fields = table_fields, conditions = table_conditions, values = table_values)
        return result
    
    def delete(self):
        try:
            subprocess.run(["ls", "-l", "/home"], check=True)
        except RuntimeError as e:
            print(f"Error when deleting database: {e}")
    

class Table:
    def __init__(self, name, attributes: list[str], db_path, db_cursor):
        self.name = name
        self.attributes = ", ".join(attributes)
        self.db_path = db_path
        self.db_cursor = db_cursor
        self.commands = SQL_general_commands()
    
    def create(self) -> bool:
        try:
            command = self.commands.create_table.format(
                name = self.name, 
                attributes = self.attributes
            )
            self.db_cursor.execute(command)
            return True
        except sqlite3.Error as e:
            print(f"Error when creating {self.name}: {e}")
            return False
    
    def insert(self, record: list):
        try:
            placeholders = ", ".join(["?" for _ in record])
            command = self.commands.insert_record.format(
                name = self.name,
                placeholders = placeholders
            )
            self.db_cursor.execute(command, record)
        except sqlite3.Error as e:
            print(f"Error when inserting the record: {e}")
    
    def select(self, fields: list[str] = None, condition: str = "", values: list = None):
        try:
            fields_str = ", ".join(fields) if fields else "*"
            command = self.commands.select_fields.format(
                fields = fields_str,
                name = self.name,
                condition = condition or "1=1"
            )
            return self.db_cursor.execute(command, values or ()).fetchall()
        except sqlite3.Error as e:
            print(f"Error when selecting: {e}")
            return []
    
    def delete(self):
        try:
            command = self.commands.delete_table.format(name = self.name)
            self.db_cursor.execute(command)
        except sqlite3.Error as e:
            print(f"Error when deleting {self.name}: {e}")
    

class Virtual_Table(Table):
    def __init__(self, name, attributes:list[str], db_path, db_cursor):
        super().__init__(name, attributes, db_path, db_cursor)
        self.commands = SQL_VIRTUAL_TABLE_commands()
        
    def search_similar(self, query_vectors: list, fields: list = ["rowid"], column: str = "embedding", limit_per_vector: int = 3):
        try:
            all_results = []
            for i, vector in enumerate(query_vectors):
                vector_bytes = vector.astype(np.float32).tobytes()
                fields_str = ", ".join(fields) if fields else "*"
                command = self.commands.search_with_distance.format(
                    fields = fields_str,
                    name = self.name,
                    vector_column = column
                ) + f" LIMIT {limit_per_vector}"
                self.db_cursor.execute(command, [vector_bytes])
                results = self.db_cursor.fetchall()
                all_results.extend(results)
            return sorted(all_results, key=lambda x: x[-1])[:limit_per_vector * len(query_vectors)]
        except sqlite3.Error as e:
            print(f"Error when searching in {self.name}: {e}")
            return []
    

class SQL_general_commands:
    def __init__(self):
        self.create_table = "CREATE TABLE IF NOT EXISTS {name}({attributes})"
        self.insert_record = "INSERT INTO {name} VALUES ({placeholders})"
        self.select_fields = "SELECT {fields} FROM {name} WHERE {condition}"
        self.delete_record = "DELETE FROM {table} WHERE {condition}"
        self.delete_table = "DROP TABLE IF EXISTS {name}"
        

class SQL_VIRTUAL_TABLE_commands(SQL_general_commands):
    def __init__(self):
        super().__init__()
        self.create_table = "CREATE VIRTUAL TABLE IF NOT EXISTS {name} USING vss0({attributes})"
        self.search = "SELECT {fields} FROM {name} WHERE vss_search({vector_column}, ?)"
        self.search_with_distance = """
            SELECT {fields}, distance 
            FROM {name} 
            WHERE vss_search({vector_column}, ?)
            ORDER BY distance ASC
        """
    
if __name__ == '__main__':
    database = Database()
    database.create()
