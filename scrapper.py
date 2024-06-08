from bs4 import BeautifulSoup # Importing BeautifulSoup for parsing HTML
from selenium.webdriver.chrome.service import Service # Importing Service to manage ChromeDriver service
from selenium import webdriver # Importing webdriver from selenium to control the browser
import pandas as pd # Importing pandas for data manipulation and analysis

# Setting up Chrome options
chrome_options = webdriver.chrome.options.Options()

# Path to the ChromeDriver executable
chrome_driver = "C:\\Users\\Lisandra\\Documents\\webdriver\\chromedriver-win64\\chromedriver.exe"

# Creating a Service object with the path to the ChromeDriver
service_to_pass = Service(executable_path=chrome_driver)

# Creating a WebDriver object with the service and options
wd = webdriver.Chrome(service=service_to_pass, options=chrome_options)

# URL of the website to scrape
URL_BASE = "https://www.whoscored.com/Statistics"

# Using the WebDriver to open the URL
wd.get(URL_BASE)

# Getting the page source of the opened page
soup_file = wd.page_source

# Parsing the page source with BeautifulSoup
soup_page = BeautifulSoup(soup_file, "html.parser")

# Finding the main table containing the summary statistics
main_table = soup_page.find('div', {'id': 'top-team-stats-summary'})

# Finding the table element within the main table
team_sum_stats_table = main_table.find('table', {'id': 'top-team-stats-summary-grid'})

# Finding all header columns in the table
team_sum_stats_header = team_sum_stats_table.find_all('th')

# Extracting the text from each header column and storing it in a list
header_columns = [column_name.text for column_name in team_sum_stats_header]
"""
The list Comprehension above does the same work as the code bellow
    header_columns = []
    for column_name in team_sum_stats_header:
        header_columns.append(column_name.text)
    
"""

# Finding the body of the table and all rows within it
team_sum_stats_body = team_sum_stats_table.find('tbody').find_all('tr')


# Extracting the text from each cell in each row and storing it in a list of lists
teams_stats = [
    [
        (cell.find('span', {'class': 'yellow-card-box'}).text + '|' + cell.find('span', {'class': 'red-card-box'}).text) if cell_index == 4 else cell.text
        for cell_index, cell in enumerate(row.find_all('td'))
    ]
    for row in team_sum_stats_body
]
"""
The list Comprehension above does the same work as the code bellow
teams_stats = []
for row in team_sum_stats_body:
    cells = row.find_all('td')
    row_values = []
    for cell_index in range(cells):
        if cell_index == 4:
            row_values.append((cells[cell_index].find('span', {'class': 'yellow-card-box'})+ '|' 
             + cells[cell_index].find('span', {'class': 'red-card-box'})))
        row_values.append(cells[cell_index].text)
    teams_stats.append(row_values)

"""

# Creating a DataFrame from the extracted data with appropriate headers  
df_sum = pd.DataFrame(teams_stats, columns=header_columns)

# Printing the first few rows of the DataFrame
print(df_sum.head())

# Saving the DataFrame to a CSV file
df_sum.to_csv('data/summary_data.csv')