import csv
import os
import time
from urllib.request import urlretrieve


def download_url(url, folder):
    "Download a file to a particular folder."
    filename = url.split('_')[-1]
    local_filename, headers = urlretrieve(url, folder + filename)
    print('Downloaded:', local_filename)


def load_image_data(filename):
    "Load URLs for the images."
    image_data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for entry in reader:
            coco_id = entry['coco_id']
            image_data[coco_id] = entry['coco_url']
    return image_data


def imgid2filename(coco_id):
    "Generate filename."
    return coco_id.zfill(12) + '.jpg'


def download_images(image_data, seconds=1):
    "Download all the images."
    for image, url in image_data.items():
        filename = imgid2filename(image)
        folder = './static/COCO-images/'
        path_to_image = folder + filename
        # Check if file exists. If not, download it.
        if not os.path.isfile(path_to_image):
            download_url(url, folder)
        # Be nice to the server :)
        time.sleep(seconds)

if __name__ == '__main__':
    image_data = load_image_data('./data/images.csv')
    download_images(image_data)
