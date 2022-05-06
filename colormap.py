# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:30:28 2020

@author: lenovo
"""

import numpy as np
import matplotlib.pyplot as plt
 
# Have colormaps separated into categories:
# http://matplotlib.org/examples/color/colormaps_reference.html
 
cmaps = [('Perceptually Uniform Sequential',
                            ['viridis', 'inferno', 'plasma', 'magma']),
         ('Sequential',     ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
         ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool',
                             'copper', 'gist_heat', 'gray', 'hot',
                             'pink', 'spring', 'summer', 'winter']),
         ('Diverging',      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic']),
         ('Qualitative',    ['Accent', 'Dark2', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3']),
         ('Miscellaneous',  ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                             'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'gist_ncar',
                             'nipy_spectral', 'jet', 'rainbow',
                             'gist_rainbow', 'hsv', 'flag', 'prism'])]
 
 
nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
 
 
def plot_color_gradients(cmap_category, cmap_list):
    fig, axes = plt.subplots(nrows=nrows)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    axes[0].set_title(cmap_category + ' colormaps', fontsize=14)
 
    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)
 
    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()
 
for cmap_category, cmap_list in cmaps:
    plot_color_gradients(cmap_category, cmap_list)
 
plt.show()

from matplotlib import cm
 
def get_jet():
 
    colormap_int = np.zeros((256, 3), np.uint8)
    colormap_float = np.zeros((768, 3), np.float)
 
    for i in range(0, 256, 1):
       colormap_float[i, 0] = cm.OrRd(i)[0]
       colormap_float[i, 1] = cm.OrRd(i)[1]
       colormap_float[i, 2] = cm.OrRd(i)[2]
 
       colormap_int[i, 0] = np.int_(np.round(cm.OrRd(i)[0] * 255.0))
       colormap_int[i, 1] = np.int_(np.round(cm.OrRd(i)[1] * 255.0))
       colormap_int[i, 2] = np.int_(np.round(cm.OrRd(i)[2] * 255.0))
 
    np.savetxt(r'C:\Users\lenovo\Desktop\OrRd_float.txt', colormap_float, fmt = "%f", delimiter = ' ', newline = '\n')
    np.savetxt(r'C:\Users\lenovo\Desktop\OrRd_int.txt', colormap_int, fmt = "%d", delimiter = ' ', newline = '\n')
 
    print(colormap_int）
 
    return



import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image


def normalization(data,scale):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range*(scale-1)

def gray2color(gray_array, color_map):
    
    rows, cols = gray_array.shape
    color_array = np.zeros((rows, cols, 3), np.uint8)
 
    for i in range(0, rows):
        for j in range(0, cols):
            color_array[i, j] = color_map[gray_array[i, j]]
    
    #color_image = Image.fromarray(color_array)
 
    return color_array

def test_gray2color():
    gray_image = Image.open(r'D:\XM\gpr\gray_imgs\000345C2_400M_0-512.jpg').convert("L")
 
    gray_array = np.array(gray_image)
    
    plt.figure()
    plt.subplot(211)
    plt.imshow(gray_array, cmap = 'gray')
 
    jet_map = np.loadtxt(r'D:\XM\gpr\jet_int.txt', dtype = np.int)
    color_jet = gray2color(gray_array, jet_map)
    plt.subplot(212)
    plt.imshow(color_jet)
 
    plt.show()
 
    return

raw_data=pd.read_table(r'G:\gpr\xpn_txt\ltefile81.txt',sep=',',header=None).iloc[:,0:1024]
np_data=np.array(raw_data)
scale_data=normalization(np_data,768)
scale_data=scale_data.astype(int)

plt.figure()
plt.imshow(scale_data,cmap='gray')
#plt.savefig("gray.png",dpi=300)

fuse_map=np.loadtxt(r'C:\Users\lenovo\Desktop\3colormap_int.txt', dtype = np.int)
color_fuse=gray2color(scale_data,fuse_map)
plt.figure()
plt.imshow(color_fuse)
#plt.savefig("3colorfuse.png",dpi=300)
