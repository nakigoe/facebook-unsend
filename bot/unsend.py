from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge import service
import os
os.system("cls") #clear screen from previous sessions
import time

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
my_service=service.Service(r'msedgedriver.exe')
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_experimental_option("detach", True)
options.add_argument('--no-sandbox')
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.images": 2 # Setting to disable images
})
#options.add_argument('--disable-dev-shm-usage') # uses disk instead of RAM, may be slow, use it if You receive "driver Run out of memory" crashed browser message

s = 20 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»

driver = webdriver.Edge(service=my_service, options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

username = "nakigoetenshi@gmail.com"
password = "Super_Mega_Password"
login_page = "https://www.facebook.com/login"
connections_page = "https://www.facebook.com/friends/requests"

def scroll_to_bottom(): 
    reached_page_end= False
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    #expand the skills list:
    while not reached_page_end:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            reached_page_end = True
        else:
            last_height = new_height
      
def login():
    driver.get(login_page)
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="email"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="pass"]'))).send_keys(password)
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="loginbutton"]')))).perform()
     
def main():
    login()
    time.sleep(10)
    driver.get(connections_page)
    time.sleep(3)
    
    show_page = wait.until(EC.presence_of_element_located((By.XPATH, '//div')))
    action.click(show_page).perform()
    
    show_sent_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(., "View sent requests")]//parent::div')))
    action.move_to_element(show_sent_button).perform()
    action.click(show_sent_button).perform()
    time.sleep(1)
    popup_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(., "Cancel Request") and @role="button"]/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/parent::a/parent::div/parent::div/parent::div/parent::div')))
    while True:
        try:
            unsend_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(., "Cancel Request") and @role="button"]')))
            action.move_to_element(unsend_button).perform()
            action.click(unsend_button).perform()
            
            driver.execute_script("arguments[0].scrollBy(0, 200)", popup_div)

        except:
            break
            
    os.system("cls") #clear screen from unnecessary logs since the operation has completed successfully
    print("All Your requests are unsent! \n \nSincerely Yours, \nNAKIGOE.ORG\n")
    driver.close()
    driver.quit()
main()
