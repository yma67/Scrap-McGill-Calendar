# crawl_mcgill_course
Collect course information using web crawler for McGill E-Calendar and Minerva (Administration system). 

## E-Calendar
```
python3 craw_mcgill_ecalendr.py
```
### Version 1: Naive crawler using Beautifulsoup 4 to parse course informations
* For courses with "CE Unit(s)", 1 CE Unit=1 Credit
* [Sample data set](crawl_mcgill_course/craw_minerva/ecse_course_reg_info.json) is attatched
* For courses with multiple terms and multiple instructors per term, a dictionary holds terms->list of instructors 
```Python
{'Term1': [Instructor0, Instructor1, Instructor2, ..., InstructorN], 'Term2': [Instructor0, Instructor1, Instructor2, ...,InstructorN]}
```

### Version 2: Scrapy
* Coming Soon

## Minerva
```
python3 crawl_minerva.py
```
**Attention: Please control frequency of request, McGill Minerva Server cannot handle to much load.**
**It's not the author's responsibility to maintain a proper accessing speed.**
**It's the user's responsibility if he is banned by Minerva.**

* Every section of course, including lecture, project, tutorial, labs, and others is an entry of a dictionary by course code. 
* There is a [sample data set](crawl_mcgill_course/craw_minerva/ecse_course_reg_info.json) for ECSE department in Winter 2018 
* ```
  "ECSE 436": {
    "001": {
      "title": "Signal Processing Hardware.",
      "type": "Lecture",
      "credit": "3.000",
      "days": "TR",
      "time": "08:35 AM-09:55 AM",
      "capital": "34",
      "actual": "26",
      "full reg rate": "0.7647058823529411",
      "instructor": [
        "Jan Bajcsy"
      ],
      "location": "ENGTR 2110"
    },
    "002": {
      "title": "Signal Processing Hardware.",
      "type": "Laboratory",
      "credit": "0.000",
      "days": "R",
      "time": "01:35 PM-05:25 PM",
      "capital": "34",
      "actual": "26",
      "full reg rate": "0.7647058823529411",
      "instructor": [],
      "location": "ENGTR 4180"
    }
  },
  ```
### Version 1: Iterate all department at once
* To write a input .txt file
```
/*your McGill email goes here*/
/*your McGill password goes here*/
/*determine latency between requests, too fast obeys McGill rules*/
/*Years and Terms: YYYYTT, Winter: 01, Fall: 09, Summer: 05, example: Winter 2018: 201801*/
```
* Example
```
firstname.lastname@mail.mcgill.ca
123456789
30
201801
```

### Version 2: Specifically collect one department
* To write a input .txt file
```
/*your McGill email goes here*/
/*your McGill password goes here*/
/*determine latency between requests, too fast obeys McGill rules*/
/*Years and Terms: YYYYTT, Winter: 01, Fall: 09, Summer: 05, example: Winter 2018: 201801*/
/*Department Code: example: math department->MATH*/
```
* Example
```
firstname.lastname@mail.mcgill.ca
123456789
30
201801
MATH
```

## Built With

* Python 2: Minerva
* Python 3: E-Calendar, Minerva
* Beautifulsoup 4: Both
* Selenium: Minerva

## Author

* **Mark Ma**

