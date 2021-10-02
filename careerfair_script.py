# NOTE: tried using selenium originally but found the api call directly which was easier.
# Info found here: https://medium.com/ml-book/web-scraping-using-selenium-python-3be7b8762747
import os
import time
from datetime import datetime

from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def send_msg(message):
    ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    NOTIFICATION_SERVICE = os.environ.get('NOTIFICATION_SERVICE')

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    notification = client.notify.services(NOTIFICATION_SERVICE) \
        .notifications.create(
            to_binding='{"binding_type":"sms", "address":"' + os.environ.get('NUMBER1') + '"}',
            body=message
        )
    time.sleep(15)
    client.notify.services(NOTIFICATION_SERVICE) \
        .notifications.create(
            to_binding='{"binding_type":"sms", "address":"' + os.environ.get('NUMBER2') + '"}',
            body=message
        )
    client.notify.services(NOTIFICATION_SERVICE) \
        .notifications.create(
            to_binding='{"binding_type":"sms", "address":"' + os.environ.get('NUMBER3') + '"}',
            body=message
        )
    client.notify.services(NOTIFICATION_SERVICE) \
        .notifications.create(
            to_binding='{"binding_type":"sms", "address":"' + os.environ.get('NUMBER4') + '"}',
            body=message
        )

def get_appts(driver, id):
    driver.get(f'https://app.careerfairplus.com/gt_ga/fair/3598/employer/{id}')
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'MuiTypography-subtitle1')))
    except:
        return 0

    appts = driver.find_elements_by_tag_name('body')
    
    num_appts = appts[0].text.count('Schedule Time')
    if id == 283580:
        return num_appts - 3
    elif id == 282457:
        return num_appts - 19
    else:
        return num_appts

def main():
    while True:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(executable_path=r"/home/justin/Documents/notifications/careerfair/geckodriver", options=options)

        companies = {
            283580: 'Amazon',
            282457: 'Google', 
            282455: 'Facebook'
        }
        for id in companies:
            num_appts = get_appts(driver, id)
            if num_appts > 0:
                message = \
    f"""There is {num_appts} available appointment with {companies[id]}.
    https://app.careerfairplus.com/gt_ga/fair/3598/employer/{id}"""
                send_msg(message)
                with open('/home/justin/Documents/notifications/careerfair/log.txt', 'a') as out:
                    out.write(f'{datetime.now()}: Sent text message with message: {message}\n\n')
        
        driver.quit()
        time.sleep(90)

if __name__ == '__main__':
    main()
