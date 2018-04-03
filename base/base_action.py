import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BaseAction:

    def __init__(self, driver):
        self.driver = driver

    def click(self, loc, time=10, poll=1):
        self.find_element(loc, time, poll).click()

    def input_text(self, loc, text, time=10, poll=1):
        self.find_element(loc, time, poll).send_keys(text)

    def clear_text(self, loc, time=10, poll=1):
        self.find_element(loc, time, poll).clear()

    def back(self):
        self.driver.keyevent(4)

    def find_element(self, loc, time=10, poll=1):
        loc_by, loc_value = loc
        if loc_by == By.XPATH:
            loc_value = self.make_xpath_with_feature(loc_value)
        return WebDriverWait(self.driver, time, poll).until(lambda x: x.find_element(loc_by, loc_value))

    def find_elements(self, loc, time=10, poll=1):
        loc_by, loc_value = loc
        if loc_by == By.XPATH:
            loc_value = self.make_xpath_with_feature(loc_value)
        return WebDriverWait(self.driver, time, poll).until(lambda x: x.find_elements(loc_by, loc_value))

    def scroll_page_one_time(self, direction="down"):
        window_size = self.driver.get_window_size()
        window_height = window_size["height"]
        window_width = window_size["width"]
        end_y = window_height * 0.25
        start_y = end_y * 3
        center_x = window_width * 0.5

        if direction == "down":
            self.driver.swipe(center_x, start_y, center_x, end_y)
        elif direction == "up":
            self.driver.swipe(center_x, end_y, center_x, start_y)
        else:
            raise Exception("请输入正确的direction参数")


    # 滑动当前页面到某个元素出现
    def scroll_page_until_loc(self, loc, direction="down"):
        while True:
            try:
                self.find_element(loc)
                break
            except Exception:

                self.scroll_page_one_time(direction)
                time.sleep(1)

    def make_xpath_with_feature(self, feature):
        xpath_start = "//*["
        xpath_end = "]"
        xpath = ""
        if isinstance(feature, str):
            xpath = self.make_xpath_with_unit_feature(feature)
        else:
            for i in feature:
                xpath = xpath + self.make_xpath_with_unit_feature(i)
        xpath = xpath.rstrip("and")
        xpath = xpath_start + xpath + xpath_end
        return xpath

    def make_xpath_with_unit_feature(self, unit_feature):
        xpath = ""
        args = unit_feature.split(",")
        if len(args) == 2:
            xpath = xpath + "@" + args[0] + "='" + args[1] + "'and"
        elif len(args) == 3:
            if args[2] == "1":
                xpath = xpath + "contains(@" + args[0] + ",'" + args[1] + "')and"
            elif args[2] == "0":
                xpath = xpath + "@" + args[0] + "='" + args[1] + "'and"
        return xpath

