import contextlib
import os
from pathlib import Path

import pytest
from selenium import webdriver

from file_utils import is_file_downloaded
from pages import MainPage

BROWSERS = ['chrome', 'firefox']


@pytest.fixture
def available_browsers():
    def chrome():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {'download.default_directory': os.getcwd()})
        return webdriver.Chrome(options=options)

    def firefox():
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", os.getcwd())
        profile.set_preference("browser.download.useDownloadDir", True)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        profile.set_preference("pdfjs.disabled", True)
        return webdriver.Firefox(firefox_profile=profile)

    return {
        'chrome': chrome,
        'firefox': firefox
    }


@pytest.fixture
@pytest.mark.parametrize('browser', BROWSERS)
def driver(available_browsers, browser):
    driver = available_browsers[browser]()
    driver.get('https://qualityminds.de')
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


@pytest.fixture
@pytest.mark.parametrize('browser', BROWSERS)
def download_file_path(browser):
    file_name = 'FLYER FIND THE BUG SESSION'
    if browser == 'chrome':
        file_name += '.pdf'
    download_file_path = Path(os.getcwd()) / file_name
    yield download_file_path
    with contextlib.suppress(FileNotFoundError):
        download_file_path.unlink()


@pytest.fixture
def upload_file_path():
    file_name = 'upload.txt'
    upload_file_path = Path(os.getcwd()) / file_name
    with open(upload_file_path, 'w') as upload_file:
        upload_file.write('aaaa')
    yield upload_file_path
    upload_file_path.unlink()


@pytest.mark.parametrize('browser', BROWSERS)
def test_contact_email(main_page, browser):
    kontakt_page = main_page.click_kontakt()
    assert 'hello@qualityminds.de' in kontakt_page
    main_page = kontakt_page.return_to_main_page()
    kontakt_amp_anfahrt_page = main_page.click_kontakt_amp_anfahrt()
    assert kontakt_amp_anfahrt_page == kontakt_page


@pytest.mark.parametrize('browser', BROWSERS)
def test_portfolio_mobile(main_page, download_file_path, browser):
    main_page.hover_over_portfolio()
    assert main_page.portfolio_sub_menu.is_displayed()
    wam_testing_page = main_page.click_web_automation_amp_mobile_testing()
    assert wam_testing_page.is_portfolio_item_selected()
    wam_testing_page.click_mobile_section_title()
    assert wam_testing_page.mobile_section.section_body.is_displayed()
    assert wam_testing_page.mobile_section.is_title_selected()
    assert wam_testing_page.mobile_section.flyer_download_link.is_displayed()
    assert wam_testing_page.mobile_section.flyer_download_link.get_attribute('href') == \
           'https://qualityminds.de/app/uploads/2018/11/Find-The-Mobile-Bug-Session.pdf'
    wam_testing_page.mobile_section.flyer_download_link.click()
    assert is_file_downloaded(download_file_path)


@pytest.mark.parametrize('browser', BROWSERS)
def test_career_site(main_page, upload_file_path, browser):
    karriere_page = main_page.click_karriere()
    bewerbungsformular_page = karriere_page.click_bewirb_dich_jetzt()
    bewerbungsformular_page.click_submit()
    assert len(bewerbungsformular_page.form.find_elements_by_xpath(
        ".//div[contains(@class, 'first_col')]//span[text()='Dies ist ein Pflichtfeld.']")) == 3
    bewerbungsformular_page.input_name('Franciszek')
    bewerbungsformular_page.input_surname('Podborski')
    bewerbungsformular_page.click_submit()
    assert len(bewerbungsformular_page.form.find_elements_by_xpath(
        ".//div[contains(@class, 'first_col')]//span[text()='Dies ist ein Pflichtfeld.']")) == 1
    assert bewerbungsformular_page.get_error_text_for_email() == 'Dies ist ein Pflichtfeld.'
    bewerbungsformular_page.input_email_address('aaaaaa')
    bewerbungsformular_page.click_submit()
    assert bewerbungsformular_page.get_error_text_for_email() == 'Die Eingabe muss eine gültige E-Mail-Adresse sein.'
    bewerbungsformular_page.upload_file(upload_file_path)
    assert bewerbungsformular_page.get_uploaded_file_name() == upload_file_path.name
    bewerbungsformular_page.t_and_c_checkbox.click()
    assert bewerbungsformular_page.t_and_c_checkbox.is_selected()
