__author__ = "Clement Helsens"
__email__ = "clement.helsens@gmail.com"

import json
import pandas as pd
import sys
from os.path import exists
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

#__________________________________________________________
def plot(val,date,ind,i):
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.xlabel('indicator reliability score')
    plt.hist(val, 6, range=[0,6], facecolor='g', alpha=0.4)
    plt.text(0.02, 1.02,'indicator={}'.format(ind),transform = ax.transAxes)
    plt.text(0.02, 0.95, r'$\mu={:.3f},\ \sigma={:.3f}$'.format(np.mean(val),np.std(val)),transform = ax.transAxes)
    plt.text(0.02, 0.9,'number of crises={}'.format(len(val)),transform = ax.transAxes)
    plt.text(0.02, 0.85,'date={}'.format(date),transform = ax.transAxes)
    plt.savefig('plots/question2/indicators_reliability_score_months/indicator{}_{}.png'.format(i,date))
    plt.savefig('plots/question2/indicators_reliability_score_months/indicator{}_{}.pdf'.format(i,date))
    plt.close()


#__________________________________________________________
def plotcrisis(val,date,ind,i,c):

    f = plt.figure()
    ax = f.add_subplot(111)
    ax.set_ylim([0., 5.5])
    plt.ylabel('reliability score')

    plt.text(0.02, 1.02,'indicator={}'.format(ind),transform = ax.transAxes)
    plt.text(0.02, 0.95, r'$\mu={:.3f},\ \sigma={:.3f}$'.format(np.mean(val),np.std(val)),transform = ax.transAxes)
    plt.text(0.02, 0.9,'crisi id={}'.format(c),transform = ax.transAxes)
    
    plt.plot(date, val, marker='o', ms=5, color='b')
    plt.xticks(fontsize=8,rotation=45)
    plt.grid(True, alpha=0.2,color='g')

    plt.savefig('plots/question2/indicators_reliability_score_months_crisis/indicator{}_{}.png'.format(i,c))
    plt.savefig('plots/question2/indicators_reliability_score_months_crisis/indicator{}_{}.pdf'.format(i,c))
    plt.close()

#__________________________________________________________
def ploterr(mean,std,num,date,ind,i):
    
    f, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.errorbar(date, mean, yerr=std,   marker='o', ms=5, color='b')
    ax2.plot(date, num, 'r-')
    
    ax1.set_xticks(ax1.get_xticks())    
    ax1.set_xticklabels(date, rotation=45, fontsize=8)    
    ax1.set_ylabel('indicator reliability score (mean value)', color='b')
    ax1.set_ylim([0., 4.])
    ax2.set_ylim([0.,max(num)*1.1])
    ax2.set_ylabel('number of crises', color='r')
    ax1.text(0.02, 1.02,'indicator={}'.format(ind),transform = ax1.transAxes)
    ax1.grid(True,alpha=0.2,color='g')

    plt.savefig('plots/question2/indicators_reliability_score_vs_time/indicator{}_vs_time.png'.format(i))
    plt.savefig('plots/question2/indicators_reliability_score_vs_time/indicator{}_vs_time.pdf'.format(i))
    plt.close()

#__________________________________________________________
def run(fname):
    # loading data into json dict and df
    f = open(fname)
    data = json.load(f)
    df = pd.DataFrame()
    df = df.append(pd.DataFrame(data["results"]))

    #build sub_df with less info
    sub_df = df[['crisis_id','source_and_date','date_of_entry','reliability', 'reliability_score','indicator']]

    #filter date
    sub_df = sub_df[sub_df['date_of_entry'] > '2020-04-01']

    #filter null values
    sub_df=sub_df[sub_df.reliability_score.notnull()]
    sub_df=sub_df[sub_df.indicator.notnull()]

    #build range of dates (not very elegant, but does the job)
    nmonths=18
    starting_date='2021-10-01'
    ending_date=starting_date.split('-')[0]+'-'+starting_date.split('-')[1]+'-31'
    starting_date_list=[]
    ending_date_list=[]
    for i in range(nmonths):
        starting_date_list.append(starting_date)
        ending_date_list.append(ending_date)

        if int(starting_date.split('-')[1])>1:
            month=int(starting_date.split('-')[1])-1
            if month<10:month='0'+str(month)
            starting_date = starting_date.split('-')[0]+'-'+str(month)+'-01'
        else:
            year=int(starting_date.split('-')[0])-1
            starting_date = str(year)+'-12-01'
        ending_date=starting_date.split('-')[0]+'-'+starting_date.split('-')[1]+'-31'

    #chronological order
    starting_date_list=list(reversed(starting_date_list))
    ending_date_list=list(reversed(ending_date_list))
    
    #loop over indicators, slice in months and plot mean/rms/num for all crises 
    indicator_list = sub_df.indicator.unique().tolist()
    crisis_list = sub_df.crisis_id.unique().tolist()
    counter=0
    for i in indicator_list:
        mean=[]
        std=[]
        date=[]
        num=[]
        for m in range(nmonths):
            #sub df per month
            sub_df_month = sub_df[(sub_df['date_of_entry'] > starting_date_list[m]) & (sub_df['date_of_entry'] < ending_date_list[m])]
            #get indicator i
            sub_df_month_id = sub_df_month[sub_df_month['indicator'] == i]
            #filter one crisis
            sub_df_month_id = sub_df_month_id.drop_duplicates(subset=['crisis_id'], keep=False)
            #list the score of the indicator i
            list_score = sub_df_month_id.reliability_score.tolist()
            if len(list_score)>0:
                mean.append(np.mean(list_score))
                std.append(np.std(list_score))
                date.append(ending_date_list[m].replace('-31',''))
                num.append(len(list_score))
                plot(list_score,date[-1],i,counter)
        ploterr(mean,std,num,date, i, counter)
        counter+=1


    #loop over indicators AND crises, slice in months and plot mean/rms/num for all crises 
    counter=0
    for i in indicator_list:
        #sub df per indicator
        sub_df_id = sub_df[sub_df['indicator'] == i]
        for c in crisis_list:
            #sub df per crisis
            sub_df_id_crisis = sub_df_id[sub_df_id['crisis_id'] == c]
            value=[]
            date=[]
            for m in range(nmonths):
                #sub df per month
                sub_df_id_crisis_month = sub_df_id_crisis[(sub_df_id_crisis['date_of_entry'] > starting_date_list[m]) & (sub_df_id_crisis['date_of_entry'] < ending_date_list[m])]
                list_score_crisis = sub_df_id_crisis_month.reliability_score.tolist()
                if len(list_score_crisis)==1:
                    value.append(list_score_crisis[0])
                    date.append(ending_date_list[m].replace('-31',''))
            if len(value)>0:
                diff=max(value)-min(value)
                if diff>1.9:
                    plotcrisis(value,date,i,counter,c)
        counter+=1

#__________________________________________________________
if __name__ == "__main__":
    #check arguments
    if len(sys.argv)!=2:
        print ("usage:")
        print ("python ",sys.argv[0]," file.json")
        print ("For example: python ",sys.argv[0]," data/isi_log.json")
        sys.exit(3)
        
    #check file exists
    if not exists(sys.argv[1]):
        print ('file does not exists')
        sys.exit(3)

    
    #run analysis
    run(sys.argv[1])
        
