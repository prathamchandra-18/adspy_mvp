from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import json
import time
from bs4 import BeautifulSoup

# Set up WebDriver
driver = webdriver.Chrome(executable_path="C:\\Users\\pathi\\OneDrive\\Desktop\\intern\\chromedriver\\chromedriver.exe")

# Load saved cookies
try:
    with open("facebook_cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        driver.get("https://www.facebook.com")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        print("Cookies loaded successfully!")
except FileNotFoundError:
    print("No cookies found. Please run cookieextracter.py first.")
    driver.quit()
    exit()

# Navigate to Facebook Ads Library (ZARA page)
zara_ads_url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&content_languages[0]=en&country=ALL&is_targeted_country=false&media_type=image&search_type=page&view_all_page_id=33331950906"
driver.get(zara_ads_url)
time.sleep(5)

page_source = driver.page_source

# Close the browser (not needed after getting the source)
driver.quit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Define the class name to search for
target_class = "_7jyg _7jyh"
# Find all elements with the given class
elements = soup.find_all(class_=target_class)




ads_data = []
text_file = open("source.txt", "w")
for element in elements[:min(len(elements),10)]:

    try:
        image_url = element.find_all('img')[1]['src']
    except:
        image_url = "No Image"
    caption = ""
    CallToAction = ""
    

    text_file.write(element.text)
    text_file.write("\n")



    ads_data.append({
        "brand_name": "ZARA",
        "caption": caption,
        "image_url": image_url,
        "CallToAction": CallToAction
    })

text_file.close()



# Save ads data to JSON file
with open("zara_ads.json", "w") as file:
    json.dump(ads_data, file, indent=4)

print("Ads data saved to zara_ads.json!")

# Quit WebDriver
driver.quit()
