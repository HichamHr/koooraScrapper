import time
import typing
import json
from loguru import logger

from selenium.common.exceptions import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import hcaptcha_challenger as solver
from hcaptcha_challenger import HolyChallenger
from hcaptcha_challenger.exceptions import ChallengePassed


class BaseScraper:
    def __init__(self, retries: int = 10, headless=False, screenshot=True, debug=True):
        # Init local-side of the ModelHub
        solver.install()
        self.ctx = solver.get_challenge_ctx(silence=headless)
        self.retries = retries
        self.challenger = solver.new_challenger(screenshot=screenshot, debug=debug)

    def close(self):
        self.ctx.close()
        self.ctx.quit()

    def start(self, url):
        self.ctx.get(url)

    @staticmethod
    def get_selector(selector):
        if selector == "CSS_SELECTOR":
            selector = By.CSS_SELECTOR
        elif selector == "XPATH":
            selector = By.XPATH
        return selector

    def solve_captcha(self) -> typing.Optional[str]:
        """
        Use `anti_checkbox()` `anti_hcaptcha()` to be flexible to challenges
        :return:
        """
        if self.challenger.utils.face_the_checkbox(self.ctx):
            self.challenger.anti_checkbox(self.ctx)
            if res := self.challenger.utils.get_hcaptcha_response(self.ctx):
                return res

        for _ in range(self.retries):
            try:
                if (resp := self.challenger.anti_hcaptcha(self.ctx)) is None:
                    continue
                if resp == self.challenger.CHALLENGE_SUCCESS:
                    return self.challenger.utils.get_hcaptcha_response(self.ctx)
            except ChallengePassed:
                return self.challenger.utils.get_hcaptcha_response(self.ctx)
            self.challenger.utils.refresh(self.ctx)
            time.sleep(1)

    def click_action(self, selector, path, message, sleep=0):
        logger.info("start on clicking: " + message)
        WebDriverWait(self.ctx, 15, ignored_exceptions=(ElementClickInterceptedException,)).until(
            EC.element_to_be_clickable((self.get_selector(selector), path))
        ).click()
        logger.info("end on clicking: " + message)
        time.sleep(sleep)

    def send_keys_action(self, selector, path, value, message, sleep=0):
        logger.info("start on sending keys: " + message)
        WebDriverWait(self.ctx, 15, ignored_exceptions=(ElementNotInteractableException,)).until(
            EC.presence_of_element_located((self.get_selector(selector), path))
        ).send_keys(value)
        logger.info("end on sending keys: " + message)
        time.sleep(sleep)
