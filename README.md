# AutoLabelMe
AutoLabelme is an open-source automatic image annotator created using the Tkinter library in Python. It's an extension of LabelMe, the open-source Image Annotator available in Github LabelMe. It matches the template provided by the user in an image and find same objects associating a bounding box and label for every object. Autolabelme uses Normalized Cross-Correlation to check whether two templates are similar. It is designed keeping in mind with the necessity of creating dataset for object detection purposes and currently can only find objects in the cropped image i.e the search space to find same object is the space around the current template.

# How to Run?
1. Open `Terminal`.
2. `labelme` or `python3 /path/to/labelme.py`. Check [here](https://github.com/wkentaro/labelme) for more details.
3. Create one bounding box per label.
4. Run AutoLabelme.py ` python3 /path/to/AutoLabelme.py`.
5. Open JSON and press `Next Line >>` for starting to match.
6. The Left Image will show the boxes for current Label. The smaller right image is for showing all the templates.
7. Press `<< Previous Line` for viewing the matched boxes for the previous label.
8. Press `+` for more boxes and `-` for less boxes or box repositioning.
9. If you have rotated image, fill the rotation range or just enter `min` value. For example `min=45` and `max=90` will give `list(range(45,94,5))` values or just enter `min=45` which will only rotate the image once (45 degree).
10. The `search space value` **is by default 2** which means the algorithm will check for the templates from two heights up to two heights down in the original image. Choose any value from 1 to 15. For example if your template starts from `(200,200)` and height and width is 100 and 100 respectively and search space=2, the algorithm will search for the template from `(:,0)` to `(:,400)` in the image. If you select more than 15 than it's just `heights-the value`. For example, if you choose 100 in the previous example, the it will be `(:,100)` to `(:,300)` where the templates will be searched in the image. In any case, value from 1 to 15 is sufficient.
11. Press `Rematch` button or Press `Enter` or `Return` in your keyboard.
12. (Optional) Sometimes if the template is symmetric, the algorithm picks up some templates as flipped, to fix this, press `Correct Label`.
13. Press  `Save JSON` to save a json file.
14. Open the saved json file in Labelme. Labelme will show the matched templates. Edit it if necessary.
15. Press `Save Images` in AutoLabelme if all the boxes are okay. This will save the matched templates in JPEG.

## Function of every buttons:
1. `Next Line >>`: Template matching for next label
2. `<< Previous Line`: Template Matching for the previous label
3. `-`: Increases the threshold which results in less number of boxes.
4. `+`: Decreases the threshold which results in more number of boxes.
5. `Save JSON`: Saves a JSON file which can be read by LabelMe for further edits.
6. `Save Images`: Save the cropped vignettes from the image
7. `min`: The minimum value for Rotation.
8. `max`: The maximum value for Rotation.
9. `Rematch`: Match again for current label.
10. `Correct Label`: Transform all the boxes to red boxes(no flip).

## Libraries Needed

1. Numpy (`pip install numpy`)
2. OpenCV(`pip install opencv-python`)
3. PIL (`pip install pillow`)
4. tkinter (`pip install tk`)
5. colorsys (`pip install colorsys`)
6. tkmacosx (`pip install tkmacosx`) --> (ONLY FOR MAC USERS)
7. labelme (`pip install labelme`)[WINDOWS/LINUX] (`brew install labelme`)[MAC]

## The Other Py files
1. `templatematcher.py` --> Matches templates for specified labels or all the labels. Requires JSON file created using Labelme.
2. `templatesaver.py`--> Saves the matched images.

