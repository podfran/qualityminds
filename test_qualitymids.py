import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get('https://qualityminds.de')
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


def test_contact_email(driver):
    driver.find_element_by_xpath("//a[contains(text(),'Kontakt')]").click()
    wait = WebDriverWait(driver, timeout=10)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Kontakt & Anfahrt')]")))
    assert 'hello@qualityminds.de' in driver.page_source
    kontakt_page_main_content = driver.find_element_by_id('main-content').text
    driver.get('https://qualityminds.de')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Kontakt & Anfahrt')]")))
    kontakt_amp_anfahrt = driver.find_element_by_xpath("//a[contains(text(),'Kontakt & Anfahrt')]")
    kontakt_amp_anfahrt.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Kontakt & Anfahrt')]")))
    assert driver.find_element_by_id('main-content').text == kontakt_page_main_content
