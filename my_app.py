import uvicorn, os, json
# Trigger reload
from os import environ as env
from fastapi import FastAPI, Response, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from view.parameters import MAIL_VALIDATION
from detect import predict_image, YOLO

# Middleware
from system.middleware import RequestLoggerMiddleware
import re

# Building
APP_VERSION="0.0.1"

app = FastAPI()

print(f"Test API Build is running!")

# Add the middleware to the app
app.add_middleware(RequestLoggerMiddleware)

templates = Jinja2Templates(directory="templates")

# MAIN
@app.get('/', response_class=HTMLResponse)
def hello(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "version": APP_VERSION})

@app.post("/vision-detect")
def vision_detect(file: UploadFile = File(...)):
    contents = file.file.read()
    
    detections = predict_image(contents)

    return JSONResponse(content={"detections": detections}, status_code= 200)


@app.post("/check-email")
def check_email(secret:str, params:MAIL_VALIDATION):

    input_email = params.email

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", input_email):
        return JSONResponse(content={"email": input_email, "is_valid": "false"}, status_code=200)

    return JSONResponse(content={"email": input_email, "is_valid": "true"}, status_code=200)

@app.route("/{catch_all:path}", methods=["GET","POST"])
def not_found(catch_all):
    raise HTTPException(status_code=404, detail="Page not found")

@app.exception_handler(HTTPException)
def handle_http_exception(request, exc):
    return Response(
        media_type="text/html",
        status_code=exc.status_code,
        content="Page not found",
    )

if __name__ == '__main__':
    uvicorn.run(app)
