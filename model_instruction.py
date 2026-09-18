import chromadb
from instruction import question_generator_instruction

#setting up the paths for the data and the chroma database
reference_data_chroma_path = rf"knowledge_source/reference_data/chroma_db"

#setting up the Chroma client and creating a collection for storing the documents
reference_data_client = chromadb.PersistentClient(path=reference_data_chroma_path)
rd_functional_collection = reference_data_client.get_or_create_collection(name="reference_data_functional_collection")

def question_generator(skills, courses):
    query_text = f"""
    Role Skills:
    {', '.join(skills)}

    Recommended Courses:
    {', '.join(courses)}

    Retrieve SOPs, process documentation, controls, exceptions,
    business rules and operational guidance related to these skills.
    """
    main_knowledge_source = rd_functional_collection.query(
        query_texts=[query_text],
        n_results=100
    )
    #print (main_knowledge_source['documents'])
    instruction = question_generator_instruction(main_knowledge_source)
    return instruction

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

skill = ['NIMS', 'Leaflet', 'Validation browser', 'Report extraction', 'Leaflet Coding', 'CIP / OGRDS', 'EPIC', 'RCA understanding', 'Problem solving / AI', 'Analytical skills', 'Attention to detail', 'Business communication', 'Item Coding', 'Cross Coding', 'Char Population', 'Shared item mgmt.', 'WCP process']
course = ['OGRDS Introduction', 'Global ePics User Guide', 'NIMS Overall Process', 'Leaflet process and training', 'Evidence-based RCA scenario', 'OGRDS – Retailer Data Management', 'SOP – OGRDS Weekly Change Process', 'SOP – Item Coding', 'SOP – Cross Coding', 'Configuration – Validation Rules Toolbox', 'OGRDS Reports', 'Leaflet coding learning path', 'SOP – Item Coding', 'Scenario, work sample and manager validation', 'Data scenario and work evidence', 'Quality evidence and observation', 'Communication sample and stakeholder evidence']

question_generator (skill, course)