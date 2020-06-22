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
        self.wait = WebDriverWait(self.driver, timeout=10)

    def click_kontakt(self):
        self.kontakt.click()
        return KontaktPage(self.driver)

    def click_kontakt_amp_anfahrt(self):
        self.kontakt_amp_anfahrt.click()
        return KontaktPage(self.driver)

    def hover_over_portfolio(self):
        ActionChains(self.driver).move_to_element(self.portfolio).perform()
        self.wait.until(expected_conditions.visibility_of(self.portfolio_sub_menu))

    def click_web_automation_amp_mobile_testing(self):
        web_automation_amp_mobile_testing = \
            self.portfolio_sub_menu.find_element_by_link_text("Web, Automation & Mobile Testing")
        web_automation_amp_mobile_testing.click()
        page_title = self.driver.find_element_by_class_name('page_title')
        self.wait.until(expected_conditions.visibility_of(page_title))
        assert page_title.find_element_by_tag_name('span').text == 'Web, Automation & Mobile Testing'
        return WAMTestingPage(self.driver)


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


class WAMTestingPage:
    def __init__(self, driver):
        self.driver = driver
        self.portfolio = self.driver.find_element_by_id("menu-item-220")
        self.mobile_section_title = self.driver.find_element_by_xpath("//div[@id='team-tab-three-title-desktop']/..")
        self.mobile_section = self.driver.find_element_by_id("team-tab-three-body")
        self.wait = WebDriverWait(self.driver, timeout=10)

    def is_portfolio_item_selected(self):
        return 'current_page_ancestor' in self.portfolio.get_attribute('class')

    def click_mobile_section_title(self):
        self.mobile_section_title.click()
        self.wait.until(expected_conditions.visibility_of(self.mobile_section))


