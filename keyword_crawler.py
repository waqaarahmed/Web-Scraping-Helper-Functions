import csv
import os
from itertools import cycle
from scrapingant_client import ScrapingAntClient
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

keywords = ['Momence', 'Mindbody', 'Wellnessliving', 'Vagaro', 'Arketa',
            'Punchpass', 'Schedulicity', 'Glofox', 'Walla']
results = {keyword: [] for keyword in keywords}
visited_urls = set()
domain_keywords = {}
delay_between_requests = 0.3  # seconds

# ScrapingAnt API keys
API_KEYS = ['f4e623077cd24f369fb663ab39978dc3']
api_key_cycle = cycle(API_KEYS)


def get_next_api_key():
    logger.info("Getting the next API key")
    return next(api_key_cycle)


def is_internal_link(url, base_url):
    internal = urlparse(url).netloc == urlparse(base_url).netloc
    logger.info(f"Checking if {url} is an internal link: {internal}")
    return internal


def get_internal_links(soup, base_url):
    internal_links = set()
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        if is_internal_link(full_url, base_url):
            internal_links.add(full_url)
    logger.info(f"Found {len(internal_links)} internal links on {base_url}")
    return internal_links


def scrape_page(url):
    try:
        logger.info(f"Fetching page: {url}")
        api_key = get_next_api_key()
        client = ScrapingAntClient(token=api_key)
        response = client.general_request(url)

        # Assuming the response object has status_code, headers, and content attributes
        status_code = response.status_code
        content = response.content

        # Handling different status codes
        if status_code in [301, 302, 307]:
            new_url = response.headers.get('Location')
            logger.info(f"Redirected to {new_url}")
            return scrape_page(new_url)
        elif status_code == 200:
            logger.info(f"Page fetched successfully: {url}")
            soup = BeautifulSoup(content, 'html.parser')
            logger.info(f"Successfully fetched HTML content from {url}")
            return soup
        elif status_code == 404:
            logger.error(f"Error fetching {url}: Status code 404 (Not Found)")
            return None
        elif status_code == 407:
            logger.error(f"Error fetching {url}: Status code 407 (Proxy Authentication Required)")
            return None
        elif status_code == 565:
            logger.error(f"Error fetching {url}: Status code 565 (Unknown Error)")
            return None
        else:
            logger.error(f"Error fetching {url}: Status code {status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


def search_keywords(soup, keywords):
    logger.info("Searching for keywords in the page content")
    text = soup.get_text().lower()
    found_keywords = [keyword for keyword in keywords if keyword.lower() in text]
    logger.info(f"Found keywords: {found_keywords}")
    return found_keywords


def get_domain(url):
    domain = urlparse(url).netloc
    logger.info(f"Extracted domain {domain} from URL {url}")
    return domain


def scrape_website(base_url, counter, total_urls):
    domain = get_domain(base_url)
    logger.info(f"Scraping website: {base_url} (URL {counter} of {total_urls})")

    # Skip URLs that have already been processed
    if any(base_url in entry for entry in saved_entries):
        logger.info(f"URL {base_url} has already been processed. Skipping.")
        return

    # Checking to see if domain has been scraped before
    if domain in domain_keywords:
        found_keywords = domain_keywords[domain]
        logger.info(f"Domain {domain} already scraped. Reusing keywords: {found_keywords}")
    else:
        to_visit = [base_url]
        found_keywords = set()

        while to_visit:
            url = to_visit.pop()
            if url in visited_urls:
                logger.info(f"URL {url} has already been visited")
                continue
            visited_urls.add(url)

            logger.info(f"Visiting URL: {url}")
            soup = scrape_page(url)
            if soup:
                page_keywords = search_keywords(soup, keywords)
                found_keywords.update(page_keywords)

                if found_keywords:
                    logger.info(f"Keywords found on {url}, skipping further internal links.")
                    break

                internal_links = get_internal_links(soup, base_url)
                logger.info(f"Internal links to visit: {internal_links}")
                to_visit.extend(internal_links)

            rate_limit(delay_between_requests)

        # Save found keywords for the domain
        if not found_keywords:
            found_keywords = ['Unknown']
        domain_keywords[domain] = found_keywords
        logger.info(f"Scraped domain {domain} with keywords: {found_keywords}")

    # Save results
    for keyword in found_keywords:
        if keyword not in results:
            results[keyword] = []
        results[keyword].append(base_url)

    save_results_to_csv(results, 'results.csv')

    logger.info(f"Processed {counter} out of {total_urls} URLs")


def read_urls(file_path):
    logger.info(f"Reading URLs from file: {file_path}")
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    logger.info(f"Read {len(urls)} URLs from {file_path}")
    return urls


def rate_limit(delay):
    logger.info(f"Rate limiting for {delay} seconds")
    time.sleep(delay)


def save_results_to_csv(results, output_file):
    logger.info(f"Saving results to CSV file: {output_file}")
    with open(output_file, mode='a', newline='') as csvfile:  # Open in append mode
        writer = csv.writer(csvfile)
        for keyword, urls in results.items():
            for url in urls:
                entry = (keyword, url)
                if entry not in saved_entries:
                    writer.writerow(entry)
                    saved_entries.add(entry)
    logger.info(f"Results saved to {output_file}")


def load_existing_results(output_file):
    if not os.path.exists(output_file):
        return set()

    logger.info(f"Loading existing results from CSV file: {output_file}")
    existing_results = set()
    with open(output_file, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                entry = (row[0], row[1])
                existing_results.add(entry)
    logger.info(f"Loaded {len(existing_results)} existing results from {output_file}")
    return existing_results


# Load existing results
saved_entries = load_existing_results('results.csv')

# Example usage
urls = read_urls('https_domains.txt')
total_urls = len(urls)

# Using ThreadPoolExecutor to handle multiple URLs concurrently
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = [executor.submit(scrape_website, url, counter, total_urls) for counter, url in enumerate(urls, start=1)]
    for future in as_completed(futures):
        future.result()  # This will re-raise any exceptions caught during the execution
