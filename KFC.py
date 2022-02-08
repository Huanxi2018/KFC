# 爬取肯德基指定地区的餐厅数
import requests
import json

if __name__ == "__main__":
    # 如果在搜索框输入信息，回车后网址没变而页面有变化，说明这是一个ajax请求
    # 在该网页中，这个一个post方法
    cityName = input('请输入你想爬取的肯德基餐厅的城市: ')
    url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword"
    pageIndex = '1'
    data = {
        'cname': '',
        'pid': '',
        'keyword': cityName,
        'pageIndex': pageIndex,
        'pageSize': '10'
    }
    # 进行UA伪装，携带请求头参数，否则会被网页认为你是用pycharm等编译器在进行爬虫而被禁止访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55'
    }
    try:
        # 以写文件的形式打开一个文件
        loop = True
        # 这个列表/字典用来存放北京市的所有餐厅的名字，或者用一个字典
        data_list = []
        print('肯德基在'+cityName+'分店分布为:')
        while loop:
            response = requests.post(url=url, data=data, headers=headers)
            json_data = response.json()
            # 使用if not x这种写法的前提是：必须清楚x等于None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()时对你的判断没有影响才行
            if not json_data['Table1']:
                # loop = False
                break
            # 不用json格式的数组录入，是因为追加的话，整体就不是json格式的数据了，如果解析json再拼接的话，更加耗费时间
            # json.dump(json_data, fp=fp, ensure_ascii=False) 所以该方法被舍弃
            # 以下的逻辑看似恐怖，其实只是对分页进行简单的逻辑分析
            if int(json_data['Table'][0]['rowcount'])-int(pageIndex)*int(data['pageSize']) >= 0:
                for i in range(0, int(data['pageSize'])):
                    print(json_data['Table1'][i]['storeName'])
                    data_list.append(json_data['Table1'][i]['storeName'])
            # 假如该该地区的总餐厅数没有分页的数多，则做以下操作
            elif int(data['pageSize']) > int(json_data['Table'][0]['rowcount']):
                for i in range(0, int(json_data['Table'][0]['rowcount'])):
                    print(json_data['Table1'][i]['storeName'])
                    data_list.append(json_data['Table1'][i]['storeName'])
            else:
                for i in range(0, int(json_data['Table'][0]['rowcount'])-(int(pageIndex)-1)*int(data['pageSize'])):
                    print(json_data['Table1'][i]['storeName'])
                    data_list.append(json_data['Table1'][i]['storeName'])
            # 更新页码
            pageIndex = str(int(pageIndex) + 1)
            data['pageIndex'] = pageIndex
        print('-----循环结束-----')
        # 值得注意的是:追加而不覆盖用a,而不是w
        # fp = open('./Data/BeijingKFC.json', 'a', encoding='utf-8')
        with open('./Data/BeijingKFC.txt', 'w', encoding='utf-8') as fp:
            fp.write(str(data_list))
    except IOError:
        print('写入异常!')
    else:
        print('爬取结束!')
        fp.close()
