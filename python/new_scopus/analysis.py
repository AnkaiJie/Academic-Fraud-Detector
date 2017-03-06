from credentials import API_KEY, DBNAME, USER, PASSWORD, HOST
import operator
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from apilib import ScopusApiLib

class Analysis:

    def __init__(self):
        self.api = ScopusApiLib()

    def getAuthorName(id):
        return

    def getOvercites(self, authid):
        conn = pymysql.connect(HOST, USER, PASSWORD, DBNAME, charset='utf8')
        curs = conn.cursor()
        cmd = "select * from author_overcites where targ_author_id=" + "'" + authid + "'" + " order by overcites desc"

        curs.execute(cmd)
        rows = curs.fetchall()
        df = pd.DataFrame([i for i in rows])
        df.rename(columns={0: 'Target Author', 1: 'Citing Paper', 2:'Author Count', 3:'Overcites'}, inplace=True)
        return df


    def plotOvercitesBar(self, authid):
        df = self.getOvercites(authid)
        fig, ax = plt.subplots(figsize=(10,10))
        fig.subplots_adjust(bottom=0.25)

        papers = df['Citing Paper'][:25]
        x_pos = np.arange(len(papers))
        overs = df['Overcites'][:25]
         
        ax.bar(x_pos, overs, align='center', alpha=0.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(papers, rotation="90")
        ax.set_ylabel('Overcites')
        ax.set_xlabel('Citing Paper ID')
        ax.set_title('Top 25 overcites for author ' + authid)
        plt.show()

    def plotOvercitesHist(self, authid):
        df = self.getOvercites(authid)
        fig,ax = plt.subplots(figsize=(10,10))
        fig.subplots_adjust(bottom=0.25)

        freq = {}
        for idx, row in df.iterrows():
            overs = row['Overcites']
            if overs > 14:
                f = freq.get(overs, 0)
                freq[overs] = f + 1

        sorted_freq = sorted(freq.items(), key=operator.itemgetter(0))
        x_pos = np.arange(len(sorted_freq))
        overcite_nums = [x[0] for x in sorted_freq]
        overcite_num_freqs = [x[1] for x in sorted_freq]

        ax.bar(x_pos, overcite_num_freqs, align='center', alpha=0.5)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(overcite_nums, rotation="90")
        ax.set_ylabel('Number of Papers with Overcite Amount')
        ax.set_xlabel('Number of Overcites')
        ax.set_title('Overcite frequency for >=15 overcites from ' + str(len(df)) + ' citing papers for ' + authid)
        plt.show()


# plotOvercitesBar('22954842600')
# plotOvercitesHist('22954842600')
# s = ScopusApiLib()
# print(s.getAuthorPapers('22954842600'))
# print (s.getAuthorMetrics('22954842600'))

a = Analysis()
a.plotOvercitesHist('22954842600')
