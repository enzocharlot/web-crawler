import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_urls(url, max_depth=2):
    visited_urls = set()
    found_urls = set()

    def crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        visited_urls.add(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            if next_url not in found_urls:
                found_urls.add(next_url)
                print(f"Found URL: {next_url}")
            crawl(next_url, depth + 1)

    crawl(url, 0)

def crawl_emails(url, max_depth=2):
    visited_urls = set()
    emails_found = set()

    def crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        visited_urls.add(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
        new_emails = emails - emails_found  # Subtract already found emails
        emails_found.update(new_emails)

        for email in new_emails:
            print(f"Found Email: {email}")

        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            crawl(next_url, depth + 1)

    crawl(url, 0)

def crawl_phone_numbers(url, max_depth=2):
    visited_urls = set()
    phones_found = set()

    def crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        visited_urls.add(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        phones = set(re.findall(r"\+?\d[\d -]{8,}\d", soup.text))
        new_phones = phones - phones_found  # Subtract already found phones
        phones_found.update(new_phones)

        for phone in new_phones:
            print(f"Found Phone Number: {phone}")

        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            crawl(next_url, depth + 1)

    crawl(url, 0)

if __name__ == "__main__":
    print("Select an option:")
    print("1. Crawl URLs")
    print("2. Crawl Email Addresses")
    print("3. Crawl Phone Numbers")
    
    choice = input("Enter your choice (1/2/3): ")
    
    start_url = input("Enter the starting URL: ")
    
    if choice == '1':
        crawl_urls(start_url)
    elif choice == '2':
        crawl_emails(start_url)
    elif choice == '3':
        crawl_phone_numbers(start_url)
    else:
        print("Invalid choice.")
