import json
from dataset import get_role_skills
from fastapi import FastAPI
from typing import Literal
from model_instruction import question_generator
from pydantic import BaseModel
import model

app = FastAPI()

class AssessmentRequest(BaseModel):
    department: str
    function: str
    role_id: str
    difficulty: Literal["EASY", "MODERATE", "HARD"]
    question_count: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/question_generator")
async def generate(request: AssessmentRequest):
    department = request.department
    function = request.function
    role_id = request.role_id
    difficulty = request.difficulty
    question_count = request.question_count

    skill_list, course_list = get_role_skills(role_id, function, department)
    system_prompt = question_generator(skills=skill_list, courses=course_list)

    user_prompt = f"""Create {question_count} multiple-choice questions for the department '{department}', function '{function}', with difficulty level '{difficulty}'. For every question, indicate the skill it is testing. Use the following skills: {', '.join(skill_list)}.  Use the following courses list when generating question from knowledge source: {', '.join(course_list)}."""
    model_response = model.invoke(system_prompt=system_prompt, user_prompt=user_prompt)
   
    return json.loads(model_response)

# @app.post("/training_recommender")
# async def recommend(request: AssessmentRequest):
#     prompt = f"""Department ID: {request.department_id}
#             Function ID: {request.function_id}
#             Role ID: {request.role_id}"""
#     model_response = model.invoke(training_recommender(prompt), prompt)
#     return {"message": model_response}