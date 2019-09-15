# Results viewer

This folder contains a viewer tool for the written image descriptions.
This tool allows you to look through the images and their descriptions in your browser.

## Requirements

Here are the versions that I have used. Others probably work, but remain untested.

* Python 3.6.6
* Flask 1.0.2

## How to run the viewer

Usage is fairly straightforward. The Python script will start up a server on localhost.
You can visit the locally hosted website in your browser.

* Run `python view_descriptions.py`
* Visit http://127.0.0.1:5002/ in your browser.

The viewer requires an active internet connection as long as you haven't downloaded the images.
It will automatically download each image upon viewing the descriptions for that image.

If you want to download all images first, run the following command:

* `python download_images.py`

The tool currently uses URLs from MS COCO. If these ever stop working, try the Visual Genome URLs instead.

## Data

All the relevant data files to run this tool are stored in `./data/`. These are:

* `images.csv` - This file contains identifiers and URLs of all the images in MS COCO and the Visual Genome dataset.
* `written_annotations.json` - This file contains all the written descriptions collected in our experiment.
