from embedding.generate_embeddings import embed_query



def test_embed_query():
    test_embeddings=embed_query("Hi")
    assert test_embeddings is not None
    assert  isinstance(test_embeddings,list)
    assert len(test_embeddings)>0