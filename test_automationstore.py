import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSignIn :
    def setup_method(self) :
        self.driver = webdriver.Chrome()
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

class TestFullOrder:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://automationpractice.com/index.php?id_category=3&controller=category')

    def test_add_to_cart(self):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'product-container'))\
            .click(self.driver.find_element(By.XPATH,'//*[@id="center_column"]/ul/li[1]/div/div[2]/div[2]/a[1]')).perform()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="layer_cart"]/div[1]/div[2]/div[4]/a'))).click()
        expectedresult = 'Your shopping cart contains: 1 Product'
        actualresult= self.driver.find_element(By.CLASS_NAME, 'heading-counter').text
        assert expectedresult == actualresult, 'The number of products in Cart does not match'

class TestSearch :
    def setup_method(self) :
        self.driver = webdriver.Chrome()
        self.driver.get('http://automationpractice.com/index.php')

    def test_blank_search(self) :
        searchquery = ''
        self.driver.find_element(By.ID, 'search_query_top').send_keys(f'{searchquery}', Keys.RETURN)
        expectedresult = "Please enter a search keyword"
        actualresult = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='alert alert-warning']"))).text
        assert expectedresult == actualresult, f"Error. Expected text:{expectedresult} but actual text:{actualresult}"

    def test_empty_result_search(self) :
        searchquery = '123'
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

    def teardown_method(self) :
        self.driver.quit()
