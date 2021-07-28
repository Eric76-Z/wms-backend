import copy

import pymysql


# fields为表头，将数据库中筛选出的results与表头拼接，生成字典。不断遍历，多个字典添加到列表，最后赋值给rows
def toRows(fields, results):
    column_list = []
    dict = {}
    list = []

    for i in fields:
        column_list.append(i[0])
    try:
        for i in range(0, len(results)):
            for j in range(0, len(column_list)):
                dict[column_list[j]] = results[i][j]
            list.append(copy.deepcopy(dict))
    except:  # 元组数量为1时
        for i in range(0, len(results)):
            dict[column_list[i]] = results[i]
        list.append(copy.deepcopy(dict))
    return list


def SearchMysql(sql):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Linux1175@',
        db='MyProject',
        charset='utf8',
        use_unicode=True
    )
    # 建立游标cursor
    cursor = conn.cursor()
    # 执行查
    cursor.execute(sql)
    # 查询数据库多条数据
    results = cursor.fetchall()
    fields = cursor.description
    # print(fields)
    cursor.close()
    conn.close()
    results = toRows(fields, results)
    return results


def FilePath(filename, path):  # 其中instance代表使用此函数类的一个实例，filename就是我们上传文件的文件名（为什么filename就是文件名，我只能猜测是upload_to参数规定的
    if isinstance(filename, str):  # 判断name是否是str类型的一个实例
        pic_write_path = path + filename
        return pic_write_path
