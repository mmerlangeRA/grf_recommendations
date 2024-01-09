from utils.core import load_model_and_dataset, save_model_and_dataset, build_recommender, make_recommendations
import ssl
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

""" ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/cert.pem', keyfile='/key.pem') """
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


@app.get("/hello")
async def root():
    return {"message": "Hello World"}

@app.get("/recommendations/{visitor_id}")
async def get_recos(visitor_id):
   try:
    df,model,dataset = load_model_and_dataset(model_name)
    print(visitor_id)
    recos = make_recommendations(model,dataset,visitor_id)
    urls = [rec[0] for rec in recos]
    json_str = json.dumps(urls)
    return json_str
   except Exception as e:
      raise HTTPException(status_code=404, detail="Visitor not found")

