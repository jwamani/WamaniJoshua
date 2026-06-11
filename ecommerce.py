# Users roles -> Admin, Customer, Cashier
# Entities; Product, User
#
# User{id, name, password, role, location}
# Product{id, price, dicount}
# coupon_codes; A16->5, AK9->3, BR4->10, CO7->5, 
#
# access levels;
#   1. [create|add]_product; admin,cashier
#   2. remove_product; admin
#   3. view_product; cashier,admin,customer
#   4. buy_product; admin,cashier,customer
#   5. login,logout; admin,cashier,customer


ROLES = ("customer", "cashier", "admin")

SESSION_FILE = "session.bin"
ENCODING = "utf-32"
USERS: list[dict[str, str]] = []

# login system methods
def register(name: str, password: str, location: str, role: str = "customer") -> tuple[bool, str]:
    if check_user(name=name):
        return False, "Username already exists"
    user = {
        "fullname": name.strip(),
        "password": password,
        "location": location.strip(),
        "role": role.strip()
    }
    USERS.append(user)
    return True, "Registration successful"

def registration_flow(chc: str):
    if chc == "1":
        name = input("Enter your username: ")
        password, confirm_password = "", "_"
        
        while password != confirm_password:
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")

        location = input("Enter your location: ")
        print("These are your registration details: ")
        print(f"Username: {name}")
        print(f"Password: {password}")
        print(f"Location: {location}")
        success, msg = register(name, password, location)
        if success:
            print("Registration successful!")
        else:
            print(f"Registration failed: {msg}! Please try again!")
        


def login(uname: str, password: str) -> tuple[bool, str]:
    for user in USERS:
        if user["fullname"] == uname.strip() and user["password"] == password:
            set_session(uname, user["role"])
            return True, "Login Successful"
    return False, "Invalid credentials"

def logout() -> tuple[bool, str]:
    unset_session()
    return True, "Logout successful"

def check_user(name: str) -> bool:
    for user in USERS:
        if user["fullname"] == name.strip():
            return True
    return False

def set_session(name: str, user_role: str):
    with open(SESSION_FILE, "+wb") as file:
        creds = ",".join([name, user_role])
        file.write(creds.encode(encoding=ENCODING))

def check_session(uname: str, role: str) -> tuple[bool, str]:
    try:
        with open(SESSION_FILE, "rb+") as file:
            text = file.read()
            if text:
                creds = text.decode(encoding=ENCODING).split(",")
                if creds[0] == uname.strip():
                    if creds[1] == role.strip():
                        return True, "Valid Session"
                    return False, "Invalid Role"
                else:
                    return False, "Invalid Session"
            else:
                return False, "No active session"
    except FileNotFoundError:
        return False, "No active session"

def read_session() -> tuple[str, str] | None:
    try:
        with open(SESSION_FILE, "rb+") as file:
            text = file.read()
            if text:
                creds = text.decode(encoding=ENCODING).split(",")
                return creds[0], creds[1]
            else:
                return None
    except FileNotFoundError:
        return None

def unset_session():
    with open(SESSION_FILE, "wb+") as file:
        file.write(b"")


# set_session("wamani", "customer")
# unset_session()
# print(check_session("wani", "custmer"))
# unset_session()

def login_menu_actions(name: str, role: str):
    mode = ""
    if check_session(name, role)[0]:
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. Exit")
        mode = "auth"
        return ["1", "2", "3", "4"], mode
    else: # user is not logged in
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        mode = "no-auth"
        return ["1", "2", "3"], mode

print("WELCOME TO WORMS ECOMMERCE")
while True:
    name, role = read_session() or ("", "") 
    options, mode = login_menu_actions(name, role)
    
    choice = ""
    if mode == "auth":
        while choice not in options:
            choice = input("Enter your choice: ")
        
        if choice == "1":
            registration_flow(choice)
    
        if choice == "4":
            print("Thank you for shopping with us!")
            break
    else:
        while choice not in options:
            choice = input("Enter your choice: ")
        match choice:
            case "1":
                print("Registration will be enabled soon!")
                break
            case "2":
                print("Login will be enabled soon!")
                break
            case "3":
                print("Thank you for shopping with us")
                break

# print(read_session())


