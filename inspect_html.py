"""
HTML Structure Inspector
Helps understand the structure of the ranking page
"""

import requests
from bs4 import BeautifulSoup
import json


def inspect_page_structure(url: str):
    """
    Inspect and display the structure of a ranking page
    
    Args:
        url: URL to inspect
    """
    print("="*70)
    print("HTML STRUCTURE INSPECTOR")
    print("="*70)
    print(f"\nFetching: {url}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("="*70)
        print("1. PAGE TITLE")
        print("="*70)
        title = soup.find('title')
        print(f"Title: {title.string if title else 'Not found'}\n")
        
        print("="*70)
        print("2. TABLES FOUND")
        print("="*70)
        tables = soup.find_all('table')
        print(f"Number of tables: {len(tables)}\n")
        
        for i, table in enumerate(tables, 1):
            print(f"--- Table {i} ---")
            
            # Table attributes
            print(f"Classes: {table.get('class', 'None')}")
            print(f"ID: {table.get('id', 'None')}")
            
            # Headers
            headers = table.find_all('th')
            if headers:
                print(f"Headers ({len(headers)}): {[h.get_text(strip=True) for h in headers]}")
            
            # First data row sample
            rows = table.find_all('tr')
            print(f"Total rows: {len(rows)}")
            
            if len(rows) > 1:
                first_data_row = rows[1]
                cols = first_data_row.find_all('td')
                print(f"Columns in first data row: {len(cols)}")
                print("Sample data:")
                for j, col in enumerate(cols[:8]):  # Show first 8 columns
                    print(f"  Col {j}: '{col.get_text(strip=True)}'")
            
            print()
        
        print("="*70)
        print("3. DIVS WITH 'RANK' OR 'PLAYER' IN CLASS")
        print("="*70)
        relevant_divs = soup.find_all('div', class_=lambda x: x and ('rank' in x.lower() or 'player' in x.lower()))
        print(f"Found {len(relevant_divs)} relevant divs\n")
        
        for div in relevant_divs[:3]:  # Show first 3
            print(f"Class: {div.get('class')}")
            print(f"Text: {div.get_text(strip=True)[:100]}...")
            print()
        
        print("="*70)
        print("4. SCRIPTS (FOR JAVASCRIPT DATA)")
        print("="*70)
        scripts = soup.find_all('script')
        print(f"Number of script tags: {len(scripts)}\n")
        
        # Look for JSON data in scripts
        for script in scripts:
            if script.string and ('ranking' in script.string.lower() or 'player' in script.string.lower()):
                print("Found potential data in script:")
                snippet = script.string[:200].replace('\n', ' ')
                print(f"{snippet}...")
                print()
        
        print("="*70)
        print("5. PAGINATION ELEMENTS")
        print("="*70)
        
        # Look for pagination
        pagination_keywords = ['pagination', 'page', 'next', 'prev']
        for keyword in pagination_keywords:
            elements = soup.find_all(class_=lambda x: x and keyword in x.lower())
            if elements:
                print(f"Found elements with '{keyword}': {len(elements)}")
                for elem in elements[:2]:
                    print(f"  {elem.name} - class: {elem.get('class')} - text: {elem.get_text(strip=True)[:50]}")
        
        print("\n" + "="*70)
        print("6. SAMPLE RAW HTML (First Table)")
        print("="*70)
        if tables:
            first_table_html = str(tables[0])[:1000]
            print(first_table_html)
            print("...\n")
        
        # Save full HTML for manual inspection
        with open('page_sample.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✓ Full HTML saved to: page_sample.html")
        
        print("\n" + "="*70)
        print("INSPECTION COMPLETE")
        print("="*70)
        print("\nNext steps:")
        print("1. Review the table structure above")
        print("2. Identify which table contains the rankings")
        print("3. Note the column positions for: Rank, Name, Country, GAL-ID, Points")
        print("4. Check if pagination uses pageNo, page, or offset parameter")
        print("5. Update the scraper code with correct selectors")
        
    except Exception as e:
        print(f"Error inspecting page: {e}")


def main():
    """Main function"""
    print("="*70)
    print("WORLD TAEKWONDO PAGE STRUCTURE INSPECTOR")
    print("="*70)
    print("\nThis tool helps you understand the HTML structure")
    print("of the ranking page so you can adjust the scraper.\n")
    
    url = input("Enter the URL of the ranking page: ").strip()
    
    if url:
        inspect_page_structure(url)
    else:
        print("No URL provided.")


if __name__ == "__main__":
    main()
