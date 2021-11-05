import json
import pandas as pd
import sys
from datetime import datetime
import commons

#__________________________________________________________
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

#__________________________________________________________
def run(sub_df, latex):

    print('---- size original\t',len(sub_df))

    #filter when INFORM Severity Index is Null
    sub_df = sub_df.dropna(thresh=3)
    print('---- size filter null\t',len(sub_df))

    #filter when we have at least two entries for a given crisis
    sub_df=sub_df.groupby("crisis_id").filter(lambda x: len(x) > 1)
    print('---- size filter >1\t',len(sub_df))

    #count the number of occurence of each crisis
    #crisis_count = sub_df['crisis_id'].value_counts()
    #crisis_list = crisis_count.tolist()
    
    #sort by crisis_id and date
    sub_df = sub_df.sort_values(["crisis_id", "date"], ascending = (True, True))
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print (sub_df)


    #get the list of crisis
    crisis_list=[]
    for c in sub_df['crisis_id']:
        if c not in crisis_list: crisis_list.append(c)


    #get head, tail, min and max values and corresponding date of each crisis
    print ('Over the last 18 months, the following crises have a larger "INFORM Severity Index" at the last update with respect to the first entry in the database')
    print ('id\tdate begin\tdate end\tduration\tisi begin\tisi end\t\tisi diff')
    for c in crisis_list:
        sub_df_crisis =  sub_df[sub_df['crisis_id'].isin([c])]
        #continue if df is empty
        if sub_df_crisis.empty:continue

        isi_head = sub_df_crisis.head(1)['INFORM Severity Index'].values[0]
        isi_tail = sub_df_crisis.tail(1)['INFORM Severity Index'].values[0]

        date_head    = sub_df_crisis.head(1)['date'].values[0]
        date_tail    = sub_df_crisis.tail(1)['date'].values[0]

        if isi_tail>isi_head:
            if latex:
                print (c,'&',date_head,'&',date_tail,'&',days_between(date_head,date_tail),'&',isi_head,'&',isi_tail,'&',"{:.2f}".format(isi_tail-isi_head),'\\\\')
            else:
                print (c,'\t',date_head,'\t',date_tail,'\t',days_between(date_head,date_tail),'\t\t',isi_head,'\t\t',isi_tail,'\t\t',"{:.2f}".format(isi_tail-isi_head))

    print ('')
    print ('Over the last 18 months, the following crises have an "INFORM Severity Index" that has increased wrt a previous minimum, and thus shows a larger increase with respect to first - last entry')
    print ('id\tdate min\tdate max\tduration\tisi min\t\tisi max\t\tisi diff')
    for c in crisis_list:
        sub_df_crisis =  sub_df[sub_df['crisis_id'].isin([c])]
        #continue if df is empty
        if sub_df_crisis.empty:continue
    
        isi_head = sub_df_crisis.head(1)['INFORM Severity Index'].values[0]
        isi_tail = sub_df_crisis.tail(1)['INFORM Severity Index'].values[0]

        #this is a bit dirty, to be changed if time allows
        dates=[]
        values=[]
        for i in range(len(sub_df_crisis['crisis_id'])):
            dates.append(sub_df_crisis['date'].values[i])
            values.append(sub_df_crisis['INFORM Severity Index'].values[i])

        maxid=values.index(max(values))
        minid=values.index(min(values))

        max_isi  = values[maxid]
        min_isi  = values[minid]

        max_isi_date = dates[maxid]
        min_isi_date = dates[minid]

        if (max_isi_date>min_isi_date and days_between(max_isi_date,min_isi_date)>0) and (max_isi-min_isi)>(isi_tail-isi_head):
            if latex:
                print (c,'&',min_isi_date,'&',max_isi_date,'&',days_between(max_isi_date,min_isi_date),'&',min_isi,'&',max_isi,'&',"{:.2f}".format(max_isi-min_isi),'\\\\')
            else:
                print (c,'\t',min_isi_date,'\t',max_isi_date,'\t',days_between(max_isi_date,min_isi_date),'\t\t',min_isi,'\t\t',max_isi,'\t\t',"{:.2f}".format(max_isi-min_isi))



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
    files=[f for f in files if 'months' not in f and  'log' not in f]

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
        
