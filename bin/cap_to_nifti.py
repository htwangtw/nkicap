# -*- coding: utf-8 -*-
""" Map CAP values into nifti space using combined atlas."""

import nibabel as nb
import numpy as np
import pandas as pd
from nilearn import plotting

# load CAP data & select only the relevant columns (i.e., remove index column)
cap_data = pd.read_csv("data/enhanced_nki/desc-cap_groupmap.tsv", sep="\t")

# reset index to be first column which is numbers 1-1054 for cap data
caps = cap_data.set_index("Unnamed: 0")

# load combined atlas
com = nb.load("data/parcellations/SchaeferTian_combined_MNI152_2mm.nii.gz")

# get data from combined atlas
com_atlas = com.get_fdata()

# store unique numbers from com_atlas as com_parcels
com_parcels = np.unique(com_atlas)
# remove first row as it is zero
com_parcels = np.delete(com_parcels, (0), axis=0)
# convert to integer for loop below
com_parcels = com_parcels.astype(int)

# create new nifti shape using np.zeros to be the same shape as combined atlas
new_nifti_data = np.zeros(com.shape)

# loop over each caps column to create nifti for each CAP and save to results
for cap in caps:
    # loop over each parcel number in com_parcels
    for parcel in com_parcels:
        # create mask for that parcel
        mask = np.where(com_atlas == parcel, True, False)
        # retrieve cap value
        current_number = caps[cap].loc[parcel]
        # replace mask values with cap value
        new_nifti_data[mask] = current_number

    # for each cap, plot nifti and save to results
    plotting.plot_stat_map(
        nb.Nifti1Image(new_nifti_data, header=com.header, affine=com.affine),
        title="Combined_{}".format(cap),
    )
    plotting.show()
    nifti = nb.Nifti1Image(new_nifti_data, header=com.header, affine=com.affine)
    nb.save(nifti, "results/cap_nifti/group_{}.nii.gz".format(cap))
