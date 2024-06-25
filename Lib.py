import os
from datetime import datetime, timedelta

ACCOUNT_FILE = 'account.txt'
LIBRARY_FILE = 'library.txt'
TRANSPORTATION_FILE = 'tran_system.txt'
MENU_FILE = 'menu.txt'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # Define the date format used in the file

def ask_for_account():
    return input("Do you have an account? (yes/no): ").strip().lower()

def get_account_info():
    account = input("Enter your account: ").strip()
    password = input("Enter your password: ").strip()
    return account, password

def verify_account(account, password):
    if not os.path.exists(ACCOUNT_FILE):
        return False
    with open(ACCOUNT_FILE, 'r') as file:
        for line in file:
            stored_account, stored_password = line.strip().split(maxsplit=1)
            if stored_account == account and stored_password == password:
                return True
    return False

def check_duplicate_account(account):
    if not os.path.exists(ACCOUNT_FILE):
        return False
    with open(ACCOUNT_FILE, 'r') as file:
        for line in file:
            stored_account, _ = line.strip().split(maxsplit=1)
            if stored_account == account:
                return True
    return False

def create_account():
    while True:
        new_account = input("Enter a new account name: (No spaces in between)").strip()
        if check_duplicate_account(new_account):
            print("Account name already exists. Please enter a different account name.")
        else:
            break
    new_password = input("Enter a new password: (No spaces in between)").strip()
    with open(ACCOUNT_FILE, 'a') as file:
        file.write(f"{new_account} {new_password}\n")
    print("Account created successfully.")

def prompt_for_function():
    return input("What function do you need? (check, make reservation, transportation information, food menu): ").strip().lower()

def check_library():
    if not os.path.exists(LIBRARY_FILE):
        print("Library file not found.")
        return

    now = datetime.now()

    with open(LIBRARY_FILE, 'r') as file:
        lines = file.readlines()

    with open(LIBRARY_FILE, 'w') as file:
        print("Room Name | Reservation Status | Reservation Person | Reservation Expiration Time")
        print("--------------------------------------------------------------")

        for line in lines:
            room_name, reservation_status, reservation_person, reservation_expiration_time = line.strip().split(maxsplit=3)

            if reservation_expiration_time != "NONE":
                expiration_time = datetime.strptime(reservation_expiration_time, DATE_FORMAT)
                if expiration_time < now:
                    reservation_status = "NONE"
                    reservation_person = "NONE"
                    reservation_expiration_time = "NONE"

            print(f"{room_name} | {reservation_status} | {reservation_person} | {reservation_expiration_time}")
            file.write(f"{room_name} {reservation_status} {reservation_person} {reservation_expiration_time}\n")

def make_reservation(logged_in_user):
    while True:
        check_library()
        room_name = input("Enter the room name you are interested in: ").strip()

        with open(LIBRARY_FILE, 'r') as file:
            lines = file.readlines()

        room_found = False
        for i, line in enumerate(lines):
            rn, rs, rp, ret = line.strip().split(maxsplit=3)
            if rn == room_name:
                room_found = True
                if rs == "NONE":
                    print("The room can be reserved.")
                    break
                else:
                    print("The room is already reserved.")
                    continue_choice = input("Do you want to see remaining rooms? (yes/no): ").strip().lower()
                    if continue_choice == 'no':
                        return
                    else:
                        break

        if room_found and rs == "NONE":
            break

        if not room_found or (room_found and rs != "NONE" and continue_choice == 'yes'):
            continue

    while True:
        reserve_time_str = input("When do you want to reserve the room? (in the form of %Y-%m-%d %H:%M:%S): ").strip()
        try:
            reserve_time = datetime.strptime(reserve_time_str, DATE_FORMAT)
            if reserve_time > datetime.now():
                break
            else:
                print("Reservation time must be in the future. Please re-enter.")
        except ValueError:
            print("Invalid date format. Please re-enter.")

    while True:
        reserve_duration_str = input("How many hours do you want to reserve? (must be less than 5 hours, and can only be entered as an integer in hours): ").strip()
        try:
            reserve_duration = int(reserve_duration_str)
            if 1 <= reserve_duration < 5:
                break
            else:
                print("Reservation duration must be an integer less than 5 hours. Please re-enter.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    reserve_expiration_time = reserve_time + timedelta(hours=reserve_duration)

    lines[i] = f"{room_name} BOOKED {logged_in_user} {reserve_expiration_time.strftime(DATE_FORMAT)}\n"

    with open(LIBRARY_FILE, 'w') as file:
        file.writelines(lines)

    print("Reservation successful.")
    return

def display_transportation_information():
    if not os.path.exists(TRANSPORTATION_FILE):
        print("Transportation information file not found.")
        return

    with open(TRANSPORTATION_FILE, 'r') as file:
        for line in file:
            print(line.strip())

def display_menu():
    if not os.path.exists(MENU_FILE):
        print("Menu file not found.")
        return

    with open(MENU_FILE, 'r') as file:
        for line in file:
            print(line.strip())

def main():
    user_response = ask_for_account()
    if user_response == 'yes':
        account, password = get_account_info()
        if verify_account(account, password):
            print("Login successful.")
            while True:
                function_needed = prompt_for_function()
                if function_needed == "check":
                    check_library()
                elif function_needed == "make reservation":
                    make_reservation(account)
                elif function_needed == "transportation information":
                    display_transportation_information()
                elif function_needed == "food menu":
                    display_menu()
                else:
                    print(f"The functionality '{function_needed}' is not implemented yet.")

                stay_or_leave = input("Do you want to stay on this page? (yes/no): ").strip().lower()
                if stay_or_leave == 'no':
                    print("Exiting the program.")
                    break
        else:
            print("Invalid account or password.")
    elif user_response == 'no':
        create_account()
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()




