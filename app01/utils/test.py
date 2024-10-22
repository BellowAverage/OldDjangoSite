def generate_complex_sql_filter(comment_length=(0, 200), player_level=(0, 60), recharge_amount=(0, 100000),
                                sentiment_type=None, text_search=None):
    conditions = []

    # 添加评论字数条件
    min_length, max_length = comment_length
    conditions.append(f"LENGTH(`评论内容`) >= {min_length} AND LENGTH(`评论内容`) <= {max_length}")

    # 添加玩家等级条件
    min_level, max_level = player_level
    conditions.append(f"`玩家等级` >= {min_level} AND `玩家等级` <= {max_level}")

    # 添加累计充值条件
    min_recharge, max_recharge = recharge_amount
    conditions.append(f"`累计充值rmb` >= {min_recharge} AND `累计充值rmb` <= {max_recharge}")

    # 添加情感分类条件
    if sentiment_type:
        if sentiment_type == 'positive':
            conditions.append("`情感分类` = '满意'")
        elif sentiment_type == 'negative':
            conditions.append("`情感分类` != '满意'")

    # 添加文本搜索条件
    if text_search:
        conditions.append(f"`评论内容` LIKE '%{text_search}%'")

    # 构建 SQL 查询语句
    sql = "SELECT * FROM `dim_sentiment` WHERE " + " AND ".join(conditions) + ";"
    return sql

    # 例如，查询含有“棒”，评论字数在（1，500），玩家等级大于20级，情感分类为positive，累计充值大于1000的数据的 SQL 语句


comment_length = (0, 500)
player_level = (0, 60)  # 大于20级，小于等于60级
recharge_amount = (0, 100000)  # 大于1000，小于等于100000
sentiment_type = "negative"
text_search = ""

result_sql = generate_complex_sql_filter(comment_length, player_level, recharge_amount, sentiment_type, text_search)
print(result_sql)

