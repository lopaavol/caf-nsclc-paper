import sys
import imageio
from pathlib import Path
from tqdm import tqdm
import numpy as np
from scipy.ndimage import distance_transform_edt as dist_trans

# Script to create additional images for analysis

# Create PanEpiMask distance map
inpath = Path(sys.argv[1])
outpath = Path(sys.argv[2])
files = inpath.glob('*PanEpiMask.tif')
for f in tqdm(files):
    panepimask = imageio.imread(f)
    panepimask[panepimask > 0] = 255
    panepidist = dist_trans(np.invert(panepimask)).astype(np.float32)
    outname = "{}_dist.tif".format(f.stem)
    imageio.imwrite(outpath / outname, panepidist)
