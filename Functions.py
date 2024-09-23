# Author: Ciaran O'Donovan

from datetime import date
current_date = str(date.today())


# Main menu function that provides initial option infrastructure
def main_menu():
    login_auth = False
    print("Module Record System -Login")
    print("-" * 10)

    while True:

        while True:
            name = str(input("Name:"))
            password = str(input("Password:"))
            if name == "" or password == "":
                print("Empty space is not a valid input. Try again")
            else:
                break
        user_id = name + password + ":"
        try:
            with open("login.txt", "r") as file:
                for x in file:
                    if user_id in x:
                        login_auth = True
                        break
                    else:
                        print(f"Incorrect username or password")
                        login_auth = False
                        break
        except FileNotFoundError:
            print('Error: no such file login file')

        if login_auth == True:

            print(f"\nWelcome {name}")
            print("Module Record System - Options")
            print("-" * 10)
            while True:
                try:
                    choice = int(input("1. Record Attendance \n2. Generate Statistics \n3. Exit \n"))
                    if choice < 1 or choice > 3:
                        print("Please enter 1, 2 or 3.")
                    else:
                        break
                except ValueError:
                    print("please enter an integer.")
            if choice == 1:
                return 1
            elif choice == 2:
                return 2
            elif choice == 3:
                print("Exiting Module Record System.")
                return 3
        else:
            print("Login Failed.")
            exprog = str(input("Exit program? y/n."))
            if exprog == "y":
                print("Exiting Module Record System.")
                return 3


# module list loading and data type format processing
def module_list_load(filename):
    module_list = []
    module_num_list = []
    module_name_list = []
    try:
        with open(filename, "r") as file:
            for line in file:
                module_list.append(line.strip())
                module_split = line.strip().split(",")
                module_num_list.append(module_split[0])
                module_name_list.append(module_split[1])

    except FileNotFoundError:
        print(f'Error: not such file as{filename}')

    return module_num_list, module_name_list


# module choice function allowing user to choose appropriate module for their userID

def module_choice(module_num_list):
    i = 0
    print("Module Record System- Attendance - Choose a Module")
    print("-" * 50)
    for x in module_num_list:
        i = i + 1
        print(f"{i}. {x}")

    while True:
        try:
            while True:

                choice = int(input("Enter the list number (not module number) of the module you wish to select: ")) - 1
                choice2 = choice + 1
                if choice2 > i or choice2 <= 0:
                    print("invalid input,list does not contain such a number")

                else:
                    break

            break

        except ValueError:
            print("invalid input, please enter an integer")

    selected_module = module_num_list[choice]
    return selected_module


def record_system():

    print("Module Record System - Attendance - SOFT_6017")
    print("-" * 50)
    print(f"There are")


# loads specific module data  and processes text data for use in python
def module_data(filename):
    student_list = []
    student_name_list = []
    student_absence_list = []
    student_presence_list = []
    try:
        with open(filename + ".txt", "r") as file:
            for line in file:
                student_list.append(line.strip())
                student_data_split = line.strip().split(",")
                student_name_list.append(student_data_split[0])
                student_absence_list.append(int(student_data_split[1]))
                student_presence_list.append(int(student_data_split[2]))
        return student_name_list, student_absence_list, student_presence_list
    except FileNotFoundError:
        print(f'Error: not such file as{filename}')


# takes module data from module_data() and allows user to update presence/absence python data
def recording(names, absence, presence):
    i = 0
    index = 0
    updated_presence = []
    updated_absence = []
    for x in names:
        i = i + 1
        print(f"Student #{i}: {x}")
        print("1. Present\n2. Absent")
        while True:
            try:
                while True:
                    attendance = int(input(f"Enter 1 or 2 for {x}:"))
                    if attendance > 2 or attendance < 1:
                        print("invalid input, enter 1 or 2.")
                    else:
                        break
                break
            except ValueError:
                print("Please enter an integer")

        if attendance == 1:
            updated_presence.append(presence[index] + 1)
            updated_absence.append(absence[index])

        elif attendance == 2:
            updated_absence.append(absence[index] + 1)
            updated_presence.append(presence[index])
        index = index + 1

    return updated_absence, updated_presence


# statistics update function
def stat_update(filename, names, updated_absence, updated_presence):

    i = 0
    temp_list = []
    print("Module Record System - Average Attendance Data")
    print("-" * 50)

    for x in range(len(names)):
        temp_var = names[x] + "," + str(updated_absence[x]) + "," + str(updated_presence[x])
        temp_list.append(temp_var)

    try:
        with open(filename + ".txt", 'w') as file:
            for element in temp_list:
                file.write(f'{temp_list[i]}\n')
                i = i + 1
    except FileNotFoundError:
        print(f'Error: not such file as{filename}')

    print(f"{filename}.txt was updated with the latest attendance records.")


# main stat generation
def stat_gen(number_list, name_list):
    sum_absence = 0
    sum_presence = 0
    best_attendance = 0
    poor_attendance = 0
    best_name = ""
    poor_name = []
    # Clearing any previous data assigned to txt file from same date to prevent same day redundant/obsolete data

    with open("Attendance_stats_" + current_date + ".txt", 'w') as file:
        file.write("")

    i = 0
    print("Module Record System - Average Attendance Data")
    print("-" * 50)
    for module in number_list:
        name, absence, presence = module_data(module)
        for num in absence:
            sum_absence = sum_absence + num
        for num in presence:
            sum_presence = sum_presence + num

        sum_total = sum_absence + sum_presence

        attendance = (sum_presence / sum_total) * 100
        visualizer = "*" * int((attendance * 0.1))
        if attendance > best_attendance:
            best_attendance = attendance
            best_name = name_list[i]
        if attendance < 40:
            poor_attendance = poor_attendance + 1
            poor_name.append(name_list[i])

        print(f"{name_list[i]}\t{number_list[i]}\t{attendance:.2f}\t{visualizer}")
        with open("Attendance_stats_" + current_date + ".txt", 'a') as file:
            file.write(f"{name_list[i]}\t{number_list[i]}\t{attendance:.2f}\t{visualizer}\n")

        i = i + 1
    print(f"The best attended module is {best_name} with a {best_attendance:.2f}% attendance rate.")
    print(f"There is {poor_attendance} module(s) with attendance under 40%:")
    for module in poor_name:
        print(module)
    with open("Attendance_stats_" + current_date + ".txt", 'a') as file:
        file.write(f"The best attended module is {best_name} with a {best_attendance:.2f}% attendance rate.\n")
        file.write(f"There is {poor_attendance} module(s) with attendance under 40%:\n")
        for module in poor_name:
            file.write(f"{module}\n")

    print(f"The above data is also stored at Attendance_stats_{current_date}.txt.")
    input("Press any key to continue")


def main():
    option = 0
    while option != 3:
        option = main_menu()

        if option == 1:
            module_num_list, module_name_list = module_list_load("Modules.txt")
            selected_module = module_choice(module_num_list)
            names, absence, presence = module_data(selected_module)
            updated_absence, updated_presence = recording(names, absence, presence)
            stat_update(selected_module, names, updated_absence, updated_presence)

        elif option == 2:
            module_num_list, module_name_list = module_list_load("Modules.txt")
            stat_gen(module_num_list, module_name_list)


if __name__ == '__main__':
    main()

# to prevent terminal from immediately closing once process is finished.
input()
