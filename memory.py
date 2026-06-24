import sqlite3

DB_NAME = "nova.db"

def init_db():
   
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
           key TEXT PRIMARY KEY,
            value TEXT
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
        (f"%{keyword}%",)
    )

    rows=cursor.fetchall()

    conn.close()
    return rows

def delete_memory(memory_id):
    
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor

    cursor.execute(
        "DELETE FROM memories WHERE id=?",
        (memory_id,)
    )

    conn.commit()
    conn.close()

def save_fact(key,value):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO facts(key,value)
        VALUES(?,?)
    """,(key, value))
    
    conn.commit()
    conn.close()

def get_fact(key):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT value
        FROM facts
        WHERE key=?
    """,(key,))

    row=cursor.fetchone()

    conn.close

    if row:
        return row[0]
    
    return None