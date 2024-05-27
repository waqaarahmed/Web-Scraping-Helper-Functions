from itertools import cycle
from scrapingant_client import ScrapingAntClient
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


keywords = ['Mindbody', 'Wellnessliving', 'Vagaro', 'Arketa',
            'Punchpass', 'Schedulicity', 'Glofox', 'Walla']
results = {keyword: [] for keyword in keywords}
visited_urls = set()
domain_keywords = {}
delay_between_requests = 0.3  # seconds

# ScrapingAnt API keys
API_KEYS = [ADD API KEY]
api_key_cycle = cycle(API_KEYS)


def get_next_api_key():
    return next(api_key_cycle)


def is_internal_link(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc


def get_internal_links(soup, base_url):
    internal_links = set()
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        if is_internal_link(full_url, base_url):
            internal_links.add(full_url)
    return internal_links


def scrape_page(url):
    try:
        api_key = get_next_api_key()
        client = ScrapingAntClient(token=api_key)
        response = client.general_request(url)

        # Assuming the response object has status_code, headers, and content attributes
        status_code = response.status_code
        headers = response.headers
        content = response.content

        # Handling different status codes
        if status_code in [301, 302, 307]:
            new_url = headers.get('Location')
            logger.info(f"Redirected to {new_url}")
            return scrape_page(new_url)
        elif status_code == 200:
            if 'html' in headers.get('Content-Type', ''):
                soup = BeautifulSoup(content, 'html.parser')
                return soup
            else:
                logger.error(f"Error fetching {url}: Content is not HTML")
                return None
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
    text = soup.get_text().lower()
    found_keywords = [keyword for keyword in keywords if keyword.lower() in text]
    return found_keywords


def get_domain(url):
    return urlparse(url).netloc


def scrape_website(base_url, counter, total_urls):
    domain = get_domain(base_url)

    # Checking to see if domain has been scraped before
    if domain in domain_keywords:
        found_keywords = domain_keywords[domain]
        logger.info(f"Domain {domain} already scraped. Reusing keywords.")
    else:
        to_visit = [base_url]
        found_keywords = set()

        while to_visit:
            url = to_visit.pop()
            if url in visited_urls:
                continue
            visited_urls.add(url)

            soup = scrape_page(url)
            if soup:
                page_keywords = search_keywords(soup, keywords)
                found_keywords.update(page_keywords)

                internal_links = get_internal_links(soup, base_url)
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

    logger.info(f"Processed {counter} out of {total_urls} URLs")


def read_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def rate_limit(delay):
    time.sleep(delay)


def save_results_to_csv(results, output_file):
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Keyword_found', 'URL'])
        for keyword, urls in results.items():
            for url in urls:
                writer.writerow([keyword, url])


# Example usage
urls = read_urls('https_domains.txt')
total_urls = len(urls)

# Using ThreadPoolExecutor to handle multiple URLs concurrently
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(scrape_website, url, counter, total_urls) for counter, url in enumerate(urls, start=1)]
    for future in as_completed(futures):
        future.result()  # This will re-raise any exceptions caught during the execution

# Save results to CSV for testing
save_results_to_csv(results, 'results.csv')
