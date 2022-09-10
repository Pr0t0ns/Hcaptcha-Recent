import ctypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from os import system, name
subjects_found = 0
subjects_duplicate = 0
errors = 0
options = webdriver.ChromeOptions()
headless_input = input("Headless browser (y/n): ")
if headless_input.lower() == "y" or headless_input.lower() == "yes":
    options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
def clear():
    if name == 'nt':
        return system('cls')
    else:
        return system('clear')
clear()
def menu():
    print("Made by Pr0t0ns | Github.com/@Pr0t0ns | Discord.gg/termed | Pr0t0n#5220 (More Menu Options Soon)")
    print("1) Collect Image Subject's")
    print("2) Exit")
    choice = int(input("Choice: "))
    if choice == 1:
        clear()
        threading.Thread(target=update_header).start()
        for i in range(int(input("Enter threads: "))):
            threading.Thread(target=subject_hcaptcha).start()
            time.sleep(0.1)
    elif choice >= 2:
        exit(0)
def update_header():
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f"Subject Fetcher | New Subjects Found: {subjects_found} | Duplicate Subjects: {subjects_duplicate} | Errors: {errors} | Made by Pr0t0ns | .gg/termed ON TOP")
def subject_hcaptcha():
        global subjects_found
        global subjects_duplicate
        global errors
        driver = webdriver.Chrome(options=options)
        driver.get('https://accounts.hcaptcha.com/demo')
        driver.implicitly_wait(2)
        driver.switch_to.frame(0)
        try:
            get_hcap_images = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div[1]").click()
        except Exception as error:
            print(f"An error occured maybe hcap ratelimit or Method out of date!")
            errors += 1
            return subject_hcaptcha()
        print('[/] - Clicked captcha getting image subject')
        driver.implicitly_wait(2)
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/iframe"))
        get_hcap_subject = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[1]/h2/span").text
        print(f'[/] - Found image subject ({get_hcap_subject})') 
        subject = get_hcap_subject.replace("Please click each image containing an", "")
        subject = get_hcap_subject.replace("Please click each image containing a ", "")
        file = open("data/hcap_subjects.txt", 'r+')
        file_data = file.read()
        file_data = file_data.replace("\n", "")
        file.close()
        file = open("data/hcap_subjects.txt", 'a+')
        if subject in str(file_data):
            print(f"[-] - Subject ({subject}) Already Logged")
            file.close()
            subjects_duplicate += 1
            driver.quit()
            return subject_hcaptcha()
        else:
            print(f"[+] - Found new subject ({subject})")
            file.write(f"{subject}\n")
            file.close()
            subjects_found += 1
            driver.quit()
            return subject_hcaptcha()

if __name__ == "__main__":
    menu()
