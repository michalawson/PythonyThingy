from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
import time

##  will need to have python 2.7+
##  will need to install selenium driver from cmd line
##  ->pip install selenium 
##  will need to install pynput driver from cmd line
##  ->pip install pynput f
##  will need to allow python to communicate on network
##  Make sure that selenium.exe file path is included below
##  CaseIDS.txt file creation
##  Credentials.txt file creation

def readtxt(path_to_file):
    rows = []
    myFile = open(path_to_file, 'r')
    row = myFile.readline().strip()
    while row != '':
        #  builds a list of reqs
        rows.append(row)
        row = myFile.readline().strip()
    return rows

def main():

    ##  ENTER WHERE YOU WANT TO SAVE FILES TO LOCALLY
    #download_dir = 'C:/Users/mlawson/desktop/centene_reqs'
    credentials_path = 'C:/Users/mlawson/desktop/python/credentials.txt'
    case_ids_path = 'C:/Users/mlawson/desktop/python/caseids.txt'
    care_url = 'https://enterprise.natera.com/billing_services/prior_auth/auth/'
    ref_token = 'PA Cancelled'
    cred = readtxt(credentials_path)
    usernameStr = cred[0]
    passwordStr = cred[1]
    caseids = readtxt(case_ids_path)
    
    ## ENTER YOUR PATH TO CHROMEDRIVER HERE -> EXECUTABLE PATH
    browser = webdriver.Chrome(executable_path = 'C:/Users/mlawson/Desktop/chromedriver.exe')
    link = care_url + caseids[0]
    ## ENTERS CREDENTIALS
    keyboard = Controller()
    count = 0
    stop = 0
    technical_stop = 0
    for case in caseids:
        link = care_url + case
        browser.get(link)
        time.sleep(3)
        
        if count == 0:
            username = browser.find_element_by_id('user_username')
            username.send_keys('mlawson')
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(1)
            keyboard.type(passwordStr)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(5)
    
        #time.sleep(5)

        # Assigned To: Button
        assignedTo = browser.find_elements_by_xpath('//*[@id="case-actions"]/p/strong')

        # Assign to Me Button
        assigntomeButton = browser.find_elements_by_xpath("//span[text()='Assign To Me']")

                 
        if (len(assignedTo)>0 and assignedTo[0].is_displayed()):
            time.sleep(2)
            if (len(assigntomeButton)>0 and assigntomeButton[0].is_displayed()):
                assigntomeButton[0].click()
                time.sleep(2)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(2)
                stop != 1
            else:
                stop != 1
        else:
            if (len(assigntomeButton)>0 and assigntomeButton[0].is_displayed()):
                assigntomeButton[0].click()
                stop != 1
            else:
                stop != 1
                    
        if (stop != 1):
            time.sleep(3)

            edit_button = browser.find_elements_by_xpath("//span[text()='Edit']")
            if len(edit_button)>0 and edit_button[0].is_displayed():
                edit_button[0].click()
                time.sleep(1)
            else:
                technical_stop = 1

            status_dropdown = browser.find_elements_by_xpath('//*[@id="case-fields"]/div[2]/form/div[4]/div[1]/div/select/option[6]')
            if len(status_dropdown)>0 and status_dropdown[0].is_displayed():
                status_dropdown[0].click()
                time.sleep(.5)
            else:
                technical_stop = 1
                
            #status_dropdown.click()
            closed_reason = browser.find_elements_by_xpath('//*[@id="closed_type"]/option[5]')
            if len(closed_reason)>0 and closed_reason[0].is_displayed():
                time.sleep(.5)
                closed_reason[0].click()
                time.sleep(.5)
            else:
                technical_stop = 1

            ref_token = browser.find_elements_by_id('reference_token')
            if len(ref_token)>0 and ref_token[0].is_displayed():
                ref_token[0].clear()
                ref_token[0].send_keys('Timeline Exceeded')
            else:
                technical_stop = 1

            auth_token = browser.find_elements_by_id('authorization_token')
            if len(auth_token)>0 and auth_token[0].is_displayed():
                auth_token[0].clear()
                auth_token[0].send_keys('Timeline Exceeded')
            else:
                technical_stop = 1

            save_button = browser.find_elements_by_xpath("//span[text()='Save']")
            if len(save_button)>0 and save_button[0].is_displayed():
                save_button[0].click()
                time.sleep(3)
            else:
                technical_stop = 1

            if technical_stop != 1:
                print(count)
            else:
                print('Case: ' + case + ' THIS CASE WAS SKIPPED DUE TO TECHNICAL ERROR')

            count = count + 1
            stop = 0
            technical_stop = 0

main()
