# Google-Scholar-Citation-Fraud-Data-Collector
Mass data collection functions for publishers on Google Scholar to determine suspects for citation fraud. Created as part of my Undergraduate Research Assistanceship at the University of Waterloo.


This repository examines the citing behaviours of authors on Google Scholar, as determined through their publicly published papers on Google scholar. Specifically, it looks relationships between those they cite and those who cite them. It does so through the following four automated functions.

Self-cites: Given an author’s paper on Google Scholar, returns that number of times that the author cites him/herself in the paper.
Over-cites: Given an author’s paper on Google Scholar, finds papers that cite that paper, and determines the number of times each paper cites the original author in total
Journal Frequency: Given an Author’s paper on Google Scholar, finds its most relevant citers on Google Scholar, and determines the frequency of the journals that those papers come from as listed in Google Scholar
Cross Cites: Given an author, determines other authors with whom the author has frequent citing relationships.
