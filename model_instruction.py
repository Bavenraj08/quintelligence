import chromadb
from instruction import question_generator_instruction, question_selector_instruction, training_recommender_instruction

#setting up the paths for the data and the chroma database
finance_chroma_path = rf"knowledge_source/finance/chroma_db"
reference_data_chroma_path = rf"knowledge_source/reference_data/chroma_db"

#setting up the Chroma client and creating a collection for storing the documents
finance_client = chromadb.PersistentClient(path=finance_chroma_path)
reference_data_client = chromadb.PersistentClient(path=reference_data_chroma_path)
fd_guideline_collection = finance_client.get_or_create_collection(name="finance_guideline_collection")
rd_guideline_collection = reference_data_client.get_or_create_collection(name="reference_data_guideline_collection")
rd_functional_collection = reference_data_client.get_or_create_collection(name="reference_data_functional_collection")

def question_generator(prompt):

    if "Operation" in prompt["Department ID"]:
        knowledge_source_B= rd_functional_collection.query(
            query_texts=[prompt],
            n_results=3
        )
        knowledge_source_A = rd_guideline_collection.query(
            query_texts=[prompt],
            n_results=3
        )
    else:
        knowledge_source_A = fd_guideline_collection.query(
            query_texts=[prompt],
            n_results=3
        )
    return question_generator_instruction(knowledge_source_A, knowledge_source_B)

# def question_selector(prompt):
#     knowledge_source_A = collection.query(
#         query_texts=[prompt],
#         n_results=3
#     )
#     return """ """

# def training_recommender(prompt):
#     knowledge_source_A = collection.query(
#         query_texts=[prompt],
#         n_results=3
#     )
#     return """ """