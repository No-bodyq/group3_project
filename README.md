# Mock E-Commerce Application

A console-based e-commerce platform built with Python, featuring user authentication, inventory management, shopping cart functionality, and account management.

## Project Structure

```
group3_project/
├── main.py           # Main application file
├── search.py         # Search functionality demonstration
├── README.md         # This file
├── CODE_EXPLANATION.md # Detailed code documentation
└── data/
    ├── accounts.txt  # User account storage (auto-created)
    └── warehouse3.txt # Product inventory
```

## Features

### 1. Login System

- **Sign Up**: Create new account with strong password requirements
  - Username and email must be unique
  - Password must be at least 16 characters with uppercase, lowercase, digit, and special character
  - Option to auto-generate password
- **Sign In**: Authenticate with username/email and password
- **Exit**: Safely quit the application

### 2. Main Menu

After login, users can access:

- **Fund Wallet**: Add money to account (preset amounts: 10K, 20K, 50K, 100K NGN)
- **Purchase**: Browse inventory, search items, and buy products
- **Manage Account**: Update profile information and account settings
- **Exit**: Logout and return to login screen

### 3. Shopping Features

- **Search**: Find items using regex-based pattern matching
  - Case-insensitive search
  - Supports partial matching
  - Multiple search terms must all match
- **Manage Cart**:
  - View cart contents
  - Add/remove items
  - Clear entire cart
- **Checkout**:
  - Review items and total cost
  - Verify sufficient balance
  - Process payment and update inventory

### 4. Account Management

- **Change Username**: Update username (must be unique)
- **Change Email**: Update email address (must be unique)
- **Change Password**: Set new password with strength requirements
- **View Account Details**: Display current balance and account info
- **Reset Balance**: Reset wallet to zero (requires confirmation)
- **Delete Account**: Permanently remove account (requires confirmation)
- **Logout**: Return to login screen

## How to Run

### Prerequisites

- Python 3.7 or higher
- `warehouse3.txt` file in the `data/` folder

### Running the Application

```bash
python main.py
```

The application will:

1. Automatically create the `data/` directory if it doesn't exist
2. Automatically create `accounts.txt` if it doesn't exist
3. Load all inventory from warehouse3.txt
4. Display the login menu

### Test Data

The application includes sample Nigerian food and consumer products:

- Agricultural products (Rice, Beans, Yam, Cassava, etc.)
- Beverages (Milo, Bournvita, Indomie, etc.)
- Proteins (Chicken, Beef, Fish, Eggs, etc.)
- Seasonings and spices
- Household items

All prices are in Nigerian Naira (NGN).

## User Workflow Example

1. **Launch** → `python main.py`
2. **Sign Up** → Create account with strong password
3. **Fund Wallet** → Add money (e.g., NGN 100,000)
4. **Search Items** → Search for "Rice" or "Chicken"
5. **Add to Cart** → Select items and quantities
6. **Checkout** → Review and confirm purchase
7. **Manage Account** → Update profile if needed
8. **Exit** → Logout

## Password Requirements

Passwords must meet ALL of the following criteria:

- Minimum 16 characters long
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (!@#$%^&\*)

Example strong password: `SecurePass123!@#`

## File Format

### accounts.txt

```
username, email, password, balance
john_doe, john@example.com, SecurePass123!@#, 50000.00
jane_smith, jane@example.com, JanePass456$%^, 75000.00
```

### warehouse3.txt

```
Rice (50kg): 115000;Beans (50kg): 65000;Chicken (1kg): 5500;...
```

Items are separated by semicolons (`;`), and each item has name and price separated by colon (`:`).

## Search Algorithm

The search feature uses regex pattern matching:

```python
def search_inventory(query: str, inventory: list[str]) -> list[str]:
    # Split query into words
    search_terms = query.split()

    # Create case-insensitive regex for each word
    patterns = [re.compile(re.escape(term), re.IGNORECASE)
                for term in search_terms]

    # Return items matching ALL patterns
    return [item for item in inventory
            if all(p.search(item) for p in patterns)]
```

**Example:**

- Query: "Apple Watch" → Finds: "Apple Watch Series 8"
- Query: "rice" → Finds all rice variants (case-insensitive)
- Query: "chicken 1kg" → Finds: "Chicken (frozen 1kg)" etc.

## Key Implementation Details

### Data Persistence

- User accounts saved to `accounts.txt` after each modification
- Inventory loaded fresh from warehouse files each session
- Cart is session-specific (not persisted)

### Security

- Passwords validated for strength on signup
- Password verification required for sensitive operations
- Confirmation prompts for destructive actions (delete, reset balance)

### Error Handling

- Invalid input validation throughout
- Insufficient balance detection during checkout
- Duplicate username/email prevention
- File creation if missing

## Troubleshooting

### "No items found" during search

- Ensure `warehouse3.txt` is in the `data/` folder
- Check that file format is correct (Name: Price)
- Try searching with partial terms (e.g., "Rice" instead of "white rice")

### "Username already exists"

- Choose a different username during signup

### "Insufficient funds"

- Fund your wallet before making purchases
- Check your account balance in Manage Account

### Password not meeting requirements

- Ensure password is at least 16 characters
- Include uppercase, lowercase, digit, and special character
- Use the auto-generate option if unsure

## Code Structure

The `main.py` file is organized into sections:

1. **Utility Functions** - File I/O, validation, formatting
2. **Login Section** - Authentication and account creation
3. **Run Section** - Main menu and wallet funding
4. **Purchase Features** - Search, cart, checkout
5. **Account Management** - Profile updates and settings
6. **Main Entry Point** - Application initialization

## Testing

Run the search module to test the search functionality:

```bash
python search.py
```

This demonstrates the regex-based search algorithm with example data.

## Notes for Developers

- The inventory is stored in-memory as a dictionary for fast lookup
- Cart modifications are made to a session copy of inventory
- The main function includes recursion for logout/login flow
- All currency amounts use float for precision
- File encoding is UTF-8 to support special characters

## Future Enhancements

Potential improvements:

- Database integration instead of text files
- Order history tracking
- Discount codes and promotions
- Multiple payment methods
- Admin dashboard
- Product categories and filtering
- Wishlist functionality
- User reviews and ratings
