from chromadb import PersistentClient

print("Starting...")

client = PersistentClient(
    path="./data_warehouse/rag_vector_db"
)

print("Client created")

collections = client.list_collections()

print("Collections:")
print(collections)

for collection in collections:

    print("\nCollection Name:")
    print(collection.name)

    print("Count:")
    print(collection.count())

    results = collection.get(
        limit=5
    )

    print(results)

print("Finished")