from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time, re
from bs4 import BeautifulSoup
import json


def process1_name(namestr):
    ent=list()
    if namestr.find("TBA")!=-1:
        return []
    else:
        matchObj=re.compile(r'[\,]').split(namestr)
    for every in matchObj:
        every=every.lstrip().rstrip()
        name_component=re.compile(r'[\s]*').split(every)
        name_prof=str()
        for parts in name_component:
            name_prof=name_prof+" "+parts
        ent.append(name_prof.lstrip().rstrip())
    return ent


with open('username_pswd_by_dept.txt') as f:
    lines = f.readlines()

driver = webdriver.Firefox()
driver.implicitly_wait(30)
course_db = dict()
driver.get("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")
driver.find_element_by_id("mcg_un").click()
driver.find_element_by_id("mcg_un").clear()
driver.find_element_by_id("mcg_un").send_keys(lines[0].lstrip().rstrip())
driver.find_element_by_id("mcg_pw").click()
driver.find_element_by_id("mcg_pw").clear()
driver.find_element_by_id("mcg_pw").send_keys(lines[1].lstrip().rstrip())
# Select Term
driver.find_element_by_id("mcg_un_submit").click()
driver.find_element_by_link_text("Student Menu").click()
driver.find_element_by_link_text("Registration Menu").click()
driver.find_element_by_link_text("Step 2: Search Class Schedule and Add Course Sections").click()
driver.find_element_by_xpath("//option[@value='"+lines[3].lstrip().rstrip()+"']").click()
driver.find_element_by_xpath("//input[@value='Submit']").click()

# Select chosen department
driver.find_element_by_xpath("//option[@value='"+lines[4].lstrip().rstrip()+"']").click()
driver.find_element_by_xpath("/html/body/div[3]/form/input[17]").click()

# for all course, parse information
res=driver.find_elements(By.NAME, 'SUB_BTN')
for course in range(1, len(res)+1):
    course_title=driver.find_element_by_xpath("/html/body/div[3]/table[2]/tbody/tr["+str(2+course)+"]/td[1]").text
    print(course_title)
    driver.find_element_by_xpath("(//input[@name='SUB_BTN'])["+str(course)+"]").click()
    bsobj=BeautifulSoup(driver.page_source)
    while bsobj.find("h1").get_text().find("No Response from Application Web Server")!=-1:
        time.sleep(3)
        driver.execute_script("window.history.go(-1)")
        driver.find_element_by_xpath("(//input[@name='SUB_BTN'])[" + str(course) + "]").click()

    # for courses involve a lecture, crawl lecture, for courses involve a project, crawl project
    try:
        sections = bsobj.find_all("td", text=course_title)
        if len(sections)==0:
            raise AttributeError
        sections = [sec.parent for sec in sections]
    except AttributeError:
        print("l")
        sections=bsobj.find_all('td', {'class': 'dddefault'})
        sections=[sec.parent for sec in sections][:1]
    tabl=list()
    lecs=dict()


    for section in sections:
        tabl=section.find_all("td", {'class': 'dddefault'})
        tabl=[se.get_text() for se in tabl]
        try:
            full_rat = int(tabl[11]) / int(tabl[10])
        except ZeroDivisionError:
            full_rat = 0
        lecs[tabl[4]]={'title': tabl[7], 'type': tabl[5], 'credit': tabl[6], 'days': tabl[8], 'time': tabl[9], 'capital': tabl[10], 'actual': tabl[11], 'full reg rate': str(full_rat), 'instructor': process1_name(tabl[16]), 'location': tabl[18]}

    course_db[tabl[2] + " " + tabl[3]] = lecs
    driver.execute_script("window.history.go(-1)")
    time.sleep(1)
    continue
print(course_db)

with open("ecse_course_reg_info.json", "w") as myfile:
    myfile.write(json.dumps(course_db))

