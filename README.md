# GSC-Citation-Fraud-Data-Collector

This repository examines the citing behaviours of authors on Google Scholar, as determined through their publicly published papers on Google scholar. Specifically, it looks relationships between those they cite and those who cite them. It does so through the following four automated functions.

1. Self-cites: Given an author’s paper on Google Scholar, returns that number of times that the author cites him/herself in the paper.
 
2. Over-cites: Given an author’s paper on Google Scholar, finds papers that cite that paper, and determines the number of times each paper cites the original author in total

3. Journal Frequency: Given an Author’s paper on Google Scholar, finds its most relevant citers on Google Scholar, and determines the frequency of the journals that those papers come from as listed in Google Scholar

4. Cross Cites: Given an author, determines other authors with whom the author has frequent citing relationships.

# HOW TO RUN

1. Clone this repository.
2. Run scrapper.py and follow on screen instructions.
