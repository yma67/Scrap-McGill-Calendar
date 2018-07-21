from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import json

#data structure for storing course information
course_info=dict()
listdecours=list()


#to open url behaving as a web brawser
def openurl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    if url.find("https://www.mcgill.ca") == -1:
        req = Request(url="https://www.mcgill.ca" + url, headers=headers)
    else:
        req = Request(url=url, headers=headers)
    try:
        res = urlopen(req)
    except HTTPError as e:
        return None
    bsobj = BeautifulSoup(res)
    return bsobj


#given a string of prof, parse them to output a dictionary (term->instructors)
def process1_name(namestr):
    ent=dict()
    iterady=list()
    if namestr.find("no professors")!=-1:
        return {}
    else:
        matchObj=re.compile(r'[\,\(\)]').split(namestr)
    for every in matchObj:
        every=every.lstrip().rstrip()
        if every.find("Fall")==-1 and every.find("Winter")==-1 and every.find("Summer")==-1:
            iterady.append(every)
        else:
            ent[every]=list()
            for j in iterady:
                ent[every].append(j)
            iterady.clear()
    return ent


#this method returns a list of all courses in mcgill
def list_all_mcgill():
    listdecours=list()
    j=int()
    linkstr="https://www.mcgill.ca/study/2017-2018/courses/search?search_api_views_fulltext=&sort_by=field_subject_code&page="
    #while openurl(linkstr+str(j))!=None:
    for j in range(1, 517):
        for v in openurl(linkstr+str(j)).find(
                "div", class_="view-content").findAll("a", href=re.compile("(/courses/)")):
            if 'href' in v.attrs:
                if v.attrs['href'].find("fr") == -1:
                    print(v.attrs['href'])
                    listdecours.append(v.attrs['href'])
        j=j+1
    return listdecours


#this method parse entire page of course information
"""
    Course ID: {
    "title": ,
    "credit": ,
    "description": ,
    "faculty": ,
    "department": ,
    "prerequesite":,
    "corequesite":,
    "prof name":
}
"""
def get_entry(url):
    global course_info
    bsobj = openurl(url)
    temp=dict()
    prereq = str()
    coreq = str()
    restr = str()
    verbtitl=str()
    cr=str()
    try:
        title = bsobj.body.h1.get_text()
        instru = bsobj.body.find("p", {"class": "catalog-instructors"}).get_text()
        descrip = bsobj.body.find("div", {"class": "block-inner"}).find("div", class_="content").\
            find("div", class_="content").p.get_text()
        facdept = bsobj.body.find("div", {"class": "meta"}).get_text()
        pre_co = bsobj.body.findAll(name="li", class_=None)
    except AttributeError:
        print("页面缺少属性")
        return
    matchObj = re.compile(r'[\s]').split(title[9:])
    try: 
        if title.find("credit")!=-1 or title.find("CE Unit")!=-1:
            cr_verbtitl = re.compile(r'[0-9A-Z]{4} [0-9A-Z]* ').split(title[9:])[1]
            cr_verbtitl = re.compile(r'[\(\)]').split(cr_verbtitl)
            cr = re.compile(r'\s').split(cr_verbtitl[1])[0]
            verbtitl = cr_verbtitl[0].rstrip()
        else:
            cr="0"
            for j in matchObj[2:]:
                verbtitl=verbtitl+j+" "
        title = matchObj[0] + " " + matchObj[1]
        for each in pre_co:
            temp = str(each.get_text())
            if each.get_text().find("Prereq") != -1:
                prereq = prereq + re.compile(r"[^0-9]*\:\s|\n").split(temp.lstrip())[1] + " "
            if each.get_text().find("Coreq") != -1:
                coreq = coreq + re.compile(r"[^0-9]*\:\s|\n").split(temp.lstrip())[1] + " "
            if each.get_text().find("Restric") != -1:
                restr = restr + re.compile(r"[^0-9]*\:\s|\n").split(temp.lstrip())[1] + " "
        dep = re.compile(r"\:\s|\s\(|\)\n").split(facdept)[1]
        fac = re.compile(r"\:\s|\s\(|\)\n").split(facdept)[2]
        course_info[title] = {'title': verbtitl, 'credit': cr, 'description': str(descrip).lstrip(), 'faculty': fac,
                              'department': dep,
                              'prerequesite': prereq, 'corequesite': coreq, 'prof name': process1_name(instru[25:])}
        print(course_info[title])
    except Exception:
        course_info[title]={}
        return

#save list of course info pages in txt
thefile = open('websitelist.txt', 'w')
ls=list_all_mcgill()
for links in ls:
    thefile.write("%s\n" % links)
thefile.close()

#parse every course in course list
for link in ls:
    get_entry(link)

#write dictionary to json file
with open("ecalendar.json", "w") as myfile:
    myfile.write(json.dumps(course_info))

#print result
print(course_info)
