# Student Management System Report

## Overview

The student management system is a console-based CRUD application that stores student records in two separate files:

- `students.csv` for the core academic record
- `students.json` for additional profile details

The program is implemented in `student_management.py` and uses a menu-driven loop so the user can add, view, search, update, or delete student records from one interface. This design keeps the application simple while still separating structured tabular data from flexible metadata.

## Program Design

The application is organized into three main layers:

1. Validation helpers
   - `validate_reg_number()` checks the registration number format.
   - `validate_email()` checks for a basic email structure.
   - `validate_gpa()` ensures GPA is numeric and within the expected range.
   - `validate_date()` ensures dates follow `YYYY-MM-DD`.

2. File helpers
   - `_init_csv()`, `load_csv()`, and `save_csv()` manage the CSV storage.
   - `_init_json()`, `load_json()`, and `save_json()` manage the JSON storage.

3. User actions
   - `add_student()` inserts a new record into both files.
   - `view_all_students()` displays all CSV records.
   - `search_student()` looks up a student by registration number and prints both CSV and JSON data.
   - `update_student()` edits existing student data in both files.
   - `delete_student()` removes a student from both files after confirmation.

The `main()` function initializes the storage files, displays the menu, and dispatches the selected action in a loop until the user exits.

## Key Functions

### `add_student()`

This function gathers user input, validates it, checks for duplicate registration numbers, and then writes the data to both storage files. The CSV file receives the core academic fields, while the JSON file stores address, contact number, program, and enrollment date. This split allows the program to keep the main record compact while still preserving extra details.

### `search_student()`

This function finds a student by registration number in the CSV file and then enriches the result with any matching JSON details. It provides a complete view of one student’s record without requiring the user to inspect both files manually.

### `update_student()`

This function loads the existing student record, allows the user to leave values unchanged by pressing Enter, and then writes the updated data back to both files. It updates only the fields the user changes, which keeps the workflow efficient.

### `delete_student()`

This function first confirms the registration number exists, then asks the user for confirmation before deleting the record. If the user types anything other than `yes`, the deletion is cancelled. When deletion proceeds, the record is removed from both CSV and JSON storage.

## Exception Handling Strategy

The program uses custom exceptions to separate business-rule errors from unexpected system failures:

- `StudentNotFoundError` is raised when a requested registration number does not exist.
- `DuplicateRegistrationError` is raised when the user tries to add a student whose registration number already exists.
- `InvalidInputError` is raised when validation fails for registration number, email, GPA, date, or required text fields.

The CRUD functions catch these exceptions and display user-friendly error messages instead of allowing the application to crash. File access problems are handled in the storage helpers, where `OSError` and JSON decoding errors are logged and re-raised. Each user action also has a `finally` block that records when the routine finishes, which makes the log easier to follow.

This strategy gives the program two levels of protection:

- predictable user mistakes are handled cleanly with clear feedback
- low-level file problems are logged for debugging and troubleshooting

## Testing Results

The files in this workspace show that the system was exercised with both valid and invalid inputs.

### Evidence from `student_system.log`

The log shows the following outcomes:

- the system started successfully
- one add operation failed because the JSON file could not be read at first
- a view operation succeeded and displayed one record
- an update attempt failed because the registration number format was invalid
- a later update succeeded after the JSON file was initialized
- one add attempt failed because the date format was invalid
- a later add succeeded for a second student
- the system exited normally

### Evidence from `students.csv`

The CSV file contains two student records, showing that successful add operations were persisted correctly.

### Evidence from `students.json`

The JSON file contains extended details for the stored students, including address, contact, program, and enrollment information. This confirms that the application saved the supporting metadata alongside the core CSV data.
