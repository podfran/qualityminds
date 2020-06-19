import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get('https://qualityminds.de')
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def wait():
    return WebDriverWait(driver, timeout=10)


def test_contact_email(driver, wait):
    driver.find_element_by_xpath("//a[contains(text(),'Kontakt')]").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Kontakt & Anfahrt')]")))
    assert 'hello@qualityminds.de' in driver.page_source
    kontakt_page_main_content = driver.find_element_by_id('main-content').text
    driver.get('https://qualityminds.de')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Kontakt & Anfahrt')]")))
    kontakt_amp_anfahrt = driver.find_element_by_xpath("//a[contains(text(),'Kontakt & Anfahrt')]")
    kontakt_amp_anfahrt.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Kontakt & Anfahrt')]")))
    assert driver.find_element_by_id('main-content').text == kontakt_page_main_content


def test_portfolio_mobile(driver, wait):
    portfolio = driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]")
    portfolio_hover = ActionChains(driver).move_to_element(portfolio)
    portfolio_hover.perform()
    portfolio_sub_menu = portfolio.find_element_by_xpath("//ul")
    wait.until(EC.visibility_of(portfolio_sub_menu))
    web_automation_amp_mobile_testing = driver.find_element_by_link_text("Web, Automation & Mobile Testing")
    web_automation_amp_mobile_testing.click()
    a = driver.find_element_by_class_name('page_title')
    assert a.find_element_by_tag_name('span').text == 'Web, Automation & Mobile Testing'
    wait.until(EC.visibility_of(a))
    portfolio = driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]/..")
    assert 'current_page_ancestor' in portfolio.get_attribute('class')
    mobile_section_title = driver.find_element_by_xpath("//div[@id='team-tab-three-title-desktop']/..")
    mobile_section_title.click()
    mobile_section = driver.find_element_by_id("team-tab-three-body")
    wait.until(EC.visibility_of(mobile_section))
    assert 'inactive-team-tab' not in mobile_section_title.get_attribute('class')
    assert mobile_section.find_element_by_class_name('sb_mod_acf_single_item').is_displayed()
    assert mobile_section.find_element_by_class_name('tab-download-button').is_displayed()
