"""
Mock E-Commerce Application
A console-based e-commerce platform with user authentication, 
inventory management, and shopping cart functionality.
"""

import re
import string
import random
from pathlib import Path
from typing import Dict, List, Optional


# ==================== UTILITY FUNCTIONS ====================

def ensure_data_directory() -> str:
    """Ensure data directory exists and return its path."""
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
    return str(data_dir)


def ensure_accounts_file(data_dir: str) -> str:
    """Ensure accounts.txt file exists."""
    accounts_file = Path(data_dir) / "accounts.txt"
    if not accounts_file.exists():
        accounts_file.touch()
    return str(accounts_file)


def load_warehouse_inventory(data_dir: str) -> Dict[str, int]:
    """
    Load all warehouse files and create inventory dictionary.
    Returns: {item_name: price}
    """
    inventory = {}
    warehouse_dir = Path(data_dir)
    
    # Find all warehouse files
    warehouse_files = sorted(warehouse_dir.glob("warehouse*.txt"))
    
    for warehouse_file in warehouse_files:
        with open(warehouse_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                continue
            
            # Split by semicolon to get items
            items = content.split(';')
            for item in items:
                item = item.strip()
                if not item or ':' not in item:
                    continue
                
                # Split by colon to get name and price
                parts = item.rsplit(':', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    try:
                        price = int(parts[1].strip())
                        inventory[name] = price
                    except ValueError:
                        continue
    
    return inventory


def load_accounts(accounts_file: str) -> Dict[str, Dict]:
    """
    Load all accounts from accounts.txt.
    Returns: {username: {email, password, balance}}
    """
    accounts = {}
    
    if not Path(accounts_file).exists():
        return accounts
    
    with open(accounts_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = [p.strip() for p in line.split(',')]
            if len(parts) == 4:
                username, email, password, balance = parts
                accounts[username] = {
                    'email': email,
                    'password': password,
                    'balance': float(balance)
                }
    
    return accounts


def save_accounts(accounts_file: str, accounts: Dict):
    """Save accounts dictionary to accounts.txt."""
    with open(accounts_file, 'w', encoding='utf-8') as f:
        for username, data in accounts.items():
            line = f"{username}, {data['email']}, {data['password']}, {data['balance']}\n"
            f.write(line)


def generate_password(length: int = 16) -> str:
    """Generate a strong password with uppercase, lowercase, digit, and special char."""
    required_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    
    remaining = length - len(required_chars)
    all_chars = string.ascii_letters + string.digits + string.punctuation
    required_chars.extend(random.choice(all_chars) for _ in range(remaining))
    
    random.shuffle(required_chars)
    return ''.join(required_chars)


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    Requirements: min 16 chars, at least one lowercase, uppercase, digit, special char.
    """
    if len(password) < 16:
        return False
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    return has_lower and has_upper and has_digit and has_special


def search_inventory(query: str, inventory: Dict[str, int]) -> List[str]:
    """
    Search inventory using regex patterns.
    Returns list of matching item names.
    """
    search_terms = query.split()
    regex_patterns = [re.compile(re.escape(term), re.IGNORECASE) for term in search_terms]
    
    search_output = []
    for item_name in inventory.keys():
        if all(pattern.search(item_name) for pattern in regex_patterns):
            search_output.append(item_name)
    
    return search_output


def format_currency(amount: float) -> str:
    """Format amount as NGN currency."""
    return f"NGN {amount:,.2f}"


def get_valid_input(prompt: str, input_type=str, condition=None) -> any:
    """Get validated user input."""
    while True:
        try:
            value = input_type(input(prompt))
            if condition and not condition(value):
                print("Invalid input. Please try again.")
                continue
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


# ==================== LOGIN SECTION ====================

def login_menu(accounts: Dict, accounts_file: str) -> Optional[str]:
    """
    Main login menu. Returns username if successful, None if exit.
    """
    while True:
        print("\n" + "="*50)
        print("WELCOME TO E-COMMERCE APP")
        print("="*50)
        print("\n1. Sign In")
        print("2. Sign Up")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            username = sign_in(accounts)
            if username:
                return username
        elif choice == '2':
            sign_up(accounts, accounts_file)
        elif choice == '3':
            print("\nThank you for visiting! Goodbye!")
            return None
        else:
            print("Invalid option. Please try again.")


def sign_in(accounts: Dict) -> Optional[str]:
    """Sign in existing user. Returns username if successful, None otherwise."""
    print("\n--- SIGN IN ---")
    username_or_email = input("Enter username or email: ").strip()
    
    # Find account by username or email
    account_username = None
    for uname, data in accounts.items():
        if uname == username_or_email or data['email'] == username_or_email:
            account_username = uname
            break
    
    if not account_username:
        print("ERROR: Username or email not found.")
        return None
    
    password = input("Enter password: ").strip()
    
    if accounts[account_username]['password'] == password:
        print(f"\nWelcome back, {account_username}!")
        return account_username
    else:
        print("ERROR: Incorrect password.")
        return None


def sign_up(accounts: Dict, accounts_file: str):
    """Create new user account."""
    print("\n--- SIGN UP ---")
    
    # Get unique username
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if username in accounts:
            print("Username already exists.")
            continue
        break
    
    # Get unique email
    while True:
        email = input("Enter email: ").strip()
        if not email:
            print("Email cannot be empty.")
            continue
        if any(data['email'] == email for data in accounts.values()):
            print("Email already registered.")
            continue
        break
    
    # Get password
    print("\nPassword Options:")
    print("1. Enter password manually")
    print("2. Generate password automatically")
    
    while True:
        pwd_choice = input("Select option (1-2): ").strip()
        
        if pwd_choice == '1':
            while True:
                password = input("Enter password (min 16 chars, must include uppercase, "
                               "lowercase, digit, special char): ").strip()
                if validate_password(password):
                    break
                else:
                    print("Password does not meet requirements.")
            break
        elif pwd_choice == '2':
            password = generate_password()
            print(f"Generated password: {password}")
            break
        else:
            print("Invalid option.")
    
    # Save account
    accounts[username] = {
        'email': email,
        'password': password,
        'balance': 0.0
    }
    
    save_accounts(accounts_file, accounts)
    print(f"\nAccount created successfully! Welcome, {username}!")


# ==================== RUN SECTION ====================

def run_menu(username: str, accounts: Dict, accounts_file: str, 
             inventory: Dict[str, int]) -> bool:
    """
    Main run menu. Returns True to continue, False to exit.
    """
    while True:
        print("\n" + "="*50)
        print(f"MAIN MENU - {username}")
        print("="*50)
        print("\n1. Fund Wallet")
        print("2. Purchase")
        print("3. Manage Account")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            fund_wallet(username, accounts, accounts_file)
        elif choice == '2':
            purchase_menu(username, accounts, accounts_file, inventory)
        elif choice == '3':
            manage_account(username, accounts, accounts_file)
        elif choice == '4':
            exit_program(username)
            return False
        else:
            print("Invalid option. Please try again.")
    
    return True


def fund_wallet(username: str, accounts: Dict, accounts_file: str):
    """Allow user to fund their wallet."""
    print("\n--- FUND WALLET ---")
    
    funding_options = [10000, 20000, 50000, 100000]
    
    while True:
        print("\nFunding Options:")
        for i, amount in enumerate(funding_options, 1):
            print(f"{i}. {format_currency(amount)}")
        print("5. Back to Main Menu")
        
        choice = input("Select option (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            idx = int(choice) - 1
            amount = funding_options[idx]
            accounts[username]['balance'] += amount
            save_accounts(accounts_file, accounts)
            print(f"Funded {format_currency(amount)}")
            print(f"New balance: {format_currency(accounts[username]['balance'])}")
        elif choice == '5':
            break
        else:
            print("Invalid option.")


def purchase_menu(username: str, accounts: Dict, accounts_file: str, 
                  inventory: Dict[str, int]):
    """Main purchase menu."""
    cart = {}  # {item_name: quantity}
    inventory_copy = inventory.copy()  # Local copy for this session
    
    while True:
        print("\n" + "="*50)
        print("PURCHASE MENU")
        print("="*50)
        print("\n1. Search Items")
        print("2. Manage Cart")
        print("3. Checkout")
        print("4. Exit Purchase Menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            search_items(cart, inventory_copy)
        elif choice == '2':
            manage_cart(cart, inventory_copy)
        elif choice == '3':
            checkout(username, accounts, accounts_file, cart, inventory_copy)
        elif choice == '4':
            break
        else:
            print("Invalid option.")


def search_items(cart: Dict, inventory: Dict[str, int]):
    """Search and add items to cart."""
    while True:
        query = input("\nEnter search query (or 'back' to return): ").strip()
        
        if query.lower() == 'back':
            break
        
        results = search_inventory(query, inventory)
        
        if not results:
            print("No items found matching your search.")
            continue
        
        print("\nSearch Results:")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item} - {format_currency(inventory[item])}")
        
        while True:
            print("\n1. Search Again")
            print("2. Add Items to Cart")
            print("3. Exit Search Menu")
            
            menu_choice = input("Select option (1-3): ").strip()
            
            if menu_choice == '1':
                break
            elif menu_choice == '2':
                add_items_to_cart(cart, results, inventory)
                break
            elif menu_choice == '3':
                return
            else:
                print("Invalid option.")


def add_items_to_cart(cart: Dict, items: List[str], inventory: Dict[str, int]):
    """Add items from search results to cart."""
    print("\nAdd Items to Cart:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item} - {format_currency(inventory[item])}")
    
    while True:
        try:
            item_num = int(input("\nEnter item number to add (or 0 to go back): ").strip())
            if item_num == 0:
                break
            if 1 <= item_num <= len(items):
                item = items[item_num - 1]
                quantity = int(input(f"How many {item}? ").strip())
                
                if quantity <= 0:
                    print("Invalid quantity.")
                    continue
                
                if item not in cart:
                    cart[item] = 0
                
                cart[item] += quantity
                inventory[item] -= quantity
                print(f"Added {quantity} x {item} to cart")
                break
            else:
                print("Invalid item number.")
        except ValueError:
            print("Invalid input.")


def manage_cart(cart: Dict, inventory: Dict[str, int]):
    """Manage shopping cart."""
    while True:
        print("\n" + "="*50)
        print("MANAGE CART")
        print("="*50)
        
        if not cart:
            print("Cart is empty.")
        else:
            print("\nCart Contents:")
            for i, (item, qty) in enumerate(cart.items(), 1):
                price = inventory.get(item)  # Price from inventory copy
                if price is None:
                    continue
                item_total = price * qty
                print(f"{i}. {item}")
                print(f"   Quantity: {qty}, Price: {format_currency(price)}, "
                      f"Total: {format_currency(item_total)}")
        
        print("\n1. View Items in Cart")
        print("2. Add Items to Cart")
        print("3. Remove Items from Cart")
        print("4. Clear Cart")
        print("5. Exit Manage Cart Menu")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            continue
        elif choice == '2':
            add_items_menu(cart, inventory)
        elif choice == '3':
            remove_items_from_cart(cart, inventory)
        elif choice == '4':
            # Restore inventory
            for item, qty in cart.items():
                if item in inventory:
                    inventory[item] += qty
            cart.clear()
            print("Cart cleared.")
        elif choice == '5':
            break
        else:
            print("Invalid option.")


def add_items_menu(cart: Dict, inventory: Dict[str, int]):
    """Menu to add items to cart."""
    print("\nAvailable Items:")
    items = list(inventory.keys())
    for i, item in enumerate(items, 1):
        print(f"{i}. {item} - {format_currency(inventory[item])}")
    
    try:
        item_num = int(input("\nEnter item number (or 0 to go back): ").strip())
        if item_num == 0:
            return
        if 1 <= item_num <= len(items):
            item = items[item_num - 1]
            quantity = int(input(f"How many {item}? ").strip())
            
            if quantity > 0:
                if item not in cart:
                    cart[item] = 0
                cart[item] += quantity
                inventory[item] -= quantity
                print(f"Added {quantity} x {item} to cart")
        else:
            print("Invalid item number.")
    except ValueError:
        print("Invalid input.")


def remove_items_from_cart(cart: Dict, inventory: Dict[str, int]):
    """Remove items from cart."""
    if not cart:
        print("Cart is empty.")
        return
    
    print("\nItems in Cart:")
    items = list(cart.keys())
    for i, item in enumerate(items, 1):
        print(f"{i}. {item} (qty: {cart[item]})")
    
    try:
        item_num = int(input("\nEnter item number to remove (or 0 to go back): ").strip())
        if item_num == 0:
            return
        if 1 <= item_num <= len(items):
            item = items[item_num - 1]
            qty_to_remove = int(input(f"How many to remove? ").strip())
            
            if qty_to_remove > 0 and qty_to_remove <= cart[item]:
                cart[item] -= qty_to_remove
                inventory[item] += qty_to_remove
                if cart[item] == 0:
                    del cart[item]
                print("Item removed from cart.")
            else:
                print("Invalid quantity.")
        else:
            print("Invalid item number.")
    except ValueError:
        print("Invalid input.")


def checkout(username: str, accounts: Dict, accounts_file: str, 
             cart: Dict, inventory: Dict[str, int]):
    """Process checkout."""
    if not cart:
        print("Cart is empty. Nothing to checkout.")
        return
    
    print("\n" + "="*50)
    print("CHECKOUT")
    print("="*50)
    
    print("\nCart Summary:")
    total = 0
    for item, qty in cart.items():
        price = inventory.get(item)
        if price is None:
            continue
        item_total = price * qty
        total += item_total
        print(f"{item}: {qty} x {format_currency(price)} = {format_currency(item_total)}")
    
    print(f"\nTotal: {format_currency(total)}")
    
    proceed = input("Proceed to payment? (yes/no): ").strip().lower()
    if proceed != 'yes':
        print("Checkout cancelled.")
        return
    
    # Check balance
    balance = accounts[username]['balance']
    if balance < total:
        print(f"ERROR: Insufficient funds. Your balance: {format_currency(balance)}")
        return
    
    # Process payment
    accounts[username]['balance'] -= total
    save_accounts(accounts_file, accounts)
    cart.clear()
    
    print(f"\nPayment successful! Remaining balance: {format_currency(accounts[username]['balance'])}")


# ==================== ACCOUNT MANAGEMENT ====================

def manage_account(username: str, accounts: Dict, accounts_file: str):
    """Manage user account."""
    while True:
        print("\n" + "="*50)
        print("MANAGE ACCOUNT")
        print("="*50)
        print("\n1. Change Username")
        print("2. Change Email")
        print("3. Change Password")
        print("4. View Account Details")
        print("5. Reset Balance")
        print("6. Delete Account")
        print("7. Logout")
        print("8. Exit Manage Account")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            username = change_username(username, accounts, accounts_file)
        elif choice == '2':
            change_email(username, accounts, accounts_file)
        elif choice == '3':
            change_password(username, accounts, accounts_file)
        elif choice == '4':
            view_account_details(username, accounts)
        elif choice == '5':
            reset_balance(username, accounts, accounts_file)
        elif choice == '6':
            if delete_account(username, accounts, accounts_file):
                return username  # Signal to logout
        elif choice == '7':
            return username  # Signal to logout
        elif choice == '8':
            break
        else:
            print("Invalid option.")


def verify_password(username: str, accounts: Dict) -> bool:
    """Verify user password."""
    password = input("Enter your password to verify: ").strip()
    return accounts[username]['password'] == password


def change_username(username: str, accounts: Dict, accounts_file: str) -> str:
    """Change username."""
    print("\n--- CHANGE USERNAME ---")
    
    if not verify_password(username, accounts):
        print("ERROR: Incorrect password.")
        return username
    
    while True:
        new_username = input("Enter new username: ").strip()
        if not new_username:
            print("Username cannot be empty.")
            continue
        if new_username in accounts:
            print("Username already exists.")
            continue
        break
    
    accounts[new_username] = accounts.pop(username)
    save_accounts(accounts_file, accounts)
    print(f"Username changed to {new_username}")
    return new_username


def change_email(username: str, accounts: Dict, accounts_file: str):
    """Change email."""
    print("\n--- CHANGE EMAIL ---")
    
    if not verify_password(username, accounts):
        print("ERROR: Incorrect password.")
        return
    
    while True:
        new_email = input("Enter new email: ").strip()
        if not new_email:
            print("Email cannot be empty.")
            continue
        if any(data['email'] == new_email for uname, data in accounts.items() if uname != username):
            print("Email already registered.")
            continue
        break
    
    accounts[username]['email'] = new_email
    save_accounts(accounts_file, accounts)
    print(f"Email changed to {new_email}")


def change_password(username: str, accounts: Dict, accounts_file: str):
    """Change password."""
    print("\n--- CHANGE PASSWORD ---")
    
    old_password = input("Enter current password: ").strip()
    if accounts[username]['password'] != old_password:
        print("ERROR: Incorrect password.")
        return
    
    while True:
        new_password = input("Enter new password: ").strip()
        if validate_password(new_password):
            break
        else:
            print("Password does not meet requirements.")
    
    accounts[username]['password'] = new_password
    save_accounts(accounts_file, accounts)
    print("Password changed successfully.")


def view_account_details(username: str, accounts: Dict):
    """View account details."""
    print("\n--- ACCOUNT DETAILS ---")
    
    if not verify_password(username, accounts):
        print("ERROR: Incorrect password.")
        return
    
    data = accounts[username]
    print(f"Username: {username}")
    print(f"Email: {data['email']}")
    print(f"Balance: {format_currency(data['balance'])}")


def reset_balance(username: str, accounts: Dict, accounts_file: str):
    """Reset balance to zero."""
    print("\n--- RESET BALANCE ---")
    
    if not verify_password(username, accounts):
        print("ERROR: Incorrect password.")
        return
    
    confirm = input("Are you sure you want to reset your balance to zero? (yes/no): ").strip().lower()
    if confirm == 'yes':
        accounts[username]['balance'] = 0.0
        save_accounts(accounts_file, accounts)
        print("Balance reset to zero.")


def delete_account(username: str, accounts: Dict, accounts_file: str) -> bool:
    """Delete user account. Returns True if deleted."""
    print("\n--- DELETE ACCOUNT ---")
    
    if not verify_password(username, accounts):
        print("ERROR: Incorrect password.")
        return False
    
    confirm = input("Are you sure you want to delete your account? This cannot be undone. (yes/no): ").strip().lower()
    if confirm == 'yes':
        del accounts[username]
        save_accounts(accounts_file, accounts)
        print("Account deleted successfully.")
        return True
    
    return False


def exit_program(username: str):
    """Exit the program."""
    print(f"\nThank you for your visit, {username}!")
    print("We look forward to seeing you again. Goodbye!")


# ==================== MAIN ====================

def main():
    """Main application entry point."""
    # Setup data directory and files
    data_dir = ensure_data_directory()
    accounts_file = ensure_accounts_file(data_dir)
    
    # Load data
    accounts = load_accounts(accounts_file)
    inventory = load_warehouse_inventory(data_dir)
    
    if not inventory:
        print("ERROR: No inventory items found.")
        return
    
    # Login
    username = login_menu(accounts, accounts_file)
    if not username:
        return
    
    # Main application loop
    while True:
        continue_app = run_menu(username, accounts, accounts_file, inventory)
        if not continue_app:
            break
    
    # Check if user deleted account or logged out
    if username not in accounts:
        print("\nAccount deleted. Returning to login...")
        main()
    else:
        print("\nReturning to login...")
        main()


if __name__ == "__main__":
    main()
