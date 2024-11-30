import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class Item:
    def __init__(self, title, english_title, poster_url, category, date, country, genres, description):
        self.title = title  # 中文标题
        self.english_title = english_title  # 英文标题
        self.poster_url = poster_url  # 海报链接
        self.category = category  # 类型（如电视、电影）
        self.date = date  # 发布时间
        self.country = country  # 国家
        self.genres = genres  # 类型标签（如喜剧、动画等）
        self.description = description  # 简介

    def to_dict(self):
        return {
            "title": self.title,
            "english_title": self.english_title,
            "poster_url": self.poster_url,
            "category": self.category,
            "date": self.date,
            "country": self.country,
            "genres": self.genres,
            "description": self.description,
        }


# 解析单条条目
def parse_item(div):
    try:
        title = div.find("div", class_="fs-5 fw-bold text-truncate").get_text(strip=True)
    except AttributeError:
        title = ""

    try:
        english_title = div.find("div", class_="fs-6 fw-light text-truncate mb-2").get_text(strip=True)
    except AttributeError:
        english_title = ""

    try:
        poster_url = div.find("img", class_="w-100 rounded-start")["src"]
    except (AttributeError, KeyError):
        poster_url = None

    try:
        category = div.find("span", class_="p-1 me-1 border rounded-3").get_text(strip=True)
    except AttributeError:
        category = ""

    try:
        date = div.find("span", class_="me-1 py-1 px-2 border rounded-3").get_text(strip=True)
    except AttributeError:
        try:
            date = div.find("span", class_="me-1 py-1 px-2 border rounded-3 fw-bold").get_text(strip=True)
        except AttributeError:
            date = ""

    try:
        country = div.find_all("span", class_="me-1 text-secondary")[0].get_text(strip=True)
    except (AttributeError, IndexError):
        country = ""

    try:
        genres = [span.get_text(strip=True) for span in div.find_all("span", class_="me-1 text-secondary")[1:]]
    except AttributeError:
        genres = []

    try:
        description = div.find("div", class_="pt-2 text-truncate d-none d-md-block").get_text(strip=True)
    except AttributeError:
        description = ""

    return Item(title, english_title, poster_url, category, date, country, genres, description)


def parse_items(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"解析 HTML 时出错: {e}")
        return []

    item_divs = soup.find_all("div", class_="bg-white rounded-3 border mb-3")
    items = [parse_item(div) for div in item_divs]
    return items


def get_source():
    url = "https://huo720.com/calendar/upcoming"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        return response
    except requests.RequestException as e:
        print(f"从数据源网站获取信息失败: {e}")
        return None


def save_to_json(data):
    date_str = datetime.now().strftime("%Y%m%d")
    file_name = f"{date_str}.json"
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"数据已保存到 {file_name}")
    except Exception as e:
        print(f"保存 JSON 文件时出错: {e}")


def filter_items_by_today(items):
    today_str = datetime.now().strftime("%m月%d日") 
    return [item for item in items if item.date == today_str]  


if __name__ == "__main__":
    response = get_source()
    if response:
        items = parse_items(response.text)
        filtered_items = filter_items_by_today(items)  
        items_dict = [item.to_dict() for item in filtered_items]
        save_to_json(items_dict)