from bs4 import BeautifulSoup

file = open('amazon_tire_list.html', 'r')
soup = BeautifulSoup(file, 'html.parser')
soup.find_all("a", class_="a-link-normal")

