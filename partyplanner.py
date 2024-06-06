#Chris Giggleman CPT-168 Python Programming
#Party Planner Final Exam Project
#July 2, 2023
import csv

# List of attendee types and fees which are pre-set for the event.
attendee_types = {
    'Member': 22.00,
    'Guest': 22.00,
    'VIP': 20.00,
    'Staff': 25.00,
    'Sponsor': 25.00,
    'Volunteer': 25.00,
    'Other': 25.00
}

# Function to read the CSV file and return a list of attendees
def read_csv():
    try:
        with open('Partyplanner.csv', 'r') as file:
            reader = csv.reader(file)
            attendees = list(reader)
        return attendees
    except FileNotFoundError:
        return []

# Function to write the list of attendees to the CSV file
def write_csv(attendees):
    with open('Partyplanner.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(attendees)

# Function to add a new attendee to the list
def add_attendee(attendees):
    print("Enter New Attendee Information:")
    name = input("Enter the attendee's name: ")

    # Displaying attendee types and getting user input for attendee type
    print("Attendee Types:")
    for i, attendee_type in enumerate(attendee_types.keys(), 1):
        print(f"{i}. {attendee_type}")
    attendee_type_choice = input("Enter the number for the attendee type: ")

    try:
        attendee_type_choice = int(attendee_type_choice)
        if 1 <= attendee_type_choice <= len(attendee_types):
            attendee_type = list(attendee_types.keys())[attendee_type_choice - 1]
        else:
            print("Invalid attendee type choice.")
            return
    except ValueError:
        print("Invalid input, please choose from the list.")
        return

    # Displaying menu choices and getting user input for menu choice
    menu_choices = ["Chicken", "Fish", "Vegetarian", "Pork", "Other"]
    print("Menu Choices:")
    for i, menu_choice in enumerate(menu_choices, 1):
        print(f"{i}. {menu_choice}")
    menu_choice = input("Enter the number for the menu choice: ")

    try:
        menu_choice = int(menu_choice)
        if 1 <= menu_choice <= len(menu_choices):
            menu_choice = menu_choices[menu_choice - 1]
        else:
            print("Invalid menu choice.")
            return
    except ValueError:
        print("Invalid input for menu choice.")
        return

    # Displaying drink choices and getting user input for drink choice
    drink_choices = ["Water", "Soda", "Coffee", "Tea", "Wine", "Beer", "Other"]
    print("Drink Choices:")
    for i, drink_choice in enumerate(drink_choices, 1):
        print(f"{i}. {drink_choice}")
    drink_choice = input("Enter the number for the drink choice: ")

    try:
        drink_choice = int(drink_choice)
        if 1 <= drink_choice <= len(drink_choices):
            drink_choice = drink_choices[drink_choice - 1]
        else:
            print("Invalid drink choice.")
            return
    except ValueError:
        print("Invalid input for drink choice.")
        return

    fee_paid = attendee_types[attendee_type]  # Calculating the fee based on the attendee type

    attendees.append([name, attendee_type, menu_choice, drink_choice, format(fee_paid, ".2f")])

    print("Attendee added successfully!")

# Function to generate reports based on the list of attendees
def generate_reports(attendees):
    print("-------Attendees List-------")
    print("Name\t\tAttendee Type\tMenu Choice\tDrink Choice\tFee Paid")
    print("------------------------------------------------------------")
    for attendee in attendees:
        name = attendee[0].ljust(15)
        attendee_type = attendee[1].ljust(14)
        menu_choice = attendee[2].ljust(20)
        drink_choice = attendee[3].ljust(15)
        fee_paid = attendee[4]
        print(f"{name}{attendee_type}{menu_choice}{drink_choice}${fee_paid.replace('.00', '')}")

    total_fees = sum(float(attendee[4].replace("$", "")) for attendee in attendees)
    print("\nTotal Fees: ${:.2f}".format(total_fees))
    print("Total Attendees:", len(attendees))

    attendee_type_counts = {type: 0 for type in attendee_types}
    for attendee in attendees:
        attendee_type_counts[attendee[1]] += 1

    print("\nAttendee Type Counts:")
    for type, count in attendee_type_counts.items():
        print(f"{type}: {count}")

    menu_choices = [attendee[2] for attendee in attendees]
    menu_choice_counts = {choice: menu_choices.count(choice) for choice in set(menu_choices)}
    print("\nMenu Choice Counts:")
    for choice, count in menu_choice_counts.items():
        print(f"{choice}: {count}")

    drink_choices = [attendee[3] for attendee in attendees]
    drink_choice_counts = {choice: drink_choices.count(choice) for choice in set(drink_choices)}
    print("\nDrink Choice Counts:")
    for choice, count in drink_choice_counts.items():
        print(f"{choice}: {count}")

# Function to update an existing attendee in the list
def update_attendee(attendees):
    name = input("Enter the name of the attendee to update: ")
    for attendee in attendees:
        if attendee[0] == name:
            print(f"Attendee found: {attendee[0]}")
            
            # Displaying attendee types and getting user input for the new attendee type
            print("Attendee Types:")
            for i, attendee_type in enumerate(attendee_types.keys(), 1):
                print(f"{i}. {attendee_type}")
            attendee_type_choice = input("Enter the number for the new attendee type: ")

            try:
                attendee_type_choice = int(attendee_type_choice)
                if 1 <= attendee_type_choice <= len(attendee_types):
                    attendee_type = list(attendee_types.keys())[attendee_type_choice - 1]
                    fee_paid = attendee_types[attendee_type]

                    menu_choices = ["Chicken", "Fish", "Vegetarian", "Pork", "Other"]
                    print("Menu Choices:")
                    for i, menu_choice in enumerate(menu_choices, 1):
                        print(f"{i}. {menu_choice}")
                    menu_choice_index = input("Enter the number for the new menu choice: ")

                    drink_choices = ["Water", "Soda", "Coffee", "Tea", "Wine", "Beer", "Other"]
                    print("Drink Choices:")
                    for i, drink_choice in enumerate(drink_choices, 1):
                        print(f"{i}. {drink_choice}")
                    drink_choice_index = input("Enter the number for the new drink choice: ")

                    try:
                        menu_choice_index = int(menu_choice_index)
                        drink_choice_index = int(drink_choice_index)

                        if 1 <= menu_choice_index <= len(menu_choices) and 1 <= drink_choice_index <= len(drink_choices):
                            menu_choice = menu_choices[menu_choice_index - 1]
                            drink_choice = drink_choices[drink_choice_index - 1]

                            # Updating the attendee details
                            attendee[1] = attendee_type
                            attendee[2] = menu_choice
                            attendee[3] = drink_choice
                            attendee[4] = format(fee_paid, ".2f")

                            print("Attendee updated successfully!")
                        else:
                            print("Invalid menu choice or drink choice.")
                    except ValueError:
                        print("Invalid input for menu choice or drink choice.")
                else:
                    print("Invalid attendee type choice.")
            except ValueError:
                print("Invalid input for attendee type choice.")

            return

    print("Attendee not found.")


# Function to delete an attendee from the list
def delete_attendee(attendees):
    name = input("Enter the name of the attendee to delete: ")
    for attendee in attendees:
        if attendee[0] == name:
            attendees.remove(attendee)
            print("Attendee deleted successfully!")
            return

    print("Attendee not found.")

# Function to search for an attendee in the list
def search_attendee(attendees):
    search_name = input("Enter the name or a part of the name of the attendee to search: ")
    search_results = []

    for attendee in attendees:
        if search_name.lower() in attendee[0].lower():
            search_results.append(attendee)

    if len(search_results) > 0:
        print("Attendee(s) found:")
        for result in search_results:
            print(f"Name: {result[0]}")
            print(f"Attendee Type: {result[1]}")
            print(f"Menu Choice: {result[2]}")
            print(f"Drink Choice: {result[3]}")
            print(f"Fee Paid: ${result[4]}")
            print("---------------------")
    else:
        print("Attendee not found.")

# Function to sort the attendee list based on a chosen field
def sort_attendee_list(attendees):
    sort_by = input("Enter the field to sort by (Name/Type/Menu/Drink/Fee): ")
    if sort_by.lower() == "name":
        attendees.sort(key=lambda x: x[0])
        print("Attendee list sorted by Name.")
    elif sort_by.lower() == "type":
        attendees.sort(key=lambda x: x[1])
        print("Attendee list sorted by Attendee Type.")
    elif sort_by.lower() == "menu":
        attendees.sort(key=lambda x: x[2])
        print("Attendee list sorted by Menu Choice.")
    elif sort_by.lower() == "drink":
        attendees.sort(key=lambda x: x[3])
        print("Attendee list sorted by Drink Choice.")
    elif sort_by.lower() == "fee":
        attendees.sort(key=lambda x: float(x[4].replace("$", "")))
        print("Attendee list sorted by Fee Paid.")
    else:
        print("Invalid field to sort by.")

# Main menu function to manage the party planner application
def menu():
    attendees = read_csv()

    while True:
        print("\n----- Party Planner Menu -----")
        print("1. Add Attendee")
        print("2. Generate Reports")
        print("3. Update Attendee")
        print("4. Delete Attendee")
        print("5. Search Attendee")
        print("6. Sort Attendee List")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_attendee(attendees)
        elif choice == "2":
            generate_reports(attendees)
        elif choice == "3":
            update_attendee(attendees)
        elif choice == "4":
            delete_attendee(attendees)
        elif choice == "5":
            search_attendee(attendees)
        elif choice == "6":
            sort_attendee_list(attendees)
        elif choice == "0":
            write_csv(attendees)
            print("Exiting Party Planner...")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the party planner application
menu()

