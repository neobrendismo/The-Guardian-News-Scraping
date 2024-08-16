import scrapy
from readability import Document
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

class NewSpiderSpider(scrapy.Spider):
    name = "newspider"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/au"]

    # Initialize an empty list to store the data
    data = []

    def parse(self, response):
        # Extract article links using a general CSS selector to capture more links
        article_links = response.css('a.dcr-lv2v9o::attr(href)').getall()
        self.log(f"Found {len(article_links)} article links")
        
        # Filter links to include only those that lead to articles
        filtered_article_links = [link for link in article_links if link.startswith('/')]
        self.log(f"Filtered down to {len(filtered_article_links)} article links")
        
        for article_link in filtered_article_links:
            full_article_link = response.urljoin(article_link)
            self.log(f"Following link: {full_article_link}")
            yield scrapy.Request(url=full_article_link, callback=self.parse_article)

    def parse_article(self, response):
        # Use the readability library to extract content from the article
        doc = Document(response.text)

        # Extract information from the article
        date = response.css('.dcr-u0h1qy::text').get()
        title = response.css('.dcr-1fasd0d, .dcr-qao4mw::text').get()
        author = response.css('div.dcr-1umb6ym a::text').get()
        text = response.css('.dcr-1lpi6p1 ::text').getall()

        # Convert the list of strings into a single string
        text_as_string = '\n'.join(text)

        # Get the URL of the article
        article_url = response.url

        # Check if all necessary information has been extracted
        if date and title and author and text_as_string:
            data = {
                'title': title,
                'author': author,
                'text': text_as_string,
                'date': date,
                'url': article_url,
            }
            self.log(f"Data extracted: {data}")
            self.data.append(data)

    def closed(self, reason):
        if not self.data:
            self.log("No data extracted; nothing to upload to BigQuery.")
            return
        
        # Convert the list of data into a pandas DataFrame
        df = pd.DataFrame(self.data)

        # BigQuery configuration
        project_id = 'news-content-collect-store'  
        dataset_id = 'TheGuardia_scraper'  
        table_id = 'TheGuardian'      

        table_path = f'{project_id}.{dataset_id}.{table_id}'
        key_path = r'C:\Users\brend\OneDrive\Documents\scraping_project\news-content-collect-store-68cabe219565.json'  
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])

        # Save the data to a local CSV file for debugging purposes
        df.to_csv("output_test.csv", index=False)

        # Upload the DataFrame to BigQuery
        self.log(f"Attempting to upload {len(df)} rows to BigQuery.")
        df.to_gbq(destination_table=table_path, project_id=project_id, if_exists='replace', credentials=credentials)
        self.log("Data uploaded to BigQuery.")
