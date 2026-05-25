import os
import re
from datetime import datetime


# ==================================================
# TickIt: A Ticketing System
# ==================================================


MANAGER_CODE = "123"


CUSTOMER_LIST = "Customer List.txt"
VENUE_LIST = "Venue List.txt"
EVENT_LIST = "Event List.txt"
BOOKING_LIST = "Booking List.txt"
AVAILABILITY_FILE = "availability.txt"


# ==================================================
# GENERAL UTILITIES
# ==================================================


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


def validate_mobile(number):
    pattern = r"^(09\d{9}|\+639\d{9})$"
    return re.match(pattern, number)


def get_next_id(prefix, list_file):
    if not os.path.exists(list_file):
        return f"{prefix}-001"


    with open(list_file, "r") as file:
        lines = file.readlines()


    if not lines:
        return f"{prefix}-001"


    last_line = lines[-1].strip()
    last_id = last_line.split()[0]
    last_num = int(last_id.split("-")[1])


    return f"{prefix}-{last_num + 1:03d}"


def manager_access():
    code = input("Enter Manager Code: ")


    if code == MANAGER_CODE:
        return True


    print("Access Denied.")
    return False


# ==================================================
# CUSTOMER BLOCK
# ==================================================


def add_customer():


    print("\n===== ADD CUSTOMER =====")


    last_name = input("Last Name: ").strip()
    given_name = input("Given Name: ").strip()
    middle_initial = input("Middle Initial (Press Enter if none): ").strip()


    address_parts = []


    house = input("House Number: ").strip()
    street = input("Street Name: ").strip()
    subdivision = input("Subdivision/Building Name: ").strip()
    barangay = input("Barangay Name: ").strip()
    city = input("City/Municipality: ").strip()


    for item in [house, street, subdivision]:
        if item:
            address_parts.append(item)


    if barangay:
        address_parts.append(f"Bgy. {barangay}")


    if city:
        address_parts.append(city)


    address = ", ".join(address_parts)


    while True:
        mobile = input("Mobile Number (09XXXXXXXXX or +639XXXXXXXXX): ").strip()


        if validate_mobile(mobile):
            break


        print("Invalid mobile number format.")


    while True:
        birthday = input("Birthday (MM/DD/YYYY): ").strip()


        try:
            birth_date = datetime.strptime(birthday, "%m/%d/%Y")


            today = datetime.today()


            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )


            if age < 18:
                print("Customer must be 18 years old or above.")
                return


            break


        except ValueError:
            print("Invalid date format.")


    while True:
        email = input("Email Address: ").strip()


        if validate_email(email):
            break


        print("Invalid email format.")


    customer_id = get_next_id("C", CUSTOMER_LIST)


    full_name = f"{last_name}, {given_name} {middle_initial}".strip()


    filename = f"{customer_id}.txt"


    with open(filename, "w") as file:
        file.write(full_name + "\n")
        file.write(address + "\n")
        file.write(mobile + "\n")
        file.write(birthday + "\n")
        file.write(email + "\n")
        file.write(f"Customer ID # {customer_id}")


    with open(CUSTOMER_LIST, "a") as file:
        file.write(f"{customer_id} {full_name}\n")


    print(f"Customer successfully added. Assigned ID: {customer_id}")


def show_all_customers():


    print("\n===== ALL CUSTOMERS =====")


    if not os.path.exists(CUSTOMER_LIST):
        print("No customers found.")
        return


    with open(CUSTOMER_LIST, "r") as file:
        print(file.read())


def show_customer():


    customer_id = input("Enter Customer ID: ").upper()


    filename = f"{customer_id}.txt"


    if os.path.exists(filename):


        with open(filename, "r") as file:
            print("\n" + file.read())


    else:
        print("Customer not found.")


def delete_customer():


    customer_id = input("Enter Customer ID to delete: ").upper()


    filename = f"{customer_id}.txt"


    if not os.path.exists(filename):
        print("Customer not found.")
        return


    os.remove(filename)


    if os.path.exists(CUSTOMER_LIST):


        with open(CUSTOMER_LIST, "r") as file:
            lines = file.readlines()


        updated_lines = [
            line for line in lines if not line.startswith(customer_id)
        ]


        with open(CUSTOMER_LIST, "w") as file:
            file.writelines(updated_lines)


    print("Customer deleted successfully.")


# ==================================================
# VENUE BLOCK
# ==================================================


def add_venue():


    print("\n===== ADD VENUE =====")


    venue_code = get_next_id("V", VENUE_LIST)


    venue_name = input("Venue Name: ").strip()
    street = input("Street Name: ").strip()
    subdivision = input("Subdivision/Building Name: ").strip()
    barangay = input("Barangay Name: ").strip()
    city = input("City/Municipality: ").strip()


    address = f"{street}, {subdivision}, {barangay}, {city}"


    while True:
        try:
            capacity = int(input("Capacity: "))
            if capacity > 0:
                break
        except ValueError:
            pass


        print("Invalid capacity.")


    while True:
        try:
            sections = int(input("Number of Sections: "))
            if sections > 0:
                break
        except ValueError:
            pass


        print("Invalid section count.")


    while True:
        contact = input("Contact Number (+639XXXXXXXXX): ").strip()


        if validate_mobile(contact):
            break


        print("Invalid contact number.")


    entertainment = input(
        "Entertainment Types (sports game, film, contest, show): "
    )


    filename = f"{venue_code}.txt"


    with open(filename, "w") as file:
        file.write(f"{venue_name}\n")
        file.write(f"{address}\n")
        file.write(f"{capacity}\n")
        file.write(f"Number of Sections: {sections}\n")
        file.write(f"{contact}\n")
        file.write(f"Entertainment Type: {entertainment}\n")
        file.write(f"Venue Code # {venue_code}")


    with open(VENUE_LIST, "a") as file:
        file.write(f"{venue_code} {venue_name}\n")


    print(f"Venue successfully added. Assigned Code: {venue_code}")


def show_all_venues():


    print("\n===== ALL VENUES =====")


    if not os.path.exists(VENUE_LIST):
        print("No venues found.")
        return


    with open(VENUE_LIST, "r") as file:
        print(file.read())


def show_venue():


    venue_code = input("Enter Venue Code: ").upper()


    filename = f"{venue_code}.txt"


    if os.path.exists(filename):


        with open(filename, "r") as file:
            print("\n" + file.read())


    else:
        print("Venue not found.")


def delete_venue():


    venue_code = input("Enter Venue Code to delete: ").upper()


    filename = f"{venue_code}.txt"


    if not os.path.exists(filename):
        print("Venue not found.")
        return


    os.remove(filename)


    if os.path.exists(VENUE_LIST):


        with open(VENUE_LIST, "r") as file:
            lines = file.readlines()


        updated_lines = [
            line for line in lines if not line.startswith(venue_code)
        ]


        with open(VENUE_LIST, "w") as file:
            file.writelines(updated_lines)


    print("Venue deleted successfully.")


# ==================================================
# EVENT BLOCK
# ==================================================


def add_event():


    print("\n===== ADD EVENT =====")


    event_id = get_next_id("E", EVENT_LIST)


    event_name = input("Event Name: ").strip()


    entertainment_type = input(
        "Entertainment Type (sports game, film, contest, show): "
    ).strip()


    show_type = ""


    if entertainment_type.lower() == "show":
        show_type = input(
            "Show Type (concert, play, dance, comedy): "
        ).strip()


    date = input("Date (MM/DD/YYYY): ").strip()


    base_price = input("Base Ticket Price: ").strip()


    contact_person = input("Contact Person: ").strip()


    while True:
        mobile = input("Mobile Number (+639XXXXXXXXX): ").strip()


        if validate_mobile(mobile):
            break


        print("Invalid mobile number.")


    while True:
        email = input("Email Address: ").strip()


        if validate_email(email):
            break


        print("Invalid email address.")


    filename = f"{event_id}.txt"


    with open(filename, "w") as file:
        file.write(event_name + "\n")
        file.write(entertainment_type.title() + "\n")


        if show_type:
            file.write(show_type.title() + "\n")


        file.write(date + "\n")
        file.write(f"Base ticket price: {base_price}\n")
        file.write(contact_person + "\n")
        file.write(mobile + "\n")
        file.write(email + "\n")
        file.write(f"Event ID # {event_id}")


    with open(EVENT_LIST, "a") as file:
        file.write(f"{event_id} {event_name}\n")


    print(f"Event successfully added. Assigned ID: {event_id}")


def show_all_events():


    print("\n===== ALL EVENTS =====")


    if not os.path.exists(EVENT_LIST):
        print("No events found.")
        return


    with open(EVENT_LIST, "r") as file:
        print(file.read())


def show_event():


    event_id = input("Enter Event ID: ").upper()


    filename = f"{event_id}.txt"


    if os.path.exists(filename):


        with open(filename, "r") as file:
            print("\n" + file.read())


    else:
        print("Event not found.")


def delete_event():


    event_id = input("Enter Event ID to delete: ").upper()


    filename = f"{event_id}.txt"


    if not os.path.exists(filename):
        print("Event not found.")
        return


    os.remove(filename)


    if os.path.exists(EVENT_LIST):


        with open(EVENT_LIST, "r") as file:
            lines = file.readlines()


        updated_lines = [
            line for line in lines if not line.startswith(event_id)
        ]


        with open(EVENT_LIST, "w") as file:
            file.writelines(updated_lines)


    print("Event deleted successfully.")


# ==================================================
# BOOKING BLOCK
# ==================================================


def manager_set_availability():


    print("\n===== SET EVENT AVAILABILITY =====")


    event_name = input("Event Name: ").strip()
    venue = input("Venue: ").strip()


    sections = int(input("Number of Sections: "))
    slots = int(input("Available Slots per Section: "))
    base_price = float(input("Base Ticket Price: "))


    with open(AVAILABILITY_FILE, "w") as file:
        file.write(event_name + "\n")
        file.write(venue + "\n")
        file.write(str(sections) + "\n")
        file.write(str(slots) + "\n")
        file.write(str(base_price) + "\n")


    print("Availability saved successfully.")


def load_availability():


    if not os.path.exists(AVAILABILITY_FILE):
        return None


    with open(AVAILABILITY_FILE, "r") as file:
        data = file.readlines()


    return {
        "event_name": data[0].strip(),
        "venue": data[1].strip(),
        "sections": int(data[2].strip()),
        "slots": int(data[3].strip()),
        "base_price": float(data[4].strip())
    }


def get_booking():


    availability = load_availability()


    if availability is None:
        print("No availability data found.")
        return


    print("\n===== CUSTOMER BOOKING =====")


    customer_name = input("Customer Name: ").strip()


    while True:
        mobile = input("Mobile Number: ").strip()


        if validate_mobile(mobile):
            break


        print("Invalid mobile number.")


    payment_type = input(
        "Payment Type (Credit Card, Gcash, Paypal): "
    ).strip()


    section_number = int(input("Section Number: "))
    slots = int(input("Number of Slots: "))


    booking_id = get_next_id("B", BOOKING_LIST)


    if slots <= availability["slots"]:


        total_payment = (
            availability["base_price"]
            * section_number
            * slots
        )


        availability["slots"] -= slots


        with open(AVAILABILITY_FILE, "w") as file:
            file.write(availability["event_name"] + "\n")
            file.write(availability["venue"] + "\n")
            file.write(str(availability["sections"]) + "\n")
            file.write(str(availability["slots"]) + "\n")
            file.write(str(availability["base_price"]) + "\n")


        with open(f"{booking_id}.txt", "w") as file:
            file.write(f"Customer name: {customer_name}\n")
            file.write(f"{mobile}\n")
            file.write(f"Type of payment: {payment_type}\n")
            file.write(f"Event name: {availability['event_name']}\n")
            file.write(f"Venue: {availability['venue']}\n")
            file.write(f"Section number: {section_number}\n")
            file.write(f"Slots: {slots}\n")
            file.write(f"{booking_id}\n")
            file.write(f"Total payment: {total_payment:.2f}\n")


        with open(BOOKING_LIST, "a") as file:
            file.write(f"{booking_id} {total_payment:.2f}\n")


        print("\n===== YOUR ORDER =====")
        print(f"Event name: {availability['event_name']}")
        print(f"Venue: {availability['venue']}")
        print(f"Section number: {section_number}")
        print(f"Slots: {slots}")
        print(f"Type of payment: {payment_type}")
        print(f"Total payment: {total_payment:.2f}")
        print(f"Booking ID: {booking_id}")


    else:


        print("\n===== YOUR ORDER =====")
        print("Total payment: NOT AVAILABLE")


def display_booking():


    booking_id = input("Enter Booking ID: ").upper()


    filename = f"{booking_id}.txt"


    if os.path.exists(filename):


        with open(filename, "r") as file:
            print("\n" + file.read())


    else:
        print("Booking not found.")


def display_all_bookings():


    print("\n===== ALL BOOKINGS =====")


    if not os.path.exists(BOOKING_LIST):
        print("No bookings found.")
        return


    with open(BOOKING_LIST, "r") as file:
        print(file.read())


def delete_booking():


    booking_id = input("Enter Booking ID to delete: ").upper()


    filename = f"{booking_id}.txt"


    if not os.path.exists(filename):
        print("Booking not found.")
        return


    os.remove(filename)


    if os.path.exists(BOOKING_LIST):


        with open(BOOKING_LIST, "r") as file:
            lines = file.readlines()


        updated_lines = [
            line for line in lines if not line.startswith(booking_id)
        ]


        with open(BOOKING_LIST, "w") as file:
            file.writelines(updated_lines)


    print("Booking deleted successfully.")


# ==================================================
# MENUS
# ==================================================


def customer_menu():

    # Requires manager code before opening the customer menu
    if not manager_access():
        return


    while True:


        print("\n===== CUSTOMER MENU =====")
        print("[1] Add Customer")
        print("[2] Show All Customers")
        print("[3] Show Customer")
        print("[4] Delete Customer")
        print("[5] Return to Main Menu")


        choice = input("Enter Choice: ")


        if choice == "1":
            add_customer()


        elif choice == "2":
            show_all_customers()


        elif choice == "3":
            show_customer()


        elif choice == "4":
            delete_customer()


        elif choice == "5":
            break


        else:
            print("Invalid choice.")


def venue_menu():


    if not manager_access():
        return


    while True:


        print("\n===== VENUE MENU =====")
        print("[1] Add Venue")
        print("[2] Show All Venues")
        print("[3] Show Venue")
        print("[4] Delete Venue")
        print("[5] Return to Main Menu")


        choice = input("Enter Choice: ")


        if choice == "1":
            add_venue()


        elif choice == "2":
            show_all_venues()


        elif choice == "3":
            show_venue()


        elif choice == "4":
            delete_venue()


        elif choice == "5":
            break


        else:
            print("Invalid choice.")


def event_menu():


    if not manager_access():
        return


    while True:


        print("\n===== EVENT MENU =====")
        print("[1] Add Event")
        print("[2] Show All Events")
        print("[3] Show Event")
        print("[4] Delete Event")
        print("[5] Return to Main Menu")


        choice = input("Enter Choice: ")


        if choice == "1":
            add_event()


        elif choice == "2":
            show_all_events()


        elif choice == "3":
            show_event()


        elif choice == "4":
            delete_event()


        elif choice == "5":
            break


        else:
            print("Invalid choice.")


def booking_menu():


    while True:


        print("\n===== BOOKING MENU =====")
        print("[1] Manager Set Availability")
        print("[2] Get Booking")
        print("[3] Display Booking")
        print("[4] Display All Bookings")
        print("[5] Delete Booking")
        print("[6] Return to Main Menu")


        choice = input("Enter Choice: ")


        if choice == "1":


            if manager_access():
                manager_set_availability()


        elif choice == "2":
            get_booking()


        elif choice == "3":
            display_booking()


        elif choice == "4":
            display_all_bookings()


        elif choice == "5":


            if manager_access():
                delete_booking()


        elif choice == "6":
            break


        else:
            print("Invalid choice.")


# ==================================================
# MAIN MENU
# ==================================================


def main():


    while True:


        print("\n===================================")
        print(" TickIt: A Ticketing System ")
        print("===================================")
        print("[1] Customer Block")
        print("[2] Venue Block")
        print("[3] Event Block")
        print("[4] Booking Block")
        print("[5] Exit")


        choice = input("Enter Choice: ")


        if choice == "1":
            customer_menu()


        elif choice == "2":
            venue_menu()


        elif choice == "3":
            event_menu()


        elif choice == "4":
            booking_menu()


        elif choice == "5":
            print("Program terminated.")
            break


        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()