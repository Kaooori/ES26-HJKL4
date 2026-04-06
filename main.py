import os
import sys
import venue_block

# Configuration
ACCESS_CODE = "123"
MAX_ATTEMPTS = 3
SESSION_LOG_FILE = "session_log.txt"


def authenticate_manager():
    """Authenticates manager with 3-digit access code."""
    print("\n" + "="*60)
    print("     ENTERTAINMENT COMPANY SYSTEM - MANAGER ACCESS")
    print("="*60)
    
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            pass_input = input(f"Enter 3-digit Manager Code (Attempt {attempts + 1}/{MAX_ATTEMPTS}): ").strip()
            
            if len(pass_input) != 3 or not pass_input.isdigit():
                print("Invalid format. Code must be exactly 3 digits.")
                attempts += 1
                continue
            
            if pass_input == ACCESS_CODE:
                print("✓ Access Granted. Welcome to Venue Management System.")
                log_session("LOGIN_SUCCESS")
                return True
            else:
                attempts += 1
                remaining = MAX_ATTEMPTS - attempts
                if remaining > 0:
                    print(f"✗ Incorrect Code. {remaining} attempt(s) remaining.")
                else:
                    print("✗ Access Denied. Maximum attempts exceeded.")
                    log_session("LOGIN_FAILED")
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"Error during authentication: {e}")
            attempts += 1
    
    return False


def log_session(event):
    """Logs session events for audit trail."""
    try:
        with open(SESSION_LOG_FILE, "a") as file:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {event}\n")
    except IOError:
        pass  # Silently fail if logging not possible


def display_main_menu():
    """Displays the main menu."""
    print("\n" + "="*60)
    print("     VENUE MANAGEMENT BLOCK - MAIN MENU")
    print("="*60)
    print("1. Add Venue")
    print("2. Show All Venues")
    print("3. Show Venue Details")
    print("4. Delete Venue")
    print("5. View Session Log")
    print("6. Exit System")
    print("="*60)


def view_session_log():
    """Displays the session activity log."""
    print("\n--- SESSION LOG ---")
    
    if not os.path.exists(SESSION_LOG_FILE):
        print("No session log available.")
        return
    
    try:
        with open(SESSION_LOG_FILE, "r") as file:
            content = file.read().strip()
            if content:
                print(content)
            else:
                print("Session log is empty.")
    except IOError as e:
        print(f"Error reading session log: {e}")


def main():
    """Main application loop."""
    # Authenticate manager
    if not authenticate_manager():
        print("\n✗ System Access Denied. Exiting...")
        log_session("LOGIN_FAILED_MAX_ATTEMPTS")
        sys.exit(1)
    
    log_session("SESSION_START")
    
    # Main menu loop
    while True:
        try:
            display_main_menu()
            choice = input("Select an option (1-6): ").strip()
            
            if choice == "1":
                venue_block.add_venue()
                log_session("ACTION: ADD_VENUE")
            
            elif choice == "2":
                venue_block.show_all_venues()
                log_session("ACTION: SHOW_ALL_VENUES")
            
            elif choice == "3":
                venue_block.show_venue()
                log_session("ACTION: SHOW_VENUE")
            
            elif choice == "4":
                venue_block.delete_venue()
                log_session("ACTION: DELETE_VENUE")
            
            elif choice == "5":
                view_session_log()
            
            elif choice == "6":
                print("\n" + "="*60)
                print("Thank you for using the Entertainment Company System.")
                print("="*60)
                log_session("SESSION_END")
                break
            
            else:
                print("✗ Invalid choice. Please select 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n✗ System interrupted by user.")
            log_session("SESSION_INTERRUPTED")
            break
        
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")
            log_session(f"ERROR: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)