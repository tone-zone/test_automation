import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.mark.signin
class TestSignIn :
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('http://automationpractice.com/index.php')
        self.driver.find_element(By.XPATH, '//a[@class="login"]').click()
        self.driver.find_element(By.ID, 'email').send_keys('dpzxgplnwruquftlpn@mhzayt.online')
        self.driver.find_element(By.ID, 'passwd').send_keys('qwerty', Keys.RETURN)

    def test_signin(self) :
        assert WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'account'))).text \
               == 'test one', "cannot find the username, verify credentials"

    def test_signout(self) :
        self.driver.find_element_by_xpath('//a[@class="logout"]').click()
        assert self.driver.find_element(By.XPATH, '//a[@class="login"]').text == \
               'Sign in', "cannot find the sign in button, still logged in"

    def teardown_method(self) :
        self.driver.quit()


class TestFullOrder :
    def setup_method(self) :
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('http://automationpractice.com/index.php?id_category=3&controller=category')

    def test_pay_by_check(self) :
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'product-container')) \
            .click(
            self.driver.find_element(By.XPATH, '//*[@id="center_column"]/ul/li[1]/div/div[2]/div[2]/a[1]')).perform()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="layer_cart"]/div[1]/div[2]/div[4]/a'))).click()
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "standard-checkout"))).click()
        self.driver.find_element(By.ID, 'email').send_keys('dpzxgplnwruquftlpn@mhzayt.online')
        self.driver.find_element(By.ID, 'passwd').send_keys('qwerty', Keys.RETURN)
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='center_column']/form/p/button"))).click()
        self.driver.find_element(By.CLASS_NAME, 'checker').click()
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "standard-checkout"))).click()
        self.driver.find_element(By.CLASS_NAME, 'cheque').click()
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='cart_navigation']/button"))).click()
        expectedresult = 'Your order on My Store is complete.'
        actualresult = self.driver.find_element(By.CLASS_NAME, 'alert-success').text
        assert expectedresult == actualresult, 'The order did not go through'

    def teardown_method(self) :
        self.driver.quit()

@pytest.mark.search
class TestSearch :
    def setup_method(self) :
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('http://automationpractice.com/index.php')
        assert self.driver.title == 'My Store'

    def test_blank_search(self) :
        searchquery = ''
        self.driver.find_element(By.ID, 'search_query_top').send_keys(f'{searchquery}', Keys.RETURN)
        expectedresult = "Please enter a search keyword"
        actualresult = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='alert alert-warning']"))).text
        assert expectedresult == actualresult, f"Error. Expected text:{expectedresult} but actual text:{actualresult}"

    def test_empty_result_search(self) :
        searchquery = 'se'
        self.driver.find_element(By.ID, 'search_query_top').send_keys(f'{searchquery}', Keys.RETURN)
        expectedresult = f'No results were found for your search \"{searchquery}\"'
        actualresult = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='alert alert-warning']"))).text
        assert expectedresult == actualresult, f"Error. Expected text:{expectedresult} but actual text:{actualresult}"

    def test_correct_search(self) :
        searchquery = 'dress'
        self.driver.find_element(By.ID, 'search_query_top').send_keys(f'{searchquery}', Keys.RETURN)
        expectedresult = f'\"{searchquery}\"'.lower()
        actualresult = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='lighter']"))).text.lower()
        assert expectedresult == actualresult, f"Error. Expected text:{expectedresult} but actual text:{actualresult}"

    def test_fail(self):
        assert False

    def teardown_method(self) :
        self.driver.quit()