from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import json
import time
from bs4 import BeautifulSoup
import openai
import json




def parse_and_validate_json(text):
    try:
        # Try parsing the text into JSON
        data = json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

    # Ensure both keys exist and are strings
    expected_keys = ["caption", "CTA"]
    
    for key in expected_keys:
        if key not in data:
            return {"error": f"Missing key: {key}"}
        
        if not isinstance(data[key], str):
            return {"error": f"Invalid type for {key}, expected a string"}

    return {"success": "Valid JSON", "parsed_data": data}


def get_brand_data(brand, brand_url):


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



    openai.api_key = "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"




    driver.get(brand_url)
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
    for element in elements:

        try:
            image_url = element.find_all('img')[1]['src']
        except:
            image_url = "No Image"


        try:
            video_url = element.find('video')['src']
        except:
            video_url = "No Video"

        user_prompt = element.text + "    This is text extracted from the source code of a meta ad. Find the caption and Call-To-Action which are present inside this text. Return the pair as a JSON with keys 1. caption 2. CTA . Don't return anything except the json parsable text."

        response1 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"user","content": user_prompt}
            ],
            temperature=0
        )
        raw_text1 = response1.choices[0].message["content"]
        gpt_out = parse_and_validate_json(raw_text1)
        if 'success' not in gpt_out.keys():
            continue


        caption = gpt_out['parsed_data']['caption']
        CallToAction = gpt_out['parsed_data']['CTA']


        ads_data.append({
            "brand_name": brand,
            "caption": caption,
            "image_url": image_url,
            "video_url": video_url,
            "CallToAction": CallToAction
        })



    outfile = brand+"_ads.json"
    # Save ads data to JSON file
    with open(outfile, "w") as file:
        json.dump(ads_data, file, indent=4)

    print("Ads data saved to "+outfile)


    # Quit WebDriver
    driver.quit()

brand_data = {
    "ZARA" : "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&content_languages[0]=en&country=ALL&is_targeted_country=false&media_type=video&search_type=page&view_all_page_id=33331950906",
    "H&M" : "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=348767591942030",
    "LV" : "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=215138065124",
      "Gucci": "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=44596321012"
}


for key, value in brand_data.items():

    get_brand_data(key,value)