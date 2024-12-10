import requests
import json
import os
from datetime import datetime

accessToken = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYmE3ZTA0MWYyOGY5ZDAyNzNhMDIyYjc3NjRlZjgzZCIsIm5iZiI6MTY5NTE0NzY5OS4wNDYwMDAyLCJzdWIiOiI2NTA5ZTZiM2NhZGI2YjAwYzRmNmYzZTQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.ISi9GUXPRsWXnqBf6jR6TZBvgzdwozUmOXDESCQPSuI"


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
        "nb": "挪威语(伯克梅尔)",
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
        "zh": "中文",
        "cn": "中文",
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
        10759: "动作与冒险",   # Action & Adventure
        10762: "儿童",       # Kids
        10763: "新闻",       # News
        10764: "真人秀",     # Reality
        10765: "科幻与奇幻", # Sci-Fi & Fantasy
        10766: "肥皂剧",     # Soap
        10767: "脱口秀",     # Talk
        10768: "战争与政治", # War & Politics
    }

    # 获取 genre_ids 对应的中文名称
    return [genre_mapping.get(id, id) for id in genre_ids]


def save_filtered_shows(data):
    """
    根据 first_air_date 与当前日期比较，过滤结果并保存到按日期命名的 JSON 文件，避免重复 ID。

    Args:
        data (dict): 包含节目列表的 API 响应数据。
    """

    # 过滤出符合条件的节目
    filtered_results = [
        show for show in data.get("results", []) if "first_air_date" in show
    ]

    # 根据 first_air_date 进行分组
    grouped_by_date = {}
    for show in filtered_results:
        first_air_date = datetime.strptime(show["first_air_date"], "%Y-%m-%d").date()
        date_str = first_air_date.strftime("%Y%m%d")  # 格式化为 yyyymmdd

        # 使用字典分组，根据日期存储
        if date_str not in grouped_by_date:
            grouped_by_date[date_str] = []
        grouped_by_date[date_str].append(show)

    # 遍历分组并保存每个日期的 JSON 文件
    for date_str, shows in grouped_by_date.items():
        filename = f"{date_str}.json"

        # 加载现有数据
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # 合并并去重（基于 id）
        combined_data = {item["id"]: item for item in existing_data + shows}.values()
        
        # 保存去重后的结果
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(list(combined_data), file, ensure_ascii=False, indent=4)

        print(f"Filtered results for {date_str} saved to {filename}")


def get_tv_shows(with_networks):
    try:
        url = f"https://api.themoviedb.org/3/discover/tv"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "accept": "application/json",
        }
        params = {
            "include_adult": "false",
            "include_null_first_air_dates": "false",
            "language": "zh-CN",
            "page": 1,
            "sort_by": "first_air_date.desc",
            "timezone": "Asia/Shanghai",
            "with_networks": with_networks,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            for show in data.get("results", []):
                show["network_id"] = with_networks
                show["genre_ids"] = replace_genre_ids(show["genre_ids"])
                show["original_language_zh"] = replace_language_codes(
                    show["original_language"]
                )
                show["origin_country"] = replace_country_codes(show["origin_country"])
                if show["original_language"] == 'cn':
                    show["original_language"] = 'zh'
            return data
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except Exception as e:
        print("Request TMDB API ERROR", e)


networks = [
    "97898",
    "1330",
    "2007",
    "1631",
    "1605",
    "1363",
    "521",
    "213",
    "2552",
    "2739",
    "1024",
    "49",
    '6783',
    "453",
    "3353",
    "4330",
    "64",
    "6",
    "16",
    "2",
    "2334",
    "160",
    "3341",
    "103",
    "98",
    "57",
    "94",
]

for network in networks:
    result = get_tv_shows(network)
    save_filtered_shows(result)
