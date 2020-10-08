from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from random_sleep import Sleep
from enum import Enum


class SearchType(Enum):
    user = 'user'
    hashtag = 'hashtag'
    many_users = 'many_users'


class InstaBot:
    def __init__(self, driver, user, max_scroll=4, wait_to_load_page=30):
        self.driver: webdriver = driver
        self.user = user
        self._max_scroll = max_scroll
        self._wait_to_load_page = wait_to_load_page


    def login(self):
        print("=== Open Instagram page ===")

        try:
            self.driver.get("https://www.instagram.com")
            Sleep.medium()

            self._input_login()
            Sleep.short()
            self._input_password()
            Sleep.short()
            print("Login successful!")

        except Exception as e:
            print(f"[!] Error: {e}")


    def like_posts(self, posts):
        print(f"=== Like posts ===")
        counter = 0
        max_links = len(posts)
        for post in posts:
            counter += 1
            self.driver.get(post)
            Sleep.medium()

            try:
                like_btn = self.driver.find_element_by_css_selector("svg[aria-label='Like']")
                like_btn.click()
                Sleep.short()
                print(f"[{counter} of {max_links}] Like this: {post}")

            except Exception as e:
                print(f"[!] {e}")
                print(f"[{counter} of {max_links}] Link {post} skipped")
                Sleep.short()


    def get_posts(self, type_of_posts, search):
        print(f"=== Collecting posts for {type_of_posts} '{search}' ===")
        posts = []
        counter = 1

        if type_of_posts == SearchType.hashtag:
            url = f"https://www.instagram.com/explore/tags/{search}/"
        elif type_of_posts == SearchType.user:
            url = f"https://www.instagram.com/{search}/"


        print(f"Open page: {url}")
        self.driver.get(url)
        Sleep.medium()


        max_posts = self._get_number_of_posts(type_of_posts)
        if max_posts == -1:
            self.driver.quit()
        max_pages = int(max_posts / 12) + 1
        print(f"Find {max_posts} posts on {max_pages} pages")
        scrolls = min(max_pages, self._max_scroll)

        for n in range(scrolls + 1):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            print(f"[{n} of {scrolls}] Scroll down")
            Sleep.short()

            all_hrefs = self.driver.find_elements_by_tag_name('a')
            for a in all_hrefs:
                try:
                    href = a.get_attribute("href")

                    if href.startswith("https://www.instagram.com/p/"):
                        if href not in posts:
                            posts.append(href)
                            print(f"[{counter}]: {href}")
                            counter += 1

                except Exception as e:
                    print(f"[!] Error: {e}")
                    continue
        return posts


    def _get_number_of_posts(self, type_of_posts):
        if type_of_posts == SearchType.hashtag:
            try:
                max_posts = WebDriverWait(self.driver, self._wait_to_load_page).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "/html/body/div[1]/section/main/header/div[2]/div/div[2]/span/span")
                    )
                )
                max_posts = max_posts.text
            except Exception as e:
                print(f"[!]] {e}")
                return -1

        elif type_of_posts == SearchType.user:
            try:
                max_posts = WebDriverWait(self.driver, self._wait_to_load_page).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span")
                    )
                )
                max_posts = max_posts.text
            except Exception as e:
                print(f"[!]] {e}")
                return -1
        max_posts = int(''.join(max_posts.split(',')))
        return max_posts


    def _input_login(self):
        print(f"Input login {self.user.name}")
        username_input = self.driver.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(self.user.name)
        Sleep.short()


    def _input_password(self):
        print("Input password ******")
        password_input = self.driver.find_element_by_name("password")
        password_input.clear()
        password_input.send_keys(self.user.password)
        password_input.send_keys(Keys.ENTER)
        Sleep.short()
