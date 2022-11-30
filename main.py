import numpy as np
import cv2
from flask import Flask,render_template,request,redirect,url_for
import os

# start flask to get image
app=Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/home/subrata/Desktop/dress try/responsive website for dress try/static/Images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]

from werkzeug.utils import secure_filename

@app.route("/home",methods=["GET","POST"])
def upload_image():
    if request.method=='POST':
        image=request.files['file'] #accessing file
        
        if image.filename=='':  #if file name is empty
            print ('file name invalid')
            return redirect(request.url)
        
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"],filename))

        return render_template("main.html",filename=filename)    
    return render_template("main.html")

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='/Images/'+filename), code=301)

app.run(debug=True,port=2000)
    
# end of flask
"""
# main python code

frame = cv2.imread() 
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert img to img hsv

# define range of green color in HSV/find green color
lower_green = np.array([25, 52, 72])
upper_green = np.array([102, 255, 255])
# Threshold the HSV image to get only blue colors
mask_white = cv2.inRange(hsv,lower_green, upper_green) #def musk for detect color
mask_black = cv2.bitwise_not(mask_white)

#converting mask_black to 3 channels
W,L = mask_black.shape
mask_black_3CH = np.empty((W, L, 3), dtype=np.uint8)
mask_black_3CH[:, :, 0] = mask_black
mask_black_3CH[:, :, 1] = mask_black
mask_black_3CH[:, :, 2] = mask_black

cv2.imshow('orignal',frame)
# cv2.imshow('mask_black',mask_black_3CH)

dst3 = cv2.bitwise_and(mask_black_3CH,frame)
# cv2.imshow('Pic+mask_inverse',dst3)

#///////
W,L = mask_white.shape
mask_white_3CH = np.empty((W, L, 3), dtype=np.uint8)
mask_white_3CH[:, :, 0] = mask_white
mask_white_3CH[:, :, 1] = mask_white
mask_white_3CH[:, :, 2] = mask_white

# cv2.imshow('Wh_mask',mask_white_3CH)
dst3_wh = cv2.bitwise_or(mask_white_3CH,dst3)
# cv2.imshow('Pic+mask_wh',dst3_wh)

#/////////////////

# changing for design
design = cv2.imread('d_1.jpg')
design = cv2.resize(design, mask_black.shape[1::-1])
# cv2.imshow('design resize',design)

design_mask_mixed = cv2.bitwise_or(mask_black_3CH,design)
# cv2.imshow('design_mask_mixed',design_mask_mixed)

final_mask_black_3CH = cv2.bitwise_and(design_mask_mixed,dst3_wh)
cv2.imshow('final_out',final_mask_black_3CH)


cv2.waitKey(0) 
cv2.destroyAllWindows()

"""