from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
# from predictor import ImageInferencer
import shutil
from ultralytics import YOLO
from PIL import Image
import hashlib
cache = {}
class ImageInferencer:
    def __init__(self):
        # initiate model
        self.model = YOLO("best2.pt")
    
    def __draw_detection(self, results, path):
        for result in results:
            # plot results
            im_array = result.plot()
            # turns BGR to RGB
            im = Image.fromarray(im_array[..., ::-1])
            # save
            im.save(path)
        
    def inference_image(self, path, new_path):
        # inference image
        results = self.model(path)
        
        # plot frame
        plotted_frame = self.__draw_detection(results, new_path)
        print(results)
        
        return plotted_frame

# start engine
app = FastAPI()
model = ImageInferencer()

@app.post("/inference-image")
async def inference_uploaded_image(file: UploadFile = File()):
    # save paths
    path = f"{Path.cwd()}/images/{file.filename}"
    final_path = f"{Path.cwd()}/images/inferenced_{file.filename}"
    
    # save file
    with open(path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    file_hash = hashlib.md5(open(path, 'rb').read()).hexdigest()
    if file_hash in cache:
        return FileResponse(cache[file_hash])
    
    # inference image
    model.inference_image(path, final_path)
    cache[file_hash] = final_path
    
    return FileResponse(final_path)

        
        
    