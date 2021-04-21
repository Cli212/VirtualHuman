from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import pandas as pd
import requests
import wget
import json
import wget

from cdqa.pipeline import QAPipeline

app = Flask(__name__)
CORS(app)

print("Started main.py !!!")

#print("Fetching original file from google docs")
#response = requests.get('https://docs.google.com/uc?export=download&id=1oSUFKZMao_gQxGDpCZuRXV6EULjFjmoZ')
#sapiens_original = response.json()

print("Fetching original file from folder level")
with open('./sapiens_original.json', 'r') as file:
  sapiens_original = json.load(file)

#print("Fetching annotated file from google docs")
#response = requests.get('https://docs.google.com/uc?export=download&id=1mf5CajTUX6mUhmazSsTK7G63Sm_RDXbk')
#sapiens_annotated = response.json()
#with open('./sapiens_annotated.json', 'w') as file:
#  json.dump(sapiens_annotated, file)

dictionary_df = []

for item in sapiens_original['data']:
  title = item['title']
  paragraphs = []

  for paragraph in item['paragraphs']:
    paragraphs.append(paragraph['context'])
  
  dictionary_df.append({'title':title, 'paragraphs':paragraphs})

df = pd.DataFrame(dictionary_df)

# Get original Bert_qa and then train on our annotated dataset
#wget.download(url='https://github.com/cdqa-suite/cdQA/releases/download/bert_qa/bert_qa.joblib', out='./')
#cdqa_pipeline = QAPipeline(reader='./bert_qa.joblib')
#cdqa_pipeline.fit_retriever(df=df)
#cdqa_pipeline.fit_reader('./sapiens_annotated.json')

#print("Use the pretrained annotated distilbert file")
#wget.download(url='https://github.com/Rathore25/SapiensAI/raw/main/Pretrained Data/sapiens_distilbert.joblib', out='./')
#cdqa_pipeline = QAPipeline(reader='./sapiens_distilbert.joblib')
#cdqa_pipeline.fit_retriever(df=df)

print("Using the local pretrained file for local server")
cdqa_pipeline = QAPipeline(reader='./sapiens_bert.joblib')
cdqa_pipeline.fit_retriever(df=df)

@app.route("/api", methods=["GET"])
def api():

    query = request.args.get("query")
    prediction = cdqa_pipeline.predict(query=query)

    return jsonify(
        query=query, answer=prediction[0], title=prediction[1], paragraph=prediction[2], score=prediction[3]
    )

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to Sapiens AI server !!</h1>"