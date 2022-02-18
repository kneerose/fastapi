import uvicorn
from fastapi import FastAPI,File,UploadFile
from numpy import imag
from readImage import  predict_shot, read_image
from uuid import uuid4
from warnings import filterwarnings
filterwarnings('ignore')

app = FastAPI()

@app.get("/")
def readroot():
    return {"ping":"pong"}

@app.post("/files/",tags=["imageupload"])
async def upload_file(file:UploadFile):
    # read image file
     image = read_image(await file.read())
     result_shot= predict_shot(image)
     result_eff = "Unknown"
     return {"PredictedShot": result_shot, "Efficiency": result_eff}

@app.get("/shotname",tags=["shots"])
def get_name():
     return {"Shots":[{
         "0":"Cut Shot"},{"1":"Cover Drive"},{"2":"Straight Drive"},{"3":"Pull Shot"},{"4":"Leg Glance Shot"},{"5":"Scoop Shot"}]}

@app.get("/uuid",tags=["Token generate"])
def get_token():
     return {
        "token":str(uuid4())
     }

if __name__ == "__main__":
    uvicorn.run(app, debug=True)