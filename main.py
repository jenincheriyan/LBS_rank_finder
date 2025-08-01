import sys
import requests
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
)

class RankFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kerala MCA Rank Finder")
        self.setGeometry(100, 100, 400, 300)

        # Widgets
        self.label = QLabel("Enter your Application Number:")
        self.input = QLineEdit()
        self.button = QPushButton("Find Rank")
        self.result = QTextEdit()
        self.result.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(self.result)
        self.setLayout(layout)

        # Event
        self.button.clicked.connect(self.find_rank)

    def find_rank(self):
        self.result.setText("Fetching data, please wait...")
        app_number = self.input.text().strip()
        if not app_number:
            self.result.setText("Please enter a valid application number.")
            return

        try:
            # Start browser
            driver = webdriver.Firefox()
            driver.get("https://lbsapplications.kerala.gov.in/mca2025/")
            link = driver.find_element(By.PARTIAL_LINK_TEXT, "Revised Ranklist")
            pdf_url = link.get_attribute("href")
            driver.quit()

            # Download PDF
            response = requests.get(pdf_url)
            with open("ranklist.pdf", "wb") as f:
                f.write(response.content)

            # Read PDF
            with open("ranklist.pdf", "rb") as f:
                reader = PyPDF2.PdfReader(f)
                full_text = ''
                for page in reader.pages:
                    full_text += page.extract_text()

            # Search
            lines = full_text.splitlines()
            print(lines)
            found = False
            for line in lines:
                if app_number in line:
                    parts = line.split()
                    rank = parts[-1]
                    self.result.setText(f"Application Number: {app_number}\nRank: {rank}")
                    found = True
                    break
            if not found:
                self.result.setText("No Result Found.")

        except Exception as e:
            self.result.setText(f"An error occurred:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RankFinder()
    window.show()
    sys.exit(app.exec_())
