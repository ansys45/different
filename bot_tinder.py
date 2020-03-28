from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random


options = webdriver.ChromeOptions()
options.add_argument('disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ['enable-automation'])
PATH_TO_DRIVER = '/Users/anatolysysoev/Desktop/code/python/scraping/chromedriver'

url = 'https://tinder.com'
FB_LOGIN = '+79267995628'
FB_PASS = 'Fyfnjkbq28'
.get_attribute
class TinderBot():

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH_TO_DRIVER, options=options)
    
    def login(self):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        try:
            fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
            print('login1')
            fb_btn.click()
        except:
            try:
                #exit popups
                try:
                    self.driver.find_element_by_class('Sq(24px) P(4px)').click()
                    print("login_popup1 closed")
                except:
                    pass
                
                #login button
                self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button').click()
                #more options button
                self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button').click()
                #login with facebool button
                self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button').click()
                print('login2')
            except:
                self.driver.quit()



        base_window = self.driver.window_handles[0]
        popup_window = self.driver.window_handles[1]

        #switch to popup
        self.driver.switch_to_window(popup_window)
        #enter login
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(FB_LOGIN)
        #enter password
        self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys(FB_PASS)
        #pressing login button
        self.driver.find_element_by_xpath('//*[@id="loginbutton"]').click()

        #switch to base_window
        self.driver.switch_to_window(base_window)
        try:
            #allow location
            self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
            try:
                #allow notifications
                self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
            except:
                pass
        except:
            pass

    def setAge(self, begin, end):
        if (begin - end > -4 or begin < 18 or end > 55):
            return False

        #go to settings
        self.driver.get('https://tinder.com/app/profile')

        current_age_begin = int(self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[3]/div/div[1]/div').text.split()[-3])
        current_age_end = int(self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[3]/div/div[1]/div').text.split()[-1])
        age_slider_begin = self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[3]/div/div[2]/div/div[2]/button[1]')
        age_slider_end = self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[3]/div/div[2]/div/div[2]/button[2]')

        first_to_move, second_to_move = age_slider_end, age_slider_begin
        #define direction
        mult1, mult2 = 1, 1
        if (end < current_age_end):
            mult1 = -1
        if (begin < current_age_begin):
            mult2 = -1
        if (end < current_age_begin):
            first_to_move, second_to_move = age_slider_begin, age_slider_end
            mult1, mult2 = mult2, mult1
            
        
        cnt = abs(end - current_age_end)
        while cnt:
            cnt -= 1
            act = ActionChains(self.driver)
            print("1")
            act.drag_and_drop_by_offset(first_to_move, mult1 * 10, 0).perform()
            # del act
        
        cnt = abs(begin - current_age_begin)
        while cnt:
            cnt -= 1
            act = ActionChains(self.driver)
            print("2")
            act.drag_and_drop_by_offset(second_to_move, mult2 * 10, 0).perform()
            # del act


    def setDist(self, dist):
        #go to settings
        self.driver.get('https://tinder.com/app/profile')
        sleep(2)
        current_dist = int(self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[1]/div/div[1]/div').text.split()[0])
        dist_slider = self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[1]/div/div[2]/div/div[2]/button')

        cnt = abs(dist - current_dist)
        mult = 1
        if (dist < current_dist):
            mult = -1

        while cnt:
            cnt -= 1
            act = ActionChains(self.driver)
            act.drag_and_drop_by_offset(dist_slider, mult * 10, 0)
            del act


    def setUp(self, dist = 2, age = 22):
        #go to settings
        self.driver.get('https://tinder.com/app/profile')

        current_dist = int(self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[1]/div/div[1]/div').text.split()[0])
        current_age = int(self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[3]/div/div[1]/div').text.split()[-1])

        #seting up distance
        dist_slider = self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[1]/div/div[2]/div/div[2]/button')
        try:
            ActionChains(self.driver).drag_and_drop_by_offset(dist_slider, 10*(dist - current_dist) % 2, 0).perform()
        except:
            pass

        #seting up age
        age_slider = self.driver.find_element_by_xpath('//*[@id="settings"]/div/div/div/div[4]/div/div[3]/div/div[2]/div/div[2]/button[2]')
        try:
            ActionChains(self.driver).drag_and_drop_by_offset(age_slider, 10*(age - current_age), 0).perform()
        except:
            pass

        #exit settings
        self.driver.get('https://tinder.com/app/recs')
    
    def dislike(self):
        self.driver.implicitly_wait(10)
        try:
            #dislike button
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button').click()
        except:
            pass
        
    def like(self):
        self.driver.implicitly_wait(10)
        try:
            #like button
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button').click()
        except:
            pass

    def swipe(self):
        while True:
            cnt = 0
            try:
                sleep(0.5)
                rand = random.random() * 100
                if rand > 70:
                    self.dislike()
                else:
                    self.like()
                
                cnt += 1
                if cnt == 100:
                    break
            except:
                sleep(1)
                try:
                    #close popup
                    self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]').click()
                except:
                    self.close_match()

    def close_match(self):
        #type in message
        #//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form
        #send message
        #//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(base_window)
        #click keep swiping button   
        self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a').click()



# def main():
#     for i in range(10):
#         bot = TinderBot()
#         bot.login()
#         bot.driver.quit()



# if __name__ == "__main__":
#     main()


#enter your mobile CROSS
#//*[@id="modal-manager"]/div/div/div[1]/button

#get started CROSS
#//*[@id="modal-manager"]/div/div/button