from fastapi import FastAPI, Response, status
import json
import os
import stat
import pwd
import grp
import datetime as dt

app = FastAPI()

roots = {}

with open('config/roots.json') as f:
    roots = json.load(f)["roots"]


@app.get('/')
def index():
    return {"roots": list(roots.keys())}


def file_properties(path: str, file: str):
    props = {}
    result = os.stat(os.path.join(path, file))

    props["filemode"] = stat.filemode(result.st_mode)
    props["size"] = result.st_size
    props["uid"] = pwd.getpwuid(result.st_uid).pw_name
    props["gid"] = grp.getgrgid(result.st_gid).gr_name
    props["ctime"] = dt.datetime.fromtimestamp(result.st_ctime)
    props["atime"] = dt.datetime.fromtimestamp(result.st_atime)
    props["mtime"] = dt.datetime.fromtimestamp(result.st_mtime)

    return props


@app.get('/{root}', status_code=status.HTTP_200_OK)
def list_contents(response: Response, root: str, path: str | None = None):
    contents = {}
    if root in list(roots.keys()):
        full_path = os.path.join(roots[root], path if path else "")
        if os.path.exists(full_path) and os.path.isdir(full_path):
            for f in os.listdir(full_path):
                contents[f] = file_properties(full_path, f)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

    return contents
