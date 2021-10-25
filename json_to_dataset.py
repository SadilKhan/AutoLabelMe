import sys
import os
import io
import base64
import PIL.ExifTags
import PIL.Image
import PIL.ImageOps
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd


class JsonToCSV:
   # A class to transfom JSON file to CSV containing Image boundaries

    def __init__(self,json_file):

        self.json_file=json_file

        # Read The JSON File
        self.json_data= json.load(open(self.json_file))
        self.imageData=self.json_data.get("imageData") # Contains the Image
        self.imagePath=self.json_data.get("imagePath").split("/")[-1] # Contains the Image Name
        self.length=len(self.json_data.get('shapes')) # Total number of bounding boxes

        # To obtain the Image
        self.image=self.img_b64_to_arr()

        # To obtain the DataFrame containing labels and bounding boxes
        self.dataset=self.get_dataframe()


    def img_data_to_pil(self,img_data):
        f = io.BytesIO()
        f.write(img_data)
        img_pil = PIL.Image.open(f)
        return img_pil


    def img_data_to_arr(self,img_data):
        img_pil = self.img_data_to_pil(img_data)
        img_arr = np.array(img_pil)
        return img_arr
    
    def img_b64_to_arr(self):
        img_data = base64.b64decode(self.imageData)
        img_arr = self.img_data_to_arr(img_data)
        return img_arr 

    def get_dataframe(self):
        bbox=[] # Bounding Boxes
        labels=[] # Labels
        
        for i in range(self.length):
            labels.append(self.json_data.get("shapes")[i]['label'])
            bbox.append(self.json_data.get("shapes")[i]['points'])
        
        dataset=pd.DataFrame({"image_name":[self.imagePath]*self.length,"bbox":bbox,"label":labels})
        return dataset

    def plot_image(self):
        plt.imshow(self.image)
        
        """for bx in bboxes:
            transormed_bboxes.append([bx[0][0],bx[0][0],bx[1][0],bx[1][0],bx[0][0]])"""

    def plot_image_bounding_box(self,label="all",figsize=(20,20),color='red',save=False,name=None):
        print(f"Argument: label={label},figsize={figsize},color={color},save={save},name={name}")
        if label=="all":
            points=self.dataset['bbox']
        else:
            points=self.dataset['bbox'][self.dataset['label']==label]
        
        fig,ax=plt.subplots(figsize=figsize)
        ax.imshow(self.image)

        for p in points:
            rect=Rectangle(p[0],p[1][0]-p[0][0],p[1][1]-p[0][1],edgecolor=color,facecolor='none')
            ax.add_patch(rect)
        plt.show()
        if save:
            fig.savefig(name,dpi=90)



if __name__=="__main__":
    j2csv=JsonToCSV('/Users/ryzenx/Documents/Internship/Dataset/image1.json')
    

