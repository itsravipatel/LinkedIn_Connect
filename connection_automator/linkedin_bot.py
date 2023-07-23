import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import consts as c

class LinkedinBot():
    def __init__(self):
        self.user = c.USERNAME
        self.password = c.PASSWORD
        self.num_requests = c.NUM_REQUESTS
        self.min_connections = c.MINIMUM_CONNECTION_COUNT
        self.excel = c.EXCEL_INPUT_LOCATION
        self.message = c.MESSAGE
        options = Options()
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/114.0.5735.133 Safari/537.36")
        
        options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome('./chromedriver', options=options)
    
    def login(self):
        # Enter username and password into fields
        self.driver.get("https://linkedin.com/login")
        username_field = self.driver.find_element("id", "username")
        username_field.send_keys(self.user)
        password_field = self.driver.find_element("id", "password")
        password_field.send_keys(self.password)

        # Randomize wait to avoid being flagged
        time.sleep(random.uniform(3,5))

        # Submit
        password_field.send_keys(Keys.ENTER)

        # Check success
        time.sleep(random.uniform(3,5))
        if self.driver.current_url == "https://www.linkedin.com/feed/":
            return True
        else:
            time.sleep(30)
        return False

    def send_connection_request(self, message):
        try:
            connect_button = self.driver.find_element("xpath", 
                ( "(//button[contains(@aria-label,"
                " 'Invite') and contains(@class, "
                "'pvs-profile-actions__action')])"))
            connect_button.click()
            time.sleep(random.uniform(3,5))

            add_note_button = self.driver.find_element("xpath", 
                                        "//button[@aria-label='Add a note']")
            add_note_button.click()
            time.sleep(random.uniform(3,5))

            message_entry = self.driver.find_element("xpath", 
                                        "//textarea[@name='message']")
            message_entry.send_keys(message)
            time.sleep(random.uniform(3,5))

            send_button = self.driver.find_element("xpath", 
                                    "//button[@aria-label='Send now']")
            send_button.click()
            time.sleep(random.uniform(3,5))

            self.driver.find_element('xpath', 
                ("//button[contains(@aria-label, 'Pending') and contains(@class,"
                 " 'pvs-profile-actions__action') and .//span[contains(@class, "
                 "'artdeco-button__text') and text()='Pending']]"))
            return True
        
        except NoSuchElementException:
            return False
        
    def more_then_connect(self, message):
        try:
            more_button = self.driver.find_element("xpath", 
                ("(//button[contains(@class, 'artdeco-dropdown__trigger') "
                 "and contains(@class, 'artdeco-dropdown__trigger--placement-"
                 "bottom') and contains(@class, 'ember-view') and contains(@class,"
                 " 'pvs-profile-actions__action') and contains(@class, "
                 "'artdeco-button') and contains(@class, "
                 "'artdeco-button--secondary') and contains(@class, "
                 "'artdeco-button--muted') and contains(@class,"
                 " 'artdeco-button--2') and @aria-label='More actions'])[2]"))
            more_button.click()
            self.driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(random.uniform(3,5))

            connect_button = self.driver.find_element("xpath", 
                    ("(//div[contains(@aria-label, 'Invite') and "
                     "contains(@aria-label, 'to connect')])"))
            self.driver.execute_script("arguments[0].click();", connect_button)
            time.sleep(random.uniform(3,5))

            add_note_button = self.driver.find_element("xpath", 
                "//button[@aria-label='Add a note']")
            add_note_button.click()
            time.sleep(random.uniform(3,5))

            message_entry = self.driver.find_element("xpath", 
                "//textarea[@name='message']")
            message_entry.send_keys(message)
            time.sleep(random.uniform(3,5))

            send_button = self.driver.find_element("xpath", 
                "//button[@aria-label='Send now']")
            send_button.click()
            time.sleep(random.uniform(3,5))

            self.driver.find_element('xpath', 
                ("//div[contains(@aria-label, 'Pending') and "
                 "contains(@class, 'artdeco-dropdown__item')]"))
            return True
        
        except WebDriverException:
            return False
        
    def accept_request(self):
        try:
            accept_button = self.driver.find_element("xpath", 
                ("//button[contains(@aria-label, 'Accept') and "
                 "contains(@class, 'pvs-profile-actions__action')]"))
            accept_button.click()
            time.sleep(random.uniform(3,5))

            self.driver.find_element("xpath", 
                ("//button[contains(@aria-label, 'Message') and "
                 "contains(@class, 'artdeco-button--primary')]"))
            return True
        
        except NoSuchElementException:
            return False
        
    def extract_connection_count(self):
        time.sleep(random.uniform(3,5))
        try:
            connection_count = self.driver.find_element("xpath",
                '(//span[@class="t-bold"])[1]')
            number = connection_count.text.replace(",", "")
            if number.isnumeric():
                return int(number)
            elif connection_count.text == "500+":
                return 500
            else:
                return 0
        except NoSuchElementException:
            return 0

    def has_connect_button(self):
        try:
            connect = self.driver.find_element("xpath", 
                "(//span[@class='artdeco-button__text'])[6]")
            connect_following = self.driver.find_element("xpath", 
                "(//span[@class='artdeco-button__text'])[8]")
            if connect.text == "Connect" or connect_following.text=="Connect":
                return True
            else:
                return False
        except NoSuchElementException:
            return False
        
    def has_accept_button(self):
        try:
            accept = self.driver.find_element("xpath", 
                "(//span[@class='artdeco-button__text'])[6]")
            if accept.text == "Accept":
                return True
            else:
                return False
        except NoSuchElementException:
            return False
    
    def has_hidden_connect_button(self):
        try:
            self.driver.find_element("xpath", 
                ("(//div[contains(@class, 'artdeco-dropdown__item') and "
                 "contains(@class, 'artdeco-dropdown__item--is-dropdown')"
                 " and contains(@class, 'ember-view') and contains(@class,"
                 " 'full-width') and contains(@class, 'display-flex') and"
                 " contains(@class, 'align-items-center')]/"
                 "span[text()='Connect'])[1]"))
            return True
        except NoSuchElementException:
            return False
    
    def write_message(self):
        full_name = self.driver.find_element("xpath", 
            ('(//h1[@class="text-heading-xlarge inline t-24'
             ' v-align-middle break-words"])[1]')).text
        name_list = full_name.split(" ")
        first = name_list[0]
        if first.lower() not in ['dr.', 'mr.' 'mrs.', 
                                 'ms.', 'dr', 'mr', 'mrs' 'ms']:
            first_name = name_list[0]
        else: 
            first_name = name_list[1]

        msg = c.MESSAGE.replace('[FULL NAME]', full_name)
        msg =msg.replace('[FIRST NAME]', first_name)
        return msg
        
    def check_weekly_limit(self):
        try:
            self.driver.find_element("xpath", 
                ("//h2[@class='ip-fuse-limit-alert__header t-20 t-black ph4' "
                 "and @id='ip-fuse-limit-alert__header' and text()='You’ve "
                 "reached the weekly invitation limit']"))
            return True
        except NoSuchElementException:
            return False
        