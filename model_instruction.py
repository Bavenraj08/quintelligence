import chromadb

#setting up the paths for the data and the chroma database
data_path = r"data" 
chroma_path = r"chroma_db" 

#setting up the Chroma client and creating a collection for storing the documents
chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="ia_status")

def question_generator(prompt):
    results = collection.query(
        query_texts=[prompt],
        n_results=3
    )
    return """You are a helpful assistant that provides information about the status of stores based on the provided documents. 
    Use the information from the documents to answer the user's query accurately and concisely.
    The data is as follows:"""+str(results["documents"])+ """ """

def question_selector(prompt):
    results = collection.query(
        query_texts=[prompt],
        n_results=3
    )
    return """ """

def training_recommender(prompt):
    results = collection.query(
        query_texts=[prompt],
        n_results=3
    )
    return """ """