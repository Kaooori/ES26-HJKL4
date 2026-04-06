import os
import re

VENUE_LIST_FILE = "Venue List.txt"
PHONE_PATTERN = r"^\+63\d{9,}$"
VALID_ENTERTAINMENT_TYPES = {"sports game", "film", "contest", "show"}
VALID_SHOW_SUBTYPES = {"concert", "play", "dance", "comedy"}


def get_next_venue_code():
    """Generates the next unique venue code (V-XXX)."""
    if not os.path.exists(VENUE_LIST_FILE):
        return "V-001"
    
    try:
        with open(VENUE_LIST_FILE, "r") as file:
            lines = file.readlines()
            if not lines:
                return "V-001"
            
            last_line = lines[-1].strip()
            if not last_line:
                return "V-001"
            
            last_code = last_line.split(" ")[0]
            last_num = int(last_code.split("-")[1])
            return f"V-{last_num + 1:03d}"
    except (IndexError, ValueError):
        print("Error reading venue codes. Starting from V-001")
        return "V-001"


def validate_contact_number():
    """Validates contact number format (+63...).  with at least 9 digits."""
    while True:
        num = input("Contact Number (Format: +63...): ").strip()
        if re.match(PHONE_PATTERN, num):
            return num
        print("Invalid format. Use +63 followed by at least 9 digits (e.g., +639123456789)")


def get_entertainment_types():
    """Prompts user to select entertainment types with show subtypes."""
    selected_types = []
    
    while True:
        print("\nAvailable entertainment types: sports game, film, contest, show")
        choice = input("Enter entertainment type (or 'done' to finish): ").strip().lower()
        
        if choice == 'done':
            if selected_types:
                break
            else:
                print("You must enter at least one entertainment type.")
                continue
        
        if choice not in VALID_ENTERTAINMENT_TYPES:
            print(f"Invalid type. Choose from: {', '.join(sorted(VALID_ENTERTAINMENT_TYPES))}")
            continue
        
        if choice == "show":
            print(f"Show subtypes: {', '.join(sorted(VALID_SHOW_SUBTYPES))}")
            subtypes_input = input("Enter show subtype(s) (comma-separated): ").strip().lower()
            subtypes = [s.strip() for s in subtypes_input.split(",") if s.strip() in VALID_SHOW_SUBTYPES]
            
            if subtypes:
                selected_types.append(f"Show ({', '.join(subtypes)})")
            else:
                print(f"Invalid subtypes. Choose from: {', '.join(sorted(VALID_SHOW_SUBTYPES))}")
        else:
            formatted = "Sports Game" if choice == "sports game" else choice.capitalize()
            if formatted not in selected_types:
                selected_types.append(formatted)
    
    return ", ".join(selected_types)


def add_venue():
    """Creates a new venue with V-XXX file and updates Venue List."""
    print("\n--- ADD VENUE ---")
    
    # Generate next venue code
    venue_code = get_next_venue_code()
    print(f"New Venue Code: {venue_code}")
    
    # Get user input
    print("\nEnter venue details:")
    name = input("Venue Name: ").strip()
    street = input("Street Name: ").strip()
    subdiv = input("Subdivision/Building Name: ").strip()
    brgy = input("Barangay Name: ").strip()
    city = input("City/Municipality: ").strip()
    
    # Validate capacity
    while True:
        try:
            capacity = int(input("Capacity: ").strip())
            if capacity > 0:
                break
            print("Capacity must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Validate sections
    while True:
        try:
            sections = int(input("Number of sections: ").strip())
            if sections > 0:
                break
            print("Number of sections must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Get and validate contact
    contact = validate_contact_number()
    
    # Get entertainment types
    ent_type = get_entertainment_types()
    
    # Create individual venue file
    filename = f"{venue_code}.txt"
    try:
        with open(filename, "w") as file:
            file.write(f"Venue Name: {name}\n")
            file.write(f"Address: {street}, {subdiv}, {brgy}, {city}\n")
            file.write(f"Capacity: {capacity}\n")
            file.write(f"Number of Sections: {sections}\n")
            file.write(f"Contact Number: {contact}\n")
            file.write(f"Entertainment Types: {ent_type}\n")
            file.write(f"Venue Code: {venue_code}\n")
        
        # Update Venue List
        with open(VENUE_LIST_FILE, "a") as file:
            file.write(f"{venue_code} {name}\n")
        
        print(f"\n✓ Venue '{name}' added successfully with code {venue_code}")
    except IOError as e:
        print(f"Error creating venue file: {e}")


def show_all_venues():
    """Displays all venues from Venue List.txt."""
    print("\n--- SHOW ALL VENUES ---")
    
    if not os.path.exists(VENUE_LIST_FILE):
        print("No venues have been added yet.")
        return
    
    try:
        with open(VENUE_LIST_FILE, "r") as file:
            content = file.read().strip()
            if content:
                print("\nVenue List:")
                print("-" * 50)
                print(content)
                print("-" * 50)
            else:
                print("The venue list is empty.")
    except IOError as e:
        print(f"Error reading venue list: {e}")


def show_venue():
    """Displays details of a specific venue."""
    print("\n--- SHOW VENUE ---")
    venue_code = input("Enter Venue Code (e.g., V-001): ").strip().upper()
    
    # Validate code format
    if not re.match(r"^V-\d{3}$", venue_code):
        print("Invalid venue code format. Use format: V-XXX")
        return
    
    filename = f"{venue_code}.txt"
    
    if os.path.exists(filename):
        try:
            print(f"\n--- Details for {venue_code} ---")
            with open(filename, "r") as file:
                print(file.read().strip())
            print("-" * 50)
        except IOError as e:
            print(f"Error reading venue file: {e}")
    else:
        print(f"Error: Venue '{venue_code}' not found.")


def delete_venue():
    """Deletes a venue and its entry from Venue List."""
    print("\n--- DELETE VENUE ---")
    venue_code = input("Enter Venue Code to delete (e.g., V-001): ").strip().upper()
    
    # Validate code format
    if not re.match(r"^V-\d{3}$", venue_code):
        print("Invalid venue code format. Use format: V-XXX")
        return
    
    filename = f"{venue_code}.txt"
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete {venue_code}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Deletion cancelled.")
        return
    
    # Delete individual venue file
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"✓ Venue file '{filename}' deleted.")
        except IOError as e:
            print(f"Error deleting venue file: {e}")
            return
    else:
        print(f"Venue file '{filename}' not found.")
        return
    
    # Remove from Venue List
    if os.path.exists(VENUE_LIST_FILE):
        try:
            with open(VENUE_LIST_FILE, "r") as file:
                lines = file.readlines()
            
            with open(VENUE_LIST_FILE, "w") as file:
                for line in lines:
                    if not line.startswith(venue_code):
                        file.write(line)
            
            print(f"✓ Venue List updated.")
        except IOError as e:
            print(f"Error updating Venue List: {e}")
    else:
        print("Venue List file not found, but venue file was deleted.")


def main_menu():
    """Main menu for venue management system."""
    while True:
        print("\n" + "="*50)
        print("     ONLINE TICKETING SYSTEM - VENUE MANAGER")
        print("="*50)
        print("1. Add Venue")
        print("2. Show All Venues")
        print("3. Show Venue Details")
        print("4. Delete Venue")
        print("5. Exit")
        print("="*50)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            add_venue()
        elif choice == "2":
            show_all_venues()
        elif choice == "3":
            show_venue()
        elif choice == "4":
            delete_venue()
        elif choice == "5":
            print("\nThank you for using Venue Manager. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main_menu()