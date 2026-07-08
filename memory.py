import sqlite3

DB_NAME = "database/nova.db"

def init_db():
   
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE,
        value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        content TEXT,
        importance INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        speaker TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS semantic_memory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def add_memory(memory_type, content, importance=1):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memories(type, content, importance)
        VALUES(?, ?, ?)
        """,(memory_type, content, importance))

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
        """,(f"%{keyword}%",))

    rows=cursor.fetchall()

    conn.close()
    
    return rows

def delete_memory(memory_id):
    
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor

    cursor.execute("""
        DELETE FROM memories 
        WHERE id=?",
    """,(memory_id,))

    conn.commit()
    conn.close()

def get_recent_memories(limit=10):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT type, content, importance, created_at
        FROM memories
        ORDER BY importance DESC, id DESC
        LIMIT ?
    """,(limit,))

    rows=cursor.fetchall()

    conn.close()

    return rows

def clear_memories():

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM memories
    """)

    conn.commit()
    conn.close()

def save_fact(key,value):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO facts(key, value)
        VALUES(?, ?)
        ON CONFLICT(key)
        DO UPDATE SET
            value = excluded.value,
            updated_at = CURRENT_TIMESTAMP
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

    return row[0] if row else None

def get_all_facts():

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT key, value
        FROM facts
    """)

    rows=cursor.fetchall()

    conn.close()

    return rows

def delete_fact(key):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM facts
        WHERE key=?
    """,(key,))

    conn.commit()
    conn.close()

def clear_facts():

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM facts
    """)

    conn.commit()
    conn.close()

def add_conversation(speaker, message):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO conversations(speaker,message)
        VALUES(?, ?)
    """,(speaker, message))
    
    conn.commit()
    conn.close()

def get_recent_conversations(limit=20):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT speaker,message
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
    """,(limit,))

    rows=cursor.fetchall()

    conn.close

    return rows[::-1]

def clear_conversations():

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM conversations
    """)

    conn.commit()
    conn.close()

def add_semantic_memory(content):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO semantic_memory(content)
        VALUES(?)
    """,(content,))

    conn.commit()
    conn.close()

def search_semantic_memory(keyword):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT content
        FROM semantic_memory
        WHERE content LIKE ?
        ORDER BY id DESC
        LIMIT 10            
    """,(f"%{keyword}%",))

    rows=cursor.fetchall()

    conn.close()

    return rows

def get_recent_semantic_memory(limit=10):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT content
        FROM semantic_memory
        ORDER BY id DESC
        LIMIT ?
    """,(limit,))

    rows=cursor.fetchall()

    conn.close()

    return rows

def clear_semantic_memory():

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM semantic_memory
    """)

    conn.commit()
    conn.close()

def get_relevant_context(user_input):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    words=user_input.lower().split()

    results=[]

    for word in words:

        cursor.execute("""
            SELECT key, value
            FROM facts
            WHERE key LIKE ?
            OR value LIKE ?
        """,(f"%{word}%",f"%{word}%"))

        results.extend(cursor.fetchall())

    for word in words:

        cursor.execute("""
            SELECT content
            FROM memories
            WHERE content LIKE ?
            LIMIT 5
        """,(f"%{word}%",))

        results.extend(cursor.fetchall())

    for word in words:

        cursor.execute("""
            SELECT content
            FROM semantic_memory
            WHERE content LIKE ?
            LIMIT 5
        """,(f"%{word}%",))

        results.extend(cursor.fetchall())

   
    conn.close()

    return results