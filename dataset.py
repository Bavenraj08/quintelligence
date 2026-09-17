import pandas as pd

excel_file = r"knowledge_source\reference_data\excel\reference_data.xlsx"

sheets = pd.read_excel(
    excel_file,
    sheet_name=None,  # Load all sheets
    engine="openpyxl"
)

dept_df = sheets["Department_Function"]
role_df = sheets["Role_Master"]
skill_df = sheets["Skill_Master"]
proficiency_df = sheets["Proficiency_Level"]
role_skill_df = sheets["Role_Skill_Map"]
training_df = sheets["Training_Catalogue"]
training_skill_df = sheets["Training_Skill_Map"]

def get_role_skills(role_id):
    role_skills = (
        role_skill_df
        .merge(dept_df, on="Function_ID", how="left", suffixes=("", "_dept"))
        .merge(role_df, on="Role_ID", how="left" ,suffixes=("", "_role"))
        .merge(skill_df, on="Skill_ID", how="left", suffixes=("", "_skill"))
        .merge(proficiency_df, on="Proficiency_ID", how="left", suffixes=("", "_proficiency"))
    )

    role_skills = role_skills[
        role_skills["Role_ID"] == role_id
    ]

    skill_list = role_skills['Skill_Name'].tolist()
    course_list = get_course_skills(skill_list)

    return skill_list, course_list

def get_course_skills(skill_list):
    course_skills = (
        training_skill_df
        .merge(training_df, on="course_id", how="left", suffixes=("", "_course"))
        .merge(skill_df, on="Skill_ID", how="left", suffixes=("", "_skill"))
        .merge(dept_df, on="Function_ID", how="left", suffixes=("", "_dept"))
    )

    course_skills = course_skills[
        course_skills["Skill_Name"].isin(skill_list)
    ]
    course_list = course_skills['course_title'].tolist()
    return course_list

get_role_skills("RD_R01")