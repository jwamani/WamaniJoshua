
import csv
import json
import logging
import os
import re
from datetime import datetime
from typing import Any


CSV_FILE  = "students.csv"
JSON_FILE = "students.json"
LOG_FILE  = "student_system.log"

# CSV column headers
CSV_HEADERS = ["reg_number", "first_name", "last_name", "dob", "email", "gpa"]

# logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Custom System Exceptions
class StudentNotFoundError(Exception):
    """Raised when a student registration number does not exist in the system."""
    pass


class DuplicateRegistrationError(Exception):
    """Raised when a user tries to add a student whose reg number already exists."""
    pass


class InvalidInputError(Exception):
    """Raised when user-provided data fails validation rules."""
    pass


# validation helpers
def validate_reg_number(reg: str) -> str:
    """
    validates the registration number to match the pattern 2[0-5]-U-xxx for 2020 to date and 1[0-9]-U-xxx for 2019 and below
    """
    reg = reg.strip().upper()
    if not re.match(r"^([2][0-5]|[1][0-9])-U-[\d]{4,5}$", reg):
        raise InvalidInputError(
            "Registration number must match pattern 2x-U-xxxx "
            "e.g. 24-U-00001."
        )
    return reg


def validate_email(email: str) -> str:
    """Basic e-mail format validation. Returns stripped email or raises InvalidInputError."""
    email = email.strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise InvalidInputError(f"'{email}' is not a valid e-mail address.")
    return email


def validate_gpa(gpa_str: str) -> float:
    """
    Validate GPA is a float between 0.0 and 5.0.
    Returns the float value or raises InvalidInputError.
    """
    try:
        gpa = float(gpa_str)
    except ValueError:
        raise InvalidInputError("GPA must be a numeric value (e.g. 3.5).")
    if not (0.0 <= gpa <= 5.0):
        raise InvalidInputError("GPA must be between 0.0 and 4.0.")
    return round(gpa, 2)


def validate_date(date_str: str) -> str:
    """Validate date in YYYY-MM-DD format. Returns the string or raises InvalidInputError."""
    date_str = date_str.strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise InvalidInputError("Date must be in YYYY-MM-DD format (e.g. 2002-05-14).")
    return date_str

# core student operations
def _init_csv() -> None:
    """Create the CSV file with headers if it does not already exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
        logger.info("CSV file initialised: %s", CSV_FILE)


def load_csv() -> list[dict]:
    """Read all student records from the CSV file and return as a list of dicts."""
    _init_csv()
    records: list[dict[str, Any]] = []
    try:
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except OSError as e:
        logger.error("Failed to read CSV: %s", e)
        raise
    return records


def save_csv(records: list[dict[str, Any]]) -> None:
    """Overwrite the CSV file with the provided list of student record dicts."""
    try:
        with open(CSV_FILE, "w") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(records)
    except OSError as e:
        logger.error("Failed to write CSV: %s", e)
        raise


# additional student details with json
def _init_json() -> None:
    """Create an empty JSON object file if it does not already exist."""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as f:
            json.dump({}, f, indent=4)
        logger.info("JSON file initialised: %s", JSON_FILE)


def load_json() -> dict[str, dict[str, Any]]:
    """Load the JSON details store (keyed by reg_number) and return as a dict."""
    _init_json()
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logger.error("Failed to read JSON: %s", e)
        raise
    return data


def save_json(data: dict[str, Any]) -> None:
    """Persist the JSON details store back to disk."""
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        logger.error("Failed to write JSON: %s", e)
        raise


# Core CRUD functions
def add_student() -> None:
    """
    Raises DuplicateRegistrationError if the reg number already exists.
    """
    print("\n--- Add New Student ---")
    logger.info("User initiated: Add Student")

    try:
        # Collect and validate user input
        reg_number = validate_reg_number(input("Registration Number (e.g. 24-U-xxxxx): "))
        first_name = input("First Name: ").strip()
        last_name  = input("Last Name:  ").strip()

        if not first_name or not last_name:
            raise InvalidInputError("First name and last name cannot be empty.")

        dob   = validate_date(input("Date of Birth (YYYY-MM-DD): "))
        email = validate_email(input("Email Address: "))
        gpa   = validate_gpa(input("GPA (0.0 - 5.0): "))

        # Collect additional/JSON fields 
        address = input("Address: ").strip()
        contact = input("Contact Phone: ").strip()
        program = input("Program (e.g. BSc Computer Science): ").strip()

        # Check for duplicate reg number 
        records = load_csv()
        if any(r["reg_number"] == reg_number for r in records):
            raise DuplicateRegistrationError(
                f"A student with registration number '{reg_number}' already exists."
            )

        #Persist to CSV
        records.append({
            "reg_number": reg_number,
            "first_name": first_name,
            "last_name":  last_name,
            "dob":        dob,
            "email":      email,
            "gpa":        gpa,
        })
        save_csv(records)

        # Persist additional details to JSON
        details = load_json()
        details[reg_number] = {
            "address": address,
            "contact": contact,
            "program": program,
            "enrolled": datetime.today().strftime("%Y-%m-%d"),
        }
        save_json(details)

        print(f"\nStudent '{first_name} {last_name}' added successfully.")
        logger.info("Student added: %s (%s %s)", reg_number, first_name, last_name)

    except (DuplicateRegistrationError, InvalidInputError) as e:
        print(f"\nError: {e}")
        logger.warning("Add student failed: %s", e)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        logger.error("Unexpected error in add_student: %s", e)
    finally:
        logger.debug("add_student() routine completed.")


def view_all_students() -> None:
    """Display all student records stored in the CSV file."""
    print("\n--- All Students ---")
    logger.info("User initiated: View All Students")

    try:
        records = load_csv()

        if not records:
            print("No student records found.")
            logger.info("View all: no records present.")
            return

        # Print a simple table
        print(f"\n{'Reg Number':<14} {'First Name':<14} {'Last Name':<14} "
              f"{'DOB':<12} {'Email':<28} {'GPA'}")
        print("-" * 90)
        for r in records:
            print(f"{r['reg_number']:<14} {r['first_name']:<14} {r['last_name']:<14} "
                  f"{r['dob']:<12} {r['email']:<28} {r['gpa']}")
        print(f"\nTotal students: {len(records)}")
        logger.info("View all: displayed %d records.", len(records))

    except Exception as e:
        print(f"\n  Could not retrieve records: {e}")
        logger.error("Error in view_all_students: %s", e)
    finally:
        logger.debug("view_all_students() routine completed.")


def search_student() -> None:
    """
    Search for a student by registration number and display both CSV core data
    and JSON additional details.
    Raises StudentNotFoundError if the reg number is not found.
    """
    print("\n--- Search Student ---")
    logger.info("User initiated: Search Student")

    try:
        reg_number = validate_reg_number(input("Enter Registration Number to search: "))

        records = load_csv()
        match   = next((r for r in records if r["reg_number"] == reg_number), None)

        if match is None:
            raise StudentNotFoundError(
                f"No student found with registration number '{reg_number}'."
            )

        # Display core record
        print(f"\n{'─'*45}")
        print(f"  Registration : {match['reg_number']}")
        print(f"  Name         : {match['first_name']} {match['last_name']}")
        print(f"  Date of Birth: {match['dob']}")
        print(f"  Email        : {match['email']}")
        print(f"  GPA          : {match['gpa']}")

        # Display JSON additional details (if available)
        details = load_json()
        if reg_number in details:
            d = details[reg_number]
            print(f"  Program      : {d.get('program', 'N/A')}")
            print(f"  Address      : {d.get('address', 'N/A')}")
            print(f"  Contact      : {d.get('contact', 'N/A')}")
            print(f"  Enrolled     : {d.get('enrolled', 'N/A')}")
        print(f"{'─'*45}")

        logger.info("Search: found student %s.", reg_number)

    except (StudentNotFoundError, InvalidInputError) as e:
        print(f"\n  {e}")
        logger.warning("Search failed: %s", e)
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        logger.error("Unexpected error in search_student: %s", e)
    finally:
        logger.debug("search_student() routine completed.")


def update_student() -> None:
    """
    Look up a student by registration number and allow the user to update
    any or all fields. Blank input leaves the current value unchanged.
    """
    print("\n--- Update Student ---")
    logger.info("User initiated: Update Student")

    try:
        reg_number = validate_reg_number(input("Enter Registration Number to update: "))

        records = load_csv()
        idx     = next((i for i, r in enumerate(records) if r["reg_number"] == reg_number), None)

        if idx is None:
            raise StudentNotFoundError(
                f"No student found with registration number '{reg_number}'."
            )

        student = records[idx]
        print(f"\nEditing record for: {student['first_name']} {student['last_name']}")
        print("(Press Enter to keep current value)\n")

        #Update core CSV fields
        new_first = input(f"First Name [{student['first_name']}]: ").strip()
        new_last  = input(f"Last Name  [{student['last_name']}]:  ").strip()
        new_dob   = input(f"DOB        [{student['dob']}]: ").strip()
        new_email = input(f"Email      [{student['email']}]: ").strip()
        new_gpa   = input(f"GPA        [{student['gpa']}]: ").strip()

        if new_first: student["first_name"] = new_first
        if new_last:  student["last_name"]  = new_last
        if new_dob:   student["dob"]        = validate_date(new_dob)
        if new_email: student["email"]      = validate_email(new_email)
        if new_gpa:   student["gpa"]        = validate_gpa(new_gpa)

        records[idx] = student
        save_csv(records)

        #Update JSON additional details ─
        details = load_json()
        old_details = details.get(reg_number, {})

        new_address = input(f"Address [{old_details.get('address', '')}]: ").strip()
        new_contact = input(f"Contact [{old_details.get('contact', '')}]: ").strip()
        new_program = input(f"Program [{old_details.get('program', '')}]: ").strip()

        if new_address: old_details["address"] = new_address
        if new_contact: old_details["contact"] = new_contact
        if new_program: old_details["program"] = new_program

        details[reg_number] = old_details
        save_json(details)

        print(f"\n  Student '{reg_number}' updated successfully.")
        logger.info("Student updated: %s", reg_number)

    except (StudentNotFoundError, InvalidInputError) as e:
        print(f"\n  {e}")
        logger.warning("Update failed: %s", e)
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        logger.error("Unexpected error in update_student: %s", e)
    finally:
        logger.debug("update_student() routine completed.")


def delete_student() -> None:
    """
    Remove a student record from both the CSV and JSON files
    after explicit user confirmation.
    Raises StudentNotFoundError if the reg number does not exist.
    """
    print("\n--- Delete Student ---")
    logger.info("User initiated: Delete Student")

    try:
        reg_number = validate_reg_number(input("Enter Registration Number to delete: "))

        records = load_csv()
        match   = next((r for r in records if r["reg_number"] == reg_number), None)

        if match is None:
            raise StudentNotFoundError(
                f"No student found with registration number '{reg_number}'."
            )

        print(f"\nStudent to delete: {match['first_name']} {match['last_name']} "
              f"({reg_number})")
        confirm = input("Are you sure you want to delete this record? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Deletion cancelled.")
            logger.info("Deletion cancelled by user for %s.", reg_number)
            return

        # Remove from CSV
        updated_records = [r for r in records if r["reg_number"] != reg_number]
        save_csv(updated_records)

        # Remove from JSON
        details = load_json()
        if reg_number in details:
            del details[reg_number]
            save_json(details)

        print(f"\n  Student '{reg_number}' deleted successfully.")
        logger.info("Student deleted: %s", reg_number)

    except (StudentNotFoundError, InvalidInputError) as e:
        print(f"\n  {e}")
        logger.warning("Delete failed: %s", e)
    except Exception as e:
        print(f"\n  Unexpected error: {e}")
        logger.error("Unexpected error in delete_student: %s", e)
    finally:
        logger.debug("delete_student() routine completed.")


#
# MAIN MENU
#
def display_menu() -> None:
    """Print the main menu options to the console."""
    print("\n" + "=" * 45)
    print("   STUDENT RECORD MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  1. Add New Student")
    print("  2. View All Students")
    print("  3. Search Student by Registration Number")
    print("  4. Update Student Details")
    print("  5. Delete Student Record")
    print("  6. Exit")
    print("=" * 45)


def main() -> None:
    """
    Application entry point.
    Runs a continuous menu loop until the user selects 'Exit'.
    """
    logger.info("=== Student Management System started ===")
    _init_csv()
    _init_json()

    menu_actions = {
        "1": add_student,
        "2": view_all_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
    }

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        logger.debug("Menu choice selected: %s", choice)

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice == "6":
            print("\nGoodbye! All changes have been saved.")
            logger.info("=== Student Management System exited by user ===")
            break
        else:
            print("\n  Invalid option. Please enter a number between 1 and 6.")
            logger.warning("Invalid menu choice entered: '%s'", choice)


if __name__ == "__main__":
    main()
