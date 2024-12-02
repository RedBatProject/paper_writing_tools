import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

columns_ = ["refference","DOI","topdown","abstrakt","discussion","all4one","methodology in details","origin","inter","bib"]

def doibib(doi):
    # Replace with your DOI
    doi = re.sub('https://www.doi.org/','',doi)
    # Construct the URL for the CrossRef API

    # url_chicago = f"https://api.crossref.org/works/{doi}/transform/application/vnd.citationstyles.csl+json?style=chicago-author-date"
    # url_mla = f"https://api.crossref.org/works/{doi}/transform/application/vnd.citationstyles.csl+json?style=mla"

    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"

    # Make the request to the CrossRef API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the BibTeX citation
        return response.text
    else:
        return doi


# Load the HTML file
with open('./l2.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'lxml')

# Find the table body
tbody = soup.find('tbody')

# Extract rows and cells
data = []
po = tbody.find_all('tr')
for row in po:
    cells = row.find_all('td')
    
    # Extract href from the first column with the specified class
    if cells:
        link = cells[0].find('a', class_='text-primary text-base no-underline hover:underline')
        first_column_href = link['href'] if link else None
        link2 = cells[0].find('a', class_='text-typo-gray text-xs no-underline hover:underline')
        first_column_href2 = link2['href'] if link else None
        
        # Extract text from the rest of the columns
        other_columns = [cell.get_text(strip=True) for cell in cells[1:]]
        
        # Append the href and other columns to the data list
        data.append([first_column_href]+[first_column_href2]+ other_columns)

# Create a DataFrame
df = pd.DataFrame(data)

# Optionally, set the first row as the header if needed
# df.columns = df.iloc[0]
# df = df[1:]
df["bib"] = df[df.columns[1]].apply(doibib)
df.columns = columns_

# Display the DataFrame
df.to_csv('./resiliencepowergridcyber.csv',index=False)