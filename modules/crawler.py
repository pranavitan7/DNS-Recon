import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from queue import Queue
import threading
import os
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def banner():
    console.print("""
==============================================
              Web Crawler Tool
==============================================
""")

class WebCrawler:
    def __init__(self, base_url, max_threads=10, max_depth=3, timeout=5):
        self.base_url = self.sanitize_url(base_url)
        self.max_threads = max_threads
        self.max_depth = max_depth
        self.timeout = timeout
        self.visited = set()
        self.queue = Queue()
        self.queue.put((self.base_url, 0))
        self.results = []
        self.lock = threading.Lock()
        self.headers = {'User-Agent': 'CustomWebCrawler/1.0'}
        self.rate_limit = 0.5
        self.progress = Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console)
        self.task = self.progress.add_task("Crawling...", total=None)

    def sanitize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    def crawl(self):
        while not self.queue.empty():
            url, depth = self.queue.get()
            if url in self.visited or depth > self.max_depth:
                self.queue.task_done()
                continue
            self.visited.add(url)
            self.progress.update(self.task, description=f"Crawling: {url}")
            try:
                time.sleep(self.rate_limit)
                response = requests.get(url, timeout=self.timeout, headers=self.headers)
                status_code = response.status_code
                content_type = response.headers.get('Content-Type', '')
                console.print(f"[cyan][+][/] Found: {url} [green](Status: {status_code})[/] [yellow](Content-Type: {content_type})[/]")
                with self.lock:
                    self.results.append((url, status_code, content_type))
                if 'text/html' in content_type:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = urljoin(url, link.get('href').split('#')[0])
                        if urlparse(self.base_url).netloc == urlparse(href).netloc and href not in self.visited:
                            self.queue.put((href, depth + 1))
            except requests.RequestException:
                console.print(f"[red][!][/] Error accessing: {url}")
            finally:
                self.queue.task_done()

    def run(self):
        with self.progress:
            threads = [threading.Thread(target=self.crawl, daemon=True) for _ in range(self.max_threads)]
            for t in threads: t.start()
            self.queue.join()
            for t in threads: t.join()
        self.save_results()

    def save_results(self):
        os.makedirs("results", exist_ok=True)
        filename = os.path.join("results", f"{urlparse(self.base_url).netloc}_crawl_results.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            for url, status, content_type in self.results:
                file.write(f"{url} (Status: {status}) (Content-Type: {content_type})\n")
        console.print(f"[green][+][/green] Report saved to {filename}")

if __name__ == "__main__":
    banner()
    user_url = input("Enter the website URL: ").strip()
    crawler = WebCrawler(user_url, max_threads=10, max_depth=3, timeout=5)
    crawler.run()
