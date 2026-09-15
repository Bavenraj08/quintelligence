from fastapi import FastAPI
from model_instruction import question_generator, question_selector, training_recommender
from pydantic import BaseModel
import model

app = FastAPI()

class AssessmentRequest(BaseModel):
    department_id: str
    function_id: str
    role_id: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/question_generator")
async def generate(request: AssessmentRequest):
    prompt = f"""Department ID: {request.department_id}
            Function ID: {request.function_id}
            Role ID: {request.role_id}"""
    model_response = model.invoke(question_generator(prompt), prompt)
    return {"message": model_response}

@app.post("/question_selector")
async def select(request: AssessmentRequest):
    prompt = f"""Department ID: {request.department_id}
            Function ID: {request.function_id}
            Role ID: {request.role_id}"""
    model_response = model.invoke(question_selector(prompt), prompt)
    return {"message": model_response}

@app.post("/training_recommender")
async def recommend(request: AssessmentRequest):
    prompt = f"""Department ID: {request.department_id}
            Function ID: {request.function_id}
            Role ID: {request.role_id}"""
    model_response = model.invoke(training_recommender(prompt), prompt)
    return {"message": model_response}