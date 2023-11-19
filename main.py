import requests
from bs4 import BeautifulSoup
from save_data import save_to_csv

def get_product_data(urls, csv_file_path):
    product_data = []  # Initialize an empty list to store product data

    for url in urls:
        print(f"Scraping data from {url}")
        while url:  # Continue until there are no more pages
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find and process each product on the page
                product_elements = soup.find_all('p', class_='product-name')
                price_elements = soup.find_all('span', class_='price')

                for product_element, price_element in zip(product_elements, price_elements):
                    product_title = product_element.find('a').text.strip()
                    print(f"Product Title: {product_title}")

                    # Extract euros and cents from the HTML structure
                    euros = int(price_element.contents[0])
                    cents = int(price_element.find('sup').text)

                    # Format the price with two decimal places
                    formatted_price = f"{euros}.{cents:02d}"
                    print(f"Product Price: {formatted_price}")
                    print("-" * 30)

                    # Append product data to the list
                    product_data.append({"title": product_title, "price": formatted_price})

                # Save the current page's data to the CSV file
                save_to_csv(product_data, csv_file_path)

                # Check for pagination
                next_page_element = soup.find('li', class_='pagination-next')
                if next_page_element:
                    next_page_url = next_page_element.find('a')['href']
                    url = f"https://220.lv{next_page_url}"
                    # Clear product_data for each new page
                    product_data = []
                else:
                    url = None  # No more pages

            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
                url = None  # Stop if there's an error


# Replace 'your-urls' with the actual list of URLs you want to scrape
urls = [
    'https://220.lv/lv/datortehnika/biroja-tehnika-un-piederumi/izejmateriali/kartridzi-lazerprinteriem',
    'https://220.lv/lv/datortehnika/biroja-tehnika-un-piederumi/izejmateriali/kartridzi-lazerprinteriem?page=2',
    'https://220.lv/lv/datortehnika/biroja-tehnika-un-piederumi/izejmateriali/kartridzi-lazerprinteriem?page=3',
    'https://220.lv/lv/datortehnika/biroja-tehnika-un-piederumi/izejmateriali/kartridzi-lazerprinteriem?page=4',
    'https://220.lv/lv/datortehnika/biroja-tehnika-un-piederumi/izejmateriali/kartridzi-lazerprinteriem?page=5'
]

csv_file_path = "product_data.csv"
get_product_data(urls, csv_file_path)
