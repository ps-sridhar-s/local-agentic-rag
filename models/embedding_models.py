from langchain_ollama import OllamaEmbeddings

# embed_model=OllamaEmbeddings(model="mxbai-embed-large")
# from langchain_ollama import OllamaEmbeddings

# Explicitly define the base_url if Ollama is not on the default port
embed_model = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url="http://localhost:11434"
)