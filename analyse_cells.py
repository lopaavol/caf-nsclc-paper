import os
import re
import glob
from tqdm import tqdm
import imageio
from multiprocessing import Pool
from functools import partial
import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import seaborn as sns
import skimage.filters
import skimage.transform
import skimage.morphology
import skimage.measure
import skimage.segmentation
import sklearn.preprocessing


def measure_objects(labels, img, channel):
    """
    Measure mean, std, mad, stdev, lower quartile and upper quartile
    """
    intmean = np.zeros(labels.max(), dtype=np.float32)
    intstd = np.zeros(labels.max(), dtype=np.float32)
    intmedian = np.zeros(labels.max(), dtype=np.float32)
    intmad = np.zeros(labels.max(), dtype=np.float32)
    intlower = np.zeros(labels.max(), dtype=np.float32)
    intupper = np.zeros(labels.max(), dtype=np.float32)
    
    for i,label in enumerate(range(1,labels.max()+1)):
        obj = img[labels == label]
        lower,median,upper = np.quantile(obj, [0.25, 0.5, 0.75])
        intmean[i] = obj.mean()
        intstd[i] = obj.std()
        intmedian[i] = median
        intmad[i] = scipy.stats.median_absolute_deviation(obj)
        intlower[i] = lower
        intupper[i] = upper

    df = pd.DataFrame(data={channel+'_mean': intmean,
                            channel+'_std': intstd,
                            channel+'_median': intmedian,
                            channel+'_mad': intmad,
                            channel+'_lower_quartile': intlower,
                            channel+'_upper_quartile': intupper})
    return df

def measure_spot(spot, glass='', glassApath='', BOMI=2):
    selem = skimage.morphology.disk(celldil)
    if BOMI==2:
        nucpath = os.path.join(glassApath,"dl_segm","{}~A-Spot{}-{}.tif".format(glass,spot,channels[0][1]))
    else:
        nucpath = os.path.join(glassApath,"dl_segm","{}_{}_roi{}.tif".format(glass,channels[0],spot))
    nucimg = imageio.imread(nucpath)
    nucimg = skimage.morphology.dilation(nucimg, selem)

    if BOMI==2:
        masknegpath = os.path.join(glassApath,"{}~A-Spot{}-{}.tif".format(glass,spot,negmask))
    else:
        masknegpath = os.path.join(glassApath,"{}_{}_roi{}_{}.tif".format(glass,channels[0],spot,negmask))
    
    try:
        masknegimg = imageio.imread(masknegpath)
    except:
        masknegimg = np.zeros(nucimg.shape, dtype=nucimg.dtype)
    
    nucimg[masknegimg==1] = 0
    nucimg = skimage.segmentation.relabel_sequential(nucimg)[0].astype(np.uint16)
    # Save masked and relabeled nuclei image
    imageio.imwrite(os.path.join(glassApath,"vis_segm","{}_{}_roi{}.tif".format(glass,negmask,spot)), nucimg)

    # iterate over channels in spot
    df_spot = None
    for channel in channels:
        try:
            if BOMI==2:
                channelpath = os.path.join(glassApath,"{}~A-Spot{}-{}.tif".format(glass,spot,schannel))
            else:
                channelpath = os.path.join(glassApath,"{}_{}_roi{}.tif".format(glass,channel,spot))
            img = imageio.imread(channelpath)
        except:
            img = np.zeros(nucimg.shape, dtype=np.uint8)

        # Calculate region props for img
        df_meas = measure_objects(nucimg, img, channel_map[channel])
        if df_spot is None:
            df_spot = pd.DataFrame(data={'glass': [glass]*df_meas.shape[0],
                                         'spot': [spot]*df_meas.shape[0]})
            
        df_spot = pd.concat([df_spot, df_meas], axis=1)
    
    return df_spot

def measure_glass(glass, BOMI, pool_procs):
    if BOMI==2:
        glassApath = os.path.join(panelpath,glass+'~A-Spots')
    else:
        glassApath = os.path.join(panelpath,glass)
    spots = [spotre.match(os.path.basename(x)).group(1) for x in glob.glob(os.path.join(glassApath,'*.tif'))]
    spots = sorted(list(dict.fromkeys(spots)))

    measurefunc = partial(measure_spot, glass=glass, glassApath=glassApath, BOMI=BOMI)
    pool = Pool(processes=pool_procs)
    spot_dfs = pool.map(measurefunc, spots)

    glassdf = pd.concat(spot_dfs, ignore_index=True)
    return glassdf


# Feature extraction methods
def fmean(img):
    return [("mean", np.mean(img))]

def fmedian(img):
    return [("median", np.median(img))]

def fstd(img):
    return [("stdev", np.std(img))]

def fmad(img):
    return [("mad", scipy.stats.median_absolute_deviation(img, axis=None))]

def fhistogram(img):
    ar = img.flatten()
    valrange = (0,255)
    hist,edges = np.histogram(ar, bins=10, range=valrange)
    return [("bin_{:d}".format(i+1),hist[i]) for i in range(hist.shape[0])]

def main():
    # BOMI2 settings
    """
    panelpath = "BOMI2"
    channels = ['1B', '1G', '1O', '1R', '1V', '1B_PanEpiMask', '1B_PanEpiMask_dist', '2B', '2R', '2V']
    channel_map = {'1B': '1DAPI', '1G': 'PDGFRB', '1O': 'PDGFRA', '1R': 'FAP', '1V': 'SMA', '1B_PanEpiMask': 'PanEpiMask', '1B_PanEpiMask_dist': 'PanEpiMask_dist', '2B': '2DAPI', '2R': 'CD34', '2V': 'PanEpi'}
    negmask = 'G_RedCellMask'
    spotre = re.compile("[\w\-]*Spot(\d+)[\w\-\.]*")
    BOMI = 2
    """

    # BOMI1 settings
    panelpath = "BOMI1"
    channels = ['DAPI_ORG', 'AF488_ORG', 'AF555_ORG', 'AF750_ORG', 'AF647_ORG', 'PanEpiMask', 'PanEpiMask_dist']
    channel_map = {'DAPI_ORG': 'DAPI', 'AF488_ORG': 'PDGFRB', 'AF555_ORG': 'PDGFRA', 'AF750_ORG': 'FAP', 'AF647_ORG': 'SMA', 'PanEpiMask': 'PanEpiMask', 'PanEpiMask_dist': 'PanEpiMask_dist'}
    negmask = 'RedCellMask'
    spotre = re.compile("[\w\-]*roi(\d+)[\w\-\.]*")
    BOMI = 1

    # General settings
    pool_procs = 10
    celldil = 6

    # Feature settings
    featfunc = [fmean, fmedian, fstd, fmad, fhistogram]

    if BOMI==2:
        glasses = [x.split('~')[0] for x in os.listdir(panelpath) if os.path.isdir(os.path.join(panelpath,x))]
    else:
        glasses = [x for x in os.listdir(panelpath) if os.path.isdir(os.path.join(panelpath,x)) and '1-ImageExport' in x]
    glasses = sorted(list(dict.fromkeys(glasses)))

    # iterate over glasses
    for glass in glasses:
        df = measure_glass(glass, BOMI, pool_procs)
        df.to_csv(os.path.join(panelpath,glass+'_features.csv'), index=False)
        
if __name__=="__main__":
    main()
