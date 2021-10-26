import copy
import datetime
import uuid
import random

import pymysql

# fields为表头，将数据库中筛选出的results与表头拼接，生成字典。不断遍历，多个字典添加到列表，最后赋值给rows
from django.core.mail import send_mail
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from wms.settings import EMAIL_FROM


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


def FilePath(instance, filename):  # 其中instance代表使用此函数类的一个实例，filename就是我们上传文件的文件名（为什么filename就是文件名，我只能猜测是upload_to参数规定的
    instance_name = str(instance)
    # 获取当前时间
    now_time = datetime.datetime.now()
    # 格式化时间字符串
    str_time = now_time.strftime("%Y-%m")
    # 后缀
    ext = filename.split('.')[-1]
    # 默认路径
    path = 'img/'
    if instance_name.startswith('roimg'):
        path = 'img/blade/roimg/' + str(str_time) + '/'
    if isinstance(filename, str):  # 判断name是否是str类型的一个实例
        pic_write_path = path + instance_name + '-{}.{}'.format(uuid.uuid4().hex[:10], ext)
        return pic_write_path


def SecondToLast(dict, dicts):
    for item in dicts:
        # print(item)
        if item['order_status'] == 4 and (item['weldinggun_num'] == dict['weldinggun_num']):
            # results中每个item按创建时间顺序从晚到早排序。目的是上次领用时间比目前item的时间晚，所以当遍历到早于当前item的领用时间，
            # 会由于已经被datetime格式化而无法再次被datetime格式化，报错后走except
            try:
                return datetime.datetime.strftime(item['receive_time'], '%Y-%m-%d %H:%M')
            except:
                pass
            # except:
            #     return item['receive_time']
    return '首次领用'


def CodeRandom():
    # 随机数函数
    _str = '1234567890'
    return ''.join(random.choice(_str) for i in range(6))


# 发送邮件
def SendEmailCode(email, send_type):
    # 第一步，创建邮箱验证码对象，保存数据库，用来以后做对比
    from workstation.models.base_models import EmailVerifyRecord
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = CodeRandom()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 第二部：正式的发邮件功能
    if send_type == 'register':
        send_title = '欢迎注册：'
        send_body = '请点击一下链接进行激活您的账号：\n http://127.0.0.1:8000/users/user_activate/' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])
    # 忘记密码
    if send_type == 'reset':
        send_title = 'wms--密码重置：'
        send_body = '''您好：
            您正在修改你的密码，您的验证码是: {}，请在5分钟之内完整密码重置。
        '''.format(code)
        send_status = send_mail(send_title, send_body, EMAIL_FROM,
                                [email])
        if not send_status == 1:
            return {
                'code': 0,
                'msg': '邮件发送失败'
            }
        else:
            return {
                'code': '1',
                'msg': '邮件发送成功'
            }
        # 忘记密码
    if send_type == 'forget':
        send_title = '更换邮箱：'
        send_body = '请点击一下链接进行重置您的邮箱：\n http://127.0.0.1:8000/users/user_mail_reset/' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])


# 涉及两个列表的排序，list1根据list2的排序顺序排序
def SortListAndList(list1, list2, reverse):
    # 升序
    if reverse == False:
        for i in range(0, len(list2)):
            min = i
            for j in range(i + 1, len(list2)):
                if list2[j] < list2[min]:
                    min = j
            list2[min], list2[i] = list2[i], list2[min]
            list1[min], list1[i] = list1[i], list1[min]
    # 降序
    else:
        for i in range(0, len(list2)):
            max = i
            for j in range(i + 1, len(list2)):
                if list2[j] > list2[max]:
                    max = j
            list2[max], list2[i] = list2[i], list2[max]
            list1[max], list1[i] = list1[i], list1[max]
    # print(list1)
    # print(list2)
    return [list1, list2]
