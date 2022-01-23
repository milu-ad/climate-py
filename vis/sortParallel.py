from collections import OrderedDict
import json

f = open('provinceParallel.json', 'r', encoding='utf8')
content = json.load(f)
print(content)

monitorItems = OrderedDict()
alist = ["北京市", "天津市", "河北省", "山东省", "上海市", "江苏省", "浙江省", "辽宁省", "吉林省", "黑龙江省", "福建省", "广东省", "海南省", "香港特别行政区", "台湾省", "山西省",
         "内蒙古自治区", "河南省", "陕西省", "安徽省", "江西省", "湖北省", "湖南省", "广西壮族自治区", "重庆市", "四川省", "贵州省", "云南省", "西藏自治区", "甘肃省",
         "青海省", "宁夏回族自治区", "新疆维吾尔自治区"]
for index, row in content.items():
    for key in alist:
        print(row)
        if row.has_key(key):
            monitorItems[key] = row.get(key)
print(monitorItems)
