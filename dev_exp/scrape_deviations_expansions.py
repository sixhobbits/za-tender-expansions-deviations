import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '.pdf' in href:
            full_url = urljoin(url, href)
            link_text = a_tag.text.strip()
            pdf_links.append((full_url, link_text))
    print(pdf_links)
    return pdf_links

def save_pdf(pdf_url, filename):
    response = requests.get(pdf_url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def standardize_filename(link_text):
    parts = link_text.split(' ')

    if parts[0] == "Expansions":
        doc_type = "expansion"
    elif parts[0] == "Deviations":
        doc_type = "deviation"
    else:
        return

    for i, part in enumerate(parts):
        if part == "Quarter":
            quarter = parts[i+1]
            break

    for part in parts:
        if "20" in part and ("-" in part or "/" in part):
            year = part
            break

    filename = f"{year.replace('/', '-')}_q{quarter}_{doc_type}.pdf"
    print(filename)
    return filename

def main():
    url = 'http://ocpo.treasury.gov.za/Suppliers_Area/Pages/Deviations-and-Exspansions.aspx'
    dest_dir = './pdfs'
    os.makedirs(dest_dir, exist_ok=True)

    pdf_links = fetch_pdf_links(url)
    for pdf_url, link_text in pdf_links:
        filename = standardize_filename(link_text)
        if not filename:
            continue
        filepath = os.path.join(dest_dir, filename)
        save_pdf(pdf_url, filepath)

main()

