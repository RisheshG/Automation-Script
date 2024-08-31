from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import StaleElementReferenceException

# Function to initialize the Chrome WebDriver
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start maximized
    driver = webdriver.Chrome(options=options)  # Remove executable_path
    return driver

# Function to log in to Gmail
def login_to_gmail(driver):
    email = "linda.p@runxemaildeliver.com"
    driver.get("https://mail.google.com/")
    time.sleep(2)  # Wait for the page to load
    email_field = driver.find_element(By.ID, "identifierId")
    email_field.send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(3)  # Wait for password field to appear

    # Give the user time to enter their password manually
    print("Please enter your password in the browser. The script will continue after 30 seconds.")
    time.sleep(30)  # Wait for 30 seconds

# Function to read unread emails
def read_unread_emails(driver):
    time.sleep(5)  # Wait for the inbox to load
    unread_emails = driver.find_elements(By.XPATH, '//tr[@class="zA zE"]')
    print(f"Found {len(unread_emails)} unread emails.")

    for _ in range(len(unread_emails)):
        try:
            unread_emails = driver.find_elements(By.XPATH, '//tr[@class="zA zE"]')  # Re-fetch unread emails
            email = unread_emails[0]  # Click the first unread email
            email.click()  # Click on the unread email
            time.sleep(3)  # Wait for the email to open
            
            links = driver.find_elements(By.TAG_NAME, "a")  # Find all links in the email
            for link in links:
                print(f"Link found: {link.get_attribute('href')}")
            
            driver.back()  # Go back to the inbox
            time.sleep(2)  # Wait for the inbox to load again
        except StaleElementReferenceException:
            print("StaleElementReferenceException caught. Re-fetching unread emails.")
            continue  # Continue to the next unread email

# Main function
if __name__ == "__main__":
    driver = initialize_driver()
    login_to_gmail(driver)
    read_unread_emails(driver)
    driver.quit()
