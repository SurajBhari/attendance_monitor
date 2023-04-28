from calendar import month
from json import load
from datetime import datetime
from operator import ne
from mplcal.mplcal import MplCalendar
from matplotlib import pyplot as plt


def get_data():
    data = load(open("responses.json"))
    classes_names = {}
    possible_dates = []
    date_wise = {}

    for entry in data["taken"]:
        dt = datetime.strptime(
            entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M"
        )
        date = dt.date()

        try:
            classes_names[entry["class_name"]]["total"] += 1
        except KeyError:
            classes_names[entry["class_name"]] = {
                "total": 1,
                "taken": 1,
                "not_taken": 0,
                "cancelled": 0,
            }
        else:
            classes_names[entry["class_name"]]["taken"] += 1

        if date not in possible_dates:
            possible_dates.append(date)
        try:
            date_wise[date]["total"] += 1
        except KeyError:  # first time seeing this class
            date_wise[date] = {"total": 1, "taken": 1, "not_taken": 0, "cancelled": 0}
        else:
            date_wise[date]["taken"] += 1

    for entry in data["not_taken"]:
        dt = datetime.strptime(
            entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M"
        )
        date = dt.date()

        try:
            date_wise[date]["total"] += 1
        except KeyError:  # first time seeing this class
            date_wise[date] = {"total": 1, "taken": 0, "not_taken": 1, "cancelled": 0}
        else:
            date_wise[date]["not_taken"] += 1

        if date not in possible_dates:
            possible_dates.append(date)

        try:
            classes_names[entry["class_name"]]["total"] += 1
        except KeyError:
            classes_names[entry["class_name"]] = {
                "total": 1,
                "taken": 0,
                "not_taken": 1,
                "cancelled": 0,
            }
        else:
            classes_names[entry["class_name"]]["not_taken"] += 1

        dt = datetime.strptime(
            entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M"
        )
        date = dt.date()
        if date not in possible_dates:
            possible_dates.append(date)

    for entry in data["cancelled"]:
        try:
            classes_names[entry["class_name"]]["total"] += 1
        except KeyError:
            classes_names[entry["class_name"]] = {
                "total": 1,
                "taken": 0,
                "not_taken": 0,
                "cancelled": 1,
            }
        else:
            classes_names[entry["class_name"]]["cancelled"] += 1

        dt = datetime.strptime(
            entry["class_date"] + " " + entry["class_time"], "%d/%m/%Y At %H:%M"
        )
        date = dt.date()
        if date not in possible_dates:
            possible_dates.append(date)

        try:
            date_wise[date]["total"] += 1
        except KeyError:  # first time seeing this class
            date_wise[date] = {"total": 1, "taken": 0, "not_taken": 0, "cancelled": 1}
        else:
            date_wise[date]["cancelled"] += 1

    months_to_make = []
    for date in possible_dates:
        new_date = datetime(year=date.year, month=date.month, day=1)
        if new_date not in months_to_make:
            months_to_make.append(new_date)

    calenders = []
    for month in months_to_make:
        cale = MplCalendar(month.year, month.month)
        for date in date_wise:
            if date.month == month.month and date.year == month.year:
                string = (
                    "total - "
                    + str(date_wise[date]["total"])
                    + "\ntaken - "
                    + str(date_wise[date]["taken"])
                    + "\nNot Taken - "
                    + str(date_wise[date]["not_taken"])
                    + "\nCancelled - "
                    + str(date_wise[date]["cancelled"])
                )
                cale.add_event(date.day, string)
        calenders.append(cale)

    string = "```\n"
    for key in classes_names.keys():
        total = classes_names[key]["total"]
        present = classes_names[key]["taken"] + classes_names[key]["cancelled"]
        ratio = (present / total) * 100
        value = classes_names[key]
        string += key + "\n" + f"Percentage - {ratio}" + "\n\n"
    file_names = []
    for cale in calenders:
        saving_name = f"{cale.month}-{cale.year}.png"
        cale.save(saving_name)
        file_names.append(saving_name)

    attended_class = {}
    overall = {"taken": 0, "not_taken": 0, "cancelled": 0, "total": 0}
    for clas in classes_names.keys():
        attended_class[clas[:10]] = (
            classes_names[clas]["taken"] + classes_names[clas]["cancelled"]
        )
        overall["taken"] += classes_names[clas]["taken"]
        overall["not_taken"] += classes_names[clas]["not_taken"]
        overall["cancelled"] += classes_names[clas]["cancelled"]
        overall["total"] += classes_names[clas]["total"]

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("equal")
    ax.pie(list(attended_class.values()), autopct="%1.1f%%", shadow=True, startangle=90)
    plt.legend(list(attended_class.keys()), loc="best")
    plt.savefig("pie_graph.png")
    file_names.append("pie_graph.png")
    string += f"Total classes - {overall['total']}\n"
    string += f" Taken Classes - {overall['taken']}\n"
    string += f" Not Taken Classes - {overall['not_taken']}\n"
    string += f" Cancelled Classes - {overall['cancelled']}\n"
    string += "```"
    return string, file_names


if __name__ == "__main__":
    print(get_data())
