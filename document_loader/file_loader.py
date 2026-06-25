from langchain_community.document_loaders import PDFPlumberLoader
import os


import re
from langchain_core.documents import Document


def clean_documents(documents: list[Document]) -> list[Document]:

    cleaned_docs = []

    for doc in documents:

        text = doc.page_content

        # Remove emojis and special symbols
        text = re.sub(
            r"[^\x00-\x7F]+",
            " ",
            text
        )

        # Replace bullets
        text = text.replace("", "-")
        text = text.replace("•", "-")

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Remove multiple newlines
        text = re.sub(r"\n+", "\n", text)

        # Strip leading/trailing spaces
        text = text.strip()

        cleaned_docs.append(
            Document(
                page_content=text,
                metadata=doc.metadata
            )
        )

    return cleaned_docs


def data_loader(file_path: str):

    _, ext = os.path.splitext(file_path)

    if ext.lower() == '.pdf':

        loader = PDFPlumberLoader(
            file_path=file_path,
            extract_images=False
        )

        loaded_context = loader.load()

        return loaded_context

    raise ValueError(
        f"Unsupported file type: {ext}"
    )