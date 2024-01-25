from .utils.selenium_base import WebDriverUtility

if __name__ == '__main__':
    """
    MasterCralwer 인스턴스
    """
    masterCrawler = WebDriverUtility()

    print(masterCralwer)
    print(masterCrawler.driver)

    element = masterCrawler.targeting_element("id", "Title")
    """Title ID 반환"""
    link_elements = masterCrawler.targeting_elements_list("div", "a", element)
    """ 위 엘리먼트 내부에서 a tag 리스트 반환"""

