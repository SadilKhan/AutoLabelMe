from tkinter import *
import numpy as np
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
from platform import system
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk,Image,ImageDraw
from templatematcher import TemplateMatcher
from templatesaver import TemplateSaver
import os
import shutil
import random
import sys
import json
import webbrowser
import warnings
import colorsys
platformD = system()
if platformD == 'Darwin':
    from tkmacosx import Button



CUR_DIR=os.curdir

class GUI():

    def __init__(self):
        # Create a gui
        self.root=Tk()
        self.root.title("Auto Image Annotator")
        self.root.geometry("2500x1600")

        # Menu
        self.menu()

        # Frame

    def menu(self):
        # Main menu bar
        self.my_menu=Menu(self.root)

        # File Menu
        self.file_menu=Menu(self.my_menu)
        self.my_menu.add_cascade(label="File",menu=self.file_menu)
        self.file_menu.add_command(label="Open JSON",command=self.open_json_file)
        self.file_menu.add_command(label="Restart",command=self.restart)
        self.file_menu.add_command(label="Exit",command=self.quit)

        # Edit Menu
        self.edit_menu=Menu(self.my_menu)
        self.my_menu.add_cascade(label="Edit",menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo",state=DISABLED)

        # Help Menu
        self.help_menu=Menu(self.my_menu)
        self.my_menu.add_cascade(label="Help",menu=self.help_menu)
        self.help_menu.add_command(label="About AutoLabelme",command=self.open_help)

        self.root.config(menu=self.my_menu)
    def open_help(self):
        webbrowser.open("https://github.com/SadilKhan/internship-hubert-curien-2021/tree/main/Data%20Generation")
    
    def frame(self,image):
        self.image_frame=Frame(self.root,width=1600,height=1000)
        self.my_image=ImageTk.PhotoImage(image)
        self.label=Label(self.image_frame,image=self.my_image)
        self.image_frame.place(x=10,y=10)
        self.label.place(x=11,y=11)
    def frame_all(self,image):
        self.image_frame_all=Frame(self.root,width=1600,height=1000)
        self.my_image_all=ImageTk.PhotoImage(image)
        self.label_all=Label(self.image_frame_all,image=self.my_image_all)
        self.image_frame_all.place(x=1050,y=420)
        self.label_all.place(x=11,y=11)
        
        
    def restart(self):
        self.image_frame_all.place_forget()
        self.save_button.place_forget()
        self.save_img_button.place_forget()
        self.image_frame.place_forget()
        self.less_button.place_forget()
        self.more_button.place_forget()
        self.show_button.place_forget()
        self.next_button.place_forget()
        self.prev_button.place_forget()
        self.correction_button.place_forget()
        self.add_button.place_forget()
        self.label.place_forget()
        self.label_for_search.place_forget()
        self.label_min.place_forget()
        self.label_max.place_forget()
        self.label_search.place_forget()
        self.entry_min.place_forget()
        self.entry_max.place_forget()
        self.search_space_entry.place_forget()
 
    
    def quit(self):
        message=messagebox.askyesno("My Popup","Do you want to exit?")
        if message:
            self.root.quit()
    
    def less_boxes(self):
        label=self.all_labels[self.label_no]
        # Increasing the threshold will result in less boxes
        threshold=self.all_threshold[label]+0.05
        self.all_threshold[label]=threshold
        self.all_boxes[label],self.all_box_dict[label]=self.tm.match_template(label,threshold,self.search_space,self.rotation_min,self.rotation_max,True)
        
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((1000,1000),Image.ANTIALIAS)
        img=ImageDraw.Draw(image)
        for bx in self.all_boxes[label]:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="blue")
            elif "_rotated_" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="green")
            else:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="red")
        self.image_frame.place_forget()
        self.image_frame_all.place_forget()
        self.frame(image)
        self.button()
        self.prev_button["state"]=NORMAL
        #self.start_button["state"]=DISABLED
        self.show_all_boxes()
        
    
    def more_boxes(self):
        label=self.all_labels[self.label_no]
        # Decreasing the threshold will result in more boxes
        threshold=self.all_threshold[label]-0.05
        self.all_threshold[label]=threshold
        self.all_boxes[label],self.all_box_dict[label]=self.tm.match_template(label,threshold,self.search_space,self.rotation_min,self.rotation_max,True)
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((1000,1000),Image.ANTIALIAS)
        img=ImageDraw.Draw(image)
        for bx in self.all_boxes[label]:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="blue")
            elif "rotated" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="green")
            else:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="red")
        self.image_frame.place_forget()
        self.image_frame_all.place_forget()
        self.frame(image)
        self.button()
        self.prev_button["state"]=NORMAL
        #self.start_button["state"]=DISABLED
        self.show_all_boxes()

    def check_boxes_label(self,label):
        """ Check if all the labels are flipped, mirrored or not"""
        bx=self.all_boxes[label]
        box_dict=self.all_box_dict[label]
        nbx=len(bx)
        n_flipped=0
        n_mirrored=0
        for i in bx:
            if "flipped" == box_dict[(i[0][0],i[0][1])][2].split("_")[-1]:
                n_flipped+=1
            if "mirrored" in box_dict[(i[0][0],i[0][1])][2].split("_")[-1]:
                n_mirrored+=1
        if n_flipped==nbx or n_mirrored==nbx:
            new_label="_".join(box_dict[(i[0][0],i[0][1])][2].split("_")[:-1])
            return True,new_label
        return False,None
   
    def save(self):
        """ A class to transform JSON or CSV file to LabelMe JSON format """

        # Since the file is saved, self.save is True
        self.saved=True

        # Store all the keys.
        keys=self.jsondata.keys()

        # Store all the labels from all_boxes
        labels=list(self.all_boxes.keys())

        # Get all the colors
        shapes=self.jsondata['shapes']

        # Outline for boxes
        colors=dict()
        for i in range(len(labels)):
            color=self.tm.random_color(int(labels[i]))
            #color=[int(i) for i in color]
            colors[labels[i]]=color
        
        self.jsondata['shapes']=[]

        # Append all the all boxes.
        for lb in labels:
            try:
                # if all the boxes are of flipped category, change it to normal
                all_flipped,new_label=self.check_boxes_label(lb)
                print(len(self.all_boxes[lb]))
                for bx in self.all_boxes[lb]:
                    # A temporary Dictionary
                    temp=dict()
                    if not all_flipped:
                        temp['label']=self.imagePath.split("/")[-1].split(".")[0]+"_"+self.all_box_dict[lb][tuple(bx[0])][2]
                    else:
                        temp["label"]=self.imagePath.split("/")[-1].split(".")[0]+"_"+new_label
                    temp['line_color']=colors[lb]
                    temp['fill_color']=None
                    bx=[[int(bx[0][0]),int(bx[0][1])],[int(bx[1][0]),int(bx[1][1])]]
                    temp['points']=bx
                    temp['shape_type']="rectangle"
                    self.jsondata['shapes'].append(temp)
            except:
                print("Something Went Wrong during saving")
        
        # Store the json file.
        self.json_file_name=self.root.filename.split(".")[0]+"_matched.json"
        with open(self.json_file_name, 'w+') as fp:
            json.dump(self.jsondata, fp,indent=2)
        print("JSON FILE SAVED. REOPEN THE JSON FILE IN LABELME. ",self.json_file_name)
    
    def matching_window(self):
        if self.label_no<0:
            self.label_no=0
        label=self.all_labels[self.label_no]
        threshold=self.all_threshold[label]
        self.all_boxes[label],self.all_box_dict[label]=self.tm.match_template(label,threshold,self.search_space,self.rotation_min,self.rotation_max,True)
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((1000,1000),Image.ANTIALIAS)
        img=ImageDraw.Draw(image)
        for bx in self.all_boxes[label]:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="blue")
            elif "_rotated_" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="green")
            else:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="red")
        self.image_frame.place_forget()
        self.image_frame_all.place_forget()
        self.frame(image)
        self.button()
        if self.label_no+1==len(self.all_labels):
            self.next_button["state"]=DISABLED
        elif self.label_no==0:
            self.prev_button["state"]=DISABLED
        self.show_all_boxes()
        

    def next_matching(self):
        # Change the Search spaces and rotations to default value
        self.search_space=2
        self.rotation_min=None
        self.rotation_max=None

        self.label_no+=1
        label=self.all_labels[self.label_no]
        if len(self.all_boxes[label])==0:   
            threshold=self.all_threshold[label]
            self.all_threshold[label]=threshold
            self.all_boxes[label],self.all_box_dict[label]=self.tm.match_template(label,threshold,self.search_space,self.rotation_min,self.rotation_max,True)
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((1000,1000),Image.ANTIALIAS)
        img=ImageDraw.Draw(image)
        for bx in self.all_boxes[label]:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="blue")
            elif "rotated" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="green")
            else:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="red")
        self.image_frame.place_forget()
        self.image_frame_all.place_forget()
        self.frame(image)
        self.button()
        self.prev_button["state"]=NORMAL
        #self.start_button["state"]=DISABLED
        # Disable the next button if there are no more labels
        if self.label_no+1==len(self.all_labels):
            self.next_button["state"]=DISABLED 
        if self.label_no==0:
            self.prev_button["state"]=DISABLED
        self.show_all_boxes()

    def prev_matching(self):
        # Change the Search spaces and rotations to default value
        self.search_space=2
        self.rotation_min=None
        self.rotation_max=None
        self.show_all_boxes()

        self.label_no-=1
        label=self.all_labels[self.label_no]
        if len(self.all_boxes[label])==0:   
            threshold=self.all_threshold[label]
            self.all_threshold[label]=threshold
            self.add()
            self.all_boxes[label],self.all_box_dict[label]=self.tm.match_template(label,threshold,self.search_space,self.rotation_min,self.rotation_max,True)
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((1000,1000),Image.ANTIALIAS)
        img=ImageDraw.Draw(image)
        for bx in self.all_boxes[label]:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="blue")
            elif "rotated" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="green")
            else:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="red")
        self.image_frame.place_forget()
        self.image_frame_all.place_forget()
        self.frame(image)
        self.button()
        
        # Disable the next button if there are no more labels
        if self.label_no!=0:
            self.prev_button["state"]=NORMAL
        self.show_all_boxes()

        #self.start_button["state"]=DISABLED


    
    def save_img(self):
        ts=TemplateSaver(self.json_file_name)
        ts.save_template()
        print(f"CSV SAVED IN {ts.data_path}.")
        print(f"TEMPLATE IMAGES ARE SAVED IN {ts.image_path}.")
    
    def show_all_boxes(self):
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((400,400),Image.ANTIALIAS)
        img=ImageDraw.Draw(image,"RGBA")
        for lb in self.all_labels:
            if len(self.all_boxes[lb])!=0:
                for bx in self.all_boxes[lb]:
                    flip=False
                    rotated=False
                    bx=np.array(bx).reshape(-1)
                    if "flipped" in self.all_box_dict[lb][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[lb][(bx[0],bx[1])][2]:
                        flip=True
                    if "rotated" in self.all_box_dict[lb][(bx[0],bx[1])][2]:
                        rotated=True
                    bx=bx*np.array([400])/np.array([w,h,w,h])
                    bx=tuple(bx)
                    if flip:
                        img.rectangle(bx,outline="white",fill=(0,0,255,100))
                    elif rotated:
                        img.rectangle(bx,outline="white",fill=(0,255,0,100))
                    else:
                        img.rectangle(bx,outline="white",fill=(255,0,0,100))
        self.frame_all(image)

    def correction(self):
        """ Correct Labels for boxes. If any box has been misclassfied as flipped then this will fix it"""
        label=self.all_labels[self.label_no]
        all_boxes=self.all_boxes[label]
        for bx in all_boxes:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2] or "mirrored" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                x1,x2,x3=self.all_box_dict[label][(bx[0],bx[1])]
                x3="_".join(x3.split("_")[:-1])
                self.all_box_dict[label][(bx[0],bx[1])]=(x1,x2,x3)
        # Plot the image with the bounding boxes
        image=Image.fromarray(self.tm.original_image.copy())
        w,h=image.width,image.height
        image=image.resize((1000,1000),Image.ANTIALIAS)
        img=ImageDraw.Draw(image)
        for bx in self.all_boxes[label]:
            bx=np.array(bx).reshape(-1)
            if "flipped" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="blue")
            elif "rotated" in self.all_box_dict[label][(bx[0],bx[1])][2]:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="green")
            else:
                bx=bx*np.array([1000])/np.array([w,h,w,h])
                bx=tuple(bx)
                img.rectangle(bx,outline="red")
        self.image_frame_all.place_forget()
        self.image_frame.place_forget()
        self.frame(image)
        self.button()
        if self.label_no>0:
            self.prev_button["state"]=NORMAL
        self.show_all_boxes()
    
    def left(self,event):
        if self.label_no>=0:
            self.prev_matching()

    def right(self,event):
        if self.label_no<len(self.all_labels):
            self.next_matching()  
    def rematch(self,event):
        self.add() 

    def rotation_entry(self):
        self.label=Label(self.root,text="Rotation Range",fg="black")
        self.label_for_search=Label(self.root,text="Search Space",fg="black")
        self.label_min=Label(self.root,text="Min",fg="black")
        self.label_max=Label(self.root,text="Max",fg="black")
        self.label_search=Label(self.root,text="Value",fg="black")
        self.entry_min=Entry(self.root,width=20)
        self.entry_max=Entry(self.root,width=20)
        self.search_space_entry=Entry(self.root,width=20)
        
        self.label.place(x=1050,y=180)
        self.label_min.place(x=1020,y=200)
        self.entry_min.place(x=1050,y=200)     
        self.entry_max.place(x=1050,y=230)
        self.label_max.place(x=1020,y=230)
        self.label_for_search.place(x=1050,y=260)
        self.label_search.place(x=1020,y=280)
        self.search_space_entry.place(x=1060,y=280)
    
    def add(self):
        try:
            self.rotation_min=int(self.entry_min.get())
        except:
            self.rotation_min=None
            
        try:
            self.rotation_max=int(self.entry_max.get())
        except:
            self.rotation_max=None

        try:
            self.search_space=int(self.search_space_entry.get())
        except:
            self.search_space=2
        self.entry_min.delete(0,END)
        self.entry_max.delete(0,END)
        self.search_space_entry.delete(0,END)

        self.matching_window()



    def button(self):
        #self.start_button=Button(self.root,text="Start Matching",fg="black",command=self.matching_window,disabledforeground="black")
        self.next_button=Button(self.root,text="Next Line >>",fg="black",command=self.next_matching,disabledforeground="black")
        self.prev_button=Button(self.root,text="<< Previous Line",fg="black",command=self.prev_matching,disabledforeground="black",
        state=DISABLED)
        self.less_button=Button(self.root,text="-",fg="black",command=self.less_boxes)
        self.show_button=Button(self.root,text="Show all boxes",fg="black",command=self.show_all_boxes)
        #self.refine_button=Button(self.root,text="Resize Boxes",fg="black",command=self.less_boxes)
        #self.finer_resize_button=Button(self.root,text="Finer Resize Boxes",fg="black",command=self.finer_less_boxes,padx=100)
        self.more_button=Button(self.root,text="+",fg="black",command=self.more_boxes)
        self.save_button=Button(self.root,text="Save JSON",fg="black",command=self.save,disabledforeground="black",padx=125)
        self.save_img_button=Button(self.root,text="Save Images",fg="black",command=self.save_img,disabledforeground="black",padx=120)
        self.correction_button=Button(self.root,text="Correct Label",fg="black",command=self.correction,padx=120)
        self.add_button=Button(self.root,text="Rematch",fg="black",command=self.add)
        
        #self.start_button.place(x=1150,y=100)
        self.next_button.place(x=1270,y=50)
        self.prev_button.place(x=1050,y=50)
        self.less_button.place(x=1050,y=100)
        #self.refine_button.place(x=1150,y=150)
        self.more_button.place(x=1280,y=100)
        #self.finer_resize_button.place(x=1050,y=200)
        self.save_button.place(x=1050,y=350)
        self.save_img_button.place(x=1050,y=380)
        self.correction_button.place(x=1050,y=130)
        self.add_button.place(x=1050,y=320)

        # Rotation Entry
        self.rotation_entry()
    def create_descriptor(self,value):
        # Split the string containing label and metadata
        values=value.split(" ")

        # Store the metadata in the dicttionary
        metadata=' '.join(values[1:])

        # If we have duplicate label and different information then we need to save the info in a list for the same label key
        name=self.tm.imagePath.split("/")[-1].split(".")[0]+"_"+str(values[0])
        try:
            self.descriptor[name].append(metadata)
        except:
            self.descriptor[name]=[metadata]
        
        return values[0]

    def open_json_file(self):
        self.root.filename=filedialog.askopenfilename(initialdir=CUR_DIR,
        title="Select A File",filetypes=(("JSON Files","*.json"),
        ("All Files","*.*")))
        self.tm=TemplateMatcher(self.root.filename)
        # JSON data\
        self.jsondata=self.tm.labelmeData
        # ImagePath
        self.imagePath=self.tm.imagePath
        # All labels
        self.all_labels=list(self.tm.data['label'].unique())
        # Store the descriptor 
        self.descriptor=dict()
        for num,lb in enumerate(self.all_labels):
            self.all_labels[num]=self.create_descriptor(lb)
        
        self.descriptor_name=self.tm.json_file.split(".")[0]+"_descriptor.json"
        with open(self.descriptor_name, 'w+') as fp:
            json.dump(self.descriptor, fp,indent=2)
        
        #self.all_labels=list(self.descriptor.keys())

        """self.all_labels=sorted([int(i) for i in self.all_labels])
        self.all_labels=[str(i) for i in self.all_labels]"""
        # All the images are saved for every labels 
        self.all_images=[]
        # All the boxes are saved for every labels
        self.all_boxes=dict()
        for lb in self.all_labels:
            self.all_boxes[lb]=[]
        
        # All the metadata about the box
        self.all_box_dict=dict()
        for lb in self.all_box_dict:
            self.all_box_dict[lb]=[]
        # All the thresholds are saved for every labels
        self.all_threshold=dict()
        for lb in self.all_labels:
            self.all_threshold[lb]=0.45
        
        # INITIALISATION
        self.label_no=-1
        self.search_space=2
        self.rotation_min=None
        self.rotation_max=None


        # Plot the image and the button.
        image=Image.fromarray(self.tm.original_image.copy())
        image=image.resize((1000,1000),Image.ANTIALIAS)
        self.frame(image)
        self.button()
        self.show_all_boxes()
        self.root.bind("<Left>",self.left)
        self.root.bind("<Right>",self.right)
        self.root.bind("<Return>",self.rematch)

        # For rotation Entry
        self.rotation_entry()
        
        


    
if __name__=="__main__":
    gui=GUI()
    gui.root.mainloop()
