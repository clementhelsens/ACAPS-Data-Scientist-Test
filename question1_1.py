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
    print('---- data set size original\t\t',len(sub_df))
    crisis_list_test = sorted(list(set([c for c in sub_df['crisis_id']])))
    print('---- number of crisis original\t\t',len(crisis_list_test))

    #filter when INFORM Severity Index is Null
    sub_df = sub_df.dropna()
    print('---- data set size filter null\t\t',len(sub_df))
    crisis_list_test = sorted(list(set([c for c in sub_df['crisis_id']])))
    print('---- number of crisis filter null\t',len(crisis_list_test))

    #filter when we have at least two entries for a given crisis
    sub_df=sub_df.groupby("crisis_id").filter(lambda x: len(x) > 1)
    print('---- data set size filter >1\t\t',len(sub_df))
    crisis_list_test = sorted(list(set([c for c in sub_df['crisis_id']])))
    print('---- number of crisis filter >1\t\t',len(crisis_list_test))

    #count the number of occurence of each crisis
    #crisis_count = sub_df['crisis_id'].value_counts()
    #crisis_list = crisis_count.tolist()
    
    #sort by crisis_id and date
    sub_df = sub_df.sort_values(["crisis_id", "Last updated"], ascending = (True, True))
    
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #    print (sub_df)

    #get the list of crisis
    crisis_list = sorted(list(set([c for c in sub_df['crisis_id']])))
    #get head, tail, min and max values and corresponding date of each crisis
    print ('Over the last 18 months, the following crises have a larger "INFORM Severity Index" at the last update with respect to the first entry in the database')
    print ('number\tid\tdate begin\tdate end\tduration\tisi begin\tisi end\t\tisi diff')
    counter=0
    for c in crisis_list:
        sub_df_crisis =  sub_df[sub_df['crisis_id'].isin([c])]
        #continue if df is empty (should not be the case...)
        if sub_df_crisis.empty:continue

        isi_head = sub_df_crisis.head(1)['INFORM Severity Index'].values[0]
        isi_tail = sub_df_crisis.tail(1)['INFORM Severity Index'].values[0]

        date_head    = sub_df_crisis.head(1)['Last updated'].values[0]
        date_tail    = sub_df_crisis.tail(1)['Last updated'].values[0]

        if isi_tail>isi_head:
            if latex:
                print (counter,'&',c,'&',date_head,'&',date_tail,'&',days_between(date_head,date_tail),'&',isi_head,'&',isi_tail,'&',"{:.2f}".format(isi_tail-isi_head),'\\\\')
            else:
                print (counter,'\t',c,'\t',date_head,'\t',date_tail,'\t',days_between(date_head,date_tail),'\t\t',isi_head,'\t\t',isi_tail,'\t\t',"{:.2f}".format(isi_tail-isi_head))
            counter+=1

    counter=0
    print ('')
    print ('Over the last 18 months, the following crises have an "INFORM Severity Index" that has increased wrt a previous minimum, and thus shows a larger increase with respect to first - last entry')
    print ('number\tid\tdate min\tdate max\tduration\tisi min\t\tisi max\t\tisi diff')
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
                print (counter,'&',c,'&',min_isi_date,'&',max_isi_date,'&',days_between(max_isi_date,min_isi_date),'&',min_isi,'&',max_isi,'&',"{:.2f}".format(max_isi-min_isi),'\\\\')
            else:
                print (counter,'\t',c,'\t',min_isi_date,'\t',max_isi_date,'\t',days_between(max_isi_date,min_isi_date),'\t\t',min_isi,'\t\t',max_isi,'\t\t',"{:.2f}".format(max_isi-min_isi))

            counter+=1
                          
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
        




    


