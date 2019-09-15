"""
Run: python view_descriptions.py
View: http://127.0.0.1:5002/
"""

from flask import Flask, redirect, render_template

import json
import csv
import os
from collections import defaultdict
from urllib.request import urlretrieve

################################################################################
# Data

def download_url(url, folder):
    "Download a file to a particular folder."
    filename = url.split('_')[-1]
    local_filename, headers = urlretrieve(url, folder + filename)
    print('Downloaded:', local_filename)
    print('Headers:', headers)


def get_entry_index(filename):
    with open(filename) as f:
        data = json.load(f)
        entries_by_image = defaultdict(list)
        for entry in data:
            img = entry['image']
            entries_by_image[img].append(entry)
    return entries_by_image


def load_image_data(filename):
    "Load URLs for the images."
    image_data = defaultdict(dict)
    with open(filename) as f:
        reader = csv.DictReader(f)
        for entry in reader:
            coco_id = entry['coco_id']
            genome_id = entry['genome']
            url = entry['coco_url']
            image_data[genome_id] = dict(coco_id= entry['coco_id'],
                                         url= entry['coco_url'])
    return image_data

entry_index = get_entry_index('./data/written_annotations.json')
image_data = load_image_data('./data/images.csv')

images = list(entry_index)
index_to_img = dict(enumerate(sorted(images, key=lambda x:int(x))))
img_to_index = {img:index for index, img in index_to_img.items()}
num_images = len(images)
max_index = num_images - 1


################################################################################
# Utilities

def get_previous_next(image):
    "Get the indices for previous and next."
    index = img_to_index[image]
    previous = None if index == 0 else index_to_img[index -1]
    next = None if index == max_index else index_to_img[index + 1]
    return previous, next


def imgid2filename(coco_id):
    "Generate filename."
    return coco_id.zfill(12) + '.jpg'

################################################################################
# Interface

app = Flask(__name__)

@app.route('/')
def index():
    imgid = index_to_img[0]
    return redirect('/images/' + imgid)

@app.route('/images/<imgid>')
def image_page(imgid):
    entries = entry_index[imgid]
    descriptions = [(entry['participant'], entry['description']) for entry in entries]
    previous, next = get_previous_next(imgid)
    
    coco_id = image_data[imgid]['coco_id']
    filename = imgid2filename(coco_id)
    folder = './static/COCO-images/'
    path_to_image = folder + filename
    if not os.path.isfile(path_to_image):
        print("We need to download the image!")
        url = image_data[imgid]['url']
        download_url(url, folder)
    else:
        print('Already downloaded.')
    
    return render_template('index.html',
                           descriptions=descriptions,
                           previous=previous,
                           next=next,
                           filename=filename,
                           vg_id=imgid,
                           coco_id=coco_id)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
