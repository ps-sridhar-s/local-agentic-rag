from document_loader.file_loader import data_loader

def test_data_loader():
    data=data_loader(r"C:\Users\SridharS\Downloads\Sridhar_Project\Local_Agentic_Rag\data_source\langchain-basics-with-llama.pdf")
    assert len(data)>0
