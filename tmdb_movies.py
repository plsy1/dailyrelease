import requests
import json
import os
from datetime import datetime
import pytz

accessToken = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYmE3ZTA0MWYyOGY5ZDAyNzNhMDIyYjc3NjRlZjgzZCIsIm5iZiI6MTY5NTE0NzY5OS4wNDYwMDAyLCJzdWIiOiI2NTA5ZTZiM2NhZGI2YjAwYzRmNmYzZTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.ISi9GUXPRsWXnqBf6jR6TZBvgzdwozUmOXDESCQPSuI"
base_url = "https://api.themoviedb.org/3/discover/movie"

def replace_language_codes(code):
    """
    根据语言代码列表替换为语言名称。

    Args:
        language_codes (list): 包含语言代码的列表（例如 ['en', 'zh', 'es']）。

    Returns:
        list: 替换后的语言名称列表。
    """
    language_mapping = {
        "af": "南非语",
        "ar": "阿拉伯语",
        "az": "阿塞拜疆语",
        "be": "比利时语",
        "bg": "保加利亚语",
        "ca": "加泰隆语",
        "cs": "捷克语",
        "cy": "威尔士语",
        "da": "丹麦语",
        "de": "德语",
        "dv": "第维埃语",
        "el": "希腊语",
        "en": "英语",
        "eo": "世界语",
        "es": "西班牙语",
        "et": "爱沙尼亚语",
        "eu": "巴士克语",
        "fa": "法斯语",
        "fi": "芬兰语",
        "fo": "法罗语",
        "fr": "法语",
        "gl": "加里西亚语",
        "gu": "古吉拉特语",
        "he": "希伯来语",
        "hi": "印地语",
        "hr": "克罗地亚语",
        "hu": "匈牙利语",
        "hy": "亚美尼亚语",
        "id": "印度尼西亚语",
        "is": "冰岛语",
        "it": "意大利语",
        "ja": "日语",
        "ka": "格鲁吉亚语",
        "kk": "哈萨克语",
        "kn": "卡纳拉语",
        "ko": "韩语",
        "kok": "孔卡尼语",
        "ky": "吉尔吉斯语",
        "lt": "立陶宛语",
        "lv": "拉脱维亚语",
        "mi": "毛利语",
        "mk": "马其顿语",
        "mn": "蒙古语",
        "mr": "马拉地语",
        "ms": "马来语",
        "mt": "马耳他语",
        "no": "挪威语",
        "nl": "荷兰语",
        "ns": "北梭托语",
        "pa": "旁遮普语",
        "pl": "波兰语",
        "pt": "葡萄牙语",
        "qu": "克丘亚语",
        "ro": "罗马尼亚语",
        "ru": "俄语",
        "sa": "梵文",
        "se": "北萨摩斯语",
        "sk": "斯洛伐克语",
        "sl": "斯洛文尼亚语",
        "sq": "阿尔巴尼亚语",
        "sv": "瑞典语",
        "sw": "斯瓦希里语",
        "syr": "叙利亚语",
        "ta": "泰米尔语",
        "te": "泰卢固语",
        "th": "泰语",
        "tl": "塔加路语",
        "tn": "茨瓦纳语",
        "tr": "土耳其语",
        "ts": "宗加语",
        "tt": "鞑靼语",
        "uk": "乌克兰语",
        "ur": "乌都语",
        "uz": "乌兹别克语",
        "vi": "越南语",
        "xh": "班图语",
        "zh": "汉语",
        "cn": "汉语",
        "zu": "祖鲁语",
    }

    return language_mapping.get(code, code)


def replace_country_codes(origin_country):
    country_mapping = {
        "CN": "中国",
        "US": "美国",
        "JP": "日本",
        "KR": "韩国",
        "GB": "英国",
        "DE": "德国",
        "FR": "法国",
        "IN": "印度",
        "IT": "意大利",
        "BR": "巴西",
        "CA": "加拿大",
        "AU": "澳大利亚",
        "RU": "俄罗斯",
        "MX": "墨西哥",
        "ZA": "南非",
        "ES": "西班牙",
        "AR": "阿根廷",
        "EG": "埃及",
        "NG": "尼日利亚",
        "TR": "土耳其",
        "SE": "瑞典",
        "NO": "挪威",
        "FI": "芬兰",
        "DK": "丹麦",
        "PL": "波兰",
        "PT": "葡萄牙",
        "NL": "荷兰",
        "BE": "比利时",
        "CH": "瑞士",
        "AT": "奥地利",
        "SG": "新加坡",
        "TH": "泰国",
        "PH": "菲律宾",
        "ID": "印度尼西亚",
        "ZA": "南非",
        "MY": "马来西亚",
        "KW": "科威特",
        "QA": "卡塔尔",
        "UA": "乌克兰",
        "EG": "埃及",
        "CO": "哥伦比亚",
        "VE": "委内瑞拉",
        "PE": "秘鲁",
        "CL": "智利",
        "GT": "危地马拉",
        "HN": "洪都拉斯",
        "CR": "哥斯达黎加",
        "EC": "厄瓜多尔",
        "PY": "巴拉圭",
        "BO": "玻利维亚",
        "CU": "古巴",
        "DO": "多米尼加",
        "JM": "牙买加",
        "LC": "圣卢西亚",
        "TT": "特立尼达和多巴哥",
        "LB": "黎巴嫩",
        "JO": "约旦",
        "KW": "科威特",
        "AE": "阿联酋",
        "SA": "沙特阿拉伯",
        "OM": "阿曼",
        "YE": "也门",
        "IR": "伊朗",
        "IQ": "伊拉克",
        "SY": "叙利亚",
        "KW": "科威特",
        "KZ": "哈萨克斯坦",
        "UZ": "乌兹别克斯坦",
        "TJ": "塔吉克斯坦",
        "KG": "吉尔吉斯斯坦",
        "TM": "土库曼斯坦",
        "PK": "巴基斯坦",
        "AF": "阿富汗",
        "LK": "斯里兰卡",
        "NP": "尼泊尔",
        "MM": "缅甸",
        "BD": "孟加拉国",
        "KH": "柬埔寨",
        "LA": "老挝",
        "MN": "蒙古",
        "BT": "不丹",
        "KW": "科威特",
        "QA": "卡塔尔",
        "KH": "柬埔寨",
        "LK": "斯里兰卡",
        "NG": "尼日利亚",
        "GH": "加纳",
        "KE": "肯尼亚",
        "UG": "乌干达",
        "TZ": "坦桑尼亚",
        "RW": "卢旺达",
        "ZW": "津巴布韦",
        "MO": "澳门",
        "TW": "台湾",
        "HK": "香港",
    }

    return [country_mapping.get(id, id) for id in origin_country]


def replace_genre_ids(genre_ids):
    """
    根据 genre_ids 列表中的数字 ID 替换为对应的中文名称。

    Args:
        genre_ids (list): 包含 genre_ids 的列表（例如 [28, 12, 16]）。

    Returns:
        list: 替换后的中文名称列表，例如 ["动作", "冒险", "动画"]。
    """
    genre_mapping = {
        28: "动作",
        12: "冒险",
        16: "动画",
        35: "喜剧",
        80: "犯罪",
        99: "纪录",
        18: "剧情",
        10751: "家庭",
        14: "奇幻",
        36: "历史",
        27: "恐怖",
        10402: "音乐",
        9648: "悬疑",
        10749: "爱情",
        878: "科幻",
        10770: "电视电影",
        53: "惊悚",
        10752: "战争",
        37: "西部",
    }

    # 获取 genre_ids 对应的中文名称
    return [genre_mapping.get(id, id) for id in genre_ids]

def save_filtered_movies(data):
    """
    根据传入的数据过滤并保存到按日期命名的 JSON 文件中，避免重复 ID。

    Args:
        data (list): 包含电影信息的列表，每部电影应包含 "id" 和 "first_air_date"。
    """
 
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of movie data, but got {type(data).__name__}")
    tz = pytz.timezone('Asia/Shanghai')
    today_date = datetime.now(tz).strftime("%Y%m%d")
    filename = f"{today_date}.json"


    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []


    if not isinstance(existing_data, list):
        raise ValueError(f"Invalid JSON format in {filename}: expected a list")

    all_data = {item["id"]: item for item in existing_data if isinstance(item, dict)}  # 先加入现有数据
    for movie in data:
        if not isinstance(movie, dict) or "id" not in movie:
            print(f"Skipping invalid movie entry: {movie}")
            continue
        if movie["original_language"] == 'cn':
            movie["original_language"] = 'zh'
        movie["genre_ids_zh"] = replace_genre_ids(movie["genre_ids"])
        movie["original_language_zh"] = replace_language_codes(
            movie["original_language"]
        )
        all_data[movie["id"]] = movie 

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(all_data.values()), file, ensure_ascii=False, indent=4)

    print(f"Movies results saved to {filename}")
        
def fetch_all_movies_for_today(language):
    """
    分页获取当天的电影信息，直到没有更多结果为止。

    Args:
        language (str): 语言代码，例如 "zh-CN" 或 "en-US"。

    Returns:
        list: 包含当天所有电影信息的列表。
    """
    
    tz = pytz.timezone('Asia/Shanghai')
    today_date = datetime.now(tz).strftime("%Y-%m-%d")

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "zh-CN",
        "primary_release_date.gte": today_date,
        "primary_release_date.lte": today_date,
        "sort_by": "popularity.desc",
        "with_original_language": language,
        "page": 1,  
    }

    headers = {
        "Authorization": f"Bearer {accessToken}",
        "accept": "application/json",
    }

    all_results = [] 

    while True:
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:  
                break

            all_results.extend(results)

            if params["page"] >= data.get("total_pages", 1):
                break

            params["page"] += 1

        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break

    return all_results  

languages = ['zh','cn','en','ja','ko','th','de','fr','es','pt','ru','it','nl','pl','hi','tr','sv','no','fi']
for language in languages:
    result = fetch_all_movies_for_today(language)
    save_filtered_movies(result)
