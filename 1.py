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
            
            if date.split(" ")[0].replace("号", "") == datetime.now().strftime("%d"):
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



def get_date(date_str):
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m")
    day = date_str.split(" ")[0].replace("号", "")
    formatted_day = day.zfill(2)
    return f"{formatted_date}{formatted_day}"


if __name__ == "__main__":
    response = get_html("https://yysub.net/tv/schedule")
    if response:
        result = parse_items(response.text)
        for item in result:
            print(item)
