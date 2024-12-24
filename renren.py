import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


class Item:
    def __init__(self, title, link, ep, date, status):
        self.title = title
        self.link = link
        self.ep = ep
        self.date = date
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "ep": self.ep,
            "date": self.date,
            "status": self.status,
        }

    def __repr__(self):
        return f"Item(title={self.title}, link={self.link}, ep={self.ep}, date={self.date},status={self.status})"


class ImdbData:
    def __init__(self, title):
        if not title:
            raise ValueError("Title data is None or invalid.")

        self.id = title.get("id", None)
        self.type = title.get("type", None)
        self.primary_title = title.get("primary_title", None)
        self.original_title = title.get("original_title", None)
        self.runtime_minutes = title.get("runtime_minutes", None)
        self.plot = title.get("plot", None)
        self.genres = title.get("genres", [])
        self.poster_urls = [p["url"] for p in title.get("posters", [])]
        self.spoken_language_codes = [
            l["code"] for l in title.get("spoken_languages", [])
        ]
        self.spoken_language_names = [
            l["name"] for l in title.get("spoken_languages", [])
        ]
        self.origin_country_codes = [
            c["code"] for c in title.get("origin_countries", [])
        ]
        self.origin_country_names = [
            c["name"] for c in title.get("origin_countries", [])
        ]


def parse_items(html_content):
    """
    从网页内容中提取每日节目安排的项目。
    """
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    days = table.find_all("td", class_="ihbg")

    # 存储解析结果
    schedule = []

    for day in days:
        date_info = day.find("dt")
        if not date_info:
            continue

        date_text = date_info.get_text(strip=True)
        episodes = day.find_all("dd")

        for episode in episodes:
            a_tag = episode.find("a")
            if a_tag:
                title = "".join(a_tag.find_all(string=True, recursive=False)).strip()
                link = a_tag["href"]

            spans = a_tag.find_all("span")
            if len(spans) >= 2:
                ep = spans[0].get_text(strip=True)
                status = spans[1].get_text(strip=True)
            else:
                ep = spans[0].get_text(strip=True)
                status = None

            date = date_text

            schedule.append(Item(title, f'https://yysub.net{link}', ep, date, status))

    return schedule


def get_html(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"从数据源网站获取信息失败: {e}")
        return None


def save_to_json(data, date):
    file_name = f"{date}.json"

    # 如果文件已经存在，加载现有数据并追加新条目
    if os.path.exists(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except Exception as e:
            print(f"读取现有 JSON 文件时出错: {e}")
            existing_data = []
    else:
        existing_data = []

    # 合并现有数据和新数据
    existing_data.extend(data)

    # 保存合并后的数据到对应的文件
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        print(f"数据已保存到 {file_name}")
    except Exception as e:
        print(f"保存 JSON 文件时出错: {e}")


def load_country_data(file_path="country-code.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_chinese_name_from_json(country_name):
    """
    根据英文国家名称从 JSON 中获取中文名称。
    :param country_name: 英文国家名称
    :return: 中文名称（如果找不到则返回原始英文名称）
    """
    for country in country_data:
        if country["en"] == country_name:
            return country["cn"]
    return country_name


def convert_country_name_to_chinese(item):
    """
    将 Item 的国家英文名称转换为中文（使用 JSON 数据）。
    :param item: 包含国家信息的 Item 对象
    """
    country_name = item.country
    chinese_name = get_chinese_name_from_json(country_name)
    item.country = chinese_name


def get_date(date_str):
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m")
    day = date_str.split(" ")[0].replace("号", "")
    formatted_day = day.zfill(2)
    return f"{formatted_date}{formatted_day}"


if __name__ == "__main__":
    country_data = load_country_data()
    response = get_html("https://yysub.net/tv/schedule")
    if response:
        result = parse_items(response.text)
        for item in result:
            item.date = get_date(item.date)
            save_to_json([item.to_dict()], item.date)
