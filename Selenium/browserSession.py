import ssl

# Ovo sprečava Python da "pukne" kada naiđe na loš ASN1 format u Windowsu
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from config.parameters import Parameters


class BrowserSession(object):
    obj = Parameters()

    def __init__(self, url):
        self.driverPath = self.obj.driver
        self.url = url
        service = Service(executable_path=self.driverPath)
        self.pageSource = ''
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.set_capability("acceptInsecureCerts", True)

        try:
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f'Error: {e}')
        self.driver.get(self.url)

    def extractRacePageSource(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'trustarc-agree-btn'))).click()
        except:
            pass
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div.rp-horseTable__pedigreesBtn.ui-btn.ui-btn_tiertiary.ui-btn_small'))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rp-raceInfo')))
        self.pageSource = self.driver.page_source
        self.driver.close()

    def extractDatePageSource(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.rp-timeView__list')))
            self.pageSource = self.driver.page_source
        except:
            print(f"{self.url} Don't have races")
        finally:
            self.driver.close()

    def extractRaceCardPageSource(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'trustarc-agree-btn'))).click()
        except:
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             'div.RC-cardTabsZone > span.RC-cardTabsZone__link.ui-btn.ui-btn_tiertiary.RC-cardTabsZone__settingsBtn.js-RC-settingsPopover__openBtn'))).click()
        except:
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label[for='RC-customizeSettings__switcher_owner']"))).click()

        except:
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             'div.ui-btn.ui-btn_secondary.ui-popoverHeader__btn.RC-customizeSettings__popoverBtn.js-RC-customizeSettings__popoverBtn'))).click()
        except:
            pass

        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'body > div.ui-advertising_wrapper > div > div > main > section')))
            self.pageSource = self.driver.page_source
        except:
            print(f"{self.url} Don't have races")
        finally:
            self.driver.close()

    def RCDate(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'trustarc-agree-btn'))).click()
        except:
            pass
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             'body > div.ui-advertising_wrapper > div:nth-child(3) > div > main > div.RC-controlPanel.js-rc-list-type > div.RC-expandCollapseBtn.js-RC-expandCollapseBtn.ui-btn.ui-btn_tiertiary'))).click()
            self.pageSource = self.driver.page_source
        except:
            print(f"{self.url} Don't have races")
        finally:
            self.driver.close()

    def BHAupdate(self):

        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.TAG_NAME, "iframe")
            )
        )

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.caret"))).click()
        except Exception as e:
            print(e)
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             '#wrapper > header > div > nav > ul > li.dropdown.open > ul > li:nth-child(3)'))).click()
        except:
            pass
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             '#wrapper > header > div > nav > ul > li.dropdown.open > ul > li:nth-child(4)'))).click()
        except:
            pass
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                             '#wrapper > header > div > nav > ul > li.dropdown.open > ul > li:nth-child(5)'))).click()
        except:
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.caret"))).click()
        except Exception as e:
            print(e)
            pass
        self.pageSource = self.driver.page_source
        self.driver.close()

    def RPNonRunners(self):
        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.RC-meetingDay')))
            self.pageSource = self.driver.page_source
            self.driver.close()
        except:
            pass
