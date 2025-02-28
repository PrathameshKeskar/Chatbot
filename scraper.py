import time
import re
import json
import nltk
import numpy as np
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Download NLTK tokenizer
nltk.download('punkt')

# Configure Selenium WebDriver for Microsoft Edge
edge_options = Options()
edge_options.use_chromium = True  
edge_options.add_argument("--headless")  
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")

# Set WebDriver path
service = Service("C:/Users/PRATHAMESH/Downloads/edgedriver_win64/msedgedriver.exe")  
driver = webdriver.Edge(service=service, options=edge_options)

class DocumentationScraper:
    def __init__(self):
        self.sources = {
            "Segment": "https://segment.com/docs/",
            "mParticle": "https://docs.mparticle.com/guides/",
            "Lytics": "https://docs.lytics.com/docs",
            "Zeotap": "https://docs.zeotap.com/home/en-us/"
        }

    def scrape(self):
        """Scrapes each platform's documentation and saves it separately."""
        for platform, url in self.sources.items():
            try:
                print(f"🔄 Scraping {platform} documentation...")

                # Scrape main page
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extract structured sections
                structured_data = self.extract_sections(soup)

                # Recursively find and scrape subpages
                subpage_links = self.find_doc_links(soup, url, depth=2)  
                
                for link in subpage_links:
                    try:
                        driver.get(link)
                        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        sub_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        structured_data.update(self.extract_sections(sub_soup))
                    except Exception as subpage_error:
                        print(f"❌ Error loading {link}: {subpage_error}")

                # Save JSON for this platform
                self.save_data(platform, structured_data)
            except Exception as e:
                print(f"❌ Error scraping {platform}: {e}")

    def find_doc_links(self, soup, base_url, depth=2):
        """Finds internal documentation links up to a certain depth."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)  

            if base_url in full_url and "docs" in full_url and "#" not in full_url:
                links.add(full_url)

        if depth > 1:
            sub_links = set()
            for link in list(links)[:10]:  
                try:
                    driver.get(link)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    sub_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    sub_links.update(self.find_doc_links(sub_soup, base_url, depth-1))
                except:
                    continue
            links.update(sub_links)

        return list(links)

    def extract_sections(self, soup):
        """Extracts structured text from sections."""
        sections = {}
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            section_title = heading.get_text(strip=True)
            content = []

            for sibling in heading.find_next_siblings():
                if sibling.name in ['h1', 'h2', 'h3']:
                    break
                if sibling.name in ['p', 'ul', 'ol', 'li']:
                    content.append(sibling.get_text(strip=True))

            if content:
                sections[section_title] = " ".join(content)

        return sections

    def save_data(self, platform, data):
        """Saves structured documentation data for each platform separately."""
        filename = f"{platform.lower()}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ {platform} documentation saved to {filename}")

# 🚀 Run scraper
scraper = DocumentationScraper()
scraper.scrape()
driver.quit()
