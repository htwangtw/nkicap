"""Combine schaefer and tian in one nifti"""
import nibabel as nb
from nilearn.image import resample_img


schaefer = nb.load(
    "data/parcellations/Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm.nii.gz"
)
tian = nb.load("data/parcellations/Tian_Subcortex_S4_3T_2009cAsym.nii.gz")
tian_resampled = resample_img(
    "data/parcellations/Tian_Subcortex_S4_3T_2009cAsym.nii.gz",
    target_affine=schaefer.affine,
    target_shape=schaefer.shape,
    interpolation="nearest",
)
tian_relabel = nb.Nifti1Image(
    (tian_resampled.dataobj + 1000) * (tian_resampled.dataobj > 0).astype(int),
    header=tian_resampled.header,
    affine=tian_resampled.affine,
)
combined = nb.Nifti1Image(
    tian_relabel.dataobj + schaefer.dataobj,
    affine=schaefer.affine,
    header=schaefer.header,
)
combined.to_filename("data/parcellations/SchaeferTian_combined_MNI152_2mm.nii.gz")
