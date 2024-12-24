from datetime import datetime

# 假设你从a标签中提取到的日期是 '1号'
date_str = '1号'

# 获取当前日期，格式化为 'yyyy-MM' 格式
current_date = datetime.now()
formatted_date = current_date.strftime("%Y%m")

# 提取日期中的日期部分并去掉“号”字
day = date_str.replace('号', '')

# 将日期格式化为两位数
formatted_day = day.zfill(2)

# 合并成完整的 'yyyyMMdd' 格式
full_date = f"{formatted_date}{formatted_day}"

print(full_date)  # 输出：2024-12-01