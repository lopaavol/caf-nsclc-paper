# CAF NSCLC paper supplementary code repository

Supplementary code repository for manuscript "Identification of two novel subsets of multi-marker-defined cancer-associated fibroblasts in non-small cell lung cancer with inverse associations to immune features, driver mutations, and survival" by Pellinen T. et al. (2022).

The scripts are ran in the order defined below. MATLAB scripts are used for preparing the image data for analysis. Image analysis is run using Python scripts followed by Jupyter Notebook that provides categorization of cells and data visualization. Finally, R scripts are used for survival analysis.

Necessary data for creating manuscript figures are available in 'data' folder. There are separate files for spot ratios and case ratios for 15 CAFs used in visualize_caf.ipynb notebook for both cohorts. The Excel files include necessary case metadata for running survival analysis R scripts.

MATLAB scripts:
* roi_extract.m: Extract individual cores from a TMA slide using coordinates given manually with Fiji macro ROI 1-click.
* registration.m: Register different cyclic staining rounds using DAPI channel.

Python scripts:
* image_preprocess.py: Used to run preprocessing of images before image feature extraction. In this work, this is used to produce distance maps from epithelial cells to analyse stroma cells based on their distance to cancer.
* analyse_cells.py: Runs feature extraction using segmented nuclei images and feature channels.

Jupyter Notebook:
* analyse_caf.ipynb: Jupyter Notebook used for post-analysis of the data. Applies thresholding to define marker positivity, and creates counts and ratios of marker combinations for survival analysis.
* visualize_caf.ipynb: Jupyter Notebook used to visualize the data and generate some of the paper's figures.

R scripts:
* BOMI1_2_OS_survival_Final.Rmd: Survival analysis
* BOMI1_2_OS_Cox_survival_ContinuousValues_Final.Rmd: Cox regression
