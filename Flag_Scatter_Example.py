# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:29:21 2018

@author: Alex
"""

#import packages
import pandas as pd
import re
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

#read in csv files with data, rename column names because of issues with encoding
xdata = pd.read_csv("Data CSV.csv") #raw data for X
xdata.columns = ['Country', 'Size']
building = pd.read_csv("Building CSV.csv", encoding = "ISO-8859-1") #y data
building.columns = ['Country', 'Height'] 
c_codes = pd.read_csv("C_Codes.csv", encoding = "ISO-8859-1") #country name and abbreviation
c_codes.columns = ['Country', 'Codes'] 

#fix building text
for index, row in building.iterrows():
    text=row['Country']
    text = re.sub("^\s+|\s+$", "", text, flags=re.UNICODE) #removes empty white spaces before/after
    building['Country'].iloc[index] = text #reapply new value
dfinal_ = xdata.merge(building, on="Country", how = 'inner') #merges building and data file sizes by the country name
missing1=xdata[(~xdata.Country.isin(dfinal_.Country))]  #tells me missing countries in thefile
missing1_1=building[(~building.Country.isin(dfinal_.Country))] #tells me missing countries in the building file
dfinal = dfinal_.merge(c_codes, on="Country", how = 'inner') #merges building file with country code
missing2=xdata[(~xdata.Country.isin(dfinal.Country))] #tells me missing again
x=dfinal['Size'] #sets x
y=dfinal['Height'] #sets y

def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists

fig, ax = plt.subplots()

for index, row in dfinal.iterrows():
    x=row['Size']
    y=row['Height']
    c_str=row['Codes']
    fname='Flag_Images/'+c_str+'.png'
    image_p = fname
    imscatter(x, y, image_p, zoom=1.1, ax=ax)
    ax.plot(x, y)
    plt.show()
ax.set_xlabel("X-Variable, cm")
ax.set_ylabel("Tallest Building, Feet")
plt.rcParams.update({'font.size': 24})
