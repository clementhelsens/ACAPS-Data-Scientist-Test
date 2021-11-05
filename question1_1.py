import json
import pandas as pd
import sys
from os.path import exists
from datetime import datetime

#__________________________________________________________
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

#__________________________________________________________
def run(fname, latex):
    # loading data into json dict and df
    f = open(fname)
    data = json.load(f)
    df = pd.DataFrame()
    df = df.append(pd.DataFrame(data["results"]))

    #create sub dataframe
    sub_df = df[['Last updated','crisis_id','INFORM Severity Index']]
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
    sub_df = sub_df.sort_values(["crisis_id", "Last updated"], ascending = (True, True))
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print (sub_df)


    #get the list of crisis
    crisis_list=[]
    for c in data['results']:
        if c['crisis_id'] not in crisis_list: crisis_list.append(c['crisis_id'])
        #if c['crisis_id']=='AFG001':
        #    print (c)
        #    print('')


    #get head, tail, min and max values and corresponding date of each crisis
    print ('Over the last 18 months, the following crises have a larger "INFORM Severity Index" at the last update with respect to the first entry in the database')
    print ('id\tdate begin\tdate end\tduration\tisi begin\tisi end\t\tisi diff')
    for c in crisis_list:
        sub_df_crisis =  sub_df[sub_df['crisis_id'].isin([c])]
        #continue if df is empty
        if sub_df_crisis.empty:continue

        isi_head = sub_df_crisis.head(1)['INFORM Severity Index'].values[0]
        isi_tail = sub_df_crisis.tail(1)['INFORM Severity Index'].values[0]

        date_head    = sub_df_crisis.head(1)['Last updated'].values[0]
        date_tail    = sub_df_crisis.tail(1)['Last updated'].values[0]

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

        max_isi  = sub_df_crisis.loc[sub_df_crisis['INFORM Severity Index'].idxmax()].values[2]
        min_isi  = sub_df_crisis.loc[sub_df_crisis['INFORM Severity Index'].idxmin()].values[2]

        max_isi_date = sub_df_crisis.loc[sub_df_crisis['INFORM Severity Index'].idxmax()].values[0]
        min_isi_date = sub_df_crisis.loc[sub_df_crisis['INFORM Severity Index'].idxmin()].values[0]

        if (max_isi_date>min_isi_date and days_between(max_isi_date,min_isi_date)>0) and (max_isi-min_isi)>(isi_tail-isi_head):
            if latex:
                print (c,'&',min_isi_date,'&',max_isi_date,'&',days_between(max_isi_date,min_isi_date),'&',min_isi,'&',max_isi,'&',"{:.2f}".format(max_isi-min_isi),'\\\\')
            else:
                print (c,'\t',min_isi_date,'\t',max_isi_date,'\t',days_between(max_isi_date,min_isi_date),'\t\t',min_isi,'\t\t',max_isi,'\t\t',"{:.2f}".format(max_isi-min_isi))


                          
    # Closing file
    f.close()


#__________________________________________________________
if __name__ == "__main__":
    #check arguments
    print (len(sys.argv))
    if len(sys.argv)!=2 and len(sys.argv)!=3:
        print ("usage:")
        print ("python ",sys.argv[0]," file.json <latex>")
        print ("For example: python ",sys.argv[0]," data/isi_18months.json")
        sys.exit(3)
        
    #check file exists
    if not exists(sys.argv[1]):
        print ('file does not exists')
        sys.exit(3)

    #latex flag for tables
    latex=False
    if len(sys.argv)==3: latex=True

    #run analysis
    run(sys.argv[1], latex)
        




    

    
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print (sub_df)

#df_test =
#print ('=============df test')
#print (df_test)
#print ('=============df test')
#print (df_test.head(1)['INFORM Severity Index'].values)
#print (df_test.tail(1)['INFORM Severity Index'].values)
#sub_df = sub_df.sort_values(by="crisis_id")
#print (sub_df)
#get the last valid INFORM Severity Index for all crisis_id
#for i in crisis_id: print('------',sub_df[i])

#print ("---------------------",type(data["results"]))
#print ("---------------------",len(data["results"]))
#print ("---------------------",len(data["results"][0]))
#print ("c id  ",len(crisis_id))
#sys.exit(3)
#get the last valid INFORM Severity Index for all crisis_id


#stuff to remove
#print (df.shape)
#print (df.head)
#print (df.columns)
#print (len(df))
#print (df[['crisis_id','INFORM Severity Index','Last updated']])


