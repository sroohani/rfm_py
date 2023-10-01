from fastapi import FastAPI
import json

app = FastAPI()

roots = {}

with open('config/roots.json') as f:
    roots = json.load(f)["roots"]

@app.get('/')
def index():
    return {"roots": list(roots.keys())}
