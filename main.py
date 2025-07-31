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

#read pdf
with open("ranklist.pdf", 'rb') as file:
    reader= PyPDF2.PdfReader(file)
    test=''
    for page in reader.pages:
        test+= page.extract_text()

lines = test.splitlines()
app_number= input("application number: ").strip()

#search
is_it= False
for line in lines:
    if app_number in line and line.strip().startswith(tuple("o123456789")):
        parts= line.split()

        print(f"Name    : {' '.join(parts[3])}")
        print(f"Rank    : {parts[-1]}")
        is_it = True
        break
if not is_it:
    print('No Result')

driver.quit()

