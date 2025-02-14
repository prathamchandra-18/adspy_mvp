from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle

# Set up WebDriver
driver = webdriver.Chrome(executable_path="C:\\Users\\pathi\\OneDrive\\Desktop\\intern\\chromedriver\\chromedriver.exe")
driver.get("https://www.facebook.com")
time.sleep(2)

# Enter login credentials (replace with your credentials)
email = driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "pass")

email.send_keys("your_email@example.com")
password.send_keys("your_password")
password.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(5)

# Save cookies to a file
cookies = driver.get_cookies()
with open("facebook_cookies.pkl", "wb") as file:
    pickle.dump(cookies, file)

print("Cookies saved successfully!")

# Quit WebDriver
driver.quit()
