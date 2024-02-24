'''
this is the main module which starts everything.
'''

import logger_setup
import open_tv
from time import time
from time import sleep

# Set up logger for this file
main_logger = logger_setup.setup_logger(__name__, logger_setup.logging.DEBUG)

SCREENER_SHORT = 'Screener' # short title of the screener
DRAWER_SHORT = 'Trade' # short title of the trade drawer indicator 
SCREENER_NAME = 'Premium Screener' # name of the screener
DRAWER_NAME = 'Trade Drawer' # name of the trade drawer
REMOVE_LOG = True # remove the content of the log file (to clean it up)
INTERVAL_MINUTES = 60 # number of mins to wait until inactive alerts get reactivated and for the browser to refresh (refreshing will hopefully prevent the browser and this application from freezing)

# Convert the interval to seconds
interval_seconds = INTERVAL_MINUTES * 60

# Clean up the log
if REMOVE_LOG:
    with open('app_log.log', 'w') as file:
        pass

# Run main code
if __name__ == '__main__':
    try:
        # Just a seperator to make the log look readable
        main_logger.info('***********************************************************************************')

        # initiate Browser
        browser = open_tv.Browser(True, SCREENER_SHORT, SCREENER_NAME, DRAWER_SHORT, DRAWER_NAME, INTERVAL_MINUTES)

        # setup the indicators, alerts etc.
        setup_check = browser.setup_tv()

        # set up alerts for all the symbols
        browser.set_bulk_alerts()

        if setup_check and browser.init_succeeded:
            last_run = time()
            while True:
                # restart all the inactive alerts every INTERVAL_MINUTES minutes (this is also done in get_alert_data.py in the method get_alert_box_and_msg()) and refresh browser
                if time() - last_run > interval_seconds:
                    try:
                        browser.driver.refresh()
                        browser.WebDriverWait(browser.driver, 10).until(lambda x: x.execute_script('return document.readyState') == 'complete') # wait for the page to re-load after refreshing it
                        main_logger.info('Browser refreshed to prevent browser from getting frozen.')
                    except:
                        main_logger.exception('Failed to refresh browser. Error:')
                    
                    browser.alerts.restart_inactive_alerts()
                    last_run = time()

                # get entries from the alerts which come and post them
                alert = browser.alerts.get_alert()
                browser.alerts.post(alert, browser.indicator_visibility)
    except Exception as e:
        main_logger.exception(f'Error in main.py:')
 