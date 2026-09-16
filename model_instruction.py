import chromadb
from instruction import question_generator_instruction

#setting up the paths for the data and the chroma database
finance_chroma_path = rf"knowledge_source/finance/chroma_db"
reference_data_chroma_path = rf"knowledge_source/reference_data/chroma_db"

#setting up the Chroma client and creating a collection for storing the documents
finance_client = chromadb.PersistentClient(path=finance_chroma_path)
reference_data_client = chromadb.PersistentClient(path=reference_data_chroma_path)
fd_guideline_collection = finance_client.get_or_create_collection(name="finance_guideline_collection")
rd_guideline_collection = reference_data_client.get_or_create_collection(name="reference_data_guideline_collection")
rd_functional_collection = reference_data_client.get_or_create_collection(name="reference_data_functional_collection")

def question_generator(query_text):

    knowledge_source_B = rd_functional_collection.query(
        query_texts=[query_text],
        n_results=100
    )

    knowledge_source_A = rd_guideline_collection.query(
        query_texts=[query_text],
        n_results=100
    )
    # query_text = f"""
    # Department: {prompt['Department']}
    # Skill: {prompt['Skill']}
    # Role: {prompt['Role ID']}
    # Difficulty: {prompt['Difficulty']}
    # Question Count: {prompt['Question Count']}
    # """

    # if prompt["Department"] == "Operation Department":
    #     knowledge_source_B = rd_functional_collection.query(
    #         query_texts=[query_text],
    #         n_results=3
    #     )

    #     knowledge_source_A = rd_guideline_collection.query(
    #         query_texts=[query_text],
    #         n_results=3
    #     )

    # else:
    #     knowledge_source_A = fd_guideline_collection.query(
    #         query_texts=[query_text],
    #         n_results=3
    #     )
    print("Knowledge Source A:", knowledge_source_A["documents"])
    print("Knowledge Source B:", knowledge_source_B["documents"])

question_generator("What is the proficiency level of skills required for a Data Operation Analyst?")

    #result = question_generator_instruction(knowledge_source_A = knowledge_source_A, knowledge_source_B = None if "Operation" not in prompt["Department"] else knowledge_source_B)
    #return result
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