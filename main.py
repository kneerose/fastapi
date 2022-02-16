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
     return {"predict shot":"Cut Shot","efficiency":"90%"}

@app.get("/shotname",tags=["shots"])
def get_name():
     return {"Shots":[{
         "1":"Cut Shot"},{"2":"Cover Drive"},{"3":"Straight Drive"},{"4":"Scoop"},{"5":"Leg Glance"},{"6":"Pull Shot"}]}


if __name__ == "__main__":
    uvicorn.run(app, debug=True)