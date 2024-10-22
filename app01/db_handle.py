import csv
from datetime import datetime


# Function to format the date
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M")
    return date_obj.strftime("%B %d, %Y")


def extract_after_dot(input_string):
    # 使用 split() 方法以点号为分隔符将字符串拆分成两部分
    parts = input_string.split(".")

    # 如果拆分结果包含至少两个部分，则返回点号后面的部分
    if len(parts) > 1:
        return parts[1]
    else:
        # 如果没有点号，或者点号位于字符串的末尾，则返回空字符串
        return ""


# Read the CSV file
def db_handle(rules, num=0):
    csv_file = 'media/blog_info_table.csv'  # Replace with the actual file path
    output_list = []

    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        row_count = 0
        for row in csv_reader:
            formatted_date = format_date(row['date'])
            categories = [cat.strip() for cat in row['category'].split(',')]

            if extract_after_dot(row["link"]) == 'pdf':
                file_type =  None
            else:
                file_type = 1

            if row['class'] in rules:
                item = {
                    "pic": row['pic'],
                    "date": formatted_date,
                    "category": ", ".join(categories),
                    "title": row['title'],
                    "content": row['content'],
                    "link": row['link'],
                    "encryption": row['encryption'],
                    "class": row['class'],
                    "filetype": file_type
                }
                output_list.append(item)
                row_count += 1
                if row_count == num:
                    break

    # Print the first item as an example
    return output_list
