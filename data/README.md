# Data

```bash
├── sourcedata/                 Sourcedata of the NKI dataset used in this analysis
├── enhanced_nki/               Derivative of the NKI dataset used in this analysis
├── HCP/                        Contain `HCP_S1200_812_rfMRI_MSMAll_groupPCA_d4500ROW_zcorr_recon2.dconn.nii`
├── parcellations/              Atlas used from CAP computation
├── Arimo-VariableFont_wght.ttf Default font of word clouds
├── cap.json                    File path to CAP for subjects with complete mriq measures
├── enhanced_nki.tsv            Master spreadsheet of subject level data used in the analysis
├── mriq_labels.tsv             The questions presented to the subjects in the scanner; from public NKI dataset codebook
└── README.md                   This file you are reading
```

The github repository only contains the label files and relevant information for those who want to fetch the NKI dataset.
The raw and source data includes restricted access items that reqires DUA of the NKI dataset.
Please apply for NKI dataset access before requesting `sourcedata/`.

## Create the full dataset

1. Clone the full repository and set up the environment.
2. Unzip source data and place the two files in `sourcedata/`.
3. At the top level of this project, run `python bin/make_dataset.py`
