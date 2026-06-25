from langchain_text_splitters import CharacterTextSplitter


def fixed_chunker(documents):

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)