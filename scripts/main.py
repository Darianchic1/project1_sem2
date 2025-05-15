"""Файл для парсинга данных с AviaSales"""

import time
import json
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Set up and return the Selenium WebDriver"""
    options = Options()
    options.add_argument('--headless')  # Run in background mode
    options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_popular_destinations():
    """Scrape popular destinations from Aviasales"""
    driver = setup_driver()
    
    try:
        # Navigate to the main page 
        url = "https://www.aviasales.ru"
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(5)
        
        # Get page source
        page_source = driver.page_source
        
        # Extract popular destinations data
        popular_destinations = extract_destinations_data(page_source)
        
        return popular_destinations
    
    finally:
        driver.quit()

def extract_destinations_data(html_content):
    """Extract popular destinations data from the HTML content"""
    # Find the start of popular destinations data
    start_marker = '"popular_destinations":'
    start_index = html_content.find(start_marker)
    
    if start_index != -1:
        try:
            # Adjust start index to include the start marker
            json_str = html_content[start_index:]
            
            # Find the end of the JSON array marked by ']}]'
            end_index = json_str.find(']}]')
            if end_index != -1:
                # Include the end marker in the extracted string
                json_str = json_str[:end_index + 3]
                
                # Parse the complete JSON string
                # Add the opening brace to make it valid JSON
                json_data = json.loads('{' + json_str + '}')
                # print(json_str)
                # raise Exception("Stop here")
                return json_data['popular_destinations']
            else:
                print("Could not find the end of the JSON array")
                return []
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []
    else:
        print("No popular destinations data found in the HTML")
        return []

def save_to_csv(destinations, output_file='data/popular_destinations.csv'):
    """Save the destinations data to a CSV file"""
    if not destinations:
        print("No destinations data to save")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['destination_city', 'destination_country', 'origin_name', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for destination in destinations:
            dest_city = destination['destination_city']['name']
            dest_country = destination['destination_country']['name']
            
            for price_info in destination['prices']:
                writer.writerow({
                    'destination_city': dest_city,
                    'destination_country': dest_country,
                    'origin_name': price_info['origin_name'],
                    'price': price_info['price']['value']
                })
                
    print(f"Destinations data saved to {output_file}")

def main():
    print("Fetching popular destinations from Aviasales...")
    destinations = get_popular_destinations()
    
    if destinations:
        print(f"Found {len(destinations)} destination entries")
        save_to_csv(destinations)
    else:
        print("No destinations found")

if __name__ == "__main__":
    main()