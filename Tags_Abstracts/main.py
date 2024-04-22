from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get(
    "https://web-p-ebscohost-com.ezproxy.lib.utexas.edu/ehost/detail/detail?vid=0&sid=d14c0b69-5c75-4b08-bb8a-97b6d7e443f7%40redis&bdata=JnNpdGU9ZWhvc3QtbGl2ZQ%3d%3d#AN=1979304924&db=mzh")

driver.implicitly_wait(2)
user_box = driver.find_element(by=By.ID, value="username")
pass_box = driver.find_element(by=By.ID, value="password")
user_box.send_keys('vaa678')
pass_box.send_keys('CSbw$y5upL8n*7Y')
driver.implicitly_wait(10)
login = driver.find_element(by=By.NAME, value='_eventId_proceed')
login.click()