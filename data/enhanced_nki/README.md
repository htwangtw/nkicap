# CAP of enhanced NKI resting state data

## Participant
We are using the cross section NKI dataset (ses-BAS1).
Total subject with CAP: 721
Total subject with CAP and mriq: 711
See participants.tsv to see the subjects details


## CoActivation Pattern

### Sample, preprocessing & quality control
 - NKI-RS (N=721, TR=645)
 - CPAC preprocessed (nuisance: wm/csf/motion24/aCompCor5, 0.01-0.1Hz)
 - Timeframes with FD<0.3mm

### Method
 - Parcellation: Cortex: Schaefer1000, Subcortex: Tian S4 (54 ROIs)
 - Ref: Gutierrez-Barragan et al., 2020; Liu et al., 2013
 - Number of CAPs = 8

### Output
 - Group CAP (averaged across subjects)
