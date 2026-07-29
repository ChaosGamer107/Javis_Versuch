from sentence_transfromers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text):
    """
    Erstellt einen Embedding-Vektor für einen Text.
    """
    return model.encode(text).tolist()