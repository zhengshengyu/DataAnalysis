#-*- coding:utf-8 _*-
"""
@file : idcard_dict.py
@auther : Ma
@time : 2018/11/06
从国家民政局上更新最新的行政区划分状况，并将结果加载到数据库中
"""

import urllib
import re
# import pymysql
import sys
from numpy import *

reload(sys)
sys.setdefaultencoding('utf8')

# db = pymysql.Connect(host=host, port=3306, user="root", passwd=passwd, db=db, charset='utf8')
# cursor = db.cursor()


# 将字符串中数字取出来
def string_to_int(string):
    return re.findall(r'\d+\.?\d*',string)


# 将身份证id和归属地放在一个list里
def id_name_spider(url, res_pat ):
    h = urllib.urlopen(url=url).read()
    res = re.compile(res_pat, re.S).findall(h)
    # 里面包含空字符串，利用filter函数过滤掉所有的''
    res_list = filter(None, res)
    return res_list


if __name__ == '__main__':
    url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/2020/202003061536.html'
    res_pat = '<td class=xl7120844>(.*?)</td>'
    res_list2 = id_name_spider(url,res_pat) #县
    res_pat = '<td class=xl7020844>(.*?)</td>'
    res_list1=(id_name_spider(url,res_pat))  #省市
    res_list= concatenate((res_list2,res_list1),axis=0)
    param_list = []
    for i in range(0, len(res_list) / 2):
        id = string_to_int(res_list[i * 2])[0]
        name = res_list[i * 2 + 1]

        # 清洗一下 <span style='mso-spacerun:yes'>   </span>
        if "<span style='mso" in name:
            matchObj = re.match(r'(.*)</span>(.*)', name, re.S)
            name = matchObj.group(2)

        province_id = id[:2]
        city_id = id[2:4]
        district_id = id[4:]

        if city_id == '00' and district_id == '00':
            # 说明是省
            insert_sql_param = '(%s,"%s",%s,%s,%s)' % (id, name, 1, 0, 0)
        elif district_id == '00':
            # 说明是市
            insert_sql_param = '(%s,"%s",%s,%s,%s)' % (id, name, 0, 1, 0)
        else:
            # 说明是区县
            insert_sql_param = '(%s,"%s",%s,%s,%s)' % (id, name, 0, 0, 1)

        param_list.append(insert_sql_param)
        print(insert_sql_param)
    # # 因为条数大概在3.5k条左右，一条一条提交很慢，所以改成一个长sql
    # insert_sql_param_concat = ",".join(param_list)
    # insert_sql = 'insert into cardno_local (id,name,province,city,district) values ' + insert_sql_param_concat + ';'
    # print insert_sql
    # # 执行sql并提交
    # cursor.execute(insert_sql)
    # db.commit()
