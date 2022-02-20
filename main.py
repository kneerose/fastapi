from fastapi import FastAPI,File,UploadFile
from io import BytesIO
from PIL import Image
from warnings import filterwarnings
filterwarnings('ignore')
import numpy as np
import pickle
import mediapipe as mp
import matplotlib.pyplot as plt
from uuid import uuid4

classes_list = ['0. Cut Shot', '1. Cover Drive', '2. Straight Drive',
                '3. Pull Shot', '4. Leg Glance Shot', '5. Scoop Shot']

idx_features = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 53, 55, 56, 57, 58,
                59, 61, 63, 65, 66, 67, 68, 69, 73, 74, 75, 77, 81, 82, 83, 85, 89, 90, 91, 92, 94, 96, 98, 103, 104, 106, 107, 112, 115, 119, 120, 128]

pkl_filename = 'model/shot_classification.pkl'
with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

def read_image(image_encoded):
    print(BytesIO(image_encoded));
    pil_image = Image.open(BytesIO(image_encoded))
    print(pil_image);
    return pil_image


def predict_shot(img):

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils  # For drawing keypoints
    points = mpPose.PoseLandmark  # Landmarks

    data = []
    # img = cv2.imread(path)
    # imageWidth, imageHeight = img.shape[:2]
    # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.array(img)
    print(img);
    results = pose.process(imgRGB)
    print("image");
    print(results)

    # Run this only when landmarks are detected
    if results.pose_landmarks:
        mpDraw.draw_landmarks(imgRGB, results.pose_landmarks, mpPose.POSE_CONNECTIONS,
                              mpDraw.DrawingSpec(
                              color=(245, 117, 66), thickness=2, circle_radius=2),
                              mpDraw.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        landmarks = results.pose_landmarks.landmark
        for i, j in zip(points, landmarks):
            data = data + [j.x, j.y, j.z, j.visibility]
    data = [data[i] for i in idx_features]
    result = int(model.predict([data])[0])
    return result


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