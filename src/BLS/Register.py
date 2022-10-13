import time

from src.Scraper.Base import BaseScraper

indexUrl = "https://blsspainmorocco.com/index.php"
finalUrl = ""
headless = False


def register():
    # New Challenger
    base_scraper = BaseScraper(1, False, True, True)
    base_scraper.start(indexUrl)

    try:
        # CLose PopUp
        base_scraper.click_action("CSS_SELECTOR", ".popupCloseIcon", "Close PopUp", 2)

        # CLose cookies dialog
        base_scraper.click_action("XPATH", "//a[@onclick='setCookie();']", "CLose cookies dialog", 2)

        time.sleep(1)

        # Navigate To Login Page
        base_scraper.click_action("XPATH", "//a[@class='visaProcessItemBox' and @href='login.php']",
                                  "Navigate To Login Page", 4)

        # Navigate To Register Page
        base_scraper.click_action("XPATH", "//a[@href='register.php']", "Navigate To Register Page", 4)

        # Set Inputs
        base_scraper.send_keys_action("XPATH", "//input[@name='user_name']", "UserName", "Set Username Input", 1)
        base_scraper.send_keys_action("XPATH", "//input[@name='user_email']", "mrcharifmakaoui@gmail.com",
                                      "Set Email Input", 1)
        base_scraper.send_keys_action("XPATH", "//input[@name='user_mobile_no']", "0661315922", "Set Phone Input", 1)
        base_scraper.send_keys_action("XPATH", "//select[@name='user_location']", "Casablanca", "Set Location Input", 1)

        # If Captcha exist execute this line
        base_scraper.solve_captcha()
        time.sleep(3)

        # Click on register button
        base_scraper.click_action("XPATH", "//input[@name='register' and @type='submit']", "Click on register button",
                                  4)

        time.sleep(15)
    finally:
        base_scraper.close()


if __name__ == "__main__":
    register()
