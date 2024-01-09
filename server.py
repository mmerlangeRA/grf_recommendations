from utils.core import get_article_details, load_model_and_dataset, make_recommendations_article, save_model_and_dataset, build_recommender, make_recommendations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = "output"

class RecoRequest(BaseModel):
    dataset_url: str
    visitor_id: str


@app.get("/health")
async def root():
    return {"message": "Up and running"}

@app.get("/recommendations/{visitor_id}")
async def get_recos(visitor_id):
   try:
    df,model,dataset = load_model_and_dataset(model_name)
    recommended_article_ids = make_recommendations_article(model,dataset,visitor_id)
    recommendations= [get_article_details(article_id) for article_id in recommended_article_ids]
    json_str = json.dumps(recommendations)
    return json_str
   except Exception as e:
      raise HTTPException(status_code=404, detail="Visitor not found")