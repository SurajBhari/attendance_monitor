from calendar import month
from json import load
from datetime import datetime
from operator import ne
from mplcal import MplCalendar

def get_data():
    data = load(open('responses.json'))
    classes_names = {}
    possible_dates = []
    date_wise = {}


    for entry in data["taken"]:
        dt = datetime.strptime(entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M")
        date = dt.date()

        try:
            classes_names[entry["class_name"]]["total"] += 1
        except KeyError:
            classes_names[entry["class_name"]] = {"total": 1, "taken": 1, "not_taken": 0, "cancelled": 0}
        else:
            classes_names[entry["class_name"]]["taken"] += 1


        if date not in possible_dates:
            possible_dates.append(date)
        try:
            date_wise[date]["total"] += 1
        except KeyError: # first time seeing this class
            date_wise[date] = {"total": 1, "taken": 1, "not_taken": 1, "cancelled": 0}
        else:
            date_wise[date]["taken"] += 1



    for entry in data["not_taken"]:
        dt = datetime.strptime(entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M")
        date = dt.date()

        try:
            date_wise[date]["total"] += 1
        except KeyError: # first time seeing this class
            date_wise[date] = {"total": 1, "taken": 0, "not_taken": 1, "cancelled": 0}
        else:
            date_wise[date]["not_taken"] += 1

        if date not in possible_dates:
            possible_dates.append(date)


        try:
            classes_names[entry["class_name"]]["total"] += 1
        except KeyError:
            classes_names[entry["class_name"]] = {"total": 1, "taken": 0, "not_taken": 1, "cancelled": 0}
        else:
            classes_names[entry["class_name"]]["not_taken"] += 1


        dt = datetime.strptime(entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M")
        date = dt.date()
        if date not in possible_dates:
            possible_dates.append(date)

        

    for entry in data["cancelled"]:
        try:
            classes_names[entry["class_name"]]["total"] += 1
        except KeyError:
            classes_names[entry["class_name"]] = {"total": 1, "taken": 0, "not_taken": 0, "cancelled": 1}
        else:
            classes_names[entry["class_name"]]["cancelled"] += 1
        
        dt = datetime.strptime(entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M")
        date = dt.date()
        if date not in possible_dates:
            possible_dates.append(date)
        
        try:
            date_wise[date]["total"] += 1
        except KeyError: # first time seeing this class
            date_wise[date] = {"total": 1, "taken": 0, "not_taken": 0, "cancelled": 1}
        else:
            date_wise[date]["cancelled"] += 1
    
    months_to_make = []
    for date in possible_dates:
        new_date = datetime(year = date.year, month=date.month, day=1)
        if new_date not in months_to_make:
            months_to_make.append(new_date)
    
    calenders = []
    for month in months_to_make:
        cale = MplCalendar(month.year, month.month) 
        for date in date_wise:
            if date.month == month.month and date.year == month.year:
                string = "total - " + str(date_wise[date]["total"]) +"\ntaken - " +  str(date_wise[date]["taken"]) + "\nNot Taken - " + str(date_wise[date]["not_taken"]) + "\nCancelled - "+ str(date_wise[date]["cancelled"])
                cale.add_event(date.day, string)
        calenders.append(cale)
    
    string = "```\n"
    for key in classes_names.keys():
        total = classes_names[key]["total"]
        present = classes_names[key]["taken"] + classes_names[key]["cancelled"]
        ratio = (present/total)*100
        value = classes_names[key]
        string +=  key +  "\n"  + f"Percentage - {ratio}" + "\n\n"
    string += "```"
    file_names = []
    for cale in calenders:
        saving_name = f"{cale.month}-{cale.year}.png"
        cale.save(saving_name)
        file_names.append(saving_name)

    return string, file_names
