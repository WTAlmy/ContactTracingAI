import os
from typing import List, Optional

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from werkzeug.utils import secure_filename

from .worker.celery_app import celery_app

UPLOAD_FOLDER = "/home/test/app/uploads"
ALLOWED_EXTENSIONS = {"mp4", "mov", "mpeg", "webm", "avi", "wmv", "flv"}

app = FastAPI()
templates = Jinja2Templates(directory="/home/test/app/templates")


def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=RedirectResponse)
async def upload_files(files: Optional[List[UploadFile]] = File(...)):
  for uploaded_file in files:
    if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
      file_name = secure_filename(uploaded_file.filename)
      file_path = os.path.join(UPLOAD_FOLDER, file_name)
      with open(file_path, 'wb') as f:
        f.write(await uploaded_file.read())
  return RedirectResponse(url="/success")

@app.post("/{word}")
async def write_root(word: str):
  task_name = "home.test.app.worker.celery_worker.test_celery"
  task = celery_app.send_task(task_name, args=[word])
  print(task)
  return {"message": word}
