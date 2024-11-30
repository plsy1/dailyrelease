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
    def __init__(self, title, english_title, poster_url, category, date, country, genres, description, imdb_id):
        self.title = title  # 中文标题
        self.english_title = english_title  # 英文标题
        self.poster_url = poster_url  # 海报链接
        self.category = category  # 类型（如电视、电影）
        self.date = date  # 发布时间
        self.country = country  # 国家
        self.genres = genres  # 类型标签（如喜剧、动画等）
        self.description = description  # 简介
        self.imdb_id = imdb_id # imdb序号

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
            "imdb_id": self.imdb_id
        }

class ImdbData:
    def __init__(self, title):
        if not title:
            raise ValueError("Title data is None or invalid.") 

        self.id = title.get('id', None)
        self.type = title.get('type', None)
        self.primary_title = title.get('primary_title', None)
        self.original_title = title.get('original_title', None)
        self.runtime_minutes = title.get('runtime_minutes', None)
        self.plot = title.get('plot', None)
        self.genres = title.get('genres', [])
        self.poster_urls = [p['url'] for p in title.get('posters', [])] 
        self.spoken_language_codes = [l['code'] for l in title.get('spoken_languages', [])]
        self.spoken_language_names = [l['name'] for l in title.get('spoken_languages', [])] 
        self.origin_country_codes = [c['code'] for c in title.get('origin_countries', [])]  
        self.origin_country_names = [c['name'] for c in title.get('origin_countries', [])]

# 解析单条条目
def parse_item(div):
    try:
        div_tag = div.find("div", class_="fs-5 fw-bold text-truncate")
        title = div.find("div", class_="fs-5 fw-bold text-truncate").get_text(strip=True)
        a_tag = div_tag.find("a", class_="link-dark text-truncate") if div_tag else None
        title = a_tag.get_text(strip=True) if a_tag else ""
        href = a_tag.get("href") if a_tag else ""
    except AttributeError:
        title = ""
        
    try:
        div_tag = div.find("div", class_="fs-5 fw-bold text-truncate")
        a_tag = div_tag.find("a", class_="link-dark text-truncate") if div_tag else None
        href = a_tag.get("href") if a_tag else ""
    except AttributeError:
        href = ""

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
        
    try:
        if href:
            url = f"https://huo720.com{href}"  
            response = get_html(url) 
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                div_imdb = soup.find("div", class_="rounded-3 text-bg-warning d-inline p-1", string="IMDb")
                h3_tag = div_imdb.find_next("h3", class_="mb-0 pt-2 text-light")
                a_tag = h3_tag.find("a") if h3_tag else None
                imdb_id = a_tag['href']
                pattern = r"/title/tt(\d+)"
                match = re.search(pattern, imdb_id)
                imdb_id = f'tt{match.group(1)}'
    except Exception as e:
        imdb_id = ''
        print(f"发生错误: {e}")
        
    return Item(title, english_title, poster_url, category, date, country, genres, description,imdb_id)


def parse_items(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"解析 HTML 时出错: {e}")
        return []

    item_divs = soup.find_all("div", class_="bg-white rounded-3 border mb-3")
    items = [parse_item(div) for div in item_divs]
    
    # 测试用
    #items = [parse_item(item_divs[0])]
    
    return items


def get_html(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        return response
    except requests.RequestException as e:
        print(f"从数据源网站获取信息失败: {e}")
        return None

def save_to_json(data, date):
    # 将日期格式化为 YYYYMMDD
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

def replace_imdb_info(item: Item):
    imdb_id = item.imdb_id
    url = 'https://graph.imdbapi.dev/v1'
    query = f"""
    query titleById {{
      title(id: "{imdb_id}") {{
        id
        type
        primary_title
        original_title
        runtime_minutes
        plot
        genres
        posters {{
          url
        }}
        spoken_languages {{
          code
          name
        }}
        origin_countries {{
          code
          name
        }}
      }}
    }}
    """

    response = requests.post(url, json={'query': query})
    data = response.json().get('data', {})
    imdbData = ImdbData(data['title'])
    
    item.poster_url = imdbData.poster_urls[0] if imdbData.poster_urls else item.poster_url
    item.description = imdbData.plot if imdbData.plot else item.description

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
        
if __name__ == "__main__":
    country_data = load_country_data()
    response = get_html("https://huo720.com/calendar/upcoming")
    if response:
        items = parse_items(response.text)
        items_dict = [item.to_dict() for item in items]
        current_year = datetime.now().year
        for item in items:
            replace_imdb_info(item)
            convert_country_name_to_chinese(item)
            item_date = datetime.strptime(item.date, "%m月%d日").replace(year=current_year)
            formatted_date = item_date.strftime("%Y%m%d")  
            save_to_json([item.to_dict()], formatted_date)