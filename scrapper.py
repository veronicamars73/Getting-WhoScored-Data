from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

chrome_options = webdriver.chrome.options.Options()
chrome_driver = "C:\\Users\\Lisandra\\Documents\\webdriver\\chromedriver-win64\\chromedriver.exe"
service_to_pass = Service(executable_path="C:\\Users\\Lisandra\\Documents\\webdriver\\chromedriver-win64\\chromedriver.exe")
wd = webdriver.Chrome(service=service_to_pass, options=chrome_options)

URL_BASE = "https://www.whoscored.com/Statistics"
wd.get(URL_BASE)
soup_file = wd.page_source

soup_page = BeautifulSoup(soup_file, "html.parser")

#print(soup_page)

main_table = soup_page.find('div', {'id': 'top-team-stats-summary'})

team_stats_tables = main_table.find_all('table', {'id': 'top-team-stats-summary-grid'})

print(team_stats_tables)
