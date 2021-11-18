"""
Inspired from a simple working example of accessing ACAPS API in the Python programming language.
"""

import pandas as pd
import requests
from datetime import datetime
import time
import json
import commons


#__________________________________________________________
def savefile(output,outfilename):
    data = {'results':output}
    with open('data/{}.json'.format(outfilename), 'w') as f:
            json.dump(data, f)


#__________________________________________________________
def get_token():
    # Post credentials to get an authentication token
    credentials = {
        "username": "clement.helsens@cern.ch", # Replace with your email address
        "password": "" # Replace with your password
    }

    auth_token_response = requests.post("https://api.acaps.org/api/v1/token-auth/", credentials)
    auth_token = auth_token_response.json()['token']

    return auth_token

#__________________________________________________________
def get_data(auth_token, request_urls):
    fulloutput=[]
    for request_url in request_urls:
        counter=0
        print ('recovering data for {}'.format(request_url))
        # Make the request
        response = requests.get(request_url, headers={"Authorization": "Token %s" % auth_token})
        last_request_time = datetime.now()
        response = response.json()
        output=response["results"]

        print ('we have {} counts, expects {} pages/requests in addition to the first one'.format(response["count"],int(response["count"]/100.)))
        
        # Loop to the next page; if we are on the last page, break the loop
        while True:
            if ("next" in response.keys()) and (response["next"] != None):
                request_url = response["next"]
                # Wait to avoid throttling
                while (datetime.now()-last_request_time).total_seconds() < 1:
                    time.sleep(0.1)

                response=requests.get(request_url, headers={"Authorization": "Token %s" % auth_token})
                counter+=1
                last_request_time = datetime.now()
                response = response.json()
                output+=response["results"]
                sys.stdout.write('\r')
                sys.stdout.write('page {}/{}'.format(counter,int(response["count"]/100.)))
                sys.stdout.flush()
            else: break

        #check that we got all the data
        if len(output)==response["count"]:
            sys.stdout.write('\r')
            print ('recovered all data for {}'.format(request_url))
        else: print('incomplete data, to be checked...')
        fulloutput+=output
        print ('fulloutput  ',len(fulloutput))
    return fulloutput

#__________________________________________________________
if __name__=="__main__":
    request_url = 'https://api.acaps.org/api/v1/'

    import argparse
    import sys
    parser = argparse.ArgumentParser()
    
    typeGroup = parser.add_argument_group('type of data to get')
    typeGroup.add_argument('--type', type=str, help='type of data to get', choices = ['isi','ha','isi_log'])
    typeGroup.add_argument('-N','--nmonths', type=int, default = 18, help='Number of month to import when relevant (isi and ha)')
    typeGroup.add_argument("--merge", action='store_true', help="merge the months")
    #parse arguments
    args, _ = parser.parse_known_args()

    #check
    if args.type==None:
        print('please specify a type of data, exit')
        sys.exit(3)
        
    #identify type of data to get to map to ACAPS terminology
    outfilename='{}_{}months'.format(args.type,args.nmonths)
    if args.type=='isi':request_url+='inform-severity-index/'
    elif args.type=='ha':request_url+='humanitarian-access/'
    elif args.type=='isi_log':
        request_url+='inform-severity-index/log/'
        outfilename='{}'.format(args.type)

    #get a token
    auth_token = get_token()

    #build the month to get the data when relevant
    request_urls=[]
    if  args.type=='isi' or  args.type=='ha':
        #get the current month and year
        dt = datetime.today()
        month=dt.month
        year=dt.year
        
        #add the current month but do not count it
        request_urls.append('{}{}{}/'.format(request_url,commons.monthcode[month-1],year))

        #go back in time the N months
        counter=0
        #start with current year
        for m in reversed(range(1,month)):
            request_urls.append('{}{}{}/'.format(request_url,commons.monthcode[m-1],year))
            counter+=1
            if counter>args.nmonths-1:break
                
        #continue with previous years, starting from 2019 when data are available
        from itertools import product
        for y, m in product(reversed(range(2019,year)),  reversed(range(1,12))):        
            request_urls.append('{}{}{}/'.format(request_url,commons.monthcode[m-1],y))
            counter+=1
            if counter>args.nmonths-1:
                break

    else: request_urls=[request_url]

    if args.merge:
        #make the request
        output = get_data(auth_token, request_urls)
        #save the file
        savefile(output, outfilename)

    else:
        for r in request_urls:
            #make the request
            output = get_data(auth_token, [r])
            savefile(output, args.type+'_'+r.split('/')[-2])

    
  
