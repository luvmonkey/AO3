from itertools import count
from selenium import webdriver
#For controlling browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.support.ui import WebDriverWait

# required for headless
from selenium.webdriver.safari.options import Options
import csv
import pandas as pd

# New paradigm for path
from selenium.webdriver.safari.service import Service
from selenium.common.exceptions import NoSuchElementException

#Sets my safari driver
safari_service = Service('/usr/bin/safaridriver')

# If headless if True, you don't see the window pop up
safari_options = Options()
safari_options.headless = True

#initializing driver with the above options
driver = webdriver.Safari(service=safari_service, options=safari_options)




def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def initialize_browser(website):
    # Getting past the terms of service pop-up to content on first page
    driver.get(website)
    time.sleep(3)
    driver.find_element(By.XPATH, "//*[@id='tos_agree']").click()
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH, "//*[@id='accept_tos']").click()
    driver.implicitly_wait(10)

def create_work_dictionary(counter, page):
    # Creating a dictionary to hold all the elements of one work
    work_dictionary = {}

    work_id = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]")).get_attribute('id')
    work_dictionary["work_id"] = work_id

    user_id_raw = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]")).get_attribute('class')
    user_id = user_id_raw.split()[-1]
    work_dictionary["user_id"] = user_id

    title_of_work = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/h4/a[1]")).text
    work_dictionary["title"] = title_of_work

    username_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/div/h4/a[2]")
    if (username_present == True):
        username = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/h4/a[2]")).text
    else:
        username = 'Anonymous'
    work_dictionary["username"] = username

    fandoms = []
    fandom = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/h5")).text
    fandom = fandom.split("\n")
    fandom = fandom[2].strip()
    fandom = fandom.split(",")
    for i in range(len(fandom)):
        fandoms.append(fandom[i].strip())
    work_dictionary["fandoms"] = fandoms

    rating = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/ul/li[1]/a/span")).get_attribute('title')
    work_dictionary["rating"] = rating

    warnings = []
    warning = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/ul/li[2]/a/span")).get_attribute('title')
    warning = warning.split(",")
    for i in range(len(warning)):
        warnings.append(warning[i].strip())
    work_dictionary["warnings"] = warnings

    slash_categories = []
    slash_category = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/ul/li[3]/a/span")).get_attribute('title')
    slash_category = slash_category.split(",")
    for i in range(len(slash_category)):
        slash_categories.append(slash_category[i].strip())
    work_dictionary["slash_categories"] = slash_categories    

    status = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/ul/li[4]/a/span")).get_attribute('title')
    work_dictionary["status"] = status

    date_updated = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/div/p")).text
    work_dictionary["date_updated"] = date_updated

    relationships = []
    relationships_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/ul/li[@class='relationships']")
    if (relationships_present == True):
        for elm in driver.find_elements(By.XPATH, ("//ol/li[" + str(counter) + "]/ul/li[@class='relationships']")):
            relationships.append(elm.text)
        # print(counter, " - relationship found")
    else:
        relationships.append('No Relationship Tags')
        # print(counter, " - no relationship found")
    work_dictionary["relationships"] = relationships

    characters = []
    characters_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/ul/li[@class='characters']")
    if (characters_present == True):
        for elm in driver.find_elements(By.XPATH, ("//ol/li[" + str(counter) + "]/ul/li[@class='characters']")):
            characters.append(elm.text)
    else:
        characters.append('No Character Tags')
    work_dictionary["characters"] = characters

    freeforms = []
    freeforms_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/ul/li[@class='freeforms']")
    if (freeforms_present == True):
        for elm in driver.find_elements(By.XPATH, ("//ol/li[" + str(counter) + "]/ul/li[@class='freeforms']")):
            # print("Appending: " + elm.text)
            freeforms.append(elm.text)
    else:
        print("Nothing to append")
        freeforms.append('No Freeform Tags')
    work_dictionary["freeforms"] = freeforms

    summary_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/dl/dd[@class='blockquote']")
    if (summary_present == True):
        summary = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[@class='blockquote']")).text
    else:
        summary = 'No summary'
    work_dictionary["summary"] = summary

    language = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[1]")).text
    work_dictionary["language"] = language

    words = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[2]")).text
    work_dictionary["words"] = int(words.replace(",", ""))

    chapters = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[3]")).text
    work_dictionary["chapters"] = chapters

    comments_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/dl/dd[@class='comments']")
    if (comments_present == True):
        comments = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[@class='comments']")).text
        # print(counter, " - comments present")
    else:
        comments = '0'
        # print(counter, " - no comments present")
    work_dictionary["comments"] = int(comments.replace(",", ""))

    kudos_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/dl/dd[@class='kudos']")
    if (kudos_present == True):
        kudos = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[@class='kudos']")).text
    else:
        kudos = '0'
    work_dictionary["kudos"] = int(kudos.replace(",", ""))

    bookmarks_present = check_exists_by_xpath("//ol/li[" + str(counter) + "]/dl/dd[@class='bookmarks']")
    if (bookmarks_present == True):
        bookmarks = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[@class='bookmarks']")).text
    else:
        bookmarks = '0'
    work_dictionary["bookmarks"] = int(bookmarks.replace(",", ""))

    hits = driver.find_element(By.XPATH, ("//ol/li[" + str(counter) + "]/dl/dd[@class='hits']")).text
    work_dictionary["hits"] = int(hits.replace(",", ""))

    # Then add that work to the real dictionary.
    full_dictionary.append(work_dictionary)

    #record the count in case of error
    print('Page', page, 'article', counter, "is done.")


#This will count to 20 to build all the entries for one page
def page_dictionary_builder(page):
    for counter in range(1,21):
        create_work_dictionary(counter, page)

# Advance to the next page
def click_next_page():
    driver.find_element(By.XPATH, "//*[@id='main']/ol[2]/li[contains(@class, 'next')]/a").click()
    time.sleep(2)

full_dictionary = []

# Saves data as a csv file
def save_dictionary(file_name):
    col_name = full_dictionary[0].keys()
    with open(file_name, 'w') as ao3_top_100_kudos:
        wr = csv.DictWriter(ao3_top_100_kudos, fieldnames=col_name)
        wr.writeheader()
        for ele in full_dictionary:
            wr.writerow(ele)


# Brings all the code together and scrapes the data for given pages.
def scrape_pages(start, end):
    stop = end + 1
    website = ('https://archiveofourown.org/works/search?commit=Search&page=' + str(start) + '&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5Bcomments_count%5D=&work_search%5Bcomplete%5D=&work_search%5Bcreators%5D=&work_search%5Bcrossover%5D=&work_search%5Bfandom_names%5D=Harry+Potter+-+J.+K.+Rowling&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Blanguage_id%5D=&work_search%5Bquery%5D=&work_search%5Brating_ids%5D=&work_search%5Brelationship_names%5D=&work_search%5Brevised_at%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&work_search%5Btitle%5D=&work_search%5Bword_count%5D=')
    file = ("harry_potter_fics_by_kudos_pg" + str(start) + "_to_" + str(end) + ".csv")
    print('Starting Driver')
    initialize_browser(website)
    print('Got in to page ' + str(start) + "!")
    for page in range(start, stop):
        print(page)
        page_dictionary_builder(page)
        print('Page', page, 'Done')
        click_next_page()
    save_dictionary(file)
    print('Dictionary Saved')
    driver.quit()


# Execute
scrape_pages(21, 25)



