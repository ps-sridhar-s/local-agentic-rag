from langchain_text_splitters import RecursiveCharacterTextSplitter


def recursive_chunker(context:list)->list:
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150,separators=[" ","/n"])
    splitted_context = splitter.split_documents(context)

    return splitted_context



