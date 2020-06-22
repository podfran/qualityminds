from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.portfolio = self.driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]")
        self.portfolio_sub_menu = self.portfolio.find_element_by_xpath("./following-sibling::ul")
        self.kontakt = self.driver.find_element_by_xpath("//a[contains(text(),'Kontakt')]")
        self.karriere = self.driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]")
        self.kontakt_amp_anfahrt = self.driver.find_element_by_xpath("//a[contains(text(),'Kontakt & Anfahrt')]")

    def click_kontakt(self):
        self.kontakt.click()
        return KontaktPage(self.driver)

    def click_kontakt_amp_anfahrt(self):
        self.kontakt_amp_anfahrt.click()
        return KontaktPage(self.driver)

    def hover_over_portfolio(self):
        ActionChains(self.driver).move_to_element(self.portfolio).perform()
        wait = WebDriverWait(self.driver, timeout=10)
        wait.until(expected_conditions.visibility_of(self.portfolio_sub_menu))


class KontaktPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.find_element_by_xpath("//h1[contains(@class, 'text-padded')]/span")
        self.page_content = self.driver.find_element_by_id('main-content').text

    def __contains__(self, item):
        return item in self.page_content

    def __eq__(self, other):
        return self.page_content == other.page_content

    def return_to_main_page(self):
        self.driver.get('https://qualityminds.de')
        return MainPage(self.driver)
