import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        'download.default_directory': os.getcwd()
    })
    driver = webdriver.Chrome(options=chrome_options)
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
    page_title = driver.find_element_by_class_name('page_title')
    assert page_title.find_element_by_tag_name('span').text == 'Web, Automation & Mobile Testing'
    wait.until(EC.visibility_of(page_title))
    portfolio = driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]/..")
    assert 'current_page_ancestor' in portfolio.get_attribute('class')
    mobile_section_title = driver.find_element_by_xpath("//div[@id='team-tab-three-title-desktop']/..")
    mobile_section_title.click()
    mobile_section = driver.find_element_by_id("team-tab-three-body")
    wait.until(EC.visibility_of(mobile_section))
    assert 'inactive-team-tab' not in mobile_section_title.get_attribute('class')
    assert mobile_section.find_element_by_class_name('sb_mod_acf_single_item').is_displayed()
    assert mobile_section.find_element_by_class_name('tab-download-button').is_displayed()
    flyer_link_ref = 'https://qualityminds.de/app/uploads/2018/11/Find-The-Mobile-Bug-Session.pdf'
    flyer_link = mobile_section.find_element_by_xpath('.//a[contains(@download, "FLYER FIND THE BUG SESSION")]')
    assert flyer_link.get_attribute('href') == flyer_link_ref
    flyer_link.click()
    download_file_path = Path(os.getcwd()) / 'FLYER FIND THE BUG SESSION.pdf'
    while True:  # needs timeout
        if download_file_path.is_file():
            break
    download_file_path.unlink()


def test_career_site(driver, wait):
    driver.find_element_by_xpath("//a[contains(text(),'Karriere')]").click()
    page_title = driver.find_element_by_xpath('//h1[contains(@class, "text-padded")]/span')
    assert page_title.text == 'Werde ein QualityMind!'
    bewirb_dich_jetzt = driver.find_element_by_xpath('//a[contains(text(), "Bewirb dich jetzt!")]')
    bewirb_dich_jetzt.click()
    page_title = driver.find_element_by_id('job-ad-form-title')
    assert page_title.is_displayed()
    submit_button = driver.find_element_by_xpath('//input[contains(@value, "Jetzt Bewerben")]')
    submit_button.click()
    form = driver.find_element_by_class_name('first_row')
    assert len(form.find_elements_by_xpath(".//span[text()='Dies ist ein Pflichtfeld.']")) == 3
    vorname = driver.find_element_by_xpath("//input[contains(@placeholder, 'Vorname')]")
    vorname.send_keys('Franciszek')
    nachname = driver.find_element_by_xpath("//input[contains(@placeholder, 'Nachname')]")
    nachname.send_keys('Podborski')
    submit_button.click()
    email_container = driver.find_element_by_xpath("//label[text()='Email']/..")
    email_validation = email_container.find_element_by_xpath(".//span/span")
    assert email_validation.text == 'Dies ist ein Pflichtfeld.'
    email_filed = email_container.find_element_by_tag_name('input')
    email_filed.send_keys('aaaaaa')
    submit_button.click()
    email_validation = email_container.find_element_by_xpath(".//span/span")
    assert email_validation.text == 'Die Eingabe muss eine gültige E-Mail-Adresse sein.'
    file_name = 'upload.txt'
    upload_file_path = Path(os.getcwd()) / file_name
    with open(upload_file_path, 'w') as upload_file:
        upload_file.write('aaaa')
    upload_button = driver.find_element_by_xpath('//input[contains(@type, "file")]')
    upload_button.send_keys(str(upload_file_path))
    uploaded_file_name = driver.find_element_by_class_name('file-name')
    assert uploaded_file_name.text == file_name
    check_box = driver.find_element_by_xpath("//input[contains(@type, 'checkbox')]")
    check_box.click()
    assert check_box.is_selected()
