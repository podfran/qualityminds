from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.portfolio_sub_menu = None

    def click_kontakt(self):
        kontakt = self.driver.find_element_by_xpath("//a[contains(text(),'Kontakt')]")
        kontakt.click()
        return KontaktPage(self.driver)

    def click_kontakt_amp_anfahrt(self):
        kontakt_amp_anfahrt = self.driver.find_element_by_xpath("//a[contains(text(),'Kontakt & Anfahrt')]")
        kontakt_amp_anfahrt.click()
        return KontaktPage(self.driver)

    def click_karriere(self):
        karriere = self.driver.find_element_by_xpath("//a[contains(text(),'Karriere')]")
        karriere.click()
        return KarrierePage(self.driver)

    def hover_over_portfolio(self):
        portfolio = self.driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]")
        ActionChains(self.driver).move_to_element(portfolio).perform()
        self.portfolio_sub_menu = portfolio.find_element_by_xpath("./following-sibling::ul")
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
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.mobile_section = _MobileSection(self.driver)

    def is_portfolio_item_selected(self):
        portfolio = self.driver.find_element_by_id("menu-item-220")
        return 'current_page_ancestor' in portfolio.get_attribute('class')

    def click_mobile_section_title(self):
        self.mobile_section.title.click()
        self.wait.until(expected_conditions.visibility_of(self.mobile_section.section_body))


class _MobileSection:
    def __init__(self, driver):
        self.driver = driver
        self.title = self.driver.find_element_by_xpath('//div[@id="team-tab-three-title-desktop"]/..')
        self.section_body = self.driver.find_element_by_id('team-tab-three-body')
        self.flyer_download_link = self.section_body.find_element_by_xpath(
            './/a[@download="FLYER FIND THE BUG SESSION"]')

    def is_title_selected(self):
        return 'active-team-tab' in self.title.get_attribute('class') and \
               'inactive-team-tab' not in self.title.get_attribute('class')


class KarrierePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.wait.until(expected_conditions.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "h1.text-padded"),
            'Werde ein QualityMind!'
        ))

    def click_bewirb_dich_jetzt(self):
        jetzt_dich_bewerb = self.driver.find_element_by_xpath('//a[contains(text(), "Bewirb dich jetzt!")]')
        jetzt_dich_bewerb.click()
        return BewerbungsformularPage(self.driver)


class BewerbungsformularPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.submit_button = self.driver.find_element_by_xpath('//input[@value="Jetzt Bewerben"]')
        self.form = self.driver.find_element_by_id('CF5bcf0384b847c_1')
        self.name_field = self.form.find_element_by_id("fld_1144146_1")
        self.surname_field = self.form.find_element_by_id("fld_7067875_1")
        self.email_field = self.form.find_element_by_id("fld_3149235_1")
        self.upload_button = self.form.find_element_by_id("fld_8583967_1")
        self.t_and_c_checkbox = self.form.find_element_by_id("fld_4989725_1_opt1865542")
        self.wait.until(expected_conditions.text_to_be_present_in_element(
            (By.ID, 'job-ad-form-title'),
            'Bewerbungsformular'
        ))

    def upload_file(self, filepath: Path):
        self.upload_button.send_keys(str(filepath))

    def get_uploaded_file_name(self):
        uploaded_file_name = self.driver.find_element_by_class_name('file-name')
        return uploaded_file_name.text
