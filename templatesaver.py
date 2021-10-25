import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import shutil
import random
import sys
import json
import warnings
from error_message import *
from json_to_dataset import JsonToCSV
from datagenerator import DataGenerator
from iou import bb_intersection_over_union

class TemplateSaver(JsonToCSV):
    """ A class to store the matched templates """

    def __init__(self,json_file):
        super().__init__(json_file)

        """
        json_file --> STRING. Json File from LabelMe

        """

        self.json_file=json_file

        # Transform the image to Grayscale
        dt=DataGenerator()
        #self.image=np.asarray(dt.rgb2gray(self.image),dtype=np.uint8)
    
    def cut_template(self,bbox):
        """ Function to cut templates """
        bbox=np.int64(np.ceil(bbox))
        if len(bbox)==2:
            template=self.image[bbox[0][1]:bbox[1][1],bbox[0][0]:bbox[1][0]]
        else:
            template=self.image[bbox[1]:bbox[4],bbox[2]:bbox[3]]
        return template
        
    def save_template(self):
        """ Save the template in jpg format in different folders and create a csv file"""

        self.save = len(self.dataset["label"])!=self.dataset["label"].nunique()

        if not self.save:
            if len(self.json_data['shapes'])==0:
                raise SaveError("No Bounding Box is present in the JSON file.")

            # Raise Warning for saving only default boxes
            warnings.warn("Probably Saving default Boxes. Run CreateJSON for storing all the templates.", DefaultBoxWarning,stacklevel=2)

        path="/".join(self.json_file.split("/")[:-1])+"/"+"templates"
        try:
            x=os.listdir(path)
        except:
            os.mkdir(path)
            
        # Save the template images in template folder
        image_name=self.imagePath.split(".")[0]
        self.image_path=path+"/"+image_name
        

        # Path for the csv
        self.data_path=path+"/"+self.imagePath.split(".")[0]+"/"+image_name+"_dataset.csv"
        # Flatten the bounding boxes
        self.dataset_flatten=self.dataset.copy()
        self.dataset_flatten['bbox']=self.dataset_flatten['bbox'].apply(lambda x: list(np.array(x).flatten()))
        self.dataset_flatten["template_name"]=self.dataset_flatten['image_name']

        
        # Create a template folder
        try:
            os.mkdir(self.image_path)
        except:
            warnings.warn("Image Folder is already present. Replacing it with new folder.",ReplaceWarning,stacklevel=2)
            os.umask(0)
            shutil.rmtree(self.image_path)
            os.mkdir(self.image_path)
        
        all_labels=list(self.dataset_flatten['label'].unique())
        

        for lb in all_labels:
            i=0 #image counter
            boxes=self.dataset[self.dataset['label']==lb]['bbox'].values
            indices=list(self.dataset_flatten[self.dataset_flatten['label']==lb].index)
            for k,bx in enumerate(boxes):
                template=self.cut_template(bx)
                template_name=str(lb)+"_"+str(i)+".jpg"
                template_path=self.image_path+"/"+str(lb)+"/"+template_name
                # if folder isn't created then create a folder and then save
                try:
                    os.mkdir(self.image_path+"/"+str(lb))  
                except:
                    pass
                cv2.imwrite(template_path,template)
                i+=1
                # The original csv has same image name for all templates. Need to change in the new dataset
                self.dataset_flatten.loc[indices[k],"template_name"]=template_name

        # Create separate columns for every bounding box coordinate
        self.dataset_flatten['xmin']=self.dataset_flatten['bbox'].apply(lambda x: x[0])
        self.dataset_flatten['ymin']=self.dataset_flatten['bbox'].apply(lambda x: x[1])
        self.dataset_flatten['xmax']=self.dataset_flatten['bbox'].apply(lambda x: x[2])
        self.dataset_flatten['ymax']=self.dataset_flatten['bbox'].apply(lambda x: x[3])

        del self.dataset_flatten['bbox']
        
        self.dataset_flatten.to_csv(self.data_path,index=False)



if __name__=="__main__":

    if len(sys.argv)<2:
        print("JSON FILE --> The Json directory")
    if len(sys.argv)==2:
        json_file=sys.argv[1]
        ts=TemplateSaver(json_file)
        ts.save_template()
        print(f"CSV SAVED IN {ts.data_path}.")
        print(f"TEMPLATE IMAGES ARE SAVED IN {ts.image_path}.")

