# from multiprocessing import Pool
from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen,HTTPError,URLError
import json
import sys
import os
import ssl
import csv
import time

work_dir = "/home/peipei/RepoReaper/RegexCollection"
# str1="http://reporeapers.github.io/results/"
str1 = "https://reporeapers.github.io/results/"
str2 = ".html"
context = ssl._create_unverified_context()
# for i in range(1,4496): ##4496 pages may have different headers different
# first 3707: History    Issues    License    Size    Unit Test    State
# since 3708: History    License    Management    Unit Test    State
def getPairs(headers):
    lst = [header.text.strip() for header in headers]  # #for links, headers[1].string is NoneType
    pairs = {v:k for k, v in enumerate(lst)}
    return pairs

def processOnePage(i):
    results=list()
    results2=list()
    page = urlopen(''.join([str1, str(i), str2]), context=context)     
    soup = BeautifulSoup(page.read(), "lxml")
    print(i, len(soup.body.find_all('tr')))
    ###default to -1 index if not in keys get(header,-1)          
    for r,rep in enumerate(soup.body.find_all('tr')):     # get all rows except table header    
        if r==0:
            pairs = getPairs(rep.find_all('th')) ## x[0] has all headers
            #     print "headers: ", pairs
            headers=[u'Language', u'Unit Test', u'Links', u'Repository', u'Architecture', u'Community', u'CI', 
             u'Documentation', u'History', u'Issues', u'License', u'Size', u'State', u'# Stars']#, u'Timestamp']
            index=[pairs.get(header,-1) for header in headers]
            continue
        
        #if r<480:
        #    continue
        elements = rep.find_all('td')  # #get the columns of each row
        if len(elements)==0:  ##there is another header <tr> <th>...
            continue
#         print pairs
#         print headers
#         print index
#         print rep
        contents=[elements[i] if i>=0 else 'NA' for i in index]
#         print contents
#         print "link: ",elements[1]
#         lan=contents[0]
#         unit=contents[1]
#         unit=float(elements[11].string)
        if contents[0].string!="Java" or contents[1].string=='NA' or float(contents[1].string)==0.0: ###not satisfy requirements
            continue
        
        
        hrefs=contents[2].find_all('a', href=True)
        string_api = hrefs[0]['href']
        string_url = hrefs[1]['href']

        valid_api = True
        try:
            response=urlopen(string_api, context=context)
            webContent = response.read().decode('utf-8') ##need .decode('utf-8') in python3
            is_private=json.loads(webContent)['private']
            valid_api= not is_private
        except HTTPError as e:
            valid_api = False
            print(r, "api url HTTPError: ", e.code, e.args)
        except URLError as e:
            valid_api = False
            print(r, "api url URLError: ", e.code, e.args)

        valid_url = True
        try:
            response=urlopen(string_url, context=context)
            webContent = response.read()
            valid_url= webContent is not None
        except HTTPError as e:
            valid_url = False
            print(r, "repo url HTTPError: ", e.code, e.args)
        except URLError as e:
            valid_url = False
            print(r, "repo url URLError: ", e.code, e.args)

        #row,rep,vurl,url,vapi,api,unit(float),stars(int)  ##8
        #Architecture,Community,CI,Documentation,History,Issues,License,Size
        elem=(r,contents[3].string,valid_url,string_url,valid_api,string_api,float(contents[1].string), 'NA' if contents[13].string=='None' else int(contents[13].string.replace(',','')))
        elem2=(r,contents[4].string,contents[5].string,contents[6].string,contents[7].string,contents[8].string,contents[9].string,contents[10].string,contents[11].string,contents[12].string)
        results.append(elem)
        results2.append(elem2)
        
        time.sleep(20)
    
    return (results,results2)        

def writeToCSV(str_i,spec,results):
    file_name=str_i+"_"+spec+".csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(results)
        
if __name__ == '__main__':  # #python 2.7 version
    if sys.argv is None or len(sys.argv) < 2:  #
        sys.exit('Error! You need to specify begin and end or specific page number!!')
    
    os.chdir(work_dir)
    if len(sys.argv) == 2:
        page = sys.argv[1]    
        results,results2=processOnePage(int(page))  # #1, 2914, 3707, 4400
        writeToCSV(page,"bref",results)
        writeToCSV(page,"detail",results2)
        time.sleep(3600) ##pause 1500 seconds or 25 mins
    elif len(sys.argv) == 3:   ###[begin,end)
        begin = sys.argv[1]
        end = sys.argv[2]
        # pool = Pool(processes=2)            # start 4 worker processes ##intotal it has 4 cores
        # print(pool.map(processOnePage, range(int(begin),int(end))))       # prints "[0, 1, 4,..., 81]"
        # pool.terminate()
        for page in range(int(begin), int(end)):
            results,results2=processOnePage(page)
            writeToCSV(str(page),"bref",results)
            writeToCSV(str(page),"detail",results2)
            time.sleep(3600) ##pause 1500 seconds or 25 mins
    print("-----------end-----------")
