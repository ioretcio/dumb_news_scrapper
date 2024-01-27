from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time as t
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

autor_link = "https://progroshi.news/author/name.html"
until_time = '2023-12-26T00:00:00+00:00'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(autor_link)
posts_dict = {}
process = True

while process:
    posts = driver.find_element(By.CLASS_NAME, 'box_category-news').find_elements(By.CLASS_NAME, 'post')
    for post in posts:
        post_title = post.find_element(By.CLASS_NAME, 'post__title').text
        href = post.find_element(By.CLASS_NAME, 'post__title').find_element(By.TAG_NAME, 'a').get_attribute('href')
        time = post.find_element(By.CLASS_NAME, 'post__box').find_element(By.TAG_NAME, 'time').get_attribute('datetime')
        posts_dict[time] = post_title, href
        if time < until_time:
            process = False
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[area-label="Більше новин"]')))
    driver.execute_script("arguments[0].scrollIntoView();", element) 
    driver.execute_script(f"window.scrollBy(0, {-50});") 
    element.click()  
    t.sleep(3)


import csv

with open('posts_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['time', 'post_title', 'href']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for time, (post_title, href) in posts_dict.items():
        writer.writerow({'time': time, 'post_title': post_title, 'href': href})
