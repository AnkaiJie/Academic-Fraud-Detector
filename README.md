# NOTE: This repo has been decommissioned and relevant code has been moved to https://github.com/AnkaiJie/AfdWeb

## Academic Fraud Detector
Mass data collection functions for publishers on Scopus API to determine suspects for citation fraud. Created as part of my Undergraduate Research Assistanceship at the University of Waterloo.

This repository examines the citing behaviours of academic authors, as determined through their publicly published papers on Google scholar. Specifically, it looks relationships between those they cite and those who cite them. It does so through the following four automated functions.

Self-cites: Examines the number of times an author cites him/herself.

Over-cites: Examines the number of times that citing papers of an author's paper cite the author as a whole.

Journal Frequency: Determines the number of citing papers of an author that are from common publication journals. 

Cross Cites: Determines the number of times two authors cite each other. 
