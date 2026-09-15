teams = ['finance', 'reference_data']
for team in teams:
    
    path = f"{team}_excel_path"
    globals()[f"{team}_excel_path"] = rf"knowledge-source/{team}/excel"    
    globals()[f"{team}_pdf_path"] = rf"knowledge-source/{team}/pdf"


globals()[f"{team}_pdf_path"] = globals()[f"{team}_excel_path"]
print(reference_data_pdf_path) #type: ignore
print(finance_pdf_path) #type: ignore