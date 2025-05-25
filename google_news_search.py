import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

class NewsSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google 뉴스 검색")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색어를 입력하세요")
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("검색")
        self.search_button.clicked.connect(self.search_news)
        layout.addWidget(self.search_button)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def search_news(self):
        query = self.search_input.text().strip()
        if not query:
            return
        self.results_list.clear()

        chrome_driver_path = r"C:\tools\chromedriver-win64\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            url = f"https://news.google.com/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
            driver.get(url)
            time.sleep(3)
            articles = driver.find_elements(By.CSS_SELECTOR, "article")
            print(f"찾은 기사 수: {len(articles)}")
            for article in articles[:10]:
                title = None
                # 여러 선택자 시도
                selectors = [
                    "h3",                # h3 태그
                    "a.DY5T1d",         # 기사 링크
                    "a",                # 모든 a 태그
                    "div.MBeuO",        # BeautifulSoup에서 자주 쓰는 div
                ]
                for selector in selectors:
                    try:
                        elements = article.find_elements(By.CSS_SELECTOR, selector)
                        for el in elements:
                            text = el.text.strip()
                            if text:
                                title = text
                                break
                        if title:
                            break
                    except Exception as e:
                        continue
                if title:
                    self.results_list.addItem(title)
                    print(f"추가된 제목: {title}")
            if self.results_list.count() == 0:
                self.results_list.addItem("검색 결과가 없습니다.")
        except Exception as e:
            self.results_list.addItem(f"오류가 발생했습니다: {str(e)}")
            print(f"전체 오류: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewsSearchApp()
    window.show()
    sys.exit(app.exec_())
