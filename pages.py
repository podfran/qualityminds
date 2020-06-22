class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.kontakt = self.driver.find_element_by_xpath("//a[contains(text(),'Kontakt')]")
        self.karriere = self.driver.find_element_by_xpath("//a[contains(text(),'Portfolio')]")
        self.kontakt_amp_anfahrt = self.driver.find_element_by_xpath("//a[contains(text(),'Kontakt & Anfahrt')]")

    def click_kontakt(self):
        self.kontakt.click()
        return KontaktPage(self.driver)

    def click_kontakt_amp_anfahrt(self):
        self.kontakt_amp_anfahrt.click()
        return KontaktPage(self.driver)


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