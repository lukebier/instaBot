import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException 
from utility_methods.utility_methods import insta_method
from utility_methods.utility_methods import init_config
from utility_methods.utility_methods import get_logger
from utility_methods.utility_methods import exception
import utility_methods.mail



class InstaBot:

    def __init__(self, username=None, password=None):
        """
        Initializes an instance of the InstagramBot class. 
        Calls the login method to authenticate a user with Instagram.
        Runs headless in the terminal.
        Args: 
            username:str: The Instagram username for a user
            password:str: The Instagram password for a user

        Attributes:
            driver:Selenium.webdriver.Firefox: Geckodriver that is used to automate browser actions.

        """
        
        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_hashtag_url = config['IG_URLS']['SEARCH_HASHTAGS']
        self.get_tagged_pictures_url = config['IG_URLS']['SEARCH_TAGGED_PICTURES']

        self.options = Options()
        self.options.headless = True
        self.options.width = 1680
        self.options.height = 1050
        self.driver = webdriver.Firefox(options=self.options)
        print("Headless Firefox Initialized")
     
        self.logged_in = False


    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal.
        """

        self.driver.get(self.login_url)
        self.driver.implicitly_wait(3) # Wait for 3 seconds.

        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        self.driver.implicitly_wait(5)

        self.driver.find_elements_by_xpath("//div[contains(text(), 'Anmelden')]")[0].click()

        time.sleep(1) # Sleep for 1 second.
        print("Login successful.")
    
    
    def starter(self):
        """
        Sends a mail that the session has been started.
        """

        utility_methods.mail.main(0)
        print("Mail sent!")

    
    def quitter(self):
        """
        Quits the session.
        """

        print("Quitter activated.")
        utility_methods.mail.main(1)
        print("Mail sent!")
        self.driver.quit()


    @insta_method
    def nav_user(self, user):
        """
        Navigates to the user's page.
        Args:
            user:str: The username of the desired Instagram User
        """

        self.driver.get(self.nav_user_url.format(user))


    @insta_method
    def search_hashtag(self, hashtag):
        """
        Navigates to a search for posts with a specific hashtag on IG.
        Args:
            hashtag:str: Tag to search for
        """

        self.driver.get(self.get_hashtag_url.format(hashtag))


    @insta_method
    def search_tagged_pictures(self, user):
        """
        Navigates to a search for posts the user is tagged in on IG.
        Args:
            user:str: User whose tagged pictures to search for.
        """

        self.driver.get(self.get_tagged_pictures_url.format(user))


    @insta_method
    def follow_user(self, user, follow=True):
        """
        Follow or unfollow the user's page.
        Args:
            user:str: The username of the desired Instagram User.
            follow:bool: If True, follow a user, else if False, unfollow a user.
        Follows the user's page.
        """
        self.nav_user(user)
        if follow:
                follow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Folgen')]")[0]
                follow_button.click()
        else:
                unfollow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Abonniert')]")[0]
                unfollow_button.click()
                time.sleep(2) #Sleep for 2 seconds until the button appears.
                real_unfollow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Nicht mehr folgen')]")[0]
                real_unfollow_button.click()
    

    @insta_method
    def like_latest_posts(self, user, n_posts, like=True):
        """
        Likes or unlikes a specified number of a user's latest posts.
        Always starting from the second latest post as to appear as being humanely operated.
        Args:
            user:str: User whose posts to like or unlike.
            n_posts:int: Number of posts to like or unlike.
            like:bool: If True, likes recent posts, else if False, unlikes recent posts
        """

        action = 'Gefällt mir' if like else 'Gefällt mir nicht mehr'

        self.nav_user(user)

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in imgs[1:n_posts+1]:
            img.click() 
            time.sleep(1) 
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
                
            except Exception as e:
                print(e)

            self.driver.find_element_by_xpath("//*[@aria-label='Schließen']").click()


    @insta_method
    def like_no_tomorrow(self, search_hashtag, amount):
        """
        Likes an unspecified number of posts with a specific hashtag, the dirty way.
        Always starting from the ninth latest post as to skip the highlighted posts.
        Stops operating when as many posts have been checked as the amount defines.
        Can be extended to run quasi infinitely with sleeping to match Instagram's limits.
        Args:
            search_hashtag:str: Hashtag to search for pictures and like them.
            amount:int: Maximum pictures to be checked.
        """
        
        self.search_hashtag(search_hashtag)
        picnine = self.driver.find_elements_by_class_name('_9AhH0')[9]
        picnine.click()

        i = 0

        while i <= amount:
            time.sleep(1)
            try: 
                self.driver.find_element_by_xpath("//*[@aria-label='Gefällt mir nicht mehr']")
                print("Bereits geliked.")
                
            except NoSuchElementException: 
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Gefällt mir']"))).click()
                print("Bild geliked")
            
            time.sleep(0.1)

            self.driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
            time.sleep(1)
            i += 1


    @insta_method
    def like_latest_hashtags(self, search_hashtag):
        """
        Likes an unspecified number of a user's latest posts.
        Always starting from the ninth latest post as to skip the highlighted posts.
        Stops operating when a picture has already been liked or the counter reached the limit.
        Args:
            search_hashtag:str: Hashtag to search for pictures and like them.
        """

        self.search_hashtag(search_hashtag)
        likecounter = 0
        likedcounter = 0

        try:
            self.driver.find_element_by_xpath("//*[@aria-label='„Aktivitäten“-Meldungen']").click()
        except Exception as e:
            print(e)

        self.search_hashtag(search_hashtag)

        imgs = [] 
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in imgs[9:]:
            self.driver.execute_script("arguments[0].click();", img) 
            time.sleep(0.1) 

            try: 
                self.driver.find_element_by_xpath("//*[@aria-label='Gefällt mir nicht mehr']")
                #Bereits regulär geliked.
                likedcounter += 1

                if likedcounter == 11:
                    #11 Bilder wurden bereits vorher geliked, deshalb Abbruch.
                    break

            except NoSuchElementException: 
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Gefällt mir']"))).click()
                likecounter += 1
              

            if likecounter == 10:
                #Likelimit von 10 erreicht.
                break
            
            self.driver.find_element_by_xpath("//*[@aria-label='Schließen']").click()

        print("In this run,",likecounter,"pictures have been liked.")
        self.likecounter = likecounter


    @insta_method
    def like_latest_usertags(self, user):
        """
        Likes an unspecified number of a user's latest tagged posts.
        Stops operating when a picture has already been liked through this function in a prior run,
        or when the counter reached the limit.
        Args:
            user:str: User whose tagged pictures shall be targeted to like.
        """

        self.search_tagged_pictures(user)

        searchtag = f"#{user}"

        try:
            self.driver.find_element_by_xpath("//*[@aria-label='„Aktivitäten“-Meldungen']").click()
        except Exception as e:
            print(e)
        
        self.search_tagged_pictures(user)

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
        count = 0
        tagcounter = 0
        likecounter = 0

        for img in imgs[:]:
            img.click() 
            time.sleep(0.1) 

            try: 
                self.driver.find_element_by_xpath("//*[@aria-label='Gefällt mir nicht mehr']")
                
                try: 
                    self.driver.find_element_by_xpath("//a[contains(@class, 'xil3i') and contains(., '%s')]" % searchtag)
                    #Already liked via searchtag, which excludes pictures to be liked.
                    tagcounter += 1

                    if tagcounter == 11:
                        #Die letztem 11 Bilder wurden vorher bereits geliked, deshalb Abbruch.
                        break
                    
                except NoSuchElementException:
                    #Bereits regulär geliked.
                    likecounter += 1

                    if likecounter == 10:
                        #Die letztem 10 Bilder wurden bereits geliked, deshalb Abbruch.
                        break

            except NoSuchElementException: 
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Gefällt mir']"))).click()
                count += 1
                
            self.driver.find_element_by_xpath("//*[@aria-label='Schließen']").click()
            if count == 10:
                    #Limit von 10 Likes erreicht.
                    break

        print("In this run,",count,"pictures have been liked.")
        self.count = count
        

    @insta_method
    def shababslikebotten(self, runtime, search_hashtags, users):
        """
        This function cumulates the main operations to run the likebot.
        Likes an unspecified number of posts by hashtag and user that is tagged on them.
        Uses the functions like_latest_hashtags and like_latest_usertags.
        After every run, sleeps for one minute and then runs both functions again.
        Finishes, when the end of the runtime is reached.
        Args:
            runtime:int: Desired number of seconds the function shall run.
            search_hashtag:str: Hashtag to identify pictures that shall be liked or have already been liked.
            user:str: User whose tagged pictures shall be liked.
        """

        start_time = time.time()  # Remember when we started.
        rundencounter = 0
        hashtagdrop = 0
        usertagdrop = 0
        hashtagtime = 0
        usertagtime = 0
        wastingtime = 0
        
        while (time.time() - start_time) < runtime:
            
            rundencounter += 1
            print("--------------------","Round",rundencounter,"--------------------")

            if hashtagtime - time.time() < 0:
                for search_hashtag in search_hashtags:
                    self.like_latest_hashtags(search_hashtag)
                    print("The most recent posts with",f"#{search_hashtag}","have been liked.")
                    if self.likecounter == 0:
                        hashtagdrop +=1
                    else:
                        if hashtagdrop > 0:
                            hashtagdrop -=1
                        else:
                            hashtagdrop = 0

                hashtagtime = time.time() + hashtagdrop * 60
            

            if hashtagdrop > 0:
                print("Forced waitingperiod for like_latest_hashtags of",hashtagdrop,"minutes.")
            
            if usertagtime - time.time() < 0:
                for user in users:
                    self.like_latest_usertags(user)
                    print("The most recent posts with tags of",f"@{user}","have been liked.")
                    if self.count == 0:
                        usertagdrop +=1
                    else:
                        usertagdrop = 0

                usertagtime = time.time() + usertagdrop * 60
            
            if usertagdrop > 0:
                print("Forced waitingperiod for like_latest_usertags of",usertagdrop,"minutes.")
            
            wastingtime = runtime / (1000 / ((len(search_hashtags) + len(users)) * 10))
            print("Regular waitingtime of ",wastingtime,"seconds.")
            time.sleep(wastingtime)



if __name__ == '__main__':
    
    config_file_path = './config.ini'
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)
    
    bot = InstaBot()

    bot.starter()

    bot.login()

    bot.shababslikebotten(600, ['hashtag1', 'hashtag2', 'hashtag3'], ['user1', 'user2'])

    bot.quitter()