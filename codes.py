import requests
from bs4 import BeautifulSoup

url = "http://results.jntuh.ac.in/jsp/home.jsp"
sem11, sem12, sem21, sem22, sem31, sem32, sem41, sem42 = set(), set(), set(), set(), set(), set(), set(), set()

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table_row = soup.find("table").find_all("tr")
for tr in table_row:
    td = tr.find("td")
    a = td.find("a")
    text = a.getText()
    link = a.get("href")
    if " (R18) " in text:
        examcode = int("".join(filter(lambda i:i.isdigit(), link))[0:4])
        print(examcode)
        if " I Year I " in text:
            sem11.add(examcode)
        elif " I Year II " in text:
            sem12.add(examcode)
        elif " II Year I " in text:
            sem21.add(examcode)
        elif " II Year II " in text:
            sem22.add(examcode)
        elif " III Year I " in text:
            sem31.add(examcode)
        elif " III Year II " in text:
            sem32.add(examcode)
        elif " IV Year I " in text:
            sem41.add(examcode)
        elif " IV Year II " in text:
            sem42.add(examcode)
sem11 = sorted(sem11)
sem12 = sorted(sem12)
sem21 = sorted(sem21)
sem22 = sorted(sem22)
sem31 = sorted(sem31)
sem32 = sorted(sem32)
sem41 = sorted(sem41)
sem42 = sorted(sem42)

for i in [sem11, sem12, sem21, sem22, sem31, sem32, sem41, sem42]:
    print(i)