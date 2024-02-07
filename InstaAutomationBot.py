import os
import pickle
import random
import re
import threading
import time
import tkinter as tkr
from tkinter import filedialog
from tkinter import messagebox, END
from tkinter.ttk import *

import pyperclip
from PIL import ImageTk, Image
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError, ReadTimeout
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
# from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.exceptions import MaxRetryError, NewConnectionError
from webdriver_manager.chrome import ChromeDriverManager
import os

instagram_automation_bot = None

os.system('python3 -m pip install webdriver-manager --upgrade')

def create_selenium_webdriver(username_):
    print("Creating Chrome Driver...")
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-hang-monitor")
    chrome_options.add_argument("--disable-prompt-on-repost")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument('--disable-logging')

    # creating Chrome web driver object
    driver = webdriver.Chrome("C:\\Users\\Colby\\Download\\chromedriver.exe")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    print("Chrome Driver created.")

    # load the saved cookies if any
    cookies_file = os.path.join(os.getcwd(), 'cookies', username_ + "_cookies.pkl")
    if os.path.exists(cookies_file):
        driver.get("https://www.instagram.com/")
        try:
            # wait the ready state to be complete
            WebDriverWait(driver=driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            pass

        time.sleep(random.randint(1, 2))
        # delete the current cookies
        driver.delete_all_cookies()
        time.sleep(random.randint(1, 2))

        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        time.sleep(random.randint(2, 5))

        print("Cookies loaded.")
        driver.get("https://www.instagram.com/")

        try:
            # wait the ready state to be complete
            WebDriverWait(driver=driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            pass

        time.sleep(random.randint(2, 5))

    return driver


class InstagramAutomationBot:
    def __init__(self, username, password, mail_username, mail_password, use_proxy=False, proxy_address=None, proxy_port=None):
        self.username = username
        self.password = password
        self.mail_username = mail_username
        self.mail_password = mail_password
        self.instagram_url = "https://www.instagram.com/accounts/login/?"
        self.instagram_home_url = "https://www.instagram.com/"
        self.driver = create_selenium_webdriver(self.username)

    def login(self):
        # check if the user is already logged in using cookies or not
        # check if login is successful
        try:
            # check for the home button to be visible to confirm login
            WebDriverWait(driver=self.driver, timeout=random.randint(5, 10)).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Home']"))
            )
            print("Instagram login successful using cookies.")
            return True, "Instagram login successful using cookies."
        except TimeoutException:
            print("Instagram login failed using cookies.")
            print("Logging in using username and password...")

        print("Opening Instagram login page...")
        # open instagram
        try:
            self.driver.get(self.instagram_url)
        except (ConnectionError, MaxRetryError, NewConnectionError, SSLError, ReadTimeout) as e:
            print("Connection Error: ", e)
            return False, "Connection Error"

        try:
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            print("TimeoutException: Page load timeout")
            return False, "TimeoutException: Page load timeout"

        # login to instagram
        try:
            WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='username']"))
            )
        except TimeoutException:
            print("TimeoutException: Login failed.")
            tkr.messagebox.showerror("Error", "Login failed. Please try again.")
            return False, "TimeoutException: Login failed."

        # send username with delay
        for char in self.username:
            self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys(char)
            time.sleep(random.uniform(0.4, 0.8))

        time.sleep(random.randint(1, 2))

        # send password with delay
        for char in self.password:
            self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(char)
            time.sleep(random.uniform(0.4, 0.8))

        time.sleep(random.randint(1, 2))

        # click login button
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(random.randint(4, 5))

        try:
            WebDriverWait(driver=self.driver, timeout=random.randint(4, 6)).until(
                EC.visibility_of_element_located((By.XPATH, "//p[@data-testid='login-error-message']"))
            )

            error_message = self.driver.find_element(By.XPATH, "//p[@data-testid='login-error-message']").text

            if error_message.lower().__contains__("There was a problem logging you into Instagram.".lower()):
                print("There was a problem logging you into Instagram. Please try again soon.")
                tkr.messagebox.showerror("Error",
                                         "There was a problem logging you into Instagram. Please try again soon.")
                return False, "Problem in logging into Instagram. PTA!"
            elif error_message.lower().__contains__("Sorry, your password was incorrect.".lower()):
                print("Sorry, your password was incorrect. Please double-check your password.")
                tkr.messagebox.showerror("Error",
                                         "Sorry, your password was incorrect. Please double-check your password.")
                return False, "Sorry, your password was incorrect."
            elif error_message.lower().__contains__("The username you entered doesn't belong to an account.".lower()):
                print("The username you entered doesn't belong to an account. "
                      "Please check your username and try again.")
                tkr.messagebox.showerror("Error",
                                         "The username you entered doesn't belong to an account. "
                                         "Please check your username and try again.")
                return False, "Sorry, your username was incorrect."
            else:
                print("Login failed.")
                tkr.messagebox.showerror("Error", "Login failed. Please try again.")
                return False, "Login failed. PTA!"
        except TimeoutException:
            pass

        try:
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            print("TimeoutException: Page load timeout")
            return False, "TimeoutException: Page load timeout"

        time.sleep(random.randint(2, 4))

        # checking for the unusual login activity popup
        try:
            self.driver.find_element(By.XPATH, "//h2[contains(text(), 'We Detected An Unusual Login Attempt')]")

            # click on ok button of tkinter message box to continue the process of login to instagram account
            resp = tkr.messagebox.askokcancel("Unusual Login Attempt",
                                              "There is security barrier by Instagram Authorities.\n"
                                              "From here you have to manually verify your login by receiving "
                                              "code on your mobile or email.\n"
                                              "After receiving the code, and approval, you can continue the process.\n"
                                              "Do you want to continue?")
            if resp:
                time.sleep(random.randint(2, 4))
                try:
                    # wait the ready state to be complete
                    WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                        lambda x: x.execute_script("return document.readyState === 'complete'")
                    )
                except TimeoutException:
                    print("TimeoutException: Page load timeout")
                    return False, "TimeoutException: Page load timeout"
            else:
                return False, "Unusual Login Attempt! Need User Attention!"
        except NoSuchElementException:
            pass

        # click not now button for the save login info popup.
        print("Checking for the save login info popup.")
        try:
            WebDriverWait(driver=self.driver, timeout=random.randint(2, 5)).until(
                EC.visibility_of_element_located((By.XPATH, "//button[text()='Not Now']"))
            )
            self.driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
            time.sleep(random.randint(1, 2))
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            print("TimeoutException: Save login info popup not found.")

        # click not now button for the turn on notifications popup.
        print("Checking for the turn on notifications popup.")
        try:
            WebDriverWait(driver=self.driver, timeout=random.randint(2, 4)).until(
                EC.visibility_of_element_located((By.XPATH, "//button[text()='Not Now']"))
            )
            self.driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
            time.sleep(random.randint(1, 2))
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            print("TimeoutException: Turn on notifications popup not found.")

        try:
            self.driver.find_element(By.XPATH, '//span[@aria-label="Dismiss"]').click()
            time.sleep(0.5)
        except NoSuchElementException:
            print("No dismiss button found.")

        # check if login is successful
        try:
            # check for the home button to be visible to confirm login
            WebDriverWait(driver=self.driver, timeout=random.randint(45, 60)).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Home']"))
            )
            print("Login successful.")
        except TimeoutException:
            print("TimeoutException: Login failed.")
            tkr.messagebox.showerror("Error", "Login failed. Please try again.")
            return False, "Login failed. PTA!"

        print("Login successful.")

        # save session cookies to file for future use of the same session to avoid login again and again
        cookies_name = self.username + "_cookies.pkl"
        if not os.path.exists(os.path.join(os.getcwd(), 'cookies', cookies_name)):
            # with open(cookies_name, 'wb') as filehandler:
            #     pickle.dump(self.driver.get_cookies(), filehandler)
            pickle.dump(self.driver.get_cookies(), open(os.path.join(os.getcwd(), 'cookies', cookies_name), "wb"))
            print("Session cookies saved in 'cookies' folder to file: " + cookies_name)

        # return True if login is successful
        return True, "Login successful."

    def do_comment_on_users_posts(self, post_, comment_):
        try:
            self.driver.get(post_)
        except TimeoutException:
            print("Page load timeout for post: {}".format(post_))
            return False, "Page load timeout for post"

        time.sleep(random.randint(3, 5))

        try:
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=random.randint(30, 45)).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
        except TimeoutException:
            print("Page load timeout for post: {}".format(post_))
            return False, "Page load timeout for post"

        # select the comment button
        try:
            try:
                WebDriverWait(driver=self.driver, timeout=random.randint(4, 8)).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Add a comment…']"))
                )
            except TimeoutException:
                print("No comment button found for post: {}".format(post_))
                return False, "No comment button found for post"

            try:
                comment_text_area = self.driver.find_element(By.XPATH, "//form[@method='POST']/textarea")
            except:
                print("[Exception-5]: Comment Text Area Clicking for post: {}".format(post_))
                return False, "[Exception-5]: Comment Text Area Clicking for post"

            # copy the comment text to clipboard
            pyperclip.copy(comment_)
            time.sleep(0.5)

            # type the . to trigger the comment button
            ActionChains(self.driver).move_to_element(comment_text_area).perform()
            time.sleep(0.5)
            ActionChains(self.driver).click(comment_text_area).perform()
            time.sleep(0.5)

            # paste the comment text from clipboard
            try:
                comment_text_area.send_keys(Keys.CONTROL, 'v')
                time.sleep(random.randint(4, 7))
            except StaleElementReferenceException:
                time.sleep(5)
                comment_text_area = self.driver.find_element(By.XPATH,
                                                             "//form[@method='POST']/textarea")
                # copy the comment text to clipboard
                pyperclip.copy(comment_)
                time.sleep(0.5)

                # type the . to trigger the comment button
                ActionChains(self.driver).move_to_element(comment_text_area).perform()
                time.sleep(0.5)
                ActionChains(self.driver).click(comment_text_area).perform()
                time.sleep(0.5)

                # paste the comment text from clipboard
                comment_text_area.send_keys(Keys.CONTROL, 'v')
                time.sleep(random.randint(4, 7))

            # select the post button
            try:
                post_button = self.driver.find_element(By.XPATH, "//*[text()='Post']")

                # click on the post button
                ActionChains(self.driver).move_to_element(post_button).perform()
                time.sleep(0.5)
                ActionChains(self.driver).click(post_button).perform()
                time.sleep(random.randint(20, 25))
            except:
                print("[Exception-7]: Post Button Clicking for post: {}".format(post_))
                return False, "[Exception-7]: Post Button Clicking for post"

            print("Commented on post.")
        except TimeoutException:
            print("Comments are disabled for this post.")

        print("Comment on post done by user: {}".format(self.username))

        return True, "Comment on post done by user: {}".format(self.username)

    def close_browser(self):
        self.driver.close()
        self.driver.quit()
        self.driver = None
        return True


def start_bot():
    # get accounts file path
    accounts_file_path = accounts_file_entry.get()

    # read accounts file
    accounts = []
    with open(accounts_file_path) as f:
        for line in f:
            row = line.strip()
            row_items = row.split(':')
            account_dict = dict()
            account_dict['username'] = row_items[0]
            account_dict['password'] = row_items[1]
            account_dict['mail username'] = row_items[2]
            account_dict['mail password'] = row_items[3]
            accounts.append(account_dict)

    if len(accounts) == 0:
        tkr.messagebox.showerror("Error", "No accounts found in the accounts file.")
        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        accounts_file_entry.focus()
        return

    # get post file path
    post_file_path = post_links_file_entry.get()

    # read post links from file
    post_links = []
    with open(post_file_path, "r") as post_file:
        for post in post_file:
            post_links.append(post.strip().rstrip())

    if post_links.__len__() == 0:
        tkr.messagebox.showerror("Error", "No Post Links Found in File.")
        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        post_links_file_entry.config(state=tkr.NORMAL)
        return

    # get comments file path
    comments_file_path = comments_file_entry.get()

    # read comments from file
    comments_list = []
    with open(comments_file_path, "r", encoding="utf8") as comments_file:
        for comment in comments_file:
            comments_list.append(comment.strip().rstrip())

    if comments_list.__len__() == 0:
        tkr.messagebox.showerror("Error", "No Comments Found in File.")
        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        comments_file_entry.focus()
        return

    # use proxy is checked
    if proxy_var.get() == 1:
        # get proxy file path
        proxy_file_path = proxies_config_file_entry.get()
    else:
        proxy_file_path = None

    if proxy_file_path is not None:
        # read proxies from file
        proxies_list = []
        with open(proxy_file_path, "r") as proxy_file:
            for proxy in proxy_file:
                proxies_list.append(proxy.strip().rstrip())

        if proxies_list.__len__() == 0:
            tkr.messagebox.showerror("Error", "No Proxies Found in File.")
            stop_btn.config(state=tkr.NORMAL)
            start_btn.config(state=tkr.NORMAL)
            accounts_file_brows_btn.config(state=tkr.NORMAL)
            post_links_file_brows_btn.config(state=tkr.NORMAL)
            comment_brows_btn.config(state=tkr.NORMAL)
            proxies_config_file_brows_btn.config(state=tkr.NORMAL)

            proxies_config_file_entry.focus()
            return

    # get number of comments per post to be made by each account
    no_of_comments = no_of_comments_entry.get()
    if no_of_comments.__len__() == 0:
        tkr.messagebox.showerror("Error", "Please Enter No. of Comments to Perform on Post.")
        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        no_of_comments_entry.focus()
        return

    no_of_comments = int(no_of_comments)

    # get delay time
    delay_time = delay_entry.get()
    if delay_time.__len__() == 0:
        tkr.messagebox.showerror("Error", "Please Enter Delay Time.")
        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        delay_entry.focus()
        return

    delay_time = int(delay_time)

    while no_of_comments > 0:
        for account in accounts:
            print()
            print("Logging in to account: " + account['username'])
            # create bot instance
            global instagram_automation_bot

            # create bot
            instagram_automation_bot = InstagramAutomationBot(
                account['username'], account['password'], account['mail username'], account['mail password']
            )

            # login to instagram
            login_status, login_msg = instagram_automation_bot.login()
            if not login_status:
                print(login_msg)
                continue

            print("Logged in to account: " + account['username'])
            # comment on post
            for post in post_links:
                print("Commenting on post: " + post)
                comment = random.choice(comments_list)
                comment_status, comment_msg = instagram_automation_bot.do_comment_on_users_posts(post, comment)
                if not comment_status:
                    print(comment_msg)
                    continue

                print("Commented on post: " + post)

                print("Saving Cookies again...")
                # save session cookies to file for future use of the same session to avoid login again and again
                cookies_name = instagram_automation_bot.username + "_cookies.pkl"
                pickle.dump(instagram_automation_bot.driver.get_cookies(),
                            open(os.path.join(os.getcwd(), 'cookies', cookies_name), "wb"))
                print("Session cookies saved in 'cookies' folder to file: " + cookies_name)
                time.sleep(random.randint(2, 5))

            print("Logging out of account: " + account['username'])
            # close browser
            instagram_automation_bot.close_browser()

            print("Logged out of account: " + account['username'])

            # wait for delay
            print("Waiting for " + str(delay_time) + " seconds.")
            time.sleep(delay_time)

        no_of_comments -= 1
        print("Comments: " + str(no_of_comments) + " left to perform.")
        print("Waiting for " + str(delay_time) + " seconds.")

        print()

    print("Comments Performed Successfully.")

    # print success message
    bot_status_label.config(text="Bot Successfully Completed.")
    time.sleep(random.randint(2, 4))

    # stop bot
    stop_btn.config(state=tkr.NORMAL)
    accounts_file_entry.delete(0, tkr.END)
    post_links_file_entry.delete(0, tkr.END)
    comments_file_entry.delete(0, tkr.END)
    proxies_config_file_entry.delete(0, tkr.END)
    no_of_comments_entry.delete(0, tkr.END)
    delay_entry.delete(0, tkr.END)

    start_btn.config(state=tkr.NORMAL)
    accounts_file_brows_btn.config(state=tkr.NORMAL)
    post_links_file_brows_btn.config(state=tkr.NORMAL)
    comment_brows_btn.config(state=tkr.NORMAL)
    proxies_config_file_brows_btn.config(state=tkr.NORMAL)

    # recheck the checkbox
    if proxy_var.get() == 1:
        proxy_var.set(0)

    bot_status_label.config(text="Idle")
    accounts_file_entry.focus()


def start_bot_thread():
    start_btn.config(state=tkr.DISABLED)
    accounts_file_brows_btn.config(state=tkr.DISABLED)
    post_links_file_brows_btn.config(state=tkr.DISABLED)
    comment_brows_btn.config(state=tkr.DISABLED)
    proxies_config_file_brows_btn.config(state=tkr.DISABLED)

    thread = threading.Thread(target=start_bot)
    thread.daemon = True
    thread.start()


def stop():
    global instagram_automation_bot
    try:
        if instagram_automation_bot is not None:
            instagram_automation_bot.close_browser()
            print("Bot stopped.")
            bot_status_label.config(text="Bot Stopped.")

        accounts_file_entry.delete(0, tkr.END)
        post_links_file_entry.delete(0, tkr.END)
        comments_file_entry.delete(0, tkr.END)
        proxies_config_file_entry.delete(0, tkr.END)
        no_of_comments_entry.delete(0, tkr.END)
        delay_entry.delete(0, tkr.END)

        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        # recheck the checkbox
        if proxy_var.get() == 1:
            proxy_var.set(0)
        accounts_file_entry.focus()
    except Exception:
        accounts_file_entry.delete(0, tkr.END)
        post_links_file_entry.delete(0, tkr.END)
        comments_file_entry.delete(0, tkr.END)
        proxies_config_file_entry.delete(0, tkr.END)
        no_of_comments_entry.delete(0, tkr.END)
        delay_entry.delete(0, tkr.END)

        stop_btn.config(state=tkr.NORMAL)
        start_btn.config(state=tkr.NORMAL)
        accounts_file_brows_btn.config(state=tkr.NORMAL)
        post_links_file_brows_btn.config(state=tkr.NORMAL)
        comment_brows_btn.config(state=tkr.NORMAL)
        proxies_config_file_brows_btn.config(state=tkr.NORMAL)

        # recheck the checkbox
        if proxy_var.get() == 1:
            proxy_var.set(0)

        bot_status_label.config(text="Idle")
        accounts_file_entry.focus()


def validate_delay_entry(p):
    if len(p) != 0:
        x = re.match(r"^\d+$", p)
        if x is not None:
            return True
        else:
            tkr.messagebox.showinfo('Error Message', 'Please Enter Only Numeric Value (e.g. 5, 10, 15 etc)')
            delay_entry.delete(0, END)
            delay_entry.focus()
            return False


def validate_max_comments_entry(p):
    if len(p) != 0:
        x = re.match(r"^\d+$", p)
        if x is not None:
            return True
        else:
            tkr.messagebox.showinfo('Error Message', 'Please Enter Only Numeric Value (e.g. 5, 10, 15 etc)')
            no_of_comments_entry.delete(0, END)
            no_of_comments_entry.focus()
            return False


def select_comments_file_location():
    comments_file_location = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Text File",
                                                        filetypes=(("Text Files", "*.txt"), ("All Files", "*.txt")))
    comments_file_entry.delete(0, END)
    comments_file_entry.insert(0, comments_file_location)


def select_post_links_file_location():
    posts_file_location = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Text File",
                                                        filetypes=(("Text Files", "*.txt"), ("All Files", "*.txt")))
    post_links_file_entry.delete(0, END)
    post_links_file_entry.insert(0, posts_file_location)


def select_proxies_file_location():
    proxy_file_location = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Text File",
                                                        filetypes=(("Text Files", "*.txt"), ("All Files", "*.txt")))
    proxies_config_file_entry.delete(0, END)
    proxies_config_file_entry.insert(0, proxy_file_location)


def select_accounts_file_location():
    accounts_file_location = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Text File",
                                                        filetypes=(("Text Files", "*.txt"), ("All Files", "*.txt")))
    accounts_file_entry.delete(0, END)
    accounts_file_entry.insert(0, accounts_file_location)


if __name__ == '__main__':
    window = tkr.Tk()
    # add padding of 88px to the left of the window
    window.grid_columnconfigure(0, minsize=88)

    # add padding of 88px to the right of the window
    window.grid_columnconfigure(0, minsize=88)

    # add padding of 88px to the top of the window
    window.grid_rowconfigure(0, minsize=88)

    window.geometry('563x660')
    #window.iconbitmap(os.path.join(os.getcwd(), 'assets', 'insta_icon.ico'))
    
    window.iconbitmap(r'D:\Code\scrapper\assets\insta_icon.ico')
    window.resizable(False, False)
    window.title("Insta-Bot")
    mycolor = '#%02x%02x%02x' % (68, 68, 68)

    vcmd_1 = (window.register(validate_max_comments_entry), '%P')
    vcmd_2 = (window.register(validate_delay_entry), '%P')

    image_path = Image.open(os.path.join(os.getcwd(), 'assets', 'insta_logo.png'))
    # image_path = Image.open("./assets/insta_logo.png")
    img = ImageTk.PhotoImage(image_path)

    img_label = Label(window, image=img)
    img_label.grid(column=1, row=0, columnspan=3, padx=80, pady=5, sticky='w')
    Label(text="").grid(row=1, column=0, sticky="w")

    tkr.Label(window, text="*Accounts Text File : ").grid(column=0, row=3, pady=5, ipadx=10, ipady=3, padx=10, sticky="w")
    accounts_file_entry = tkr.Entry(window, bd=4, width=42, relief="groove")
    accounts_file_entry.grid(column=1, row=3, padx=5, pady=5, ipady=3, sticky="w")
    accounts_file_brows_btn = tkr.Button(window, text="Browse", command=select_accounts_file_location, bg='#567', fg='White')
    accounts_file_brows_btn.grid(column=2, row=3, padx=5, pady=5, ipadx=15, ipady=3)
    tkr.Label(window, text="*Text file containing credentials.", fg='red').grid(row=4, column=1)

    tkr.Label(window, text="*Post Links Text File : ").grid(column=0, row=5, pady=5, ipadx=10, ipady=3, padx=10, sticky="w")
    post_links_file_entry = tkr.Entry(window, bd=4, width=42, relief="groove")
    post_links_file_entry.grid(column=1, row=5, padx=5, pady=5, ipady=3, sticky="w")
    post_links_file_brows_btn = tkr.Button(window, text="Browse", command=select_post_links_file_location, bg='#567', fg='White')
    post_links_file_brows_btn.grid(column=2, row=5, padx=5, pady=5, ipadx=15, ipady=3)
    tkr.Label(window, text="*Text file containing posts links.", fg='red').grid(row=6, column=1)

    tkr.Label(window, text="Comments Text file : ").grid(column=0, row=7, pady=5, ipadx=10, ipady=3, padx=10, sticky="w")
    comments_file_entry = tkr.Entry(window, bd=4, width=42, relief="groove")
    comments_file_entry.grid(column=1, row=7, padx=5, pady=5, ipady=3, sticky="w")
    comment_brows_btn = tkr.Button(window, text="Browse", command=select_comments_file_location, bg='#567', fg='White')
    comment_brows_btn.grid(column=2, row=7, padx=5, pady=5, ipadx=15, ipady=3)
    tkr.Label(window, text="Select Text File with Comments.", fg='red').grid(row=8, column=1)

    # create variable for proxy checkbox
    proxy_var = tkr.IntVar()

    # checkbox for proxies selection
    proxy_checkbox = tkr.Checkbutton(window, text="Use Proxies", variable=proxy_var, onvalue=1, offvalue=0)
    proxy_checkbox.grid(row=9, column=1, sticky='w', padx=10, pady=5)

    tkr.Label(window, text="Proxies Config file : ").grid(column=0, row=10, pady=5, ipadx=10, ipady=3, padx=13, sticky="w")
    proxies_config_file_entry = tkr.Entry(window, bd=4, width=42, relief="groove")
    proxies_config_file_entry.grid(column=1, row=10, padx=5, pady=5, ipady=3, sticky="w")
    proxies_config_file_brows_btn = tkr.Button(window, text="Browse", command=select_proxies_file_location, bg='#567', fg='White')
    proxies_config_file_brows_btn.grid(column=2, row=10, padx=5, pady=5, ipadx=15, ipady=3)
    tkr.Label(window, text="Select Post Links File.", fg='red').grid(row=11, column=1)

    tkr.Label(window, text="No. of Comments : ").grid(column=0, row=12, pady=5, ipadx=10, ipady=3, padx=10, sticky="w")
    no_of_comments_entry = tkr.Entry(window, bd=4, width=42, relief="groove", validate="key", validatecommand=vcmd_1)
    no_of_comments_entry.grid(column=1, row=12, padx=5, pady=5, ipady=3, sticky="w")
    tkr.Label(window, text="Number of comments to be posted by each account.", fg='red').grid(row=13, column=1)

    # delay
    tkr.Label(window, text="Delay : ").grid(column=0, row=14, pady=5, ipadx=10, ipady=3, padx=10, sticky="w")
    delay_entry = tkr.Entry(window, bd=4, width=42, relief="groove", validate="key", validatecommand=vcmd_2)
    delay_entry.grid(column=1, row=14, padx=5, pady=5, ipady=3, sticky="w")
    tkr.Label(window, text="Delay between each comment in seconds.", fg='red').grid(row=15, column=1)

    tkr.Label(window, text="Bot Status : ").grid(column=0, row=16, pady=5, ipadx=10, ipady=3, padx=15, sticky="w")
    bot_status_label = tkr.Label(text="Idle", foreground='red')
    bot_status_label.grid(row=16, column=1, pady=5, sticky='w')

    stop_btn = tkr.Button(window, text="Stop Bot", command=stop, bg=mycolor, fg='white')
    stop_btn.grid(column=0, row=17, pady=20, ipadx=10, ipady=3, padx=25, sticky="w")

    start_btn = tkr.Button(window, text="Start Bot", command=start_bot_thread, bg=mycolor, fg='white')
    start_btn.grid(column=2, row=17, pady=20, padx=10, ipadx=10, ipady=3, sticky='w')

    window.mainloop()
