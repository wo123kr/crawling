import requests
import re

def getHTMLText(url):#获得页面
    try:
        kv = {'user-agent': 'Mozilla/5.0',
              'cookie':'[ { "domain": ".taobao.com", "expirationDate": 1680778523, "hostOnly": false, "httpOnly": false, "name": "_cc_", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "Vq8l%2BKCLiw%3D%3D", "id": 1 }, { "domain": ".taobao.com", "expirationDate": 1713409494, "hostOnly": false, "httpOnly": false, "name": "_ga", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "GA1.2.416609605.1649150308", "id": 2 }, { "domain": ".taobao.com", "expirationDate": 1713409494, "hostOnly": false, "httpOnly": false, "name": "_ga_YFVFB9JLVB", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "GS1.1.1650337494.7.0.1650337494.0", "id": 3 }, { "domain": ".taobao.com", "expirationDate": 1650337554, "hostOnly": false, "httpOnly": false, "name": "_gat_gtag_UA_202630127_1", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "1", "id": 4 }, { "domain": ".taobao.com", "expirationDate": 1650423894, "hostOnly": false, "httpOnly": false, "name": "_gid", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "GA1.2.1415751070.1650257465", "id": 5 }, { "domain": ".taobao.com", "expirationDate": 1650942294.963523, "hostOnly": false, "httpOnly": false, "name": "_m_h5_tk", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "5c7574488320677b623f0ca6828fd3a2_1650345054041", "id": 6 }, { "domain": ".taobao.com", "expirationDate": 1650942294.963581, "hostOnly": false, "httpOnly": false, "name": "_m_h5_tk_enc", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "ba5b7a122c654f9e51e9fde72fe75b8e", "id": 7 }, { "domain": ".taobao.com", "expirationDate": 1650423894, "hostOnly": false, "httpOnly": false, "name": "_uetsid", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "270d3c90bed311ecbf50394f3404bbc8", "id": 8 }, { "domain": ".taobao.com", "expirationDate": 1684033494, "hostOnly": false, "httpOnly": false, "name": "_uetvid", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "cce63a30ba3f11ec935561193b6cfaf1", "id": 9 }, { "domain": ".taobao.com", "expirationDate": 1650618403, "hostOnly": false, "httpOnly": false, "name": "ariaReadtype", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "1", "id": 10 }, { "domain": ".taobao.com", "expirationDate": 1650618449, "hostOnly": false, "httpOnly": false, "name": "ariaStatus", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "false", "id": 11 }, { "domain": ".taobao.com", "expirationDate": 2279870308, "hostOnly": false, "httpOnly": false, "name": "cna", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "PjjMGlFzBWECAWrzUL6+Devi", "id": 12 }, { "domain": ".taobao.com", "expirationDate": 1964573828, "hostOnly": false, "httpOnly": true, "name": "enc", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "PLVJ1Lv4F439Bd3DaZnPj563a0TnlW3CCu19JwzmaQwiYxdR%2BUSQnliR0K8liga2V5Ze7YaqlDf4FTCNxwcLpVuC66EcD32WuOHQHwsGhpc%3D", "id": 13 }, { "domain": ".taobao.com", "expirationDate": 1680715159, "hostOnly": false, "httpOnly": false, "name": "hng", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "CN%7Czh-CN%7CCNY%7C156", "id": 14 }, { "domain": ".taobao.com", "expirationDate": 1665889494, "hostOnly": false, "httpOnly": false, "name": "isg", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "BKSkED5hmkkchu4WbkMNHNJjdaKWPcinDqVCKr7FMG8yaUQz5k2YN9rLKdnxsQD_", "id": 15 }, { "domain": ".taobao.com", "expirationDate": 1665889494, "hostOnly": false, "httpOnly": false, "name": "l", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "eB_mM8NPLRz-FKAyKOfwourza77OSIRAguPzaNbMiOCPOu5H5M-dW62UWR8MC3MNh64vR38sRq94BeYBqIxyRW16rNWQtWDmn", "id": 16 }, { "domain": ".taobao.com", "expirationDate": 1651834523, "hostOnly": false, "httpOnly": false, "name": "lgc", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "tb7654902929", "id": 17 }, { "domain": ".taobao.com", "expirationDate": 1650893438, "hostOnly": false, "httpOnly": false, "name": "mt", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "ci=-1_0", "id": 18 }, { "domain": ".taobao.com", "expirationDate": 1680778523, "hostOnly": false, "httpOnly": true, "name": "sgcookie", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "E1009b3xHs4V%2BZEyHqe7CSLeRrnpj3eXeifQYMMbPlPXLedgeMhpAif2MOTpar5LM6KHE6U0YsUSH6V8ocBL%2Fjp7tQ3NLvzY%2BCnfW%2BGy32cYZGU%3D", "id": 19 }, { "domain": ".taobao.com", "expirationDate": 1665889494, "hostOnly": false, "httpOnly": false, "name": "tfstk", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "cqhNBuYB-CdZKSVXe5N2chcdtdZOZp0io6z7I3cRf4ne2PeGiYIY-yq38r_FmRf..", "id": 20 }, { "domain": ".taobao.com", "expirationDate": 1680254360, "hostOnly": false, "httpOnly": false, "name": "thw", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "cn", "id": 21 }, { "domain": ".taobao.com", "expirationDate": 1680778523, "hostOnly": false, "httpOnly": false, "name": "tracknick", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "tb7654902929", "id": 22 }, { "domain": ".taobao.com", "expirationDate": 1651834523, "hostOnly": false, "httpOnly": true, "name": "uc3", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dCvCtEw2JcYctvhMc%3D&nk2=F5RCY8R%2Fc3xzeF2R&id2=UUpgRKrwgLZljXSerQ%3D%3D", "id": 23 }, { "domain": ".taobao.com", "expirationDate": 1651834523, "hostOnly": false, "httpOnly": true, "name": "uc4", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "id4=0%40U2gqy1tzOIgDOnsU%2BwV%2BtoGJANych%2FnK&nk4=0%40FY4JjTlR6qN1VYmHJK1LEpqubHJEXls%3D", "id": 24 }, { "domain": ".taobao.com", "expirationDate": 1650343864, "hostOnly": false, "httpOnly": false, "name": "xlly_s", "path": "/", "sameSite": "no_restriction", "secure": true, "session": false, "storeId": "0", "value": "1", "id": 25 }, { "domain": "world.taobao.com", "expirationDate": 1664702307, "hostOnly": true, "httpOnly": false, "name": "arms_uid", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "c9617a31-23db-4675-8387-e4f4d51317d3", "id": 26 }, { "domain": "world.taobao.com", "expirationDate": 1650343867, "hostOnly": true, "httpOnly": false, "name": "dropBannerHasShow", "path": "/", "sameSite": "unspecified", "secure": false, "session": false, "storeId": "0", "value": "true", "id": 27 } ]'}
        #请自行获取
        r = requests.get(url,headers=kv,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("获取页面失败")

def parsePage(ilt,html):#对每一个获得的页面进行解析
#两个变量分别是结果的列表类型和相关的HTML页面的信息
    try:
        re1 = re.compile(r'\"view_price\"\:\"[\d\.]*\"')#编译商品价格正则表达式
        re2 = re.compile(r'\"raw_title\"\:\".*?\"')#编译商品名称正则表达式
        plt = re1.findall(html)
        tlt = re2.findall(html)
        #plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        #tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])#去掉view_price字段，只要价格部分，eval将获取到的最外层/内层的单引号或双引号去掉
            title = eval(tlt[i].split(':')[1])#去掉raw_title字段，只要名称部分
    except:
        print("网页解析失败")

def printGoodsList(ilt):#将商品的信息输出到屏幕上
    try:
        tplt = "{:4}\t{:8}\t{:16}" #定义打印模板
        print(tplt.format("序号","价格","商品名称","链接"))
        count = 0
        for s in ilt:
            count = count + 1
            print(tplt.format(count,s[0],s[1]))
    except:
        print("输出失败")

def main():
    goods = input("请输入想要搜索的商品：") #定义搜索关键词变量
    depth = input("请输入想要搜索商品的深度(整数)：") #定义爬取的深度即页数
    depth = int(depth)
    start_url = 'https://s.taobao.com/search?q='+goods
    infoList = [] #定义整个的输出结果变量
    for i in range(depth):#对每次翻页后的URL链接进行设计
        try:
            url = start_url + '&s='+str(44*i)
            html = getHTMLText(url)
            parsePage(infoList,html)
        except:
            continue
    printGoodsList(infoList)

#调用主函数
main()