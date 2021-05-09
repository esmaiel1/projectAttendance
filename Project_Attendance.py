import csv
import os
import time
files_list = os.listdir()


def get_names(name_file):
    with open(name_file) as csv_name:
        names_list = []
        reade = csv.reader(csv_name)
        for x in reade:
            try:
                if "teacher" in x[0].lower() or "peercoach" in x[0].lower():
                    n = x[0].replace('Teacher', "")
                    n = n.replace('Peercoach', "")
                    n = n.split("(")[1].replace("\t", "").split(")")[0]
                    teachers.append(n)
                else:
                    a = [z for y in x[0].split("(") for z in y.split(")")]
                    student_name = a[0]
                    student_id = a[1]
                    names_list.append({"Name": student_name, "ID": student_id, "W1P1": "Unknown", "W1P2": "Unknown",
                                       "W2P1": "Unknown", "W2P2": "Unknown",
                                       "W3P1": "Unknown", "W3P2": "Unknown",
                                       "W4P1": "Unknown", "W4P2": "Unknown",
                                       "W5P1": "Unknown", "W5P2": "Unknown",
                                       "W6P1": "Unknown", "W6P2": "Unknown",
                                       "W7P1": "Unknown", "W7P2": "Unknown"})
            except IndexError:
                pass
        return names_list


names_input = input("Enter the file that contains all students names for example : 'AllAttendees.txt'\n")

file_exist = False
while not file_exist:
    if names_input not in files_list:
        print("File not found")
        names_input = input("Enter the file that contains all students names for example : 'AllAttendees.txt'\n")
    else:
        file_exist = True

unknown_names = []
teachers = []
names = get_names(names_input)
print(teachers)
for file in files_list:
    if file[0] == "W" and file[2] == "P" and file[1].isdigit() and file[3].isdigit():
        week = file[:4]
        with open(file) as csv_file:
            reader = csv.reader(x.replace('\0', '') for x in csv_file)
            reader = filter(None, reader)
            for row in reader:
                for x in row:
                    id_exists = False
                    if "joined" in x.lower():
                        id = x.split("(")[1].replace("\t", "").split(")")[0]
                        for i in names:
                            if i["ID"] == id:
                                i[week] = "Present"
                                id_exists = True
                            elif i[week] != "Present":
                                i[week] = "Absent"
                        if not id_exists:
                            print(id)
                            print(id in teachers)
                            if id not in teachers:
                                new_unknown = {"Name": x.split("(")[0].replace("\t", ""),
                                               "ID": id,
                                               "Week": week}
                                exist = list(filter(lambda x: x['ID'] == id, unknown_names))
                                if len(exist) != 0:
                                    for i in unknown_names:
                                        if i["ID"] == exist[0]['ID']:
                                            i["Week"] += "," + week
                                else:
                                    unknown_names.append(new_unknown)

result_file = input("Enter the result file name for example: 'res.csv'\n")
with open(result_file, mode='w') as result_file:
    fields = []
    for key in names[0]:
        if names[0][key] != "Unknown":
            fields.append(key)
    fields.append("Total")
    writer = csv.DictWriter(result_file, lineterminator='\n', fieldnames=fields)
    writer.writeheader()
    for dictionary in names:
        total = 0
        rows = {'Name': dictionary["Name"], 'ID': dictionary["ID"]}
        for key in dictionary:
            if dictionary[key] != "Unknown":
                rows[key] = dictionary[key]
                if dictionary[key] == "Present":
                    total += 1
        rows["Total"] = str(round((total / (len(fields)-3)) * 100)) + "%"
        writer.writerow(rows)

with open('unknown_names.csv', mode='w') as unknown:
    fields = ['Names', 'ID', 'Week']
    writer = csv.DictWriter(unknown, lineterminator='\n', fieldnames=fields)
    writer.writeheader()
    for dictionary in unknown_names:
        writer.writerow({'Names': dictionary["Name"], 'ID': dictionary["ID"],
                         'Week': dictionary["Week"]})
