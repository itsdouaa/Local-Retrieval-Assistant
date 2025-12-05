import pysqlite3 as sqlite3
import sqlite_vss
import numpy as np
import os

class SQL_general_commands:
    def __init__(self):
        self.create_table = "CREATE TABLE IF NOT EXISTS {name}({attributes})"
        self.insert_record = "INSERT INTO {name} {columns} VALUES ({placeholders})"
        self.select_fields = "SELECT {fields} FROM {name} WHERE {condition}"
        self.delete_record = "DELETE FROM {table} WHERE {condition}"
        self.delete_table = "DROP TABLE IF EXISTS {name}"
    

class SQL_VIRTUAL_TABLE_commands(SQL_general_commands):
    def __init__(self):
        super().__init__()
        self.create_table = "CREATE VIRTUAL TABLE IF NOT EXISTS {name} USING vss0({attributes})"
        self.insert_record = "INSERT INTO {name} (rowid, {columns}) VALUES ((SELECT IFNULL(MAX(rowid), 0) + 1 FROM {name}), {placeholders})"
        self.search = "SELECT {fields} FROM {name} WHERE vss_search({vector_column}, ?)"
        self.search_with_distance = """
            SELECT {fields}, distance 
            FROM {name} 
            WHERE vss_search({vector_column}, ?)
            ORDER BY distance ASC
        """
    

class Table:
    def __init__(self, name, attributes: list[str], db_path, db_cursor):
        self.name = name
        self.attributes = attributes
        self.db_path = db_path
        self.db_cursor = db_cursor
        self.commands = SQL_general_commands()
    
    def create_if_not_exist(self) -> bool:
        try:
            command = self.commands.create_table.format(
                name = self.name, 
                attributes = ", ".join(self.attributes)
            )
            self.db_cursor.execute(command)
            self.db_cursor.connection.commit()
            return True
        except sqlite3.Error as e:
            return False
    
    def insert(self, record: list, columns: list[str] = None):
        try:
            placeholders = ", ".join(["?" for _ in record])
            command = self.commands.insert_record.format(
                name = self.name,
                columns = '('+", ".join(columns)+')' if columns else "",
                placeholders = placeholders
            )
            self.db_cursor.execute(command, record)
            self.db_cursor.connection.commit()
        except sqlite3.Error:
            pass
    
    def select(self, fields: list[str] = None, condition: str = "", values: list = None):
        try:
            fields_str = ", ".join(fields) if fields else "*"
            command = self.commands.select_fields.format(
                fields = fields_str,
                name = self.name,
                condition = condition or "1=1"
            )
            return self.db_cursor.execute(command, values or ()).fetchall()
        except sqlite3.Error:
            return []
    
    def delete_if_exist(self):
        try:
            command = self.commands.delete_table.format(name = self.name)
            self.db_cursor.execute(command)
            self.db_cursor.connection.commit()
        except sqlite3.Error:
            pass
    

class Virtual_Table(Table):
    def __init__(self, name, attributes:list[str], db_path, db_cursor):
        super().__init__(name, attributes, db_path, db_cursor)
        self.commands = SQL_VIRTUAL_TABLE_commands()
    
    def insert(self, record: list, columns: list[str] = None):
        try:
            if len(record) == 1:
                vector = record[0]
                if hasattr(vector, 'tobytes'):
                    vector_bytes = vector.tobytes()
                else:
                    vector_bytes = vector
                placeholders = ", ".join(["?" for _ in record])
                command = self.commands.insert_record.format(
                    name = self.name,
                    columns = '('+", ".join(columns)+')' if columns else self.attributes[0].split('(')[0],
                    placeholders = placeholders
                )
                self.db_cursor.execute(command, [vector_bytes])
                self.db_cursor.connection.commit()
        except Exception:
            pass
    
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
            sorted_results = sorted(all_results, key=lambda x: x[-1])[:limit_per_vector * len(query_vectors)]
            return [item[0] for item in sorted_results]
        except sqlite3.Error:
            return []
    

class NonSavedDatabaseError(Exception):
    pass
    

class NonOpenedDatabaseError(Exception):
    pass
    

class Database:
    def __init__(self, path: str = ""):
        self.path = ""
        self.name = os.path.splitext(os.path.basename(self.path))[0]
        self.tables: list['Table'] = []
        self.conn = None
        self.on_created = None
        self.on_opened = None
    
    def initiate(self, path: str):
        try:
            if not self.conn:
                self.conn = sqlite3.connect(path)
                self.conn.enable_load_extension(True)
                sqlite_vss.load(self.conn)
                self.conn.execute("PRAGMA foreign_keys = ON;")
                self.cursor = self.conn.cursor()
            
            self.path = path
            self.name = os.path.splitext(os.path.basename(self.path))[0]
            self.tables = []
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
            history = Table("history", history_attributes, path, self.cursor)
            embeddings = Virtual_Table("embeddings", embeddings_attributes, path, self.cursor)
            embeddings_message = Table("embeddings_message", embeddings_message_attributes, path, self.cursor)
            
            self.tables.extend([history, embeddings, embeddings_message])
        
            self.get_table("history").create_if_not_exist()
            self.get_table("embeddings").create_if_not_exist()
            self.get_table("embeddings_message").create_if_not_exist()
            return True
        except sqlite3.Error:
            return False
    
    def create(self, path: str = "", page=None, on_created=None):
        try:
            self.on_created = on_created
            if not path:
                from ui.components.file_save_dialog import FileSaveDialog
                FileSaveDialog.ask_saveas_filename(
                    page=page,
                    on_file_selected=self._handle_create_selection,
                    dialog_title="Create database",
                    default_filename="database.db",
                    file_types=[("SQLite Database", "*.db")]
                )
                return
            if path:
                if not path.endswith('.db'):
                    path = path + '.db'
                success = self.initiate(path)
                if success and self.on_created:
                    self.on_created(self)
        except Exception:
            if self.on_created:
                self.on_created(None)
    
    def _handle_create_selection(self, path):
        if path:
            if not path.endswith('.db'):
                path = path + '.db'
            success = self.initiate(path)
            if success and self.on_created:
                self.on_created(self)
        else:
            if self.on_created:
                self.on_created(None)
    
    def open_existing(self, path: str = "", page=None, on_opened=None):
        try:
            self.on_opened = on_opened
            if not path:
                from ui.components.file_open_dialog import FileOpenDialog
                FileOpenDialog.askopenfilename(
                    page=page,
                    on_file_selected=self._handle_open_selection,
                    dialog_title="Choose your database",
                    file_types=[("SQLite Database", "*.db")]
                )
                return
            if path:
                success = self.initiate(path)
                if success and self.on_opened:
                    self.on_opened(self)
        except Exception:
            if self.on_opened:
                self.on_opened(None)
    
    def _handle_open_selection(self, path):
        if path:
            success = self.initiate(path)
            if success and self.on_opened:
                self.on_opened(self)
        else:
            if self.on_opened:
                self.on_opened(None)
    
    def get_path(self):
        return self.path
    
    def get_table(self, name: str) -> Table:
        for table in self.tables:
            if table.name == name:
                return table
        raise ValueError(f"Table '{name}' not found!")
    
    def request(self, tables: list[Table], fields = None, conditions = None, values = None):
        result = {}
        for table in tables:
            table_fields = fields.get(table.name) if fields else None
            table_conditions = conditions.get(table.name, "") if conditions else ""
            table_values = values.get(table.name, ()) if values else ()
            
            result[table.name] = table.select(fields = table_fields, condition = table_conditions, values = table_values)
        return result
    
    def delete(self):
        try:
            import subprocess
            subprocess.run(["rm", self.path], check=True)
        except:
            pass
    
    def link_tables(self, link_Table: Table, link_record: list, link_attributes: list[str] = None):
        try:
            link_Table.insert(link_record, link_attributes)
        except:
            pass
    
    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except:
            pass
