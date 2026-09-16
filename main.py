import json

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
    prompt = {"Department": request.department,
            "Function": request.function,
            "Role ID": request.role_id,
            "Difficulty": request.difficulty,
            "Question Count": request.question_count
    }
    user_prompt = json.dumps(prompt, indent=2)
    model_response = model.invoke(question_generator(prompt), user_prompt)
    return {"message": model_response}

# @app.post("/question_selector")
# async def select(request: AssessmentRequest):
#     prompt = f"""Department ID: {request.department_id}
#             Function ID: {request.function_id}
#             Role ID: {request.role_id}"""
#     model_response = model.invoke(question_selector(prompt), prompt)
#     return {"message": model_response}

# @app.post("/training_recommender")
# async def recommend(request: AssessmentRequest):
#     prompt = f"""Department ID: {request.department_id}
#             Function ID: {request.function_id}
#             Role ID: {request.role_id}"""
#     model_response = model.invoke(training_recommender(prompt), prompt)
#     return {"message": model_response}