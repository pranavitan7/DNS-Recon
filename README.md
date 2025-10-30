DNS-Recon is a comprehensive, modular utility built in Python, specifically tailored for performing detailed DNS reconnaissance and enumerating DNS records for a given domain. This tool allows security researchers, penetration testers, and network administrators to gain deep insights into a domain's DNS configuration and infrastructure. Each module within the tool performs a specific task related to DNS inspection, ensuring clarity, maintainability, and focused functionality. 

The dnsrecord.py module retrieves and displays detailed DNS record information for a specified domain. It queries record types such as A, AAAA, MX, NS, TXT, and CNAME, providing valuable insights into a domain’s network infrastructure and configuration. This module enables users to analyze mail servers, name servers, IP addresses, and text records, which can reveal important data for footprinting and reconnaissance.

The dnssec.py module evaluates whether a domain supports and correctly implements DNS Security Extensions (DNSSEC). It validates DNS responses and checks for the presence of DNSKEY, DS, and RRSIG records that confirm authenticity and integrity of DNS data. This module helps detect DNS tampering vulnerabilities and misconfigurations by confirming if responses are cryptographically signed. 

The subdomain.py module is dedicated to discovering subdomains associated with a target domain using enumeration and brute-force techniques. It queries public DNS records, wordlists, and search methods to identify hidden or unlisted subdomains that may expose additional services or applications. This module plays a crucial role in reconnaissance by uncovering potential entry points and misconfigured assets that often go unnoticed. 

The crawler.py module is an advanced version of the basic crawl functionality, designed for deeper and more comprehensive web crawling. It recursively explores URLs within a domain, identifying internal and external links while avoiding duplicate paths or infinite loops. This module assists in enumerating web assets, analyzing site architecture, and collecting useful metadata from discovered pages. 

The crawl.py module acts as a basic crawler that collects and lists URLs found on a given website. It systematically fetches HTML pages, extracts links, and maps the structure of the target site for reconnaissance purposes. This module helps identify publicly exposed directories, hidden endpoints, or linked assets that might be useful for further investigation. 

The DOH.py module focuses on detecting and resolving DNS queries through DNS over HTTPS (DoH) endpoints. It allows users to perform secure DNS lookups via HTTPS requests instead of traditional UDP or TCP connections, ensuring privacy and integrity during DNS resolution. 


```bash
git clone https://github.com/pranavitan7/DNS-Recon.git
```

```bash
cd dns
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```
<img width="690" height="813" alt="image" src="https://github.com/user-attachments/assets/6144723b-0e6b-4c6d-89ca-4a72dd7aaa6e" />

