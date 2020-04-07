# -*- coding: utf-8 -*-
# Author: Ankush Gupta
# Date: 2015

"""
Entry-point for generating synthetic text images, as described in:

@InProceedings{Gupta16,
      author       = "Gupta, A. and Vedaldi, A. and Zisserman, A.",
      title        = "Synthetic Data for Text Localisation in Natural Images",
      booktitle    = "IEEE Conference on Computer Vision and Pattern Recognition",
      year         = "2016",
    }
"""

import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
from synthgen import *
from common import *
import wget, tarfile
import cv2 as cv
import time 

## Define some configuration variables:
NUM_IMG = -1 # no. of images to use for generation (-1 to use all available):
INSTANCE_PER_IMAGE = 1 # no. of times to use the same image
SECS_PER_IMG = 5 #max time per image in seconds

# path to the data-file, containing image, depth and segmentation:
DATA_PATH = 'data'
    
def rgb2hsv(image):
    return image.convert('HSV')

def rgb2gray(image):
    
    rgb=np.array(image)
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def combine_mask(mask,filename):
  '''
  combine the text area labeled by hand to mask
  :param mask:
  :param filename:
  :return:
  '''
  src_text = open(filename, 'r')

  for line in src_text.readlines():
    list = line.split()
    if len(list) < 4:
      continue
    mask[int(list[1]):int(list[3]),int(list[0]):int(list[2])] = 255

  src_text.close()

  return mask    

def start_generate(parameters):
  generate_flag = 0
  viz = False
  
  imgdir,txtdir, outimgdir, outtxtdir = parameters["dir"]
  font_size, font_color = parameters["fontstyle"]
  num_gen_per_img, text_number_per_image, text_content = parameters["text"] #re-use each region NUM_REP times:

  RV3 = RendererV3(DATA_PATH, max_time=SECS_PER_IMG
  , text_number = text_number_per_image
  , font_color_user = font_color
  , font_size_user = font_size
  , text_content_user = text_content)
  for files in os.listdir(imgdir):
    imgname = os.path.splitext(files)
    if imgname[1] not in ['.bmp','.jpg','.png']:
      continue

    pubimg = Image.open(os.path.join(imgdir,files),'r')
    # pubimg.show()
    sz = pubimg.size
    pubimg = np.array(pubimg)
    pubimg = pubimg[:,:,:3]
    place_mask = np.zeros((sz[1],sz[0]),'uint8')
    if(os.path.exists(os.path.join(txtdir,imgname[0]+'.txt'))):
        place_mask = combine_mask(place_mask.copy(),os.path.join(txtdir,imgname[0]+'.txt'))
    dir = {'outimgdir':outimgdir,'outtxtdir':outtxtdir,'inimgname':imgname[0]}
    RV3.render_text(pubimg, place_mask, dir, num_gen_per_img, viz=viz)
  generate_flag = 1
  return generate_flag

def main(viz=True):
  imgdir = 'data/dataset/wot/source'
  txtdir = 'data/dataset/wot/text'
  outimgdir = 'data/dataset/wot/img_gen'
  outtxtdir = 'data/dataset/wot/label_gen'


  font_size, font_color = [40, [255,0,0]]
  num_gen_per_img, text_number_per_image, text_content = [1,3,u"C:\\Users\\yarudu\\Documents\\project\\synth_tool\\SynthText\\data\\test.txt"] #re-use each region NUM_REP times:
  
  RV3 = RendererV3(DATA_PATH, max_time=SECS_PER_IMG
  , text_number = text_number_per_image
  , font_color_user = font_color
  , font_size_user = font_size
  , text_content_user = text_content)
  

  for files in os.listdir(imgdir):
    print(files)
    imgname = os.path.splitext(files)
    if imgname[1] not in ['.bmp','.jpg','.png']:
      continue

    pubimg = Image.open(os.path.join(imgdir,files),'r')
    # pubimg.show()
    sz = pubimg.size
    pubimg = np.array(pubimg)
    pubimg = pubimg[:,:,:3]
    place_mask = np.zeros((sz[1],sz[0]),'uint8')
    if(os.path.exists(os.path.join(txtdir,imgname[0]+'.txt'))):
        place_mask = combine_mask(place_mask.copy(),os.path.join(txtdir,imgname[0]+'.txt'))
    num_gen_per_img =1
    dir = {'outimgdir':outimgdir,'outtxtdir':outtxtdir,'inimgname':imgname[0]}
    RV3.render_text(pubimg, place_mask, dir, num_gen_per_img, viz=viz)
    break


if __name__=='__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Genereate Synthetic Scene-Text Images')
  parser.add_argument('--viz',action='store_true',dest='viz',default=False,help='flag for turning on visualizations')
  args = parser.parse_args()
  main(args.viz)
