from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# create new instance of chrome
browser = webdriver.Chrome(executable_path='/Users/Scity/Desktop/Programming/chromedriver')


# go to website
browser.get("http://www.python.org")
# confrim title has python word
assert "Python" in browser.title
# find element
elem = browser.find_element_by_name("q")
# it is similar to entering keys using keyboard 
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in browser.page_source
browser.close()
