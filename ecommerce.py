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

# login section 
USERS: list[dict[str, str]] = []
#register and login functions needed

def register(name: str, password: str, location: str) -> tuple[bool, str]:
    if check_user(name=name):
        return False, "Username already exists"
    user = {
        "fullname": name.strip(),
        "password": password,
        "location": location.strip()
    }
    
    USERS.append(user)
    return True, "Registration successful"

def login(uname: str, password: str) -> tuple[bool, str]:
    for user in USERS:
        if user["fullname"] == uname.strip() and user["password"] == password:
            set_session(uname)
            return True, "Login Successful"
    return False, "Invalid credentials"

def logout():
    unset_session()

def check_user(name: str) -> bool:
    for user in USERS:
        if user["fullname"] == name.strip():
            return True
    return False

def set_session(name: str):
    with open(SESSION_FILE, "+wb") as file:
        file.write(name.encode(encoding=ENCODING))

# main system loop


def check_session():
    with open(SESSION_FILE, "rb+") as file:
        text = file.read()
    print(text.decode(encoding=ENCODING))

def unset_session():
    with open(SESSION_FILE, "wb+") as file:
        file.write(b"")


set_session("wamani")
check_session()
unset_session()