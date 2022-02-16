import uvicorn
from fastapi import FastAPI,File,UploadFile
from numpy import imag
from readImage import  read_image

app = FastAPI()

@app.get("/")
def readroot():
    return {"ping":"pong"}

@app.post("/files/",tags=["imageupload"])
async def upload_file(file:UploadFile):
    # read image file
     image = read_image(await file.read())
    # after processing
    # image = preprocess(imag)
     return {"image":""}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)