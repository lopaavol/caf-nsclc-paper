# CAF NSCLC paper supplementary code repository

Supplementary code repository for manuscript "Identification of two novel subsets of multi-marker-defined cancer-associated fibroblasts in non-small cell lung cancer with inverse associations to immune features, driver mutations, and survival" by Pellinen T. et al. (2021).

The scripts are ran in the order defined below. MATLAB scripts are used for preparing the image data for analysis. Image analysis is run using Python scripts followed by Jupyter Notebook that provides categorization of cells and data visualization. Finally, R scripts are used for survival analysis.

MATLAB scripts:
* roi_extract.m: Extract individual cores from a TMA slide using coordinates given manually with Fiji macro ROI 1-click.
* registration.m: Register different cyclic staining rounds using DAPI channel.

Python scripts:
* image_preprocess.py: Used to run preprocessing of images before image feature extraction. In this work, this is used to produce distance maps from epithelial cells to analyse stroma cells based on their distance to cancer.
* analyse_cells.py: Runs feature extraction using segmented nuclei images and feature channels.

Jupyter Notebook:
* 

R scripts:
* BOMI1_2Together_Cox_Con_100621_ms.Rmd
* BOMI1_2Together_km_mutate_100621_ms.Rmd
