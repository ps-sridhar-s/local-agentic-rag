from models.embedding_models import embed_model
def embed_query(text:str)->str:

    generated_embed_query=embed_model.embed_query(text)
    return generated_embed_query

