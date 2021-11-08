__author__ = "Clement Helsens"
__email__ = "clement.helsens@gmail.com"

import json
import pandas as pd
import sys
from os.path import exists
from datetime import datetime
import numpy as np
import commons
import matplotlib.pyplot as plt
from itertools import groupby

#__________________________________________________________
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

#__________________________________________________________
def build(files,name):
    output = pd.DataFrame()
    for fname in files:
        # loading data into json dict and df
        f = open(fname)
        data = json.load(f)
        df = pd.DataFrame()
        df = df.append(pd.DataFrame(data["results"]))
        if  df.empty:continue

        #create sub dataframe
        sub_df = df[['crisis_id',name]]

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
def run(output1,output2,dir,name):   
    #build the data as results:{date,crisis_id,INFORM Severity Index,ACCESS}, with date being the first day of the month
    merged_df=pd.merge(output1,output2, how='inner')

    #filter when INFORM Severity Index or ACCESS is Null
    merged_df = merged_df.dropna()

    #make sub df with only "INFORM Severity Index" and "ACCESS"
    sub_merged_df = merged_df[['INFORM Severity Index','ACCESS']]

    #convert to numpy
    array=sub_merged_df.to_numpy()

    #1d array
    isi_1d=array[:,0:1].flatten()
    ha_1d=array[:,1:2].flatten()

    #do not calculate the correlations if one of the input array has the same values
    if all_equal(ha_1d) or all_equal(isi_1d):return []

    #calculate the correlation using all the data
    corr = np.corrcoef(isi_1d,ha_1d)

    #make a scatter plot
    scatterplot(isi_1d,ha_1d,dir,name,corr[0,1])
    
    return corr

#__________________________________________________________
def scatterplot(var1,var2,dir,name,value):
    nameplot=name
    #check if full stat
    if '2020' in name or '2021' in name: name='fullstat-'+name
    
    #build new var to take into account the same data points (to increase the marker size)
    var1_merge=[var1[0]]
    var2_merge=[var2[0]]
    size=[1]
    for i in range(1,len(var1)):
        found=False
        pos=-1
        for j in range(len(var1_merge)):
            if var1[i] == var1_merge[j] and var2[i] == var2_merge[j]:
                found=True
                pos=j
        if found:
            size[j]=size[j]+1
        else:
            var1_merge.append(var1[i])
            var2_merge.append(var2[i])
            size.append(1)
    size=[s*10 for s in size]
    
    #do the scatter plot
    f=plt.figure()
    ax = f.add_subplot(111)
    plt.xlim([0, 6])
    plt.ylim([-1, 6])
    plt.scatter(var1_merge, var2_merge, s=size, alpha=0.5)
    plt.xlabel('INFORM Severity index')
    plt.ylabel('ACCESS humanitarian index')
    plt.text(0.01, 1.01,'correlation={:.4f}'.format(value),transform = ax.transAxes)
    plt.text(0.01, 0.96,'crisis_id={}'.format(name),transform = ax.transAxes)
    plt.text(0.01, 0.91,'number of crises={}'.format(len(var1)),transform = ax.transAxes)
    
    plt.savefig('plots/{}/scatter_{}.png'.format(dir,nameplot))
    plt.savefig('plots/{}/scatter_{}.pdf'.format(dir,nameplot))
    plt.close()
    
#__________________________________________________________
if __name__ == "__main__":
    #check arguments
    if len(sys.argv)!=3:
        print ("usage:")
        print ("python ",sys.argv[0]," file.json file.json")
        print ("For example: python ",sys.argv[0]," \"data/isi_*.json\" \"data/ha_*.json\"")
        sys.exit(3)

    #get the list of files
    import glob
    files1=glob.glob(sys.argv[1])
    files1=[f for f in files1 if 'months' not in f and  'log' not in f]
    files2=glob.glob(sys.argv[2])
    files2=[f for f in files2 if 'months' not in f and  'log' not in f]

    #check the list is not 0
    if len(files1)==0 or len(files2)==0:
        print ('no files found, exit')
        sys.exit(3)

    #build the data as results:{date,crisis_id,INFORM Severity Index}, with date being the first day of the month
    output1=build(files1,"INFORM Severity Index")

    #build the data as results:{date,crisis_id,ACCESS}, with date being the first day of the month
    output2=build(files2,"ACCESS")

    #run the correlation
    corr=run(output1,output2,'question3/correlation_fullstat','fullstat')
    
    print('============ correlation between "INFORM Severity Index" and "Humanitarian ACCESS" using all the crises and all the data: ',corr[0,1])

    #calculate the correlation per month using all the crises (could be done more elegantly if times allows)
    corr_months = []
    for f_isi in files1:
        f_ha = f_isi.replace('isi','ha')
        #build the data as results:{date,crisis_id,INFORM Severity Index}, with date being the first day of the month
        output1=build([f_isi],"INFORM Severity Index")

        #build the data as results:{date,crisis_id,ACCESS}, with date being the first day of the month
        output2=build([f_ha],"ACCESS")

        if output1.empty or output2.empty:continue
        
        #run the correlation
        monthname=f_isi.replace('data/isi_','').replace('.json','')
        corr=run(output1,output2,'question3/correlation_date',monthname)
        corr_months.append([monthname,corr[0,1]])
        
    #order the dates
    corr_ordered=[]
    month_ordered=[]
    for y in commons.years:
        for m in commons.monthcode:
            for c in corr_months:
                if m+y == c[0]:
                    corr_ordered.append(c[1])
                    month_ordered.append(c[0])

    #plot the correlations versus time using all crises
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.set_ylim([0.2, 0.8])
    plt.ylabel('Correlation coefficient')

    plt.plot(month_ordered, corr_ordered, marker='o', ms=5, color='b')
    plt.xticks(fontsize=8,rotation=45)
    plt.grid(True, alpha=0.2,color='g')
    plt.savefig('plots/question3/correlation_fullstat/correlation_vs_time.png')
    plt.savefig('plots/question3/correlation_fullstat/correlation_vs_time.pdf')
    plt.close()
    
    #calculate the correlation for each crisis (could be done more elegantly if times allows)
    #build the data as results:{date,crisis_id,INFORM Severity Index}, with date being the first day of the month
    output1=build(files1,"INFORM Severity Index")
    output1 = output1.dropna()

    #build the data as results:{date,crisis_id,ACCESS}, with date being the first day of the month
    output2=build(files2,"ACCESS")
    output2 = output2.dropna()

    #get the list of crisis of one dataset (as we want the same crisis to appear in both, it does not matter which one we choose)
    #crisis_list = sorted(list(set([c for c in output1['crisis_id']])))
    crisis_list = sorted(output1.crisis_id.unique().tolist())

    corr_crisis=[]
    nocorr=[]
    for c in crisis_list:
        crisis_df1=output1[output1.crisis_id.isin([c])]
        crisis_df2=output2[output2.crisis_id.isin([c])]
        
        #run the correlation
        corr=run(crisis_df1,crisis_df2,'question3/correlation_crisis',c)
        if len(corr)==0:
            print('============ can not calculate correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id ',c)
            nocorr.append(c)
            continue
        
        print('============ correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id ',c,' ',corr[0,1])
        corr_crisis.append(corr[0,1])
    print('unable to calculate correlations for {} out of {} crises, list: {}'.format(len(nocorr),len(crisis_list),nocorr))

    #plot the distribution of correlation coefficient
    mean = np.mean(corr_crisis)
    std  = np.std(corr_crisis)
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.set_ylim([0., 20.])
    plt.hist(corr_crisis, 25, facecolor='g', alpha=0.75)
    plt.text(-0.75, 15., r'$\mu={:.3f},\ \sigma={:.3f}$'.format(mean,std))
    plt.xlabel('Correlation coefficient')
    plt.ylabel('Number of crises')

    plt.savefig('plots/question3/correlation_fullstat/correlation_crisis.png')
    plt.savefig('plots/question3/correlation_fullstat/correlation_crisis.pdf')
    plt.close()
    
        
