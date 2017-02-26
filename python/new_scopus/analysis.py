from credentials import API_KEY, DBNAME, USER, PASSWORD, HOST
import requests
import json
import time
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def getOvercites(authid):
    conn = pymysql.connect(HOST, USER, PASSWORD, DBNAME, charset='utf8')
    curs = conn.cursor()
    cmd = "select * from author_overcites where targ_author_id=" + "'" + authid + "'" + " order by overcites desc"

    curs.execute(cmd)
    rows = curs.fetchall()
    df = pd.DataFrame([i for i in rows])
    df.rename(columns={0: 'Target Author', 1: 'Citing Paper', 2:'Author Count', 3:'Overcites'}, inplace=True)
    return df

def plotOvercitesBar(authid):
    df = getOvercites(authid)
    fig, ax = plt.subplots(figsize=(10,10))
    fig.subplots_adjust(bottom=0.25)

    papers = df['Citing Paper'][:25]
    y_pos = np.arange(len(papers))
    overs = df['Overcites'][:25]
     
    ax.bar(y_pos, overs, align='center', alpha=0.5)
    ax.set_xticks(y_pos)
    ax.set_xticklabels(papers, rotation="90")
    ax.set_ylabel('Overcites')
    ax.set_xlabel('Citing Paper ID')
    ax.set_title('Top 25 overcites for author ' + authid)
    plt.show()

def plotOvercitesHist(authid):
    df = getOvercites(authid)

plotOvercitesBar('22954842600')
