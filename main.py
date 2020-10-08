"""Insta bot v.0.1
So far, he can find posts by tag or user and like them with pleasure
"""

from selenium import webdriver

from private import users_data
from user import User
from instabot import InstaBot, SearchType



def main():
    for item in users_data:
        with webdriver.Chrome("./driver/chromedriver.exe") as driver:
            bot = InstaBot(driver=driver, user=User(name=item[0], password=item[1]))
            bot.login()

            posts = []

            print("Input type of search:")
            print("1. Search by hashtag")
            print("2. Search by username")
            print("3. Search by list of users")
            type_of_search = input("> ")

            if type_of_search == "1":
                print("Input hashtag")
                while True:
                    hashtag = input("> ")
                    if hashtag.isprintable():
                        break
                    print("Input correct symbols for hashtag (a-Z)")

                posts = bot.get_posts(SearchType.hashtag, hashtag)

            elif type_of_search == "2":
                print("Input username")
                while True:
                    like_user = input("> ")
                    if like_user.isalpha():
                        break
                    print("Input correct symbols for username (a-Z)")
                posts = bot.get_posts(SearchType.user, like_user)

            elif type_of_search == "3":
                print("Input usernames separate by space")
                while True:
                    like_users_str = input("> ")
                    if like_users_str.isalpha():
                        break
                    print("Input correct symbols for usernames (a-Z)")

                like_users = like_users_str.lstrip().rstrip().split()
                for user in like_users:
                    posts.extend(bot.get_posts(SearchType.user, user))
            else:
                exit()

            print(f"Collect {len(posts)} links")
            bot.like_posts(posts)


if __name__ == "__main__":
    main()
