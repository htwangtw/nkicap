"""Combine schaefer and tian in one nifti."""
import nibabel as nb
import numpy as np
from nilearn.image import resample_img
import warnings


PATH_SCHAEFER = (
    "data/parcellations/Schaefer2018_1000Parcels_7Networks_order_FSLMNI152_2mm.nii.gz"
)
PATH_TIAN = "data/parcellations/Tian_Subcortex_S4_3T_2009cAsym.nii.gz"


def combine_atlas(img1, img2):
    """Combine two atlases in the same space. """
    max_val = np.max(img1.dataobj)
    relabe_2 = (img2.dataobj + max_val) * (img2.dataobj > 0).astype(int)
    label_combined = img1.dataobj + relabe_2

    n_max_label = sum(len(np.unique(img.dataobj)) - 1 for img in [img1, img2])
    overlap = (label_combined > n_max_label).astype(int)
    mask = (label_combined > 0).astype(int) - overlap

    if np.sum(overlap) == 0:
        return (
            nb.Nifti1Image(
                label_combined,
                affine=img1.affine,
                header=img1.header,
            ),
            None,
        )

    warnings.warn(f"Input images contain {np.sum(overlap)} overlapping voxels.")
    overlap = nb.Nifti1Image(
        overlap,
        affine=img1.affine,
        header=img1.header,
    )
    combined = nb.Nifti1Image(
        label_combined * mask,
        affine=img1.affine,
        header=img1.header,
    )
    return combined, overlap


if __name__ == "__main__":
    schaefer = nb.load(PATH_SCHAEFER)
    tian_resampled = resample_img(
        PATH_TIAN,
        target_affine=schaefer.affine,
        target_shape=schaefer.shape,
        interpolation="nearest",
    )
    combined, overlap = combine_atlas(schaefer, tian_resampled)
    combined.to_filename("data/parcellations/SchaeferTian_combined_MNI152_2mm.nii.gz")
    if overlap:
        overlap.to_filename("data/parcellations/SchaeferTian_overlap.nii.gz")


def test_combine_atlas():
    schaefer = nb.load(PATH_SCHAEFER)
    tian_resampled = resample_img(
        PATH_TIAN,
        target_affine=schaefer.affine,
        target_shape=schaefer.shape,
        interpolation="nearest",
    )
    combined, overlap = combine_atlas(schaefer, tian_resampled)
    assert np.max(combined.dataobj) == 1054
    assert np.sum(overlap.dataobj) == 168
