import subprocess

from cassandra.cluster import Cluster


def execute_script(script_name):
    try:
        subprocess.run(["python3", f"{script_name}.py"])
    except FileNotFoundError:
        print(f"Script '{script_name}.py' not found.")


def execute_script_shell(script_name):
    try:
        subprocess.run([f"./{script_name}.sh"])
    except FileNotFoundError:
        print(f"Script '{script_name}.sh' not found.")


def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. See Book Details")
        print("4. Update Book")
        print("5. Make Reservation")
        print("6. See Reservation")
        print("7. Update Reservation")
        print("8. Exit")
        print("9: Clean and fill")
        print("10: perform stress test #1")
        print("11: perform stress test #2")
        print("12: perform stress test #3")
        print("13: perform stress test #4")
        choice = input("Enter your choice: ")

        if choice == "1":
            execute_script("add_book")
        elif choice == "2":
            execute_script("delete_book")
        elif choice == "3":
            execute_script("read_book")
        elif choice == "4":
            execute_script("update_book")
        elif choice == "5":
            execute_script("make_reservation")
        elif choice == "6":
            execute_script("see_reservation")
        elif choice == "7":
            execute_script("update_reservation")
        elif choice == "8":
            break
        elif choice == "9":
            execute_script_shell("clean")
            execute_script("fill_library")
        elif choice == "10":
            execute_script("stress_one")
        elif choice == "11":
            execute_script("stress_two")
        elif choice == "12":
            execute_script("stress_three")
        elif choice == "13":
            execute_script_shell("clean")
            execute_script("fill_library")
            execute_script("stress_four")
        else:
            print("Invalid choice. Please try again.")

    print("Exiting the program.")


if __name__ == "__main__":
    main_menu()
