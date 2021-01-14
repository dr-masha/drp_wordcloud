# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 21:26:52 2020

@author: masa prodanovic, phd
@edited by: ankita singh, phd

This code produced an image of a word cloud based on 
project titles from Digital Rocks Portal in Dec 2020.
The code is provided as is in hopes of being useful.

This is one of the examples used in Digital Rocks Portal 
Newsletters in Dec 2020 and Jan 2021.
https://www.digitalrocksportal.org/

This code is based on the tutorial:
https://www.datacamp.com/community/tutorials/wordcloud-python

We modified the above tutorial to use our own mask (sand-grain shape)
and the word list coming from project titles in Digital Rocks
Portal or the word "Thank you" in multiple languages.

1. Install wordcloud (with a classic Anaconda distribution
that has numpy, pandas etc (see list of imports below), you will
likely need only install wordcloud. 

1A. regular installation
pip install wordcloud

1B. latest capability installation
git clone https://github.com/amueller/word_cloud.git
cd word_cloud
pip install.

"""

## 0. Imports

import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib as mp

## 1. Parameters

# High resolution images take some time, turn off as necessary
PRODUCE_HIGH_RES = 0
# If you have downloaded Font Awesome, set the parameter below
FONT_AWESOME = 0

## 2. Create desired text: we are importing very specific text.
# You can skip this part altogether, and just type in string text, see below.

# load information into data frame
# use the csv file - 'Projects_16_Dec_2020'. 
# This list of projects are taken from 
# https://www.digitalrocksportal.org/admin/upload/projectpublicationrequest/?o=2&p=1
filename = "Projects_16_Dec_2020.csv"
df = pd.read_csv(filename,encoding='ISO-8859-1')

# check out the top entries in the data frame
print(df.head())

# the column that has project titles is called 'Title'
# the only rows we need is where the status of the project is 'Accepted' or
# 'Created'.
num_of_items_published = df.loc[(df['Status'] == "Accepted") | 
                                (df['Status'] == "Created")].count()[0]

# create a subset dataframe with projects with status = "accepted" and "created"
df_sub = df.loc[(df['Status'] == "Accepted") | (df['Status'] == "Created")]
df_sub.reset_index(inplace=True)


# append all the title together as a string called 'text'
# add space between each last word of the previous title and the first word of 
# the new title
text = ""
for i in range(num_of_items_published):
    text += (df_sub.Title[i] + " ")
    
## Flag so-called stopwords words (that should be skipped).
## We are just added some specific ones on top of the standard set of stopwords.    
# some extra stopwords that need to be removed are vs, using, Nov, 60C, Two, Six 
# yes, Nov and 60C are not really stopwords but need to be removed as they add
# no meaning to the wordcloud    
extra_stopwords = ['vs', 'using', 'Nov', '60C', 'Two', 'Six']

for i in range(len(extra_stopwords)):
    STOPWORDS.add(extra_stopwords[i])


# 3. Create masking shape and process colormap.
# Here I am using the OCEAN colormap.
# Since, I want to avoid light colors to read well on white background
# so I need to remap the color scale.

min_val, max_val = 0, 0.8
n = 20
original_colours = plt.cm.ocean
colours = original_colours(np.linspace(min_val, max_val, n))
cmap = mp.colors.LinearSegmentedColormap.from_list("mycmap", colours)

sand_mask_array = np.array(Image.open("mask-sand-grain.png"))
sand_mask_lowres = 255-sand_mask_array

# Font Awesome is reportedly the best for using the space. Download from the web and place in this directory
# if desired
if FONT_AWESOME:
    wordcloud = WordCloud(font_path='Font-Awesome-master/otfs/Font Awesome 5 Free-Solid-900.otf',width=sand_mask_lowres.shape[1], height=sand_mask_lowres.shape[0], margin=0, contour_width=0,contour_color='blue',background_color = 'white',stopwords=STOPWORDS,mask=sand_mask_lowres).generate(text)
else:
    wordcloud = WordCloud(width=sand_mask_lowres.shape[1], height=sand_mask_lowres.shape[0], margin=0, contour_width=0,contour_color='blue',background_color = 'white',stopwords=STOPWORDS,mask=sand_mask_lowres).generate(text)
wordcloud.recolor(colormap=cmap)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
wordcloud.to_file('wordcloud_sand_lowres_cutoff_ocean.png')

# For creating high resolution images, the mask must be resized or resampled 
# before it is used to create the word cloud. This can be done via the im.resize()
# function in Pillow. Note: resizing or resampling must be done before the image
# is converted to an array

if PRODUCE_HIGH_RES:
    highres_size = (10000, 10000) 
    sand_mask_image = Image.open("images/sand-grain.png")
    sand_mask_highres = np.array(sand_mask_image.resize(highres_size))
    sand_mask_highres = 255-sand_mask_highres
    
    if FONT_AWESOME:
        wordcloud = WordCloud(font_path='Font-Awesome-master/otfs/Font Awesome 5 Free-Solid-900.otf',width=sand_mask_highres.shape[1], height=sand_mask_highres.shape[0], margin=0, contour_width=0,contour_color='blue',background_color = 'white',stopwords=STOPWORDS,mask=sand_mask_highres).generate(text)
    else:
        wordcloud = WordCloud(font_path='Font-Awesome-master/otfs/Font Awesome 5 Free-Solid-900.otf',width=sand_mask_highres.shape[1], height=sand_mask_highres.shape[0], margin=0, contour_width=0,contour_color='blue',background_color = 'white',stopwords=STOPWORDS,mask=sand_mask_highres).generate(text)
    wordcloud.recolor(colormap=cmap)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('wordcloud_sand_highres_cutoff_ocean.png')
