from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import pandas as pd

chrome_options = webdriver.chrome.options.Options()
chrome_driver = "C:\\Users\\Lisandra\\Documents\\webdriver\\chromedriver-win64\\chromedriver.exe"
service_to_pass = Service(executable_path=chrome_driver)
wd = webdriver.Chrome(service=service_to_pass, options=chrome_options)

URL_BASE = "https://www.whoscored.com/Statistics"
wd.get(URL_BASE)
soup_file = wd.page_source

soup_page = BeautifulSoup(soup_file, "html.parser")

# Summary

main_table = soup_page.find('div', {'id': 'top-team-stats-summary'})

team_sum_stats_table = main_table.find('table', {'id': 'top-team-stats-summary-grid'})

team_sum_stats_header = team_sum_stats_table.find_all('th')

header_columns = [column_name.text for column_name in team_sum_stats_header]
"""
The list Comprehension above does the same work as the code bellow
    header_columns = []
    for column_name in team_sum_stats_header:
        header_columns.append(column_name.text)
    
"""
team_sum_stats_body = team_sum_stats_table.find('tbody').find_all('tr')

teams_stats = [[cell_value.text for cell_value in row.find_all('td')] for row in team_sum_stats_body]
"""
The list Comprehension above does the same work as the code bellow
teams_stats = []
for row in team_sum_stats_body:
    cells = row.find_all('td')
    row_values = []
    for cell_value in cells:
        row_values.append(cell_value.text)
    teams_stats.append(row_values)
    
"""
    
df_sum = pd.DataFrame(teams_stats, columns=header_columns)

print(df_sum.head())

df_sum.to_csv('data/summary_data.csv')