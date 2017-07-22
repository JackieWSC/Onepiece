from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# create new instance of chrome
browser = webdriver.Chrome(executable_path='/Users/Scity/Desktop/Programming/chromedriver')


# go to website
browser.get("http://www.nike.com.hk")
# find the login btn
elem = browser.find_element_by_class_name("login-text")
links = elem.find_elements_by_tag_name("a")

# log
for link in links:
    print link.get_attribute("href"), link.get_attribute("onclick")

links[1].get_attribute("onclick")

# click the login btn
links[1].click()

# login page
login = browser.find_element_by_id("dialogLoginName")
login.clear()
login.send_keys("window6132003@yahoo.com.hk")

password = browser.find_element_by_id("dialogPassword")
password = browser.find_element_by_id("dialogAgain")
password.send_keys("Window12337!")

check = browser.find_element_by_id("dialogCheck")
check.send_keys("C68W")

login = browser.find_element_by_id("dialogLogin")
login.click()

# use WebDriverWait
# wait = WebDriverWait(browser, 10)
# user = wait.until(EC.visibility_of_element_located((By.NAME, "session[username_or_email]")))
# user.clear()
# user.send_keys(username)

# password = wait.until(EC.visibility_of_element_located((By.ID, "dialogPassword")))
# password.clear()
# password.send_keys(password)


