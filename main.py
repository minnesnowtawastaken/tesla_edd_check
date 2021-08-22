import json
import os
import sys

from discord_webhook import DiscordWebhook
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

date_changed = False
discord_text = ''
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
delay = 20

with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'edd.json')) as json_file:
    edd_data = json.load(json_file)

driver.get('https://www.tesla.com/teslaaccount')

driver.find_element_by_xpath('//*[@id="form-input-identity"]').send_keys(os.environ.get('TESLA_USERNAME'))
driver.find_element_by_xpath('//*[@id="form-input-credential"]').send_keys(os.environ.get('TESLA_PASSWORD'))

driver.find_element_by_xpath('//*[@id="form-submit-continue"]').click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[2]/a')))
except TimeoutException:
    exit(1)

driver.find_element_by_xpath('//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[2]/a').click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="prod-final-deliver-desk-product-info"]/article[2]/div/span/div/h6')))
except TimeoutException:
    exit(1)

full_edd = driver.find_element_by_xpath('//*[@id="prod-final-deliver-desk-product-info"]/article[2]/div/span/div/h6').text

edd = full_edd.split(':')[1].split('-')
edd_start = edd[0].strip()
edd_end = edd[1].strip()

if not (edd_data['start'] == edd_start):
    date_changed = True
    discord_text = discord_text + '\n' + 'New starting date: {0}'.format(edd_start)
    edd_data['start'] = edd_start
if not (edd_data['end'] == edd_end):
    date_changed = True
    discord_text = discord_text + '\n' + 'New end date: {0}'.format(edd_end)
    edd_data['end'] = edd_end

if date_changed:
    webhook = DiscordWebhook(
        url=os.environ.get('ALERT_WEBHOOK'),
        content='@here {}'.format(discord_text))
    response = webhook.execute()

    with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'edd.json'), 'w') as outfile:
        json.dump(edd_data, outfile)
else:
    webhook = DiscordWebhook(
        url=os.environ.get('STATUS_WEBHOOK'),
        content='Tesla check script successfully ran')
    response = webhook.execute()

driver.close()
driver.quit()
