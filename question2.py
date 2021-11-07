import json
import pandas as pd
import sys
from os.path import exists
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

#__________________________________________________________
def plot(list,date,ind,i):
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.xlabel('indicator reliability score')
    plt.hist(list, 5, range=[0,5], facecolor='g', alpha=0.75)
    plt.text(0.02, 1.02,'indicator={}'.format(ind),transform = ax.transAxes)
    plt.text(0.02, 0.95, r'$\mu={:.3f},\ \sigma={:.3f}$'.format(np.mean(list),np.std(list)),transform = ax.transAxes)
    plt.text(0.02, 0.9,'number of data points={}'.format(len(list)),transform = ax.transAxes)

    plt.savefig('plots/indicator{}_{}.png'.format(i,date))
    plt.savefig('plots/indicator{}_{}.pdf'.format(i,date))
    plt.close()


#__________________________________________________________
def ploterr(mean,std,num,date,ind,i):


#fig, ax1 = plt.subplots()

#ax2 = ax1.twinx()
#ax1.plot(x, y1, 'g-')
#ax2.plot(x, y2, 'b-')

#ax1.set_xlabel('X data')
#ax1.set_ylabel('Y1 data', color='g')
#ax2.set_ylabel('Y2 data', color='b')
    
    f, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.errorbar(date, mean, yerr=std, label='both limits (default)',  marker='o', ms=7, color='b')
    ax2.plot(date, num, 'r-')
    
    ax1.set_xticks(ax1.get_xticks())    
    ax1.set_xticklabels(date, rotation=45, fontsize=8)    
    ax1.set_ylabel('indicator reliability score (mean value)', color='b')
    ax2.set_ylabel('number of data points', color='r')
    
    ax1.text(0.02, 1.02,'indicator={}'.format(ind),transform = ax1.transAxes)
    plt.savefig('plots/indicator{}_vs_time.png'.format(i))
    plt.savefig('plots/indicator{}_vs_time.pdf'.format(i))
    plt.close()


    #ticks_loc = ax2.get_yticks().tolist()
#ax2.set_yticks(ax1.get_yticks().tolist())
#ax2.set_yticklabels([label_format.format(x) for x in ticks_loc])


#__________________________________________________________
def run(fname):
    # loading data into json dict and df
    f = open(fname)
    data = json.load(f)
    df = pd.DataFrame()
    df = df.append(pd.DataFrame(data["results"]))
    sub_df = df[['crisis_id','source_and_date','date_of_entry','reliability', 'reliability_score','indicator']]
    print(sub_df.head)
    print(sub_df.columns)
    print(sub_df['indicator'])
    print(sub_df.indicator.unique().tolist())
    print(len(sub_df.indicator.unique()))

    #filter date
    sub_df = sub_df[sub_df['date_of_entry'] > '2020-04-01']
    print(sub_df.head)

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

    starting_date_list=list(reversed(starting_date_list))
    ending_date_list=list(reversed(ending_date_list))
    #loop over indicators
    indicator_list = sub_df.indicator.unique().tolist()
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
        #print(sub_df_month_id)
    #print(sub_df.head)
    #print(sub_df.indicator.unique().tolist())
    #print(len(sub_df.indicator.unique()))

#__________________________________________________________
if __name__ == "__main__":
    #check arguments
    print (len(sys.argv))
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
        
