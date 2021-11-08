__author__ = "Clement Helsens"
__email__ = "clement.helsens@gmail.com"

import json
import pandas as pd
import sys
from datetime import datetime
import commons
import matplotlib.pyplot as plt
import numpy as np


#__________________________________________________________
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

#__________________________________________________________
def maxincrease(x):
    max=-9999
    for i in range(0,len(x)-1):
        for j in range(i+1,len(x)):
            if x[j]-x[i]>max:max= x[j]-x[i]
    return max

#__________________________________________________________
def maxdecrease(x):
    max=9999
    for i in range(0,len(x)-1):
        for j in range(i+1,len(x)):
            if x[j]-x[i]<max:max= x[j]-x[i]
    return max

#__________________________________________________________
def graph(x,y,dir,c):
    #plot the correlations versus time
    f = plt.figure()
    ax = f.add_subplot(111)
    plt.plot(x, y, marker='o', ms=5, color='b')
    ax.set_ylim([1, 5.5])
    
    yval=0.95
    ymin=0.
    ymax=3.5/4.5
    if np.mean(y)>3.25:
        yval=0.12
        ymin=1-3.5/4.5
        ymax=1.
    for i in range(len(x)):
        ax.axvline(x=i, linestyle='--', color='r', ymin=ymin, ymax=ymax, linewidth=1, alpha=0.2)
    for i in range(9):
        if ymax==1 and 1+i*0.5>1.9:
            ax.axhline(y=1+i*0.5, linestyle='--', color='g', linewidth=1, alpha=0.2)
        elif ymax<1 and 1+i*0.5<4.6:
            ax.axhline(y=1+i*0.5, linestyle='--', color='g', linewidth=1, alpha=0.2)
       
    plt.ylabel('ACCESS humanitarian index')
    plt.text(0.02, yval,'crisis_id={}'.format(c),transform = ax.transAxes, fontsize=9)
    plt.text(0.02, yval-1*0.05,'number of months={}'.format(len(x)),transform = ax.transAxes, fontsize=9)
    plt.text(0.02, yval-2*0.05, r'$\mu={:.3f},\ \sigma={:.3f}$'.format(np.mean(y),np.std(y)),transform = ax.transAxes, fontsize=9)

    plt.text(0.35, yval,'increase last-first={:.2f}'.format(y[-1]-y[0]),transform = ax.transAxes, fontsize=9)
    plt.text(0.35, yval-1*0.05,'max increase={:.2f}'.format(maxincrease(y)),transform = ax.transAxes, fontsize=9)
    plt.text(0.35, yval-2*0.05,'max decrease={:.2f}'.format(maxdecrease(y)),transform = ax.transAxes, fontsize=9)
    
    plt.xticks(fontsize=8,rotation=45)
    plt.savefig('plots/{}/isi_{}.png'.format(dir,c))
    plt.savefig('plots/{}/isi_{}.pdf'.format(dir,c))
    plt.close()

#__________________________________________________________
def histo(x,dir,name):
    mean=np.mean(x)
    std=np.std(x)
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.set_ylim([0, 60])
    ax.set_xlim([0, 2.5])

    plt.hist(x, 20, facecolor='g', alpha=0.75)
    plt.ylabel('number of crises')
    plt.xlabel('index difference (max-min)')
    plt.text(0.5, 0.9, r'$\mu={:.3f},\ \sigma={:.3f}$'.format(mean,std),transform = ax.transAxes)
    plt.text(0.5, 0.85,'number of crises={}'.format(len(x)),transform = ax.transAxes)
    plt.savefig('plots/{}/{}.png'.format(dir,name))
    plt.savefig('plots/{}/{}.pdf'.format(dir,name))
    plt.close()
    
#__________________________________________________________
def run(sub_df, latex):

    print('---- data set size original\t\t',len(sub_df))
    crisis_list_test =  sorted(sub_df.crisis_id.unique().tolist())
    print('---- number of crises original\t\t',len(crisis_list_test))

    #filter when INFORM Severity Index is Null
    sub_df = sub_df.dropna()
    print('---- data set size filter null\t\t',len(sub_df))
    crisis_list_test = sorted(sub_df.crisis_id.unique().tolist())
    print('---- number of crises filter null\t',len(crisis_list_test))

    #filter when we have at least two entries for a given crisis
    sub_df=sub_df.groupby("crisis_id").filter(lambda x: len(x) > 1)
    print('---- data set size filter >1\t\t',len(sub_df))
    crisis_list_test = sorted(sub_df.crisis_id.unique().tolist())
    print('---- number of crises filter >1\t\t',len(crisis_list_test))
   
    #sort by crisis_id and date
    sub_df = sub_df.sort_values(["crisis_id", "date"], ascending = (True, True))

    #get the list of crisis
    crisis_list = sorted(sub_df.crisis_id.unique().tolist())

    #get head, tail, min and max values and corresponding date of each crisis
    print ('Over the last 18 months, the following crises have a larger "INFORM Severity Index" at the last update with respect to the first entry in the database')
    print ('number\tid\t\tvar(last-first)\tmax increase\tmax decrease')
    counter=1
    counter_inc=0
    counter_dec=0
    counter_sta=0
    counter_inc_rel=0
    list_inc_full=[]
    list_inc_max=[]
    
    for c in crisis_list:
        sub_df_crisis =  sub_df[sub_df['crisis_id'].isin([c])]
        #continue if df is empty
        if sub_df_crisis.empty:continue

        #plot index versus time
        index = [c for c in sub_df_crisis['INFORM Severity Index']]
        date  = [c[:7] for c in sub_df_crisis['date']]
        for d in range(len(date)):
            m=int(date[d].split('-')[-1])
            date[d]=commons.monthcode[m-1]+date[d].split('-')[0]
        graph(date,index,'question1/isi_vs_time',c)

        increase_last_first = index[-1]-index[0]
        increase_max = maxincrease(index)
        decrease_max = maxdecrease(index)

        #if increase_last_first>0 or increase_max>0:
        if latex:
            if increase_max>0:
              print ('\color{red}{',counter,'}','&','\color{red}{',c,'}','&','\color{red}{',"{:.2f}".format(increase_last_first),'}','&','\color{red}{',"{:.2f}".format(increase_max),'}','&','\color{red}{',"{:.2f}".format(decrease_max),'}\\\\')

            else:
                print (counter,'&',c,'&',"{:.2f}".format(increase_last_first),'&',"{:.2f}".format(increase_max),'&',"{:.2f}\\\\".format(decrease_max))
        else:        print (counter,'\t',c,'\t',"{:.2f}".format(increase_last_first),'\t\t',"{:.2f}".format(increase_max),'\t\t',"{:.2f}".format(decrease_max))

        counter+=1
        if increase_last_first>0:
            counter_inc+=1
            list_inc_full.append(increase_last_first)
        elif increase_last_first==0:counter_sta+=1
        else: counter_dec+=1
        if increase_max>0:
            counter_inc_rel+=1
            list_inc_max.append(increase_max)
    print('over the full period the number of crises out of {} that have: increase={}   decrease={}   stable={}'.format(len(crisis_list),counter_inc,counter_dec,counter_sta))
    print('within each time period {} crises out of {} have suffered from an increase of the index'.format(counter_inc_rel,len(crisis_list),))
    histo(list_inc_full,'question1/isi_fullstat','isi_inc_full')
    histo(list_inc_max,'question1/isi_fullstat','isi_inc_max')

    
#__________________________________________________________
def build(files):
    output = pd.DataFrame()
    for fname in files:
        # loading data into json dict and df
        f = open(fname)
        data = json.load(f)
        df = pd.DataFrame()
        df = df.append(pd.DataFrame(data["results"]))

        #create sub dataframe
        sub_df = df[['crisis_id','INFORM Severity Index']]

        #get the date from file name
        year=fname.split('/')[-1].split('_')[-1].replace('.json','')[3:]
        month=fname.split('/')[-1].split('_')[-1].replace('.json','')[:3]
        month=commons.monthcode.index(month)+1
        if month<10:month='0{}'.format(str(month))
        date='{}-{}-01'.format(year,month)
        
        sub_df=sub_df.assign(date=date)
        output=output.append(sub_df)
        
        # Closing file
        f.close()
    return output
#__________________________________________________________
if __name__ == "__main__":
    #check arguments
    if len(sys.argv)!=2 and len(sys.argv)!=3:
        print ("usage:")
        print ("python ",sys.argv[0]," \"files*.json\" <latex>")
        print ("For example: python ",sys.argv[0]," data/isi_*.json")
        sys.exit(3)

    #get the list of files
    import glob
    files=glob.glob(sys.argv[1])
    files=[f for f in files if  'log' not in f]

    #check the list is not 0
    if len(files)==0:
        print ('no files found, exit')
        sys.exit(3)

    #latex flag for tables
    latex=False
    if len(sys.argv)==3: latex=True

    #build the data as results:{date,crisis_id,INFORM Severity Index}, with date being the first day of the month
    output=build(files)
    
    #run analysis
    run(output, latex)
        
