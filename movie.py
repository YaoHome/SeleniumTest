#coding:utf-8

from selenium import webdriver
import time

skipTime = 5

class GetMovie(object):
    def __init__(self,driver):
        self.driver = driver
    '''
        打开豆瓣选电影网站
    '''
    def open_douban_movie(self):
        driver.get("https://movie.douban.com/explore")
        time.sleep(skipTime)


    '''
        进入到选电影页面
    '''
    def to_find_movie(self):
        driver.find_element_by_xpath("//a[@class='lnk-movie']").click()
        time.sleep(skipTime)
        driver.find_element_by_xpath("//li/a[text()='选电影']").click()
        time.sleep(skipTime)
    '''
        选择电影的类型
        tagName:电影标签
    '''
    def choose_tag(self,tagName):
        xpath = "//input[@value='"+tagName+"']/parent::*"
        # driver.find_element_by_xpath(xpath+"/parent::*").click()
        driver.find_element_by_xpath(xpath).click()
        time.sleep(skipTime)
    '''
        点击加载更多
        times:点击次数
    '''
    def add_more(self,times=60000):
        num = times
        while (True):
            #页面滚动到最后
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            time.sleep(1)
            try:
                driver.find_element_by_xpath("//a[@class='more']").click()
                time.sleep(skipTime)
            except Exception as e:
                break
            num = num-1
            print (num)
            if num==0:
                break
    '''
        获取当前页面电影元素
        :return 电影元素
    '''
    def movies(self):
        list = driver.find_elements_by_xpath("//div[@class='list']/a")
        print("当前页面电影数量为：%d" % (len(list)))
        return list

    '''
        获取当前页面电影id
        :return 电影id列表
    '''
    def moviesId(self):
        elements = driver.find_elements_by_xpath("//div[@class='list']/a/div")
        list = []
        for i in range(len(elements)):
            list.append(elements[i].get_attribute("data-id"))
        print ("当前页面电影数量为：%d"%(len(list)))
        print (str(list))
        return list
    '''
        格式化影片信息内容
    '''
    def json_format(self,list):
        movie = []
        for i in range(0,len(list),2):
            movie.append("'"+list[i]+"':'"+list[i+1]+"'")

        ret = str(movie).replace('"','')
        return ret
    '''
        获取电影所有tag标签
        :return tag标签列表
    '''
    def get_tag(self):
        list = []
        tags = driver.find_elements_by_xpath("//input[@name='tag']")
        for i in range(len(tags)):
            list.append(tags[i].get_attribute("value"))
        return list
    '''
        将影片信息写入文件
        text：影片信息内容
        fileName：文件路径+文件名
    '''
    def write_to_file(self,text,fileName):
        file = open(fileName, "a",encoding="utf-8")
        file.write("\n" + text)
        file.close()
    '''
        获取当前电影的信息
        :return 信息内容
    '''
    def get_info(self):
        #如果存在“更多..”按钮，点击
        try:
            driver.find_element_by_xpath("//a[@class='more-actor']").click()
        except Exception as e:
            pass
        list = []
        # 电影名称
        list.append("电影名称")
        list.append(driver.find_element_by_xpath("//span[@property='v:itemreviewed']").text)
        #豆瓣评分
        list.append("豆瓣评分")
        list.append(driver.find_element_by_xpath("//strong[@property='v:average']").text)
        #电影资料
        text = driver.find_element_by_xpath("//div[@id='info']").text
        info_list = str(text).split("\n")
        for i in range(len(info_list)):
            info_list[i].replace(" ","")
            info = info_list[i].split(":")
            list.append(info[0])
            list.append(info[1])
        return list
    def running(self,tagName):
        self.choose_tag(tagName)
        self.add_more()
        mv = self.movies()
        for i in range(len(mv)):
            mv[i].click()
            time.sleep(skipTime)
            # 切换到电影详情标签页
            driver.switch_to_window(driver.window_handles[1])
            list = self.get_info()
            info = self.json_format(list)
            self.write_to_file(str(info),fileName)
            driver.close()
            #切换到找电影标签页
            driver.switch_to_window(driver.window_handles[0])

fileName = "c:\\douban\\0719.txt"
#初始化浏览器
driver = webdriver.Firefox()
driver.maximize_window()
gm = GetMovie(driver)
gm.open_douban_movie()
print ("打开豆瓣选电影页面")
time.sleep(skipTime)
tags = gm.get_tag()
print ("获取全部电影标签 ： %s"%(str(tags)))
for i in range(len(tags)):
    print ("获取电影标签页：%s"%(tags[i]))
    gm.running(tags[i])







# gm.open_douban_movie()
# # gm.choose_tag("可播放")
# gm.add_more()
# movies = gm.movies()
# for i in range(len(movies)):
#     movies[i].click()
#     time.sleep(skipTime)
#     #切换到电影详情标签页
#     driver.switch_to_window(driver.window_handles[1])
#     list = gm.get_info()
#     mv = gm.json_format(list)
#     gm.write_to_file(str(mv),fileName)
#     driver.close()
#     #切换到找电影标签页
#     driver.switch_to_window(driver.window_handles[0])
driver.quit()
