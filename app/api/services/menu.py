import requests
from bs4 import BeautifulSoup

def get_menu():
    """
    한양대 메뉴 이름과 가격을 튜플로 반환하는 함수

    :return: 메뉴 이름과 가격의 리스트 [(menu_name, price), ...]
    """
    MENU_URL = "https://www.hanyang.ac.kr/web/www/re12"
    request = requests.get(MENU_URL)
    soup = BeautifulSoup(request.text, "html.parser")      # HTML 내용 파싱(분석)

    menus = soup.find_all("div", class_="menu-detail")  # menu-detail 클래스의 div 요소 모두 찾기
    prices = soup.find_all("div", class_="menu-price")  # menu-price 클래스의 div 요소 모두 찾기

    result = []
    for menu, price in zip(menus, prices):              # 메뉴와 가격을 동시에 순회하며 튜플로 묶어 저장
        result.append((menu.text.strip(), price.text.strip()))      # strip()으로 불필요 공백 제거

    return result