from similarity_retrieval.vector_search_tool import vector_search


def test_vector_search():
    retrieved_chunks=vector_search(user_query="what is python",top_k=5)
    print(len(retrieved_chunks)>0)


if "__name__" == "__main__":
    test_vector_search()
    