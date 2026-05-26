import os
import re
from datetime import datetime

# ==================================================
# ONLINE TICKETING SYSTEM
# ==================================================

MANAGER_CODE = "777"

CUSTOMER_LIST = "Customer List.txt"
VENUE_LIST = "Venue List.txt"
EVENT_LIST = "Event List.txt"
BOOKING_LIST = "Booking List.txt"
AVAILABILITY_FILE = "availability.txt"


# ==================================================
# GENERAL FUNCTIONS
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
    attempts = 3

    while attempts > 0:
        code = input("Enter Manager Code: ")

        if code == MANAGER_CODE:
            print("Access Accepted.")
            return True

        attempts -= 1
        print(f"Access Denied. {attempts} attempt/s left.")

    print("Too many failed attempts.")
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
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
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
        updated_lines = [line for line in lines if not line.startswith(customer_id)]
        with open(CUSTOMER_LIST, "w") as file:
            file.writelines(updated_lines)
    print("Customer deleted successfully.")


# ==================================================
# VENUE AND EVENT HANDLERS OMITTED FOR SPACE
# NOTE: These remain unchanged unless specifically mentioned.
#
# ==================================================

# ==================================================
# UPDATED BOOKING FUNCTION STARTS HERE
# ==================================================

def get_booking():
    print("\n===== CUSTOMER BOOKING =====")

    # Step 1: Get Customer Information
    while True:
        customer_id = input("Enter Customer ID: ").upper().strip()
        if os.path.exists(f"{customer_id}.txt"):
            break
        print("Customer ID not found in system record.")

    with open(f"{customer_id}.txt", "r") as file:
        cust_data = file.readlines()
    customer_name = cust_data[0].strip()
    mobile = cust_data[2].strip()

    print(f"Booking for Customer: {customer_name} ({mobile})")

    # Step 2: Select Event
    while True:
        event_id = input("Enter Event ID: ").upper().strip()
        if os.path.exists(f"{event_id}.txt"):
            break
        print("Event ID does not exist!")
        if os.path.exists(EVENT_LIST):
            print("--- Available Events ---")
            with open(EVENT_LIST, "r") as file:
                print(file.read().strip())
            print("------------------------")

    # Load Event Information
    with open(f"{event_id}.txt", "r") as file:
        event_lines = file.readlines()

    event_name = event_lines[0].strip()
    base_price_line = event_lines[3].strip()
    try:
        base_price = float(base_price_line.split(":")[-1].strip())
    except ValueError:
        base_price = 0.0

    # Step 3: Select Section
    while True:
        try:
            section_number = int(input("Section Number (1 to 10): "))  # Assuming 10 sections for simplicity
            if 1 <= section_number <= 10:
                break
        except ValueError:
            pass
        print("Invalid Section Number.")

    # Step 4: Calculate Total Price
    while True:
        try:
            slots = int(input("Number of Slots to Buy: "))
            if slots > 0:
                break
        except ValueError:
            pass
        print("Invalid slots entry.")

    # Total price calculated using the updated formula
    total_payment = base_price * slots * section_number

    # Booking confirmation
    booking_id = get_next_id("B", BOOKING_LIST)
    with open(f"{booking_id}.txt", "w") as file:
        file.write(f"Customer ID: {customer_id}\n")
        file.write(f"Customer name: {customer_name}\n")
        file.write(f"{mobile}\n")
        file.write(f"Event name: {event_name}\n")
        file.write(f"Section number: {section_number}\n")
        file.write(f"Slots: {slots}\n")
        file.write(f"{booking_id}\n")
        file.write(f"Total payment: {total_payment:.2f}\n")

    with open(BOOKING_LIST, "a") as file:
        file.write(f"{booking_id} {total_payment:.2f}\n")

    print("\n===== YOUR ORDER =====")
    print(f"Event name: {event_name}")
    print(f"Section number: {section_number}")
    print(f"Slots Ordered: {slots}")
    print(f"Total payment: ₱{total_payment:.2f}")
    print(f"Booking ID: {booking_id}")


# ==================================================
# MAIN MENU FUNCTION BELOW
# ==================================================

def main():
    while True:
        print("\n===================================")
        print("    TickIt: A Ticketing System     ")
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