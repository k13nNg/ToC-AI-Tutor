import sqlite3

class MetadataStore:
    def __init__(self, conn_name):
        self.conn = sqlite3.connect(conn_name)

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS docs_metadata (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    section TEXT NOT NULL,
                    subsection TEXT NOT NULL,
                    week INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def insert(self, doc_id, text, section, subsection, week):
        self.conn.execute(
            "INSERT INTO docs_metadata VALUES (?, ?, ?, ?, ?)",
            (doc_id, text, section, subsection, week)
        )
        self.conn.commit()

    def fetch(self, doc_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM docs_metadata WHERE id=?", (doc_id,))
        return cur.fetchone()
    
    def close_connection(self):
        self.conn.close()