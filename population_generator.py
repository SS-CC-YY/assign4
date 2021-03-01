# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Notebook
from tkinter.ttk import Treeview
import requests
from bs4 import BeautifulSoup
import re
import csv
import sys
import socket
import os

from util import fileStruck


class PopulationGenerator:
    '''
    构造函数
    进行一些初始化
    '''

    def __init__(self):
        self.url = 'https://en.wikipedia.org/wiki/United_States_Census'
        self.stateUrl = 'https://en.wikipedia.org/wiki/%s_United_States_census'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}

        self.years = self.getYears()
        self.stateTotalMap = dict()
        self.resultData = None
        self.yearsMapIndex = {'1870': 2}
        self.outfile = open('output.csv', 'w', newline='')
        self.outDate = csv.writer(self.outfile)
        self.outDate.writerow(['input_year', 'input_state', 'output_population_size'])

    '''
    界面编写
    '''

    def ui(self):
        root = Tk()
        # 窗口的标题
        root.title('PopulationGenerator')

        # 创建大小和位置
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root_height = 400
        root_wight = 1000
        x_width = (width - root_wight) / 2
        x_height = (height - root_height) / 2
        root.geometry('%dx%d+%d+%d' % (root_wight, root_height, x_width, x_height))
        self.host = StringVar()
        self.port = StringVar()

        tab_main = Notebook(root)
        tab_main.place(relx=0.02, rely=0.02, relwidth=0.887, relheight=0.876)
        tab1 = Frame(tab_main)
        tab1.place(x=0, y=30)
        tab_main.add(tab1, text='wiki')  # 将第一页插入分页栏中

        frameTop = Frame(tab1, pady=10)
        frameTop.pack()
        frameCenter = Frame(tab1, pady=10)
        frameCenter.pack()
        frameBottom = Frame(tab1, pady=10)
        frameBottom.pack()

        # 选择年份的
        yearLabel = Label(frameTop, text='year:', font=12, pady=3, padx=5)

        yearLabel.grid(row=0, column=0)

        self.yearBox = Combobox(frameTop)

        self.yearBox['values'] = self.years
        self.yearBox.bind('<<ComboboxSelected>>', self.getState)

        self.yearBox.grid(row=0, column=1)

        # 选择州
        stateLabel = Label(frameTop, text='state:', font=12, pady=3, padx=5)
        stateLabel.grid(row=0, column=2)
        self.stateBox = Combobox(frameTop)
        self.stateBox.grid(row=0, column=3)

        hostLabel = Label(frameTop, text='host:', font=12, pady=3, padx=5)
        hostLabel.grid(row=1, column=0)
        self.hostText = Entry(frameTop, textvariable=self.host)
        self.hostText.grid(row=1, column=1)
        portLabel = Label(frameTop, text='port:', font=12, pady=3, padx=5)
        portLabel.grid(row=1, column=2)
        self.portText = Entry(frameTop, textvariable=self.port)
        self.portText.grid(row=1, column=3)

        # 请求按钮
        button = Button(frameBottom, text='generate', padx=30, pady=10, command=self.get_result)

        button.pack()

        # 显示数据结果
        # self.text = Text(frameBottom, height=4)
        self.resultData = StringVar()
        self.text = Label(frameBottom, textvariable=self.resultData, height=4, bg='green', fg='white', width=50,
                          font=15)
        self.text.pack()

        tab2 = Frame(tab_main)
        tab2.place(x=100, y=30)
        tab_main.add(tab2, text='life_server')
        frameTop2 = Frame(tab2, pady=10)
        frameTop2.pack()
        typeLabel = Label(frameTop2, text='type:', font=12, pady=3, padx=5)
        typeLabel.grid(row=0, column=0)
        self.typeValue = StringVar()
        typeEntry = Entry(frameTop2, textvariable=self.typeValue)
        typeEntry.grid(row=0, column=1)
        categoryLabel = Label(frameTop2, text='category:', font=12, pady=3, padx=5)
        categoryLabel.grid(row=1, column=0)
        self.categoryValue = StringVar()
        categoryEntry = Entry(frameTop2, textvariable=self.categoryValue)
        categoryEntry.grid(row=1, column=1)

        number_to_generateLabel = Label(frameTop2, text='number_to_generate:', font=12, pady=3, padx=5)
        number_to_generateLabel.grid(row=2, column=0)
        self.number_to_generateValue = StringVar()
        number_to_generateEntry = Entry(frameTop2, textvariable=self.number_to_generateValue)
        number_to_generateEntry.grid(row=2, column=1)

        frameBottom2 = Frame(tab2, pady=10)
        frameBottom2.pack()
        # 发送按钮
        button2 = Button(frameBottom2, text='send', padx=30, pady=10, command=self.sendToLifeServer)
        button2.pack()

        self.tableData = Treeview(tab2)
        self.tableData['columns'] = [str(i + 1) for i in range(20)]
        for item in self.tableData['columns']:
            self.tableData.column(item, width=40)
            self.tableData.heading(item, text=item)
        self.tableData.pack()
        scrollbar = Scrollbar(tab2, orient='horizontal', command=self.tableData.xview)
        scrollbar.pack()
        self.tableData.configure(yscrollcommand=scrollbar.set)

        root.mainloop()

    def sendToLifeServer(self):
        # print('sendToLifeServer')

        PORT = 5000
        HOST = 'localhost'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = [self.typeValue.get(), self.categoryValue.get(), self.number_to_generateValue.get()]
            data = [i for i in data if i != '']
            print(data)
            if len(data) >= 3:
                s.sendall(
                    bytes(','.join(data),
                          encoding="utf8"))
                server_msg = s.recv(4096).decode('utf-8')
                server_msg = eval(server_msg)
                for index, item in enumerate(server_msg):
                    print(item)
                    self.tableData.insert('', index, text=str(index), values=item)
                self.tableData.pack()

            else:
                print('输入信息不完整')

    '''
    '''

    def get_result(self):
        # # print('hello world')
        year = self.yearBox.get()
        state = self.stateBox.get()
        if self.stateTotalMap.__contains__(state):
            # print(year + ':' + state + ':' + self.stateTotalMap[state])
            self.resultData.set(self.stateTotalMap[state])
            self.outDate.writerow([year, state, self.stateTotalMap[state]])

    '''获取年份函数'''

    def getYears(self):
        return self.wikiYears()
        # return [1900, 1910, 1920]

    '''
    根据年份获取州的信息
    '''

    def getState(self, *args):
        self.stateTotalMap = self.wikiState(self.yearBox.get())
        # print(len(self.stateTotalMap), self.stateTotalMap)
        self.stateBox['values'] = [k for k in self.stateTotalMap]

    '''
    获取网页上的年份  > tbody > tr:nth-child(1) > td:nth-child(1) > a
    '''

    def wikiYears(self):
        r = requests.get(self.url, params={}).text
        soup = BeautifulSoup(r, 'html.parser')
        years = soup.select(
            '#mw-content-text > div.mw-parser-output > table.sortable.wikitable >tbody > tr >td:nth-child(1)>a')
        return [item.text for item in years]

    '''
    获取键值对 
        州：人数
    '''

    def wikiState(self, year):
        if year == '1790':
            return self.year1790(year)
        elif year == '1800':
            return self.year1800(year)
        elif year == '1870':
            return self.year1870(year)
        else:
            return self.yearOthers(year)
        return {'a': 333, 'b': 444, 'c': 555}

    def year1790(self, year):
        r = requests.get(self.stateUrl % year).text
        soup = BeautifulSoup(r, 'html.parser')
        stateNamesTemp = soup.select(
            '#mw-content-text > div.mw-parser-output>table.wikitable.sortable>tbody> tr>td:nth-child(1)>a')
        stateNames = [item.text for item in stateNamesTemp]
        stateTotalTemp = soup.select(
            '#mw-content-text > div.mw-parser-output >table.wikitable.sortable>tbody > tr > td:nth-child(8)')
        stateTotal = [getDigital(item.text) for item in stateTotalTemp]
        # print(len(stateNames), stateNames)
        # print(len(stateTotal), stateTotal)
        return {k.strip(): v for k, v in zip(stateNames, stateTotal)}

    '''

    '''

    def year1800(self, year):
        r = requests.get(self.stateUrl % year).text
        soup = BeautifulSoup(r, 'html.parser')
        stateNamesTemp = soup.select(
            '#mw-content-text > div.mw-parser-output>table.wikitable.sortable>tbody> tr>td:nth-child(1)')
        stateNames = [item.text.strip() for item in stateNamesTemp]
        stateTotalTemp = soup.select(
            '#mw-content-text > div.mw-parser-output >table.wikitable.sortable>tbody > tr > td:nth-child(14)')
        stateTotal = [getDigital(item.text) for item in stateTotalTemp]
        # print(len(stateNames), stateNames)
        # print(len(stateTotal), stateTotal)
        return {k.strip(): v for k, v in zip(stateNames, stateTotal)}

    '''
    #mw-content-text > div.mw-parser-output > table:nth-child(15) > tbody > tr:nth-child(1) > td:nth-child(2)
    '''

    def yearOthers(self, year):
        # print(year)
        r = requests.get(self.stateUrl % year).text
        soup = BeautifulSoup(r, 'html.parser')
        soupTemp = soup.select(
            '#mw-content-text > div.mw-parser-output > table.wikitable.sortable')[0]
        stateNamesTemp = soupTemp.select("tbody>tr>td:nth-child(2)")
        stateNames = [item.text for item in stateNamesTemp]
        stateTotalTemp = soupTemp.select(
            'tbody>tr>td:nth-child(3)')
        stateTotal = [getDigital(item.text) for item in stateTotalTemp]
        # print(len(stateNames), stateNames)
        # print(len(stateTotal), stateTotal)
        return {k.strip(): v for k, v in zip(stateNames, stateTotal)}

    '''
   #mw-content-text > div.mw-parser-output > table:nth-child(20) > tbody > tr:nth-child(1) > td:nth-child(2) 
    '''

    def year1870(self, year):
        # print(year)
        r = requests.get(self.stateUrl % year).text
        soup = BeautifulSoup(r, 'html.parser')
        soupTemp = soup.select(
            '#mw-content-text > div.mw-parser-output > table.wikitable.sortable.mw-collapsible')[1]

        stateNamesTemp = soupTemp.select("tbody>tr>td:nth-child(2)")
        stateNames = [item.text for item in stateNamesTemp]
        stateTotalTemp = soupTemp.select(
            'tbody>tr>td:nth-child(3)')
        stateTotal = [getDigital(item.text) for item in stateTotalTemp]
        # print(len(stateNames), stateNames)
        # print(len(stateTotal), stateTotal)
        return {k.strip(): v for k, v in zip(stateNames, stateTotal)}

    '''
    直接处理文件
    '''

    def dealCSV(self, name):
        inDate = csv.reader(open(name, 'r'))

        for row in inDate:
            # print(row)
            if row[0] != 'input_year':
                self.stateTotalMap = self.wikiState(row[0])
                row.append(self.stateTotalMap[row[1]] if self.stateTotalMap.__contains__(row[1]) else '')
                self.outDate.writerow(row)

    def getValue(self, year, state):
        state_to_pop = self.wikiState(year)
        return state_to_pop[state]
        # a_dict = {'Pennsylvania': '1,348,233', 'Virginia': '1,044,054'}
        # return a_dict[state]

    def sender(self, filename, host=None, port=None):
        '''
        发送文件给服务器
        :param filename:
        :param host:
        :param port:
        :return:
        '''
        if host is None:
            host = self.host.get()
        if port is None:
            port = self.port.get()
        if host != '' and port != '' and port.isdigit():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 连接服务，指定主机和端口
            s.connect((host, int(port)))

            fileLen = os.stat(filename).st_size

            a, b = fileStruck(filename, fileLen)

            s.send(a.to_bytes(4, byteorder='big', signed=False))

            s.send(b)

            has_sent = 0
            # print('发送文件', has_sent, fileLen)
            with open(filename, 'rb') as fb:
                while has_sent != fileLen:
                    data = fb.read(1024)
                    s.sendall(data)
                    has_sent += len(data)
                    # print(has_sent)
            s.close()

    def save(self):
        self.outfile.close()


'''
提取字符串前面的数字
'''


def getDigital(str):
    nums = re.findall(r'^[\d,\,]+', str)
    return nums[0] if len(nums) > 0 else -1


if __name__ == '__main__':
    generator = PopulationGenerator()
    host = None
    port = None
    isSend = False
    if len(sys.argv) == 1:
        generator.ui()
        isSend = True
    elif len(sys.argv) >= 2:
        generator.dealCSV(sys.argv[1])
        if len(sys.argv) == 4:
            host = sys.argv[2]
            port = sys.argv[3]
            isSend = True

    generator.save()
    if isSend:
        generator.sender('output.csv', host, port)
