import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


class DinoController:

    def __init__(self):
        self.driver = None

    def launch_browser(self):

        if self.driver is not None:
            raise RuntimeError("Browser has already been launched.")

        self.driver = webdriver.Chrome()
        print("Chrome launched successfully.")

    def _require_browser(self):

        if self.driver is None:
            raise RuntimeError("Browser has not been launched.")

        try:
            self.driver.current_window_handle

        except WebDriverException as error:
            raise RuntimeError(
                "Chrome is no longer available. "
                "It may have been closed manually."
            ) from error

        return self.driver

    def open_game(self):

        driver = self._require_browser()

        try:
            driver.get("chrome://dino/")

        except WebDriverException as error:

            if "ERR_INTERNET_DISCONNECTED" not in str(error):
                raise

        print("Chrome Dino opened.")

    def press_key(self, key):

        driver = self._require_browser()

        ActionChains(driver).send_keys(key).perform()

    def hold_key(self, key, duration):

        if (
            isinstance(duration, bool)
            or not isinstance(duration, (int, float))
            or duration <= 0
        ):
            raise ValueError("Key duration must be a positive number.")

        driver = self._require_browser()

        (
            ActionChains(driver)
            .key_down(key)
            .pause(duration)
            .key_up(key)
            .perform()
        )

    def jump(self, duration=0.1):
        self.hold_key(Keys.SPACE, duration)

    def duck(self, duration=0.2):
        self.hold_key(Keys.ARROW_DOWN, duration)

    def execute_strategy_cycle(self, strategy):

        parameters = strategy.get_parameters()

        required_parameters = {
            "jump_duration",
            "duck_duration",
            "delay_between_actions",
            "waiting_interval"
        }

        missing = required_parameters - parameters.keys()

        if missing:
            raise ValueError(
                f"Strategy is missing parameters: {', '.join(sorted(missing))}"
            )

        print("\nExecuting strategy cycle...")

        self.jump(parameters["jump_duration"])
        print(
            f"Jump action completed "
            f"({parameters['jump_duration']}s)."
        )

        time.sleep(parameters["delay_between_actions"])

        self.duck(parameters["duck_duration"])
        print(
            f"Duck action completed "
            f"({parameters['duck_duration']}s)."
        )

        time.sleep(parameters["waiting_interval"])

        print("Strategy cycle completed.")

    def close_browser(self):

        if self.driver is not None:

            try:
                self.driver.quit()
                print("Browser closed successfully.")

            except WebDriverException:
                print(
                    "Browser cleanup notice: "
                    "Chrome was already closed or disconnected."
                )

            finally:
                self.driver = None