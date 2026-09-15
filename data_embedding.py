from langchain_community.document_loaders import PyPDFDirectoryLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

teams = ['finance', 'reference_data']
for team in teams:

    #setting up the paths for the chroma database, client, and collection for each team
    globals()[f"{team}_chroma_path"] = rf"knowledge_source/{team}" 
    globals()[f"{team}_chroma_client"] = chromadb.PersistentClient(path=f"{team}_chroma_path")
    globals()[f"{team}_collection"] = globals()[f"{team}_chroma_client"].get_or_create_collection(name=f"{team}_collection")
    
    #setting up the paths for the excel and pdf data
    globals()[f"{team}_excel_path"] = rf"knowledge_source/{team}/excel/{team}.xlsx"
    globals()[f"{team}_pdf_path"] = rf"knowledge_source/{team}/pdf"
    
    #loading the documents from the specified data path using the PyPDFDirectoryLoader
    globals()[f"{team}_pdf_loader"] = PyPDFDirectoryLoader(globals()[f"{team}_pdf_path"])
    globals()[f"{team}_excel_loader"] = UnstructuredExcelLoader(globals()[f"{team}_excel_path"])
    globals()[f"{team}_pdf_docs"] = globals()[f"{team}_pdf_loader"].load()
    globals()[f"{team}_excel_docs"] = globals()[f"{team}_excel_loader"].load()

    for doc in globals()[f"{team}_pdf_docs"]:
        if team == 'finance':
            doc.metadata = {
                "source_type": "pdf",
                "department": "Finance",
                "function": "Account Payable, Order to Cash",
                "document_content": "SOP and functional documents"}
        else:
            doc.metadata = {
                "source_type": "pdf",
                "department": "Operations",
                "function": "Reference Data",
                "document_content": "SOP and functional documents"}
            
    if team == 'finance':
        globals()[f"{team}_excel_docs"].metadata = {
            "source_type": "excel",
            "department": "Finance",
            "function": "Account Payable, Order to Cash",
            "document_content": "Roles, skills, proficiencies, and training documents"}
    else:
        globals()[f"{team}_excel_docs"].metadata = {
            "source_type": "excel",
            "department": "Operations",
            "function": "Reference Data",
            "document_content": "Roles, skills, proficiencies, and training documents"}

    globals()[f"{team}_raw_documents"] = globals()[f"{team}_pdf_docs"] + globals()[f"{team}_excel_docs"]

    #splitting the loaded documents into smaller chunks using the RecursiveCharacterTextSplitter
    textsplitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=100, length_function=len,is_separator_regex=False)

    chunks = textsplitter.split_documents(globals()[f"{team}_raw_documents"])

    #preparing the documents, metadata, and ids for insertion into the Chroma collection
    documents = []
    metadata = []
    ids = []

    i = 0

    for chunk in chunks:
        documents.append(chunk.page_content)
        metadata.append(chunk.metadata)
        ids.append("ID" + str(i))
        i += 1

    #adding the prepared documents, metadata, and ids to the Chroma collection
    globals()[f"{team}_collection"].upsert(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )