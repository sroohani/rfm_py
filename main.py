from fastapi import FastAPI, Response, status
import json
import os

app = FastAPI()

roots = {}

with open('config/roots.json') as f:
    roots = json.load(f)["roots"]

@app.get('/')
def index():
    return {"roots": list(roots.keys())}

@app.get('/{root}', status_code=status.HTTP_200_OK)
def list_contents(response: Response, root: str, path: str | None = None):
    contents = []
    if root in list(roots.keys()):
        full_path = os.path.join(roots[root], path if path else "")
        if os.path.exists(full_path) and os.path.isdir(full_path):
            contents = os.listdir(full_path)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

    print(len(contents))
    return contents
