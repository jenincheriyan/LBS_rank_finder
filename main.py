from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import PyPDF2

driver = webdriver.Firefox()
driver.get("https://lbsapplications.kerala.gov.in/mca2025/")
#find the link
link= driver.find_element(By.PARTIAL_LINK_TEXT, "Revised Ranklist")
pdf_url = link.get_attribute("href")

#saving the pdf
response = requests.get(pdf_url)

with open("ranklist.pdf",'wb') as file:
    file.write(response.content)



driver.quit()

