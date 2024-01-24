from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

class WebDriverUtility:
    """
    셀레니움 크롤링의 반복을 줄이기 위한 웹 코드
    모든 인스턴스에서 공유
    """
    #Initialize Driver, WebDriverWait, ActionChins
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()))
    WebDriverWait = WebDriverWait(driver, 30)
    action = ActionChains(driver)

    tag2ref = {
        "xpath": By.XPATH,
        "id": By.ID,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME,
        "css_selector": By.CSS_SELECTOR
    }
    def __init__(self):
        pass

    @classmethod
    def regex_newline(cls, input_text: str) -> str:
        """ 개행 문자 제거
        개행 문자를 제거한 문자열을 반환
        :param input_text: 스크랩된 문자열 입력.
        :return: 개행 문자를 제거한 문자열 반환.
        """
        cleaned_text = re.sub('[\n]', '', input_text)
        return cleaned_text

    @classmethod
    def wait_element_loading(cls, tag_name: str, element: str) -> bool:
        """엘리먼트의 로딩 대기
        :param tag_name: 로딩을 기다릴 엘리먼트의 태그명 입력
        :param element: 로딩을 기다릴 엘리먼트 입력
        :return: bool
        """
        element = WebDriverWait(WebDriverUtility.driver, 10).until(
            EC.presence_of_element_located((cls.tag2ref[tag_name],
                                            element))
        )
        if element:
            return True
        else:
            return False

    @classmethod
    def click_element(cls, tag_name: str, element: str):
        """엘리먼트 클릭
        :param tag_name: 클릭할 태그명 입력
        :param element: 클릭할 엘리먼트 입력
        :return: None
        """
        WebDriverUtility.driver.find_element(
            by=cls.tag2ref[tag_name],
            value=element).click()
    @classmethod
    def targeting_element(cls, tag_name: str, element: str, parent_element=None):
        """엘리먼트 타겟팅
        특정 부분의 엘리먼트 target
        :param tag_name: 타켓팅 할 엘리먼트 태그
        :param element: 타게팅 할 엘리먼트 이름
        :param parent_element: 타겟된 엘리먼트
        :return: element return
        """
        if parent_element is None:
            target_element = WebDriverUtility.driver.find_element(
                by=cls.tag2ref[tag_name],
                value=element)
        else:
            target_element = parent_element.find_element(
                by=cls.tag2ref[tag_name],
                value=element)

        return target_element

    @classmethod
    def targeting_elements_list(cls, tag_name, element, parent_element=None):
        """엘리먼트들을 포함하는 리스트
        단일 개체를 가지는 xpath, id 는 사용하지 않음.
        :param tag_name: 타게팅 할 엘리먼트 태그
        :param element: 타게팅 할 엘리먼트 이름
        :param parent_element: 타겟된 엘리먼트
        :return: 엘리먼트들의 리스트
        """
        if parent_element is None:
            target_elements = WebDriverUtility.driver.find_elements(by=cls.tag2ref[tag_name], value=element)
        else:
            target_elements = parent_element.find_elements(by=cls.tag2ref[tag_name], value=element)
        return target_elements
    def __del__(self):
        WebDriverUtility.driver.quit()


