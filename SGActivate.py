from tkinter import *
import urllib.parse as urlparse
from urllib.parse import parse_qs

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import time, json
import threading

url = open("data.txt", "r").read()

window = Tk()
window.geometry("1200x200")
window.title("StormGain auto Activate v.1.1.1")
window.grid_rowconfigure(3)
window.grid_columnconfigure(3)


l_iframe = Label(window, text="iframe - ")
l_iframe.grid(column=0, row=0)

e_iframe = Entry(width=160)
e_iframe.insert(END, url)
e_iframe.grid(column=1, row=0)

l_Time = Label(window, text="Time - ")
l_Time.grid(column=2, row=0)

date = StringVar()
date.set('Date')
l_Date = Label(window, textvariable = date)
l_Date.grid(column=3, row=0)

l_log = Label(window, text="logout - ")
l_log.grid(column=0, row=1)

log = StringVar()
log.set('log information')
e_log = Label(window, textvariable = log)
e_log.grid(column=1, row=1)

headless = IntVar()
c_headless = Checkbutton(window, text = "Headless", variable=headless)
c_headless.grid(column=2, row=1)


xpath_activate = "/html/body/div[1]/div[2]/div/button/div"
xpath_time     = "/html/body/div[1]/div[2]/div/div[1]/span[2]"
f_options = webdriver.firefox.options.Options()
f_options.headless = True
c_options = webdriver.chrome.options.Options()
c_options.add_argument("--headless")

def activate(driver, url):
    try:
        driver.get(url)
        time.sleep(1)
        try:
            driver.find_element_by_xpath(xpath_activate).click() # Click Activate button
            time.sleep(1)
            date.set(datetime.datetime.now()+datetime.timedelta(hours=1))
            window.update_idletasks()
            return 60*60 * 4 # in 4 hours
        except:
            try:
                # Get Remain time
                t = driver.find_element_by_xpath(xpath_time).get_attribute("innerHTML")
                td = (int(t[0:2])*60 + int(t[4:6]))*60 + int(t[8:10])
                date.set(datetime.datetime.now()+datetime.timedelta(seconds=td))
                window.update_idletasks()
                return td
            except:
                return 60*60 * 1 # in 1 hour
    except:
        log.set("iframe incorrect")
        window.update_idletasks()
        return 60* 15 # in 15 minutes


def start():
    url = e_iframe.get()
    if len(url) == 0:
        log.set("Please fill the iframe URL")
        window.update_idletasks()
    else:
        open("data.txt", "w").write(url)
        parsed = urlparse.urlparse(url)
        try:
            print(parse_qs(parsed.query)['cpe'][0])
            log.set("Everything is good just wait...")
            window.update_idletasks()
            while True:
                time.sleep(1)
                try: # Connection au site
                    try:
                        if headless.get() == 1:
                            driver = webdriver.Firefox(executable_path='driver/geckodriver.exe', options=f_options)
                        else:
                            driver = webdriver.Firefox(executable_path='driver/geckodriver.exe')
                    except:
                        try:
                            if headless.get() == 1:
                                driver = webdriver.Chrome(executable_path='driver/chromedriver', options=c_options)
                            else:
                                driver = webdriver.Chrome(executable_path='driver/chromedriver')
                        except:
                            log.set("You must have Firefox or at least Chrome")
                            window.update_idletasks()
                    # driver = webdriver.Firefox(executable_path="./driver/geckodriver")
                    time.sleep(1)
                    next_attempt = time.time() + activate(driver, url)
                    driver.quit()

                except:
                    log.set("Please check your connection")
                    window.update_idletasks()
                    next_attempt = 60* 15 + time.time() # in 15 minutes
                
            
                while next_attempt > time.time():
                    time.sleep(60*5)
        except:
            log.set("iframe incorrect")
            window.update_idletasks()
        


def threadButtonOne():
    threading.Thread(target=start).start()

f_validate = Button(window, text ="--- Start ---", command=threadButtonOne)
f_validate.grid(column=3, row=1)


window.mainloop()