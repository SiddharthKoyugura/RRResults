from pprint import pprint
import aiohttp
import asyncio
from bs4 import BeautifulSoup

headers = {
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

# R18 Semester codes of all years
sem11 = [1323, 1358, 1404, 1430, 1467, 1504, 1572, 1615, 1658]
sem12 = [1356, 1363, 1381, 1435, 1448, 1481, 1503, 1570, 1620, 1622, 1656]
sem21 = [1391, 1425, 1449, 1496, 1560, 1610, 1628, 1667]
sem22 = [1437, 1447, 1476, 1501, 1565, 1605, 1627, 1663]
sem31 = [1454, 1491, 1550, 1590, 1626, 1639, 1645, 1655]
sem32 = [1502, 1555, 1595, 1625, 1638, 1649, 1654]
sem41 = [1545, 1585, 1624, 1640, 1644, 1653]
sem42 = [1580, 1600, 1623]


personal_data = {}
marks_data = []
grades_data = {"O":10, "A+":9, "A":8, "B+":7, "B":6, "C":5}
sgpa = []
results_dict = {}

# Get data from the jntuh website
async def main(exam_code, roll):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('http://results.jntuh.ac.in/resultAction', data=f"degree=btech&examCode={exam_code}&etype=r17&result=null&grad=null&type=intgrade&htno={roll}", headers=headers) as response:
                # print("Status:", response.status)
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                get_personal_data(soup)
                get_marks_data(soup)
                sgpa_calculator()
    except:
        pass
    

# Get student personal details
def get_personal_data(soup):
    global personal_data
    tables = soup.find_all("table")
    personal_data_rows = tables[0].find_all("td")
    for i in range(0, len(personal_data_rows), 2):
        personal_data[personal_data_rows[i].getText()] = personal_data_rows[i+1].getText()


def get_dict(marks_data_cell):
    return {
                "subject_code": marks_data_cell[0].getText(),
                "subject_name": marks_data_cell[1].getText(),
                "marks": marks_data_cell[4].getText(),
                "grade": marks_data_cell[5].getText(),
                "credits": marks_data_cell[6].getText(),
            }

# Get Marks of the student
def get_marks_data(soup):
    global marks_data
    tables = soup.find_all("table")
    marks_data_rows = tables[1].find_all("tr")[1:]
    if marks_data:
        # marks_data = []
        temp_data = []
        for row in marks_data_rows:
            marks_data_cell = row.find_all("td")
            temp_data.append(get_dict(marks_data_cell))
        update_marks(temp_data)
    else:
        for row in marks_data_rows:
            marks_data_cell = row.find_all("td")
            marks_data.append(get_dict(marks_data_cell))

    # pprint(marks_data)

# Update Supply data
def update_marks(supply_data):
    global marks_data
    for supply in supply_data:
        for marks in marks_data:
            if supply["subject_code"] == marks["subject_code"]:
                # index = marks_data.index(marks)
                marks["credits"] = supply["credits"]
                marks["grade"] = supply["grade"]
                marks["marks"] = supply["marks"]
                marks["subject_code"] = supply["subject_code"]
                marks["subject_name"] = supply["subject_name"]

# Calculate SGPA of the Student
def sgpa_calculator():
    global sgpa, marks_data 
    sum_of_credits = 0
    sum_of_score = 0
    for data in marks_data:
        if not(data["grade"] == "F" or data["grade"] == "-"):
            sum_of_credits += float(data["credits"])
            sum_of_score += (float(data["credits"]) * grades_data[data["grade"]])
   
    sgpa.append(round(sum_of_score / sum_of_credits, 2))
    # print(sum_of_credits, sum_of_score)
    # print("sgpa", sgpa)

def verify_results(roll, sem_code_list):
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    for sem_code in sem_code_list:
        loop.run_until_complete(main(sem_code, roll))

def get_sem_codes_list(sem_code):
    if sem_code == "1-1":
        return sem11
    elif sem_code == "1-2":
        return sem12
    elif sem_code == "2-1":
        return sem21
    elif sem_code == "2-2":
        return sem22
    elif sem_code == "3-1":
        return sem31
    elif sem_code == "3-2":
        return sem32
    elif sem_code == "4-1":
        return sem41
    elif sem_code == "4-2":
        return sem42

# Called from the Flask
def get_result(roll):
    global marks_data, sgpa, results_dict
    results_dict = {}
    # for sem_code in ["1-1"]:
    for sem_code in ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]:
        verify_results(roll.upper(), get_sem_codes_list(sem_code))
        if marks_data:
            marks_data.append({"sgpa":sgpa[-1]})
            results_dict[sem_code] = marks_data
            marks_data = []
            sgpa = []
        elif sem_code not in ["1-1", "1-2"]:
            break
    return results_dict

def get_single_sem_result(roll, sem_code):
    global marks_data, sgpa
    marks_data, sgpa = [], []
    verify_results(roll.upper(), get_sem_codes_list(sem_code))
    return [marks_data, sgpa]

# def get_result(roll, sem_code):
#     global marks_data, sgpa
#     marks_data, sgpa = [], []
#     verify_results(roll.upper(), get_sem_codes_list(sem_code))
#     return marks_data
# get_single_sem_result("20ve1a66a0", "1-1")
# print(sgpa)
# get_result("20ve1a6689", "1-1")
# pprint(personal_data)
# get_result("20ve1a6688")
# pprint(results_dict)
