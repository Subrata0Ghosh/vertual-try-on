from flask import *  
import os
import numpy as np
import cv2


app = Flask(__name__)

# file UPLOAD start'

# UPLOAD_FOLDER = os.path.join('static', 'upload')
# app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]

# chack file type
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')  
def home():  
    return render_template("index.html")  

# @app.route('/output')
@app.route('/uploads', methods = ['POST'])  
def uploadImage():  
    if request.method == 'POST':

        # file UPLOAD start'
        UPLOAD_FOLDER = os.path.join('static', 'upload')
        app.secret_key = "secret key"
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
         
        f = request.files['file']
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename) ) # add file in spacific folder
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],'sample_single.png') ) 
        
        f2 = request.files['file2']  
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],f2.filename) )
        f2.save(os.path.join(app.config['UPLOAD_FOLDER'],'d_1.jpg') ) # add file in spacific folder with spacific name        

        IMG_LIST = os.listdir('static/upload')
        IMG_LIST = ['upload/' + i for i in IMG_LIST ] 
        return render_template("index.html", imagelist=IMG_LIST,name = f.filename,name2=f2.filename) 
    else:  
        abort(415)
# file upload end       

# @app.route('/success')
# photo output processing start
@app.route('/process')  
def imageProcess():

    UPLOAD_FOLDER2 = os.path.join('static', 'output')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER2

    frame = cv2.imread('static/upload/sample_single.png')
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

    # cv2.imshow('orignal',frame)
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
    design = cv2.imread('static/upload/d_1.jpg')
    design = cv2.resize(design, mask_black.shape[1::-1])
    # cv2.imshow('design resize',design)

    design_mask_mixed = cv2.bitwise_or(mask_black_3CH,design)
    # cv2.imshow('design_mask_mixed',design_mask_mixed)

    final_mask_black_3CH = cv2.bitwise_and(design_mask_mixed,dst3_wh)
    # cv2.imshow('final_out',final_mask_black_3CH)

    # save output image
    cv2.imwrite("static/output//waka.jpg",final_mask_black_3CH)

    cv2.waitKey(0) 
    cv2.destroyAllWindows()
    
    Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'waka.jpg')
    # return render_template("output.html", imagelist=Flask_Logo )
    resp = make_response(render_template("process.html", imagelist=Flask_Logo ))
    return resp
# return render_template("output.html")
# photo output processing end 

@app.route('/about')  
def about():  
    return render_template("about.html")  

if __name__ == '__main__':  
 app.run(debug = True, port=5000) 
    