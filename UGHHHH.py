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

def get_availability_filename(event_id):
    """Generates a consistent tracking filename for each event ID."""
    clean_id = event_id.upper().strip()
    return f"availability_{clean_id}.txt"


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
    prefix = prefix.upper()
    if not os.path.exists(list_file):
        return f"{prefix}-001"

    with open(list_file, "r") as file:
        lines = file.readlines()

    if not lines:
        return f"{prefix}-001"

    last_line = lines[-1].strip()
    last_id = last_line.split()[0]
    try:
        last_num = int(last_id.split("-")[1])
    except (IndexError, ValueError):
        last_num = 0

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
    customer_id = input("Enter Customer ID: ").upper().strip()
    filename = f"{customer_id}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            print("\n" + file.read())
    else:
        print("Customer not found.")


def delete_customer():
    customer_id = input("Enter Customer ID to delete: ").upper().strip()
    filename = f"{customer_id}.txt"
    if not os.path.exists(filename):
        print("Customer not found.")
        return

    os.remove(filename)
    if os.path.exists(CUSTOMER_LIST):
        with open(CUSTOMER_LIST, "r") as file:
            lines = file.readlines()
        updated_lines = [line for line in lines if not line.upper().startswith(customer_id)]
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

    entertainment = input("Entertainment Types (sports game, film, contest, show): ")
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
    venue_code = input("Enter Venue Code: ").upper().strip()
    filename = f"{venue_code}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            print("\n" + file.read())
    else:
        print("Venue not found.")


def delete_venue():
    venue_code = input("Enter Venue Code to delete: ").upper().strip()
    filename = f"{venue_code}.txt"
    if not os.path.exists(filename):
        print("Venue not found.")
        return

    os.remove(filename)
    if os.path.exists(VENUE_LIST):
        with open(VENUE_LIST, "r") as file:
            lines = file.readlines()
        updated_lines = [line for line in lines if not line.upper().startswith(venue_code)]
        with open(VENUE_LIST, "w") as file:
            file.writelines(updated_lines)
    print("Venue deleted successfully.")


# ==================================================
# EVENT BLOCK
# ==================================================

def get_entertainment_type():
    while True:
        print("\nChoose the entertainment type of your event.\n[1] Sports Game\n[2] Film\n[3] Contest\n[4] Show\n")
        choice3 = input("Entertainment Type: ").strip()

        if choice3 == "1":
            return "Sports Game"
        elif choice3 == "2":
            return "Film"
        elif choice3 == "3":
            return "Contest"
        elif choice3 == "4":
            while True:
                print("\nChoose the show type of your event.\n[1] Concert\n[2] Play\n[3] Dance\n[4] Comedy\n")
                choice4 = input("Show Type: ").strip()

                if choice4 == "1":
                    return "Show\nConcert"
                elif choice4 == "2":
                    return "Show\nPlay"
                elif choice4 == "3":
                    return "Show\nDance"
                elif choice4 == "4":
                    return "Show\nComedy"
                else:
                    print("\n>> Invalid show type choice. Please retry.")
        else:
            print("\n>> Invalid entertainment choice. Please retry.")


def add_event():
    print("\n===== ADD EVENT =====")
    event_id = get_next_id("E", EVENT_LIST)

    event_name = input("Event Name: ").strip()
    entertainment_type = get_entertainment_type()
    date = input("Date (Month Day, Year): ").strip()
    while True:
        try:
            base_price = float(input("Base Ticket Price: ₱").strip())
            if base_price > 0:
                break
            print("Base price must be greater than 0.")
        except ValueError:
            print("Invalid base price. Please enter a valid number.")
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
        file.write(date + "\n")
        file.write(f"Base ticket price: {base_price:.2f}\n")
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
    event_id = input("Enter Event ID: ").upper().strip()
    filename = f"{event_id}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            print("\n" + file.read())
    else:
        print("Event not found.")


def delete_event():
    event_id = input("Enter Event ID to delete: ").upper().strip()
    filename = f"{event_id}.txt"
    if not os.path.exists(filename):
        print("Event not found.")
        return

    os.remove(filename)
    if os.path.exists(EVENT_LIST):
        with open(EVENT_LIST, "r") as file:
            lines = file.readlines()
        updated_lines = []
        for line in lines:
            if line.upper().startswith(event_id):
                updated_lines.append(f"{event_id} [DELETED EVENT]\n")
            else:
                updated_lines.append(line)
        with open(EVENT_LIST, "w") as file:
            file.writelines(updated_lines)

    avail_file = get_availability_filename(event_id)
    if os.path.exists(avail_file):
        os.remove(avail_file)

    print("Event deleted successfully.")


# ==================================================
# BOOKING BLOCK
# ==================================================

def manager_set_availability():
    print("\n===== SET EVENT AVAILABILITY =====")

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

    while True:
        venue_code = input("Enter Venue Code: ").upper().strip()
        if os.path.exists(f"{venue_code}.txt"):
            break
        print("Venue Code does not exist!")
        if os.path.exists(VENUE_LIST):
            print("--- Available Venues ---")
            with open(VENUE_LIST, "r") as file:
                print(file.read().strip())
            print("------------------------")

    with open(f"{event_id}.txt", "r") as f:
        event_lines = f.readlines()
    event_name = event_lines[0].strip()

    base_price_line = event_lines[3].strip()
    try:
        base_price = float(base_price_line.split(":")[-1].strip())
    except ValueError:
        base_price = 0.0

    with open(f"{venue_code}.txt", "r") as f:
        venue_lines = f.readlines()
    venue_name = venue_lines[0].strip()

    sections_line = venue_lines[3].strip()
    try:
        sections = int(sections_line.split(":")[-1].strip())
    except ValueError:
        sections = 1

    print(f"\nLinked Event: {event_name} (Base Price: ₱{base_price:.2f})")
    print(f"Linked Venue: {venue_name} (Max Sections: {sections})")

    while True:
        try:
            slots_per_section = int(input("Available Slots per Section: "))
            if slots_per_section > 0:
                break
        except ValueError:
            pass
        print("Invalid slot count.")

    slots_mapping = ",".join([f"{sec}:{slots_per_section}" for sec in range(1, sections + 1)])

    avail_file = get_availability_filename(event_id)
    with open(avail_file, "w") as file:
        file.write(event_name + "\n")
        file.write(venue_name + "\n")
        file.write(str(sections) + "\n")
        file.write(slots_mapping + "\n")
        file.write(str(base_price) + "\n")

    print(f"Availability configured successfully for Event {event_id}.")


def load_availability(event_id):
    """
    Tries to open the configuration file. If it does not exist, it extracts info
    directly from E-XXX.txt master event layout so booking can continue smoothly.
    """
    avail_file = get_availability_filename(event_id)
    
    if not os.path.exists(avail_file):
        master_event_file = f"{event_id}.txt"
        if not os.path.exists(master_event_file):
            return None
            
        with open(master_event_file, "r") as f:
            lines = f.readlines()
        event_name = lines[0].strip()
        
        try:
            base_price = float(lines[3].split(":")[-1].strip())
        except (ValueError, IndexError):
            base_price = 0.0
            
        # Defaults if manager hasn't set explicit venue layout links yet
        default_sections = 5
        default_slots = 100
        slots_mapping_str = ",".join([f"{i}:{default_slots}" for i in range(1, default_sections + 1)])
        
        with open(avail_file, "w") as file:
            file.write(event_name + "\n")
            file.write("General Arena\n")
            file.write(str(default_sections) + "\n")
            file.write(slots_mapping_str + "\n")
            file.write(str(base_price) + "\n")

    with open(avail_file, "r") as file:
        data = file.readlines()

    slots_dict = {}
    mapping_str = data[3].strip()
    if mapping_str:
        for pair in mapping_str.split(","):
            sec_num, slt_cnt = pair.split(":")
            slots_dict[int(sec_num)] = int(slt_cnt)

    return {
        "event_name": data[0].strip(),
        "venue": data[1].strip(),
        "sections": int(data[2].strip()),
        "slots_map": slots_dict,
        "base_price": float(data[4].strip())
    }


def get_booking():
    print("\n===== CUSTOMER BOOKING =====")

    while True:
        customer_id = input("Enter Customer ID: ").upper().strip()
        if os.path.exists(f"{customer_id}.txt"):
            break
        print("Customer ID not found in system record.")

    while True:
        event_input = input("Enter Event ID (e.g., E-001): ").strip()
        # Parse text so typing "E-001" or "E-001 Concert Name" both extract "E-001" safely
        match = re.match(r'^(E-\d{3})', event_input, re.IGNORECASE)
        event_id = match.group(1).upper() if match else event_input.upper()

        availability = load_availability(event_id)
        if availability is not None:
            break
            
        print(f"Event registration data '{event_id}' was not found.")
        if os.path.exists(EVENT_LIST):
            print("--- Registered Events ---")
            with open(EVENT_LIST, "r") as file:
                print(file.read().strip())
            print("-------------------------")

    with open(f"{customer_id}.txt", "r") as file:
        cust_data = file.readlines()
    customer_name = cust_data[0].strip()
    mobile = cust_data[2].strip()

    print(f"\nBooking for Customer: {customer_name} ({mobile})")
    print(f"Selected Event: {availability['event_name']} (Base Price: ₱{availability['base_price']:.2f})")
    payment_type = input("Payment Type (Credit Card, Gcash, Paypal): ").strip()

    while True:
        try:
            section_number = int(input(f"Section Number (1 to {availability['sections']}): "))
            if 1 <= section_number <= availability["sections"]:
                break
        except ValueError:
            pass
        print("Invalid Section Number.")

    available_slots = availability["slots_map"].get(section_number, 0)

    while True:
        try:
            print(f"Available Slots in Section {section_number}: {available_slots}")
            slots = int(input("Number of Slots to Buy: "))
            if slots > 0:
                break
        except ValueError:
            pass
        print("Invalid slots entry.")

    booking_id = get_next_id("B", BOOKING_LIST)

    if slots <= available_slots:
        # Combined Calculation Requirement: Section Chosen * Slots Bought * Event Base Price
        total_payment = section_number * slots * availability["base_price"]

        availability["slots_map"][section_number] -= slots
        slots_mapping_str = ",".join([f"{sec}:{slt}" for sec, slt in availability["slots_map"].items()])

        avail_file = get_availability_filename(event_id)
        with open(avail_file, "w") as file:
            file.write(availability["event_name"] + "\n")
            file.write(availability["venue"] + "\n")
            file.write(str(availability["sections"]) + "\n")
            file.write(slots_mapping_str + "\n")
            file.write(str(availability["base_price"]) + "\n")

        with open(f"{booking_id}.txt", "w") as file:
            file.write(f"Customer ID: {customer_id}\n")
            file.write(f"Customer name: {customer_name}\n")
            file.write(f"{mobile}\n")
            file.write(f"Type of payment: {payment_type}\n")
            file.write(f"Event ID: {event_id}\n")
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
        print(f"Slots Ordered: {slots}")
        print(f"Type of payment: {payment_type}")
        print(f"Total payment: ₱{total_payment:.2f} (Formula: Section {section_number} × {slots} Slots × ₱{availability['base_price']:.2f})")
        print(f"Booking ID: {booking_id}")

    else:
        print("\n===== YOUR ORDER =====")
        print("Booking failed. Not enough available slots left in this section.")


def display_booking():
    booking_id = input("Enter Booking ID: ").upper().strip()
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
    booking_id = input("Enter Booking ID to delete: ").upper().strip()
    filename = f"{booking_id}.txt"
    if not os.path.exists(filename):
        print("Booking not found.")
        return

    os.remove(filename)
    if os.path.exists(BOOKING_LIST):
        with open(BOOKING_LIST, "r") as file:
            lines = file.readlines()
        updated_lines = [line for line in lines if not line.upper().startswith(booking_id)]
        with open(BOOKING_LIST, "w") as file:
            file.writelines(updated_lines)
    print("Booking deleted successfully.")


# ==================================================
# MENUS
# ==================================================

def customer_menu():
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
        print("[1] Manager Set Availability (Manager Required)")
        print("[2] Get Booking (Public/Customer)")
        print("[3] Display Booking (Manager Required)")
        print("[4] Display All Bookings (Manager Required)")
        print("[5] Delete Booking (Manager Required)")
        print("[6] Return to Main Menu")

        choice = input("Enter Choice: ")

        if choice == "1":
            if manager_access():
                manager_set_availability()

        elif choice == "2":
            get_booking()

        elif choice == "3":
            if manager_access():
                display_booking()

        elif choice == "4":
            if manager_access():
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