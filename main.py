from PIL import Image
import requests
import shutil
import os
import cv2 as cv
import numpy as np
from fastapi import FastAPI,Request

def download_picture(url):
    # check to see if images folder exists
    path = 'images/'
    if os.path.exists(path) == False:
        os.mkdir(path)

    # get the image from the url
    response = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    response.raw.decode_content = True

    # save the image
    with open('images/{}'.format(file_name), 'wb') as pic:
        shutil.copyfileobj(response.raw, pic)

    return file_name


# TODO merge chck_pic_aspct_ratio and chekc_pic_size
def chck_pic_aspct_ratio(pic_path):
    img = Image.open('images/{}'.format(pic_path))
    width = img.width
    height = img.height

    # we prefer aspect ratios that are closer to a square
    if width / height > 4 / 3 or height / width > 4 / 3:
        return {'reason':'bad aspect ratio','score':'bad'}
    else:
        return {'reason':'good aspect ratio','score':'good'}


def chck_pic_size(pic_path):
    img = Image.open('images/{}'.format(pic_path))
    width = img.width
    height = img.height

    # prefer images that are bigger than 200*200
    if width < 200 or height < 200:
        return {'reason':'bad pic size','score':'bad'}
    else:
        return {'reason':'good pic size','score':'good'}


# TODO find a better model
def chck_pic_watermark(pic_path):
    pass


THRESHOLD_INTENSITY = 230

# TODO merge has_white_background and chck_margin
#check to see if the image has a white bg
def has_white_background(img):
    # Read image into org_img variable
    org_img = cv.imread(img, cv.IMREAD_GRAYSCALE)

    # Create a black blank image for the mask
    mask = np.zeros_like(org_img)

    # Create a thresholded image, I set my threshold to 200 as this is the value
    # I found most effective in identifying light colored object
    _, thres_img = cv.threshold(org_img, 200, 255, cv.THRESH_BINARY_INV)

    # Find the most significant contours
    contours, hierarchy = cv.findContours(thres_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # Get the outermost contours
    outer_contours_img = max(contours, key=cv.contourArea)

    # Get the bounding rectangle of the contours
    x, y, w, h = cv.boundingRect(outer_contours_img)

    # Draw a rectangle base on the bounding rectangle of the contours to our mask
    cv.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
    # Invert the mask so that we create a hole for the detected object in our mask
    mask = cv.bitwise_not(mask)

    # Apply mask to the original image to subtract it and retain only the bg
    img_bg = cv.bitwise_and(org_img, org_img, mask=mask)

    # If the size of the mask is similar to the size of the image then the bg is not white
    if h == org_img.shape[0] and w == org_img.shape[1]:
        return {'reason': 'not whit bg', 'score': 'bad'}

    # Create a np array of the
    np_array = np.array(img_bg)

    # Remove the zeroes from the "remaining bg image" so that we dont consider the black part,
    # and find the average intensity of the remaining pixels
    ave_intensity = np_array[np.nonzero(np_array)].mean()

    if ave_intensity > THRESHOLD_INTENSITY:
        return {'reason':'white bg','score':'good'}
    else:
        return {'reason': 'not whit bg', 'score': 'bad'}


#check the space between the object and edges of the picture
def chck_margin(img):
    # Read image into org_img variable
    org_img = cv.imread(img, cv.IMREAD_GRAYSCALE)
    # cv.imshow('Original Image', org_img)

    # TODO mask doesnt really do anything here
    # Create a black blank image for the mask
    mask = np.zeros_like(org_img)

    # Create a thresholded image, I set my threshold to 200 as this is the value
    # I found most effective in identifying light colored object
    _, thres_img = cv.threshold(org_img, 200, 255, cv.THRESH_BINARY_INV)

    # Find the most significant contours
    contours, hierarchy = cv.findContours(thres_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # Get the outermost contours
    outer_contours_img = max(contours, key=cv.contourArea)

    # Get the bounding rectangle of the contours
    x, y, w, h = cv.boundingRect(outer_contours_img)

    if x < .1*(2*x+w) or y < .1*(2*y+h):
        return {'reason': 'good margin', 'score': 'good'}
    else:
        return {'reason': 'bad margin', 'score': 'bad'}


def rate_picture(filename):
    data = {
        'filename': [],
        'score': 0,
        'reason': [],
    }

    ls = [
    chck_pic_size(filename),
    chck_pic_aspct_ratio(filename),
    chck_margin(f'images/{filename}'),
    has_white_background(f'images/{filename}')
    ]

    for i in ls:
        data['filename'] = filename
        data['reason'].append(i['reason'])

        if i['score'] == 'good':
            data['score'] += 1
        else:
            data['score'] -= 1

    return data


#deploy a simple api
app = FastAPI()

@app.post("/")
async def root(info : Request):
    ls = []

    #get the json
    req_info = await info.json()

    #parse the 2d array and send to rate_picture to run the methods
    for i in req_info['urls']:
        for x in i:
            ls.append(rate_picture(download_picture(x)))

    return {
        "status" : "SUCCESS",
        "data" : ls
    }
