import time
from RPA.Browser.Selenium import Selenium

class Browser:
    def __init__(self, interaction_wait, typing_wait, goto_wait):
        self.__browser = Selenium()
        self.__interaction_wait = interaction_wait
        self.__typing_wait = typing_wait
        self.__goto_wait = goto_wait

    def goto(self, url):
        self.__browser.open_available_browser(url, maximized=True)
        time.sleep(self.__goto_wait)

    def click_button(self, visible_only = 0, text = None, qclass = None, data_test_id=None):
        locator = ''

        if(type(text) != type(None)):
            locator = "text()='" + text + "'"
        elif(type(qclass) != type(None)):
            locator = "@class='" + qclass + "'"
        elif(type(data_test_id) != type(None)):
            locator = "@data-testid='" + data_test_id + "'"
        else:
            raise Exception('selector clause missing')

        if(visible_only == 0):
            self.__browser.click_button("//button[" + locator + "]")
        else:
            self.__browser.click_button_when_visible("//button[" + locator + "]")

        time.sleep(self.__interaction_wait)
    
    # def click_element(self, qclass=None, data=None):
    #     self.__browser.click_element('class:' + qclass)
    #     time.sleep(self.__interaction_wait)

    # def click_element(self, data):
    #     self.__browser.click_element('data:' + data)
    #     time.sleep(self.__interaction_wait)

    def click_element(self, css):
        self.__browser.click_element('css:' + css)
        time.sleep(self.__interaction_wait)

    def input_text(self, css, text):
        self.__browser.input_text('css:' + css, text)
        time.sleep(self.__typing_wait)

    def find_elements(self, css):
        return self.__browser.find_elements('css:' + css)