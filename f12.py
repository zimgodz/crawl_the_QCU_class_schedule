from selenium import webdriver
import requests
import time
import datetime
import json

import matplotlib.pyplot as plt
def wait_for_login(driver):
    print(f"请在打开的浏览器中完成登录操作...")
    
    # 通过URL变化判断登录状态
    while True:
        current_url = driver.current_url
        print(f"当前URL: {current_url}")
        

        if "index_initMenu.html" in current_url :
            print("检测到登录成功！")
            break
            
            
        time.sleep(2)  # 每2秒检查一次

def get_website_cookie(url):
    """打开网站，等待用户登录，然后获取cookie"""
   
    try:
        # 打开目标网站
        driver.get(url)
        
        # 等待用户登录
        wait_for_login(driver)
        
        # 获取所有cookie
        cookies = driver.get_cookies()
        print(cookies)
        # 打印cookie信
        print("\n获取到的Cookie信息：")
        for cookie in cookies:
            print(f"{cookie['name']}: {cookie['value']}")
            
        return cookies
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 保持浏览器打开一段时间，方便查看
        driver.close()
# 获取当前时间，返回当前学期课表
def current_time():
    current_datetime = datetime.datetime.now()
    if 1<current_datetime.month<8:
        return {"xnm": int(current_datetime.year)-1,"xqm": 12}
    else:
        return {"xnm": int(current_datetime.year),"xqm": 3}
    
# 爬虫主函数
def execute_main(cookies):
    url='http://jwgl.qdc.edu.cn/jwglxt/kbcx/xskbcx_cxXsgrkb.html'
    current_time_=current_time()
    # post两项参数
    data={
        'xnm': current_time_["xnm"], 
        'xqm': current_time_["xqm"], 
        'kblx':'ck',
        'xsdm':''
    }
    params = {
        'gnmkdm':'N2151'
    }
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }

    cookies_ = {
        cookies[0]["name"]:cookies[0]["value"],
        cookies[1]["name"]:cookies[1]["value"]
    }
    # 发送post请求
    json_=requests.post(url=url, data=data, headers=headers,cookies=cookies_,params=params).text
    print(json_)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(json_), f,ensure_ascii=False)

def visualization_class_hours():
    json_data =None
    with open("data.json", "r", encoding="utf-8") as f:
        json_data = f.read()
    json_data = json.loads(json_data)
    json_kblist = json_data["kbList"]
    courses_data = {}

    for i in json_kblist:
        courses_data[i["kcmc"]]={"总课时":i["zxs"],"任课老师":i["xm"]}




    # 确保中文显示正常
    plt.rcParams["font.family"] = ["SimHei"]



    # 提取课程名称、总课时和任课老师
    courses = list(courses_data.keys())
    hours = [int(courses_data[course]["总课时"]) for course in courses]
    teachers = [courses_data[course]["任课老师"] for course in courses]
    plt.figure(figsize=(7, 4))
    bars = plt.bar(courses, hours, color='skyblue')
    for bar, hour, teacher in zip(bars, hours, teachers):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{hour}课时\n({teacher})', ha='center', va='bottom', fontsize=9)

    plt.title('课程总课时分布', fontsize=16)
    plt.xlabel('课程名称', fontsize=12)
    plt.ylabel('总课时', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.ylim(0, max(hours) + 10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()    

if __name__ == "__main__":
    driver=webdriver.Edge()
    target_url = "http://jwgl.qdc.edu.cn/jwglxt/xtgl/login_slogin.html"
    cookies = get_website_cookie(target_url) 
    execute_main(cookies)
    driver.quit()
    visualization_class_hours()