# crawl_mcgill_course
Collect course information using web crawler for McGill E-Calendar and Minerva (Administration system). 

## E-Calendar
```
python3 craw_mcgill_ecalendr.py
```
### Version 1: Naive crawler using Beautifulsoup 4 to parse course informations
* For courses with "CE Unit(s)", 1 CE Unit=1 Credit
* For courses with multiple terms and multiple instructors per term, a dictionary holds terms->list of instructors 
```Python
{'Term1': [Instructor0, Instructor1, Instructor2, ..., InstructorN], 'Term2': [Instructor0, Instructor1, Instructor2, ...,InstructorN]}
```

### Version 2: Scrapy
* Coming Soon

* Crawled .json file is attatched

## Minerva
```
python3 crawl_minerva.py
```
**Attention: Please control frequency of request, McGill Minerva Server cannot handle to much load.**
**It's not the author's responsibility to maintain a proper accessing speed.**
**It's the user's responsibility if he is banned by Minerva.**

* For courses with lecture and tutorial, only lectures counts. 
* For courses without lecture, first section counts. 
* For courses with multiple lecture sections, every section of lecture is counted. 

## Built With

* Python 2: Minerva
* Python 3: E-Calendar
* Beautifulsoup 4: Both
* Selenium: Minerva

## Author

* **Mark Ma**

