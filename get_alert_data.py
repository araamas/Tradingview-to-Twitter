'''
This module gets the entry signals from the premium screener on tradingview 
by getting text from alerts
'''

# import modules
import time
import open_entry_chart
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# class
class Alerts:

  def __init__(self, driver) -> None:
    self.driver = driver
    self.chart = open_entry_chart.OpenChart(self.driver)
    
  def read_alert(self, msg):
    lines = msg.split('\n')
    self.close_alert()

    for line in lines:
      parts = line.split('|')
      if 'Buy' in line or 'Sell' in line:
        print('\n',line)
        self.chart.change_symbol(parts[4])
        self.chart.change_tframe(parts[5])
        self.chart.change_indicator_settings(parts[1], parts[2], parts[3])

  def close_alert(self):
    ok_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-D4RPB3ZC.size-small-D4RPB3ZC.color-brand-D4RPB3ZC.variant-primary-D4RPB3ZC")))
    ok_button.click()

  def get_data_from_alert(self):
    while True:
      try:
        alert_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.secondaryRow-QkiHQU0S")))
        self.read_alert(alert_msg.text)
        alert_msg = None
      except Exception as e:
        continue
      