from bs4 import BeautifulSoup

import requests

# Scrape the page
url = 'https://hertie-scraping-website.vercel.app/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

flags = []

# first 8 flags
p_tags_flags = soup.find_all('p', class_='text-base')
for p in p_tags_flags[2:]:
    flags.append(p.get_text().strip())

# number 8
num_8 = soup.find('p', class_='text-transparent').get_text().strip()
flags.append(num_8)

# flags in img tags
img_tags_flags = soup.find_all('img', alt=True)
for img in img_tags_flags:
    flags.append(img['alt'])

# Find all div elements with class "size-10"
size_10_divs = soup.find_all('div', class_='size-10')
for div in size_10_divs:
    # For each 'size-10' div, find its child div
    child_div = div.find('div')
    if child_div:
        # If the child div's id attribute is empty, use its class for the flag identifier
        if not child_div.get('id'):
            flags.append(child_div.get('class')[0])  # Assuming there's only one class that's relevant
        # If the child div's class attribute is empty or not relevant, use its id for the flag identifier
        else:
            flags.append(child_div.get('id'))

# Page 2

url_2 = "https://hertie-scraping-website.vercel.app/wowimlevel2"

response_2 = requests.get(url_2)

soup_2 = BeautifulSoup(response_2.content, 'html.parser')

# number 41
num_41 = soup_2.find('div', class_='text-center my-4').text[-8:].strip()
flags.append(num_41)

# number 42
num_42 = soup_2.find('div', class_='text-transparent').get_text().strip()
flags.append(num_42)


# Function to process an element for flags
def process_element(element):
    # Check if 'id' attribute contains 'flag'
    if 'flag' in element.get('id', ''):
        flags.append(element['id'])
    # Check if any class contains 'flag'
    elif any('flag' in cls for cls in element.get('class', [])):
        flags.extend([cls for cls in element.get('class', []) if 'flag' in cls])

# Iterate over 'p' tags
for p_tag in soup_2.find_all('p'):
    process_element(p_tag)

# Iterate over 'div' tags
for div_tag in soup_2.find_all('div'):
    process_element(div_tag)

# sort the flags
# flags.sort()

# Deduplicate flags
# flags_final = list(set(flags))

flags_copy = flags.copy()

# Extract numbers from flag identifiers and convert to integers
flag_numbers = [int(flag.split('-')[1]) for flag in flags_copy]

# Sort the numbers
sorted_numbers = sorted(flag_numbers)

# Reconstruct the sorted flag identifiers
sorted_flags = [f"flag-{num}" for num in sorted_numbers]

for flag in sorted_flags:
    print(flag)
