from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# Check your chrome version and download appropriate executable from https://chromedriver.chromium.org/downloads
# update executable_path argument to the location of chromedriver.exe
def configure_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(executable_path='C:/Users/KarnaveeKamdar/Downloads/chromedriver_win32/chromedriver.exe',
    #                           chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(60)
    return driver
