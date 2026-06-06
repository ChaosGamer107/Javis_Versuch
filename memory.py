import sqlite3

DB_NAME = "nova.db"

def init_db():
   
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def add_memory(memory_type, content):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memories(type, content)
        VALUES(?, ?)
        """,
        (memory_type, content)
    )

    conn.commit()
    conn.close()

def get_memories():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute( """
    SELECT type, content
    FROM memories
    ORDER BY id DESC
    """)

    memories = cursor.fetchall()

    conn.close()

    return memories

def search_memories(keyword):
    
    conn=sqlite3.connect(DB_NAME)

    cursor=conn.cursor()

    cursor.execute(
        """
        SELECT content
        FROM memories
        WHERE content LIKE ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (f"%{keyword}%")
    )

    rows=cursor.fetchall()

    conn.close()
    return rows

