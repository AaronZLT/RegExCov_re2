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
#work_dir = "/home/pwang7/results"
# str1="http://reporeapers.github.io/results/"
str1 = "https://reporeapers.github.io/results/"
str2 = ".html"
context = ssl._create_unverified_context()
tokens={'lab':'54bc79cb7af38b6da15bb192c0056ee628bce809','spark1':'5a01686409b43a672db482c99bf05c4655734893','spark2':'5d5df7d0eab41e6a7d5cd5340cf795431df9f017','spark3':'c6f077fb144638ec0f77c41ad9268074a6f3d889','spark4':'a7ba4128d5059e6cfe877be5cd0c07f67e4748a7'}
access='?access_token='
# for i in range(1,4496): ##4496 pages may have different headers different
# first 3707: History    Issues    License    Size    Unit Test    State
# since 3708: History    License    Management    Unit Test    State
def getPairs(headers):
    lst = [header.text.strip() for header in headers]  # #for links, headers[1].string is NoneType
    pairs = {v:k for k, v in enumerate(lst)}
    return pairs

def visitAPI(i,r,api_url):
    access='?access_token='+tokens['lab']
    tries=0
    while tries<2:
        valid_api = True
        try:
            response=urlopen(api_url+access, context=context)
            webContent = response.read().decode('utf-8') ##need .decode('utf-8') in python3
            is_private=json.loads(webContent)['private']
            valid_api= not is_private
            star=json.loads(webContent)['stargazers_count']
            watcher=json.loads(webContent)['watchers_count']
            size=json.loads(webContent)['size']
            return int(star),int(watcher), int(size)
        except HTTPError as e:
            valid_api = False
            print("page: ",i,"row: ",r, "api url HTTPError: ", e.code, e.args)           
            if e.code==403:                    
                if tries<1:
                    time.sleep(3600)
                tries+=1
                continue
                
        except URLError as e:
            valid_api = False
            print("page: ",i,"row: ",r, "api url URLError: ", e.code, e.args)
        return None
    
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
        
        if r<494:
            continue
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
        if contents[0].string!="Java" or contents[1].string=='None' or float(contents[1].string)==0.0: ###not satisfy requirements
            continue
        
        
        hrefs=contents[2].find_all('a', href=True)
        string_api = hrefs[0]['href']
        string_url = hrefs[1]['href']

        tries=0
        while tries<2:
            valid_api = True
            try:
                response=urlopen(string_api+access, context=context)
                webContent = response.read().decode('utf-8') ##need .decode('utf-8') in python3
                is_private=json.loads(webContent)['private']
                valid_api= not is_private
                
                ##get rate limit remaining and sleep one hour if it is 0
    #             left_rate=int(response.info().get('X-RateLimit-Remaining'))
    #             if left_rate<5:
    #                 time.sleep(3600)
            except HTTPError as e:
                valid_api = False
                print(r, "api url HTTPError: ", e.code, e.args)           
                if e.code==403:                    
                    if tries<1:
                        time.sleep(3600)
                    tries+=1
                    continue
                    
            except URLError as e:
                valid_api = False
                print(r, "api url URLError: ", e.code, e.args)
            break

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
        ## 9 is issues 11:size
        elem2=(r,contents[4].string,contents[5].string,contents[6].string,contents[7].string,contents[8].string,'NA' if contents[9]=='NA' else contents[9].string,contents[10].string,'NA' if contents[11]=='NA' else contents[11].string,contents[12].string)
        results.append(elem)
        results2.append(elem2)
        
#         time.sleep(20)
    
    return (results,results2)        

def writeToCSV(str_i,spec,results):
    file_name=str_i+"_"+spec+".csv"
    with open(file_name,'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(results)
        
if __name__ == '__main__':  # #python 2.7 version
    if sys.argv is None or len(sys.argv) < 2:  #
        sys.exit('Error! You need to specify begin and end or specific page number!!')
    
    access=access+tokens['lab']
    os.chdir(work_dir)
    if len(sys.argv) == 2:
        page = sys.argv[1]    
        results,results2=processOnePage(int(page))  # #1, 2914, 3707, 4400
        writeToCSV(page,"bref",results)
        writeToCSV(page,"detail",results2)
#         time.sleep(3600) ##pause 1500 seconds or 25 mins
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
#             time.sleep(3600) ##pause 1500 seconds or 25 mins
    print("-----------end-----------")
