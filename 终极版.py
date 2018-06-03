import requests
from lxml import etree
import urllib.parse
from bs4 import BeautifulSoup
from  tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import re
import importlib
import sys
import os


class Anda:
    def __init__(self):
        self.base_url = 'http://jw3.ahu.cn/default2.aspx'
        self.session = requests.session()
    def login_UI(self):
        def cancel():
            varName.set('')         #清空用户输入的用户名和密码
            varPwd.set('')
            
        # 保存验证码图片
        check_img_url = 'http://jw3.ahu.cn/CheckCode.aspx'
        img_resp = self.session.get(check_img_url, stream=True)
        image = img_resp.content
        DstDir = os.getcwd()+"\\"
        try:
            with open(DstDir+'check.jpg', 'wb') as f:
                f.write(image)
        except IOError:
            print("IO Error\n")
        finally:
            f.close
            
        
        root = tkinter.Tk()
        varName = tkinter.StringVar()
        varName.set('E11514130')
        varPwd = tkinter.StringVar()
        varPwd.set('111aaa')
        varCode = tkinter.StringVar()
        varCode.set('')


        labelName = tkinter.Label(root, text='学号:', justify=tkinter.RIGHT,width=80)
        labelName.place(x=10, y=5, width=80, height=20)    #将标签放到窗口上

        entryName = tkinter.Entry(root, width=80, textvariable=varName)        #创建文本框                            
        entryName.place(x=100, y=5, width=80, height=20)





        labelPwd = tkinter.Label(root, text='密码',justify=tkinter.RIGHT,width=80)
        labelPwd.place(x=10, y=30, width=80, height=20)

        entryPwd = tkinter.Entry(root, show='*',width=80,textvariable=varPwd)#创建密码文本框
        entryPwd.place(x=100, y=30, width=80, height=20)




        labelCode = tkinter.Label(root, text='验证码:', justify=tkinter.RIGHT,width=80)
        labelCode.place(x=10, y=55, width=80, height=20)    #将标签放到窗口上

        entryCode = tkinter.Entry(root, width=80, textvariable=varCode)        #创建文本框                            
        entryCode.place(x=100, y=55, width=80, height=20)

        def login(u,p,c,root):
            response = self.session.get(self.base_url)
            selector = etree.HTML(response.content)
            __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
            #username = input('输入学号')
            #password = input('输入密码')
            username = u
            password = p
            txtSecretCode = c

            data = {
                '__VIEWSTATE': __VIEWSTATE,
                'txtUserName': username,
                'TextBox2': password,
                'txtSecretCode': txtSecretCode,
                'RadioButtonList1': '(unable to decode value)',
                'Button1': '',
                'lbLanguage': '',
                'hidPdrs': '',
                'hidsc': '',
                }
            loginResp = self.session.post(self.base_url, data=data)
                # 登录后的url
                
            info_url = 'http://jw3.ahu.cn/xs_main.aspx?xh={}'.format(username)
            self.session.headers['Referer'] = info_url
                # 登陆后页面信息
            login_page = self.session.get(info_url)
            soup = BeautifulSoup(login_page.text, 'lxml')
                # 学生姓名
            name = soup.select('#xhxm')[0].get_text()[:-2]
            root.withdraw()
            main_UI(username, name)
            
        def main_UI(username, name):
            root1 = tkinter.Tk()
            root1.title("教务系统")
            root1.geometry("800x500+600+200")


            def get_stu_info(username, name):
                # 把学生名字编码
                name = urllib.parse.quote_plus(name.encode('gb2312'))
                    # 请求课表的url
                req_url = 'http://jw3.ahu.cn/xskbcx.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121603'
                response = self.session.get(req_url)
                soup = BeautifulSoup(response.text, 'lxml') # 学生基本信息
                
                stu_num = soup.select('#Label5')[0].get_text() # 学号
                name = soup.select('#Label6')[0].get_text() # 姓名
                faculty = soup.select('#Label7')[0].get_text() # 院系
                major = soup.select('#Label8')[0].get_text() # 专业
                class1 = soup.select('#Label9')[0].get_text() # 班级
                #Student.create(stu_num=stu_num, name=name, stu_class=class1, faculty=faculty, major=major) # 得到学生课表
                #print(stu_num, name, class1,faculty,major)
                a=[]
                a.append(stu_num)
                a.append(name)
                a.append(class1)
                a.append(faculty)
                a.append(major)
                return a


            def get_grade(username, name,n,d,tab):
                # 把学生名字编码
                name = urllib.parse.quote_plus(name.encode('gb2312'))
                    # 请求课表的url
                
                req_url = 'http://jw3.ahu.cn/xscjcx.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121605'
                response = self.session.get(req_url)
                soup = BeautifulSoup(response.text, 'lxml')    
                __VIEWSTATE = soup.select('#Form1 input')[2].get('value')
                #selector = etree.HTML(response.content)
                #__VIEWSTATE = selector.xpath('//*[@id="Form1"]/input/@value')[2]
                #ddlXN = input('输入学年(例如输入2016，查询2016-2017学年的)')
                #ddlXQ = input('输入学期(1或2)')

      
               
                
                ddlXN=n
                ddlXQ=d
                #print(xnd)
                #print(xqd)
                #print(str(xnd) + '-' + str(int(xnd)+1))
                data = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': __VIEWSTATE,
                    'ddlXN': str(ddlXN) + '-' + str(int(ddlXN)+1), # 学年 2015-2016
                    'ddlXQ': ddlXQ ,# 学期
                    'hidLanguage':'',
                    'ddl_kcxz':'',
                    'btn_xq': '%D1%A7%C6%DA%B3%C9%BC%A8'
                    }
                self.session.headers['Referer'] = 'http://jw3.ahu.cn/xs_main.aspx?xh={}'.format(username)
                resp = self.session.post(req_url, data=data)
                soup = BeautifulSoup(resp.text, 'lxml')
                tr = soup.select('tr')
                year = str(ddlXN) + '-' + str(int(ddlXN)+1) + '学年'
                term = '第' + str(ddlXQ) + '学期'
                    # 数据表名
                table_name = year + '/' + term

                for i in range(len(tr)):
                    if i>3 and i<(len(tr)-7):
                        text01=tkinter.Text(tab)
                        text01.place(x=0, y=70+20*(i-4),width=200,height=20)
                        text01.insert(1.0,tr[i].select('td')[3].get_text())
                        text02=tkinter.Text(tab)
                        text02.place(x=200, y=70+20*(i-4),width=80,height=20)
                        text02.insert(1.0,tr[i].select('td')[6].get_text())
                        text03=tkinter.Text(tab)
                        text03.place(x=280, y=70+20*(i-4),width=120,height=20)
                        text03.insert(1.0,tr[i].select('td')[7].get_text())
                        text04=tkinter.Text(tab)
                        text04.place(x=400, y=70+20*(i-4),width=80,height=20)
                        text04.insert(1.0,tr[i].select('td')[8].get_text())
                        

            def get_classroom(username, name,y,tab):
                # 把学生名字编码
                name = urllib.parse.quote_plus(name.encode('gb2312'))
                    # 请求课表的url
                
                req_url = 'http://jw3.ahu.cn/xxjsjy.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121611'
                response = self.session.get(req_url)
                soup = BeautifulSoup(response.text, 'lxml')
                #print(soup.select('#Form1 input'))
                #print(len(soup.select('#Form1 input')))
                __VIEWSTATE = soup.select('#Form1 input')[2].get('value')
                #selector = etree.HTML(response.content)
                #__VIEWSTATE = selector.xpath('//*[@id="Form1"]/input/@value')[2]
                #ddlXN = input('输入学年(例如输入2016，查询2016-2017学年的)')
                #ddlXQ = input('输入学期(1或2)')

      
               
                
                #ddlXN='2016'
                #ddlXQ='1'
                #print(xnd)
                #print(xqd)
                #print(str(xnd) + '-' + str(int(xnd)+1))

                #print(y.get())
                data = {
                    '__EVENTTARGET': 'sjd',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': __VIEWSTATE,
                    #'ddlXN': str(ddlXN) + '-' + str(int(ddlXN)+1), # 学年 2015-2016
                    #'ddlXQ': ddlXQ ,# 学期
                    
                    'xiaoq':'',
                    'jslb':'',
                    'min_zws':'0',
                    'max_zws':'',
                    #'jsbh':'101B1501',
                    'ddlSyXn':'2017-2018',
                    'ddlSyxq':'2',
                    #'dpDatagrid3%3AtxtChoosePage':'1',
                    #'dpDatagrid3%3AtxtPageSize':'20',
                    'kssj':y.get(),
                    'jssj':y.get(),
                    'xqj':'7',
                    'ddlDsz':'%CB%AB',
                    'sjd':'%271%27%7C%271%27%2C%270%27%2C%270%27%2C%270%27%2C%270%27%2C%270%27%2C%270%27%2C%270%27%2C%270%270',
                    'Button2':'%BF%D5%BD%CC%CA%D2%B2%E9%D1%AF',
                    'dpDataGrid1:txtChoosePage':'1',
                    'dpDataGrid1:txtPageSize':'20',
                    'xn':'2017-2018',
                    'xq':'2'
                    }
                self.session.headers['Referer'] = 'http://jw3.ahu.cn/xs_main.aspx?xh={}'.format(username)
                resp = self.session.post(req_url, data=data)
                soup = BeautifulSoup(resp.text, 'lxml')
                #print(soup)
                tr = soup.select('tr')
                #year = str(ddlXN) + '-' + str(int(ddlXN)+1) + '学年'
                #term = '第' + str(ddlXQ) + '学期'
                    # 数据表名
                #table_name = year + '/' + term
                
                #for i in range(len(tr)):
                    #for j in range(len(tr[i].select('td'))):
                    #print(tr[i].select('td')[1].get_text(),tr[i].select('td')[2].get_text(),tr[i].select('td')[3].get_text())
                    
                    #if i>3 and i<(len(tr)-7):
                    #print(tr[i].select('td')[3].get_text(),tr[i].select('td')[6].get_text(),tr[i].select('td')[7].get_text(),tr[i].select('td')[8].get_text())
                for i in range(len(tr)):                    
                    text01=tkinter.Text(tab)
                    text01.place(x=0, y=70+20*(i-1),width=200,height=20)
                    text01.insert(1.0,tr[i].select('td')[1].get_text())
                    text02=tkinter.Text(tab)
                    text02.place(x=200, y=70+20*(i-1),width=80,height=20)
                    text02.insert(1.0,tr[i].select('td')[2].get_text())
                    text03=tkinter.Text(tab)
                    text03.place(x=280, y=70+20*(i-1),width=120,height=20)
                    text03.insert(1.0,tr[i].select('td')[3].get_text())
                        
            def get_plan(username, name,x,tab):
                # 把学生名字编码
                name = urllib.parse.quote_plus(name.encode('gb2312'))
                    # 请求课表的url
                
                req_url = 'http://jw3.ahu.cn/pyjh.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121607'
                response = self.session.get(req_url)
                soup = BeautifulSoup(response.text, 'lxml')
                #print(soup.select('#Form1 input'))
                #print(len(soup.select('#Form1 input')))
                __VIEWSTATE = soup.select('#Form1 input')[2].get('value')
                #selector = etree.HTML(response.content)
                #__VIEWSTATE = selector.xpath('//*[@id="Form1"]/input/@value')[2]
                #ddlXN = input('输入学年(例如输入2016，查询2016-2017学年的)')
                #ddlXQ = input('输入学期(1或2)')

      
               
                xq=x
                #ddlXN='2016'
                #ddlXQ='1'
                #print(xnd)
                #print(xqd)
                #print(str(xnd) + '-' + str(int(xnd)+1))
                data = {
                    '__EVENTTARGET': 'dpDBGrid:txtPageSize',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': __VIEWSTATE,
                    #'ddlXN': str(ddlXN) + '-' + str(int(ddlXN)+1), # 学年 2015-2016
                    #'ddlXQ': ddlXQ ,# 学期
                    
                    'xq':xq,
                    'kcxz':'(unable to decode value)',
                    'dpDBGrid:txtChoosePage':'1',
                    'dpDBGrid:txtPageSize':'20',
                    'dpDatagrid6:txtChoosePage':'1',
                    'dpDatagrid6:txtPageSize':'20'
                    }
                self.session.headers['Referer'] = 'http://jw3.ahu.cn/xs_main.aspx?xh={}'.format(username)
                resp = self.session.post(req_url, data=data)
                soup = BeautifulSoup(resp.text, 'lxml')
                #print(soup)
                tr = soup.select('tr')
                #year = str(ddlXN) + '-' + str(int(ddlXN)+1) + '学年'
                #term = '第' + str(ddlXQ) + '学期'
                    # 数据表名
                #table_name = year + '/' + term
                
                #for i in range(len(tr)):
                    #for j in range(len(tr[i].select('td'))):
                    #print(tr[i].select('td')[1].get_text(),tr[i].select('td')[2].get_text(),tr[i].select('td')[3].get_text())
                    
                    #if i>3 and i<(len(tr)-7):
                    #print(tr[i].select('td')[3].get_text(),tr[i].select('td')[6].get_text(),tr[i].select('td')[7].get_text(),tr[i].select('td')[8].get_text())
                for i in range(len(tr)):
                    if i>2 and i<len(tr)-14:
                        text01=tkinter.Text(tab)
                        text01.place(x=0, y=70+20*(i-3),width=200,height=20)
                        text01.insert(1.0,tr[i].select('td')[1].get_text())
                        text02=tkinter.Text(tab)
                        text02.place(x=200, y=70+20*(i-3),width=80,height=20)
                        text02.insert(1.0,tr[i].select('td')[2].get_text())
                        text03=tkinter.Text(tab)
                        text03.place(x=280, y=70+20*(i-3),width=120,height=20)
                        text03.insert(1.0,tr[i].select('td')[5].get_text())
                        text04=tkinter.Text(tab)
                        text04.place(x=400, y=70+20*(i-3),width=120,height=20)
                        text04.insert(1.0,tr[i].select('td')[7].get_text())
                        
            def get_schedule(username, name,n,d,tab):
                # 把学生名字编码
                name = urllib.parse.quote_plus(name.encode('gb2312'))
                    # 请求课表的url
                req_url = 'http://jw3.ahu.cn/xskbcx.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121603'
                response = self.session.get(req_url)
                soup = BeautifulSoup(response.text, 'lxml') # 学生基本信息
                #self.get_stu_info(soup)
                __VIEWSTATE = soup.select('#xskb_form input')[2].get('value')
                #xnd = input('输入学年(例如输入2016，查询2016-2017学年的)')
                #xqd = input('输入学期(1或2)')
                xnd=n
                xqd=d
                #print(xnd)
                #print(xqd)
                #print(str(xnd) + '-' + str(int(xnd)+1))
                data = {
                    '__EVENTTARGET': 'xnd',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': __VIEWSTATE,
                    'xnd': str(xnd) + '-' + str(int(xnd)+1), # 学年 2015-2016
                    'xqd': xqd # 学期
                    
                    }
                self.session.headers['Referer'] = 'http://jw3.ahu.cn/xs_main.aspx?xh={}'.format(username)
                resp = self.session.post(req_url, data=data)
                soup = BeautifulSoup(resp.text, 'lxml')
                tr = soup.select('tr')
                year = str(xnd) + '-' + str(int(xnd)+1) + '学年'
                term = '第' + str(xqd) + '学期'
                    # 数据表名
                table_name = year + '/' + term

                fir = tr[4].select('td')#1、2节
                sec = tr[6].select('td')#3、4节
                thi = tr[8].select('td')#5、6节
                fou = tr[10].select('td')#7、8节
                fiv = tr[12].select('td')#9、10节
                six = tr[14].select('td')#11节
                #print(fir[2].get_text())
                
                """text1=tkinter.Text(tab,width=30,height=50)
                text1.place(x=0, y=70,width=80,height=80)
                text1.insert(1.0,fir[2].get_text())"""
                
                text11=tkinter.Text(tab)
                text12=tkinter.Text(tab)
                text13=tkinter.Text(tab)
                text14=tkinter.Text(tab)
                text15=tkinter.Text(tab)
                text16=tkinter.Text(tab)
                text17=tkinter.Text(tab)

                text11.place(x=0, y=70,width=80,height=80)
                text12.place(x=80, y=70,width=80,height=80)
                text13.place(x=160, y=70,width=80,height=80)
                text14.place(x=240, y=70,width=80,height=80)
                text15.place(x=320, y=70,width=80,height=80)
                text16.place(x=400, y=70,width=80,height=80)
                text17.place(x=480, y=70,width=80,height=80)
                
                text1=[]
                text1.append(text11)
                text1.append(text12)
                text1.append(text13)
                text1.append(text14)
                text1.append(text15)
                text1.append(text16)
                text1.append(text17)

                flag=0
                for i in range(len(fir)):
                    if i>1:
                        text1[flag].insert(1.0,fir[i].get_text())
                        flag=flag+1
                    
                    
                
                text21=tkinter.Text(tab)
                text22=tkinter.Text(tab)
                text23=tkinter.Text(tab)
                text24=tkinter.Text(tab)
                text25=tkinter.Text(tab)
                text26=tkinter.Text(tab)
                text27=tkinter.Text(tab)

                text21.place(x=0, y=150,width=80,height=80)
                text22.place(x=80, y=150,width=80,height=80)
                text23.place(x=160, y=150,width=80,height=80)
                text24.place(x=240, y=150,width=80,height=80)
                text25.place(x=320, y=150,width=80,height=80)
                text26.place(x=400, y=150,width=80,height=80)
                text27.place(x=480, y=150,width=80,height=80)

                text2=[]
                text2.append(text21)
                text2.append(text22)
                text2.append(text23)
                text2.append(text24)
                text2.append(text25)
                text2.append(text26)
                text2.append(text27)

                flag=0
                for i in range(len(sec)):
                    if i>0:
                        text2[flag].insert(1.0,sec[i].get_text())
                        flag=flag+1

                text31=tkinter.Text(tab)
                text32=tkinter.Text(tab)
                text33=tkinter.Text(tab)
                text34=tkinter.Text(tab)
                text35=tkinter.Text(tab)
                text36=tkinter.Text(tab)
                text37=tkinter.Text(tab)

                text31.place(x=0, y=230,width=80,height=80)
                text32.place(x=80, y=230,width=80,height=80)
                text33.place(x=160, y=230,width=80,height=80)
                text34.place(x=240, y=230,width=80,height=80)
                text35.place(x=320, y=230,width=80,height=80)
                text36.place(x=400, y=230,width=80,height=80)
                text37.place(x=480, y=230,width=80,height=80)

                text3=[]
                text3.append(text31)
                text3.append(text32)
                text3.append(text33)
                text3.append(text34)
                text3.append(text35)
                text3.append(text36)
                text3.append(text37)

                flag=0
                for i in range(len(thi)):
                    if i>1:
                        text3[flag].insert(1.0,thi[i].get_text())
                        flag=flag+1

                text41=tkinter.Text(tab)
                text42=tkinter.Text(tab)
                text43=tkinter.Text(tab)
                text44=tkinter.Text(tab)
                text45=tkinter.Text(tab)
                text46=tkinter.Text(tab)
                text47=tkinter.Text(tab)

                text41.place(x=0, y=310,width=80,height=80)
                text42.place(x=80, y=310,width=80,height=80)
                text43.place(x=160, y=310,width=80,height=80)
                text44.place(x=240, y=310,width=80,height=80)
                text45.place(x=320, y=310,width=80,height=80)
                text46.place(x=400, y=310,width=80,height=80)
                text47.place(x=480, y=310,width=80,height=80)

                text4=[]
                text4.append(text41)
                text4.append(text42)
                text4.append(text43)
                text4.append(text44)
                text4.append(text45)
                text4.append(text46)
                text4.append(text47)

                flag=0
                for i in range(len(fou)):
                    if i>0:
                        text4[flag].insert(1.0,fou[i].get_text())
                        flag=flag+1

                text51=tkinter.Text(tab)
                text52=tkinter.Text(tab)
                text53=tkinter.Text(tab)
                text54=tkinter.Text(tab)
                text55=tkinter.Text(tab)
                text56=tkinter.Text(tab)
                text57=tkinter.Text(tab)

                text51.place(x=0, y=390,width=80,height=80)
                text52.place(x=80, y=390,width=80,height=80)
                text53.place(x=160, y=390,width=80,height=80)
                text54.place(x=240, y=390,width=80,height=80)
                text55.place(x=320, y=390,width=80,height=80)
                text56.place(x=400, y=390,width=80,height=80)
                text57.place(x=480, y=390,width=80,height=80)

                text5=[]
                text5.append(text51)
                text5.append(text52)
                text5.append(text53)
                text5.append(text54)
                text5.append(text55)
                text5.append(text56)
                text5.append(text57)

                flag=0
                for i in range(len(fiv)):
                    if i>1:
                        text5[flag].insert(1.0,fiv[i].get_text())
                        flag=flag+1
                

                

                
                
            L_Frame=ttk.Notebook(root1,width=80)
            tab1=tk.Frame(L_Frame)
            L_Frame.add(tab1, text='个人信息')
            L_Frame.pack(side=tk.LEFT, fill="y",ipadx=50)
            
            infm=get_stu_info(username, name)
            
            label1 = tkinter.Label(L_Frame, text=infm[0], justify=tkinter.RIGHT,width=80)
            label1.place(x=10, y=40, width=170, height=20)    #将标签放到窗口上
            
            label2 = tkinter.Label(L_Frame, text=infm[1], justify=tkinter.RIGHT,width=80)
            label2.place(x=10, y=60, width=170, height=20)    #将标签放到窗口上
            
            label3 = tkinter.Label(L_Frame, text=infm[2], justify=tkinter.RIGHT,width=80)
            label3.place(x=10, y=80, width=170, height=20)    #将标签放到窗口上
            
            label4 = tkinter.Label(L_Frame, text=infm[3], justify=tkinter.RIGHT,width=80)
            label4.place(x=10, y=100, width=170, height=20)    #将标签放到窗口上

            label5 = tkinter.Label(L_Frame, text=infm[4], justify=tkinter.RIGHT,width=80)
            label5.place(x=10, y=120, width=170, height=20)    #将标签放到窗口上
            
                
            R_Frame = ttk.Notebook(root1)
            

            
            
            tab2=tk.Frame(R_Frame)
            R_Frame.add(tab2, text='课表')
            varxnd = tkinter.StringVar()
            varxnd.set('2018')
            varxqd = tkinter.StringVar()
            varxqd.set('2')
            
            label6 = tkinter.Label(tab2, text="学年", justify=tkinter.RIGHT,width=80)
            label6.place(x=100, y=40, width=40, height=20)    #将标签放到窗口上
            label7 = tkinter.Label(tab2, text="学期", justify=tkinter.RIGHT,width=80)
            label7.place(x=300, y=40, width=40, height=20)    #将标签放到窗口上
            
            
            entryxnd = tkinter.Entry(tab2, width=80,textvariable=varxnd)#创建文本框
            entryxnd.place(x=140, y=40, width=80, height=20)
            entryxqd = tkinter.Entry(tab2, width=80,textvariable=varxqd)#创建文本框
            entryxqd.place(x=340, y=40, width=80, height=20)
            button1 = tkinter.Button(tab2, text='确定',command=lambda :get_schedule(username=username,name=name,n=entryxnd.get(),d=entryxqd.get(),tab=tab2))      #创建按钮组件,同时设置按钮事件处理函数                                             
            button1.place(x=500, y=40, width=50, height=20)

            
            
            tab3=tk.Frame(R_Frame)
            R_Frame.add(tab3, text='成绩')
            varxnd1 = tkinter.StringVar()
            varxnd1.set('2016')
            varxqd1 = tkinter.StringVar()
            varxqd1.set('1')
            
            label8 = tkinter.Label(tab3, text="学年", justify=tkinter.RIGHT,width=80)
            label8.place(x=100, y=40, width=40, height=20)    #将标签放到窗口上
            label9 = tkinter.Label(tab3, text="学期", justify=tkinter.RIGHT,width=80)
            label9.place(x=300, y=40, width=40, height=20)    #将标签放到窗口上
            
            
            entryxnd1 = tkinter.Entry(tab3, width=80,textvariable=varxnd1)#创建文本框
            entryxnd1.place(x=140, y=40, width=80, height=20)
            entryxqd1 = tkinter.Entry(tab3, width=80,textvariable=varxqd1)#创建文本框
            entryxqd1.place(x=340, y=40, width=80, height=20)
            button2 = tkinter.Button(tab3, text='确定',command=lambda :get_grade(username=username,name=name,n=entryxnd1.get(),d=entryxqd1.get(),tab=tab3))      #创建按钮组件,同时设置按钮事件处理函数                                             
            button2.place(x=500, y=40, width=50, height=20)

            def get_test():
                tkinter.messagebox.showerror('tk',message='现在不能查询')
            tab4=tk.Frame(R_Frame)
            R_Frame.add(tab4, text='考试')
            button2 = tkinter.Button(tab4, text='确定',command=get_test )     #创建按钮组件,同时设置按钮事件处理函数                                             
            button2.place(x=500, y=40, width=50, height=20)
            

            
            tab5=tk.Frame(R_Frame)
            R_Frame.add(tab5, text='空教室')
            """canvas=tk.Canvas(tab5,width=200,height=180,scrollregion=(0,0,600,600)) #创建canvas
            canvas.place(x = 75, y = 265) #放置canvas的位置
            tab=tk.Frame(canvas) #把frame放在canvas里
            tab.place(width=180, height=180) #frame的长宽，和canvas差不多的
            vbar=tk.Scrollbar(canvas,orient='vertical') #竖直滚动条
            vbar.place(x = 180,width=20,height=180)
            vbar.configure(command=canvas.yview)
            hbar=tk.Scrollbar(canvas,orient='horizontal')#水平滚动条
            hbar.place(x =0,y=165,width=180,height=20)
            hbar.configure(command=canvas.xview)
            canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set) #设置  
            canvas.create_window((90,240), window=tab5)
            """
            
            comvalue=tkinter.StringVar()#窗体自带的文本，新建一个值  
            comboxlist=ttk.Combobox(tab5,textvariable=comvalue) #初始化  
            comboxlist["values"]=("714",
                                  "115","215","315","415","515","615","715",
                                  "116","216","316","416","516","616","716",
                                  "117","217","317","417","517","615","717")
            def go():
                print("")
            comboxlist.bind("<<ComboboxSelected>>",go())  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
            comboxlist.place(x=500, y=40, width=50, height=20)
            
            button3 = tkinter.Button(tab5, text='确定',command=lambda :get_classroom(username=username,name=name,y=comboxlist,tab=tab5))      #创建按钮组件,同时设置按钮事件处理函数                                             
            button3.place(x=550, y=40, width=50, height=20)



            


                                           

            
            tab6=tk.Frame(R_Frame)
            R_Frame.add(tab6, text='培养方案')
            varxnd10 = tkinter.StringVar()
            varxnd10.set('5')

            
            label10 = tkinter.Label(tab6, text="建议修读学期", justify=tkinter.RIGHT,width=80)
            label10.place(x=100, y=40, width=80, height=20)    #将标签放到窗口上

            
            
            entryxnd10 = tkinter.Entry(tab6, width=80,textvariable=varxnd10)#创建文本框
            entryxnd10.place(x=180, y=40, width=80, height=20)

            button4 = tkinter.Button(tab6, text='确定',command=lambda :get_plan(username=username,name=name,x=entryxnd10.get(),tab=tab6))      #创建按钮组件,同时设置按钮事件处理函数                                             
            button4.place(x=500, y=40, width=50, height=20)
            R_Frame.pack(expand=1, fill="both")



            
            root1.mainloop()
            
        buttonOk = tkinter.Button(root, text='登录',command=lambda :login(u=entryName.get(),p=entryPwd.get(),c=varCode.get(),root=root))      #创建按钮组件,同时设置按钮事件处理函数
                                             
        buttonOk.place(x=30, y=80, width=50, height=20)




        buttonCancel = tkinter.Button(root, text='取消', command=cancel)
        buttonCancel.place(x=90, y=80, width=50, height=20)


        root.mainloop()          #启动消息循环

    
a = Anda()
a.login_UI() 
