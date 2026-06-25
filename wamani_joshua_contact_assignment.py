"""
Contact Management System
Data structure format:
    contacts = {
        1: {name: ..., phone: ..., email: ...},
        2: {...}
    }
"""

import re

def _validate_phone(phone: str) -> bool:
    pattern = r'^\d{4}-\d{3}-\d{3}$'
    return bool(re.match(pattern, phone))


def _validate_email(email: str) -> bool:
    if not email:
        return True
    return "@" in email and "." in email

def _print_table(contacts: dict) -> None:
    """Print a dict of contacts as an ASCII table."""
    w = {"id": 4, "name": 22, "phone": 18, "email": 30}
    divider = "-" * (sum(w.values()) + 6)
    header = (
        f"{'ID':<{w['id']}}  {'Name':<{w['name']}}  "
        f"{'Phone':<{w['phone']}}  {'Email':<{w['email']}}"
    )
    print(divider)
    print(header)
    print(divider)
    for cid, info in contacts.items():
        print(
            f"{cid:<{w['id']}}  {info['name']:<{w['name']}}"
            f"{info['phone']:<{w['phone']}}  {(info['email'] or '—'):<{w['email']}}"
        )
    print(divider)


def _print_one(cid: int, info: dict) -> None:
    """Pretty-print a single contact."""
    print(
        f"\n  |- - - - - - Contact Details - - - - - -\n"
        f"  |  ID    : {cid}\n"
        f"  |  Name  : {info['name']}\n"
        f"  |  Phone : {info['phone']}\n"
        f"  |  Email : {info['email'] or '—'}\n"
        f"  |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|"
    )


class ContactManager:
    """Manages contacts stored in an in-memory dictionary."""

    def __init__(self):
        # Main store: { id(int): {name, phone, email} }
        self._contacts: dict[int, dict[str, str]] = {}
        self._next_id: int = 1

    def add_contact(self, name: str, phone: str, email: str = "") -> None:
        if not _validate_phone(phone):
            print(
                f"[ERROR] Invalid phone '{phone}'.\n"
                "Invalid phone number format. Use 'XXXX-XXX-XXX'."
            )
            return
        if not _validate_email(email):
            print(
                f"RROR] Invalid email '{email}'.\n"
                "Must contain '@' and '.'."
            )
            return
        self._contacts[self._next_id] = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
        print(f"[OK] '{name}' added with ID {self._next_id}.")
        self._next_id += 1

    def view_contact(self, contact_id: int) -> None:
        info = self._contacts.get(contact_id)
        if info is None:
            print(f"[INFO] No contact with ID {contact_id}.")
        else:
            _print_one(contact_id, info)

    def update_contact(
        self,
        contact_id: int,
        name: str = "",
        phone: str = "",
        email: str = "",
    ) -> None:
        info = self._contacts.get(contact_id)
        if info is None:
            print(f"[INFO] No contact with ID {contact_id}.")
            return
        new_name = name.strip() or info["name"]
        new_phone = phone.strip() or info["phone"]
        new_email = email.strip() if email.strip() != "" else info["email"]
        if not _validate_phone(new_phone):
            print(
                f"[ERROR] Invalid phone '{new_phone}'.\n"
                "Invalid phone number format. Use 'XXXX-XXX-XXX'."
            )
            return
        if not _validate_email(new_email):
            print(
                f"[ERROR] Invalid email '{new_email}'.\n"
                "Must contain '@' and '.'."
            )
            return
        self._contacts[contact_id] = {
            "name": new_name,
            "phone": new_phone,
            "email": new_email,
        }
        print(f"[OK] Contact ID {contact_id} updated.")

    def delete_contact(self, contact_id: int) -> None:
        if contact_id not in self._contacts:
            print(f"  [INFO] No contact with ID {contact_id}.")
            return
        removed = self._contacts.pop(contact_id)
        print(f"[OK] '{removed['name']}' (ID {contact_id}) deleted.")

    # uses name, phone or email
    def search_contacts(self, query: str) -> None:
        q = query.lower()
        results = {
            cid: info
            for cid, info in self._contacts.items()
            if q in info["name"].lower()
            or q in info["phone"].lower()
            or q in info["email"].lower()
        }
        if not results:
            print(f"[INFO] No contacts matched '{query}'.")
            return
        print(f"\nSearch results for '{query}'  ({len(results)} found)")
        _print_table(results)

    def list_all_contacts(self) -> None:
        if not self._contacts:
            print("[INFO] No contacts saved yet.")
            return
        print(f"\nAll Contacts  ({len(self._contacts)} total)")
        _print_table(self._contacts)

def _prompt(label: str, required: bool = True) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value or not required:
            return value
        print("[!] This field is required.")


def _prompt_int(label: str) -> int | None:
    raw = input(f"  {label}: ").strip()
    try:
        return int(raw)
    except ValueError:
        print(f"[ERROR] '{raw}' is not a valid number.")
        return None


def main() -> None:
    manager = ContactManager()
    menu = (
        "\n=== Contact Manager Menu ===\n"
        "1. Add Contact\n"
        "2. View Contact\n"
        "3. Update Contact\n"
        "4. Delete Contact\n"
        "5. Search Contacts\n"
        "6. List All Contacts\n"
        "7. Exit\n"
    )
    while True:
        print(menu)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "1":
            print("\n-- Add Contact --")
            name = _prompt("Name")
            phone = _prompt("Phone (digits/hyphens)")
            email = _prompt("Email (optional — press Enter to skip)", required=False)
            manager.add_contact(name, phone, email)
        elif choice == "2":
            print("\n-- View Contact --")
            cid = _prompt_int("Contact ID")
            if cid is not None:
                manager.view_contact(cid)
        elif choice == "3":
            print("\n-- Update Contact --")
            cid = _prompt_int("Contact ID to update")
            if cid is None:
                continue
            print("(Press Enter to keep the current value)")
            name = _prompt("New Name  (or Enter)", required=False)
            phone = _prompt("New Phone (or Enter)", required=False)
            email = _prompt("New Email (or Enter)", required=False)
            manager.update_contact(cid, name, phone, email)
        elif choice == "4":
            print("\n-- Delete Contact --")
            cid = _prompt_int("Contact ID to delete")
            if cid is None:
                continue
            confirm = input(f"Delete contact ID {cid}? (y/n): ").strip().lower()
            if confirm == "y":
                manager.delete_contact(cid)
            else:
                print("[INFO] Deletion cancelled.")
        elif choice == "5":
            print("\n-- Search Contacts --")
            query = _prompt("Search term (name, phone, or email)")
            manager.search_contacts(query)
        elif choice == "6":
            manager.list_all_contacts()
        elif choice == "7":
            print("\n  Goodbye!\n")
            break
        else:
            print("[!] Please choose a number between 1 and 7.")

if __name__ == "__main__":
    main()
