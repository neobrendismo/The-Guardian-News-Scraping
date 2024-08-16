# **News Content Collect and Store**
# **Introduction**

The objective of this project is to develop a solution that crawls news articles from [The Guardian website](https://www.theguardian.com/au), processes the content, and stores it in Google BigQuery. The project utilizes the [Scrapy](https://scrapy.org/) framework to efficiently scrape and cleanse the data before integration into BigQuery.

# **Methodology**

PHASE 1: **[Google Cloud Plataform(GCP) Configuration](https://cloud.google.com/free)**
1. We need to create a free account in GCP;
2. Set Up Your Google Cloud Credentials;
3. Replace the key_path in the closed method with the actual path to your Google Cloud service account JSON file;
4. Replace project_id, dataset_id, and table_id with your Google Cloud Project, BigQuery Dataset, and Table IDs, respectively;

# **Requirements**
    Python
    Scrapy
    readability
    pandas
    google-cloud-bigquery
    google-auth

PHASE 2:  **Setting up environment to start the Scrapy Project **
1. Install virtualenv in your Windows command shell, Powershell, or other terminal you are using.

```
pip install virtualenv
```
2. Navigate to the folder where you want to create the virtual environment, and run the virtualenv command. In my case:
   
``  cd \The-Guardian-News-Scraping> ``
3. Then activate the virtual environment. For windows, use this command: 

```
.venv\Scripts\activate
```

4. Now you can install Scrapy to finally creat the project
```
pip install scrapy
```
5. To create the project, run the following command. In my case, the project is named newsscraper, but feel free to choose a name that suits your preference.

```
scrapy startproject <project_name>
```

PHASE 3: **Creat our Scrapy Spider to colect news data from The Guardian** 

1.To create a new spider, use the genspider command (be sure to specify the directory name you've created), this command will creat a new file called "newspider", you can also change for a name that suits your preference: 

```
cd newsscraper

scrapy genspider newspider https://www.theguardian.com/au
```

2. Now you can run the spiper you`ve created
```
scrapy crawl newspider
```

PHASE 4:  **Using Scrapy Shell to Identify CSS Selectors**

1. To open Scrapy shell use this command:
   
```
scrapy shell
```
2. The first step is to fetch the main page of The Guardian's website in our Scrapy shell
   
 ```
fetch('https://www.theguardian.com/au)
```
We should see a response like this:
![image](https://github.com/user-attachments/assets/4b62d81c-0bf7-44a4-a1a8-0c2c12f02604)

3. Then you can use the response to find in easier way your own id's and classes. Example:
   ```
   response.css('a.dcr-lv2v9o').getall()
   ```

PHASE 4: before run the code make sure to adjust the project_id, dataset_id, table_id and key_path variables based on your Google BigQuery project setup. Also, you need to exit the Scrapy shell and run the code on the newsscraper directory, use the folloing command to run the code:

```
scrapy crawl newspider
```

# **The Challenges I Faced While Runing The Code" 
The code is running without any issues, and it is extracting data. However, the resulting file is coming up empty. Scrapy is starting correctly, opening the main page, and then closing without scraping any items. This suggests that either no links are being found to continue the scraping process, or there's an issue with the scraping logic itself.

Since I’ve confirmed that the link selector (article_links = response.css('a::attr(href)').extract()) is indeed extracting data, it indicates that the problem lies within the logic I’m using. Although I can manually extract data in the terminal, the main code isn’t performing as expected. Additionally, I’ve verified that GCP is correctly configured for authentication with BigQuery and that the path to the JSON credentials file is accurate.
That means I have to study more and find out the solution for my bug :D

