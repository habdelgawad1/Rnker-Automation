#!/usr/bin/env python3
"""
World Taekwondo Scraper - ANTI-DETECTION VERSION
Bypasses bot detection with stealth techniques
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json
import csv
from datetime import datetime
import random

# HARDCODED: All 16 World Weight Categories
WEIGHT_CATEGORIES = {
    'men': ['-54kg', '-58kg', '-63kg', '-68kg', '-74kg', '-80kg', '-87kg', '+87kg'],
    'women': ['-46kg', '-49kg', '-53kg', '-57kg', '-62kg', '-67kg', '-73kg', '+73kg']
}

BASE_URL = "https://www.worldtaekwondo.org"
RANKING_URL = "https://www.worldtaekwondo.org/athletes/Ranking/contents"
TARGET_MONTH = "December"
TARGET_YEAR = "2025"


class StealthScraper:
    """Anti-detection World Taekwondo Scraper"""
    
    def __init__(self):
        """Initialize with anti-detection measures"""
        
        print("🥋 Initializing STEALTH MODE scraper...")
        
        options = webdriver.ChromeOptions()
        
        # ANTI-DETECTION: Remove automation flags
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # ANTI-DETECTION: Real user agent
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # ANTI-DETECTION: Window size (real user)
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        
        # ANTI-DETECTION: Language
        options.add_argument('--lang=en-US')
        
        # Other necessary flags
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Disable images for faster loading (optional)
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        # ANTI-DETECTION: Execute script to hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # ANTI-DETECTION: Override Chrome automation
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        self.all_athletes = []
    
    def human_delay(self, min_seconds=2, max_seconds=5):
        """Random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        print(f"   ⏳ Waiting {delay:.1f}s (human-like delay)...")
        time.sleep(delay)
    
    def scroll_like_human(self):
        """Scroll page like a human would"""
        try:
            # Random scroll
            scroll_amount = random.randint(300, 700)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Scroll back up a bit
            scroll_back = random.randint(100, 200)
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_back})")
            time.sleep(random.uniform(0.3, 0.8))
        except:
            pass
    
    def move_mouse_randomly(self):
        """Simulate mouse movement"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            
            actions = ActionChains(self.driver)
            # Move to random element
            elements = self.driver.find_elements(By.TAG_NAME, 'a')
            if elements:
                random_element = random.choice(elements[:10])
                actions.move_to_element(random_element).perform()
                time.sleep(random.uniform(0.2, 0.5))
        except:
            pass
    
    def visit_homepage_first(self):
        """Visit homepage to get cookies and look natural"""
        
        print("\n📍 Step 1: Visiting homepage (getting cookies)...")
        
        try:
            # Go to homepage
            self.driver.get(BASE_URL)
            print(f"   ✅ Homepage loaded: {self.driver.title}")
            
            # Act like a human
            self.human_delay(3, 5)
            self.scroll_like_human()
            self.human_delay(2, 4)
            
        except Exception as e:
            print(f"   ⚠️  Homepage error: {e}")
    
    def scrape_all_categories(self):
        """Main scraping method with stealth"""
        
        print("\n" + "="*70)
        print("STARTING STEALTH SCRAPE - ANTI-DETECTION MODE")
        print("="*70)
        
        try:
            # Step 1: Visit homepage naturally
            self.visit_homepage_first()
            
            # Step 2: Navigate to ranking page
            print("\n📍 Step 2: Navigating to rankings page...")
            self.driver.get(RANKING_URL)
            
            # Check if we're blocked
            if "403" in self.driver.page_source or "Access Denied" in self.driver.page_source:
                print("❌ BLOCKED! Detected as bot.")
                print("💡 Try these solutions:")
                print("   1. Use a VPN")
                print("   2. Wait 24 hours and try again")
                print("   3. Try from a different network")
                return
            
            print(f"   ✅ Rankings page loaded: {self.driver.title}")
            
            # Act human
            self.human_delay(4, 7)
            self.scroll_like_human()
            
            # Save page for inspection
            with open('ranking_page_stealth.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print("   💾 Page saved: ranking_page_stealth.html")
            
            # Analyze page structure
            self.analyze_page_structure()
            
            # Try to scrape
            print("\n📍 Step 3: Attempting to extract rankings...")
            
            # Method 1: Try to find ranking tables directly
            athletes = self.extract_visible_rankings()
            
            if athletes:
                self.all_athletes.extend(athletes)
                print(f"\n✅ Successfully scraped {len(athletes)} athletes!")
            else:
                print("\n⚠️  No athletes found on visible page")
                print("💡 The page might require interaction (clicking, selecting)")
                print("📋 Check 'ranking_page_stealth.html' to see page structure")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if self.all_athletes:
                self.save_all_data()
            
            print("\n⏸️  Browser will stay open for 10 seconds...")
            print("   (Check what's on screen)")
            time.sleep(10)
            self.driver.quit()
    
    def analyze_page_structure(self):
        """Analyze what's on the page"""
        
        print("\n📊 Analyzing page structure...")
        
        try:
            # Count elements
            tables = self.driver.find_elements(By.TAG_NAME, 'table')
            selects = self.driver.find_elements(By.TAG_NAME, 'select')
            buttons = self.driver.find_elements(By.TAG_NAME, 'button')
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            
            print(f"   Tables found: {len(tables)}")
            print(f"   Dropdowns found: {len(selects)}")
            print(f"   Buttons found: {len(buttons)}")
            print(f"   Links found: {len(links)}")
            
            # Try to find ranking-related elements
            ranking_keywords = ['rank', 'athlete', 'weight', 'category', 'points']
            
            for keyword in ranking_keywords:
                elements = self.driver.find_elements(
                    By.XPATH, 
                    f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword}')]"
                )
                if elements:
                    print(f"   Found elements with '{keyword}': {len(elements)}")
            
        except Exception as e:
            print(f"   ⚠️  Analysis error: {e}")
    
    def extract_visible_rankings(self):
        """Extract any visible ranking data"""
        
        athletes = []
        
        try:
            # Look for tables
            tables = self.driver.find_elements(By.TAG_NAME, 'table')
            
            for idx, table in enumerate(tables):
                print(f"\n   Checking table {idx + 1}...")
                
                try:
                    rows = table.find_elements(By.TAG_NAME, 'tr')
                    
                    if len(rows) > 1:  # Has data
                        print(f"      Rows: {len(rows)}")
                        
                        # Try to extract data
                        for row in rows[1:]:  # Skip header
                            cells = row.find_elements(By.TAG_NAME, 'td')
                            
                            if len(cells) >= 3:
                                # Extract basic info
                                athlete = {
                                    'rank': cells[0].text.strip(),
                                    'name': cells[1].text.strip(),
                                    'country': cells[2].text.strip() if len(cells) > 2 else '',
                                    'points': cells[3].text.strip() if len(cells) > 3 else '',
                                }
                                
                                # Try to get GAL-ID
                                try:
                                    link = cells[1].find_element(By.TAG_NAME, 'a')
                                    href = link.get_attribute('href')
                                    athlete['profile_url'] = href
                                    
                                    # Extract GAL-ID from URL
                                    import re
                                    match = re.search(r'[?&](?:gal[-_]?id|id)=([^&]+)', href)
                                    if match:
                                        athlete['gal_id'] = match.group(1)
                                    else:
                                        match = re.search(r'/(?:athlete|profile)/([A-Z0-9-]+)', href)
                                        if match:
                                            athlete['gal_id'] = match.group(1)
                                except:
                                    pass
                                
                                if athlete['name']:
                                    athletes.append(athlete)
                                    print(f"         ✓ {athlete['rank']}. {athlete['name']}")
                
                except Exception as e:
                    print(f"      ⚠️  Error parsing table: {e}")
        
        except Exception as e:
            print(f"   ❌ Extraction error: {e}")
        
        return athletes
    
    def save_all_data(self):
        """Save scraped data"""
        
        if not self.all_athletes:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON
        json_file = f"worldtkd_stealth_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_athletes, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved: {json_file}")
        
        # CSV
        csv_file = f"worldtkd_stealth_{timestamp}.csv"
        if self.all_athletes:
            keys = self.all_athletes[0].keys()
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.all_athletes)
            print(f"✅ Saved: {csv_file}")


def main():
    print("="*70)
    print("🥋 WORLD TAEKWONDO SCRAPER - STEALTH MODE")
    print("="*70)
    print("\n🛡️  Anti-Detection Features:")
    print("   ✓ Hidden automation flags")
    print("   ✓ Real user agent")
    print("   ✓ Human-like delays")
    print("   ✓ Random scrolling")
    print("   ✓ Cookie collection from homepage")
    print("\n" + "="*70)
    
    input("\n▶️  Press ENTER to start (browser will open)...")
    
    scraper = StealthScraper()
    scraper.scrape_all_categories()
    
    print("\n✅ Session complete!")


if __name__ == "__main__":
    main()