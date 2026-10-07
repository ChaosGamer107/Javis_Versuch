import sqlite3
import json
import numpy as np
from config import DB_NAME
from memory.embeddings import create_embedding

#----------------------------------
#Datenbank
#----------------------------------
def init_db():
   
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts(
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        content TEXT,
        embedding TEXT,
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

    cursor.execute("PRAGMA table_info(facts)")
    fact_columns = [column[1] for column in cursor.fetchall()]

    if "updated_at" not in fact_columns:
        cursor.execute("""
            ALTER TABLE facts
            ADD COLUMN updated_at TIMESTAMP
        """)


    conn.commit()
    conn.close()

#----------------------------------
#Semantic memory
#----------------------------------

def add_semantic_memory(content):

    embedding=create_embedding(content)

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO memories(type, content, embedding)
        VALUES(?, ?, ?)
    """,("semantic", content, json.dumps(embedding)))

    conn.commit()
    conn.close()

def search_semantic_memory(keyword):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT content
        FROM memories
        WHERE type = ?
        AND content LIKE ?
        ORDER BY id DESC
        LIMIT 10            
    """,("semantic",f"%{keyword}%"))

    rows=cursor.fetchall()

    conn.close()

    return rows

def get_recent_semantic_memory(limit=10):

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        SELECT content
        FROM memories
        WHERE type = ?
        ORDER BY id DESC
        LIMIT ?
    """,("semantic", limit))

    rows=cursor.fetchall()

    conn.close()

    return rows

def clear_semantic_memory():

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM memories
        WHERE type = ?
    """,("semantic",))

    conn.commit()
    conn.close()

def search_memories_semantic(query, top_k=5):

    query_embedding=np.array(
        create_embedding(query),
        dtype=float
    )

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
    SELECT content, embedding
    FROM memories
    WHERE embedding IS NOT NULL
  """)

    rows=cursor.fetchall()

    conn.close()

    if not rows:
        return[]

    similarities=[]

    query_norm=np.linalg.norm(query_embedding)

    if query_norm == 0:
        return []

    for content, embedding_json in rows:

        try:

            embedding=np.array(
                json.loads(embedding_json),
                dtype=float
            )

            embedding_norm=np.linalg.norm(embedding)

            if embedding_norm == 0:
                continue

            similarity = np.dot(query_embedding, embedding) / (query_norm * embedding_norm) 

            similarities.append((float(similarity), content))

        except (json.JSONDecodeError, TypeError, ValueError):
            continue

    similarities.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return similarities[:top_k]

#----------------------------------
#Fakten
#----------------------------------

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
        ORDER BY key
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

#----------------------------------
#Conversations
#----------------------------------

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