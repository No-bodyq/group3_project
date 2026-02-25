"""
Search functionality module for the e-commerce application.
This module contains the regex-based search algorithm for inventory items.
"""

import re


def search_inventory(query: str, inventory: list[str]) -> list[str]:
    """
    Search for items in inventory using regex pattern matching.
    
    The algorithm:
    1. Splits the user query into individual words
    2. Creates case-insensitive regex patterns for each word
    3. Filters inventory by checking if all patterns match each item
    4. Returns matching items
    
    Args:
        query: The user's search query string
        inventory: List of item names to search through
        
    Returns:
        List of item names that match all search terms
        
    Example:
        >>> inventory = ["Apple iPhone 14", "Samsung Galaxy S23", "Apple Watch Series 8"]
        >>> search_inventory("Apple Watch", inventory)
        ['Apple Watch Series 8']
    """
    # Step 1: Split the user query into individual words
    search_terms: list[str] = query.split()
    
    # Step 2: Create case-insensitive regex patterns for each word
    regex_patterns: list[re.Pattern[str]] = [
        re.compile(re.escape(term), re.IGNORECASE) 
        for term in search_terms
    ]
    
    # Step 3: Filter inventory items based on the regex patterns
    search_output: list[str] = []
    for item in inventory:
        # Check if all patterns match the current item
        if all(pattern.search(item) for pattern in regex_patterns):
            search_output.append(item)
    
    # Step 4: Return matched items
    return search_output


# Example usage and demonstration
if __name__ == "__main__":
    # Example inventory
    inventory: list[str] = [
        "Apple iPhone 14",
        "Samsung Galaxy S23",
        "Google Pixel 7",
        "Sony Xperia 5",
        "Apple Watch Series 8",
        "Samsung Smart TV",
        "iPhone 14 Pro",
        "Apple MacBook Air",
        "Samsung Galaxy Buds",
    ]
    
    # Test cases
    test_queries = [
        "Apple Watch",
        "Galaxy",
        "iPhone",
        "Apple",
        "Samsung Smart",
        "nonexistent product"
    ]
    
    print("=" * 60)
    print("INVENTORY SEARCH TEST")
    print("=" * 60)
    
    for query in test_queries:
        results = search_inventory(query, inventory)
        print(f"\nQuery: '{query}'")
        if results:
            print(f"Found {len(results)} result(s):")
            for i, item in enumerate(results, 1):
                print(f"  {i}. {item}")
        else:
            print("No matching items found.")
