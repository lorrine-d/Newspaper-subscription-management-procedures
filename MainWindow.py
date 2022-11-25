import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import Sign
import matplotlib.pyplot as plt
from pylab import mpl
from rich import print
import DBConnect
import csv
import os
import pymysql

class App(QWidget):

    def __init__(self):
        super().__init__()
        conf = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'pw': 'dd20001102',
            'db': 'book',
            'charset': 'utf8mb4'
        }
        self.db = DBConnect.Database(conf)
        self.sign = Sign.Sign()
        self.sub = SubWindow(self.db)
        self.titie = "登陆/注册"
        self.left = 20
        self.top = 20
        self.width = 300
        self.height = 360
        self.initUI()

    def initUI(self):
        #self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        # """设置窗体的标题"""
        self.setWindowTitle(self.titie)
        # """使用setGeometry(left, top, width, height)方法设置窗体的参数"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create textbox
        self.textboxUp = QLineEdit(self)
        self.textboxUp.move(100, 230)
        self.textboxUp.resize(150, 20)

        # create textbox
        self.textboxDown = QLineEdit(self)
        self.textboxDown.move(100, 280)
        self.textboxDown.resize(150, 20)
        self.textboxDown.setEchoMode(QLineEdit.Password)

        self.lableLeft = QLabel('用户名：', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(30, 230)

        self.lableRight = QLabel('密码：', self)
        self.lableRight.setWordWrap(True)
        self.lableRight.move(30, 280)

        self.buttonUp = QPushButton("登陆", self)
        self.buttonUp.setToolTip("点击这里进入")
        self.buttonUp.move(50, 320)
        self.buttonUp.clicked.connect(self.on_click_login)

        self.buttonDown = QPushButton("注册", self)
        self.buttonDown.setToolTip("没有账号？点击这里注册")
        self.buttonDown.move(180, 320)
        self.buttonDown.clicked.connect(self.on_click_rigister)

        self.pixmap = QPixmap("image/login.JPG")
        self.lablepix = QLabel(self)
        self.lablepix.setPixmap(self.pixmap)
        self.lablepix.move(50, 10)

        self.show()

    def get_item(self):
        item = {}
        item['Name'] = self.textboxUp.text()
        item['Passwd'] = self.textboxDown.text()
        return item

    @pyqtSlot()
    def on_click_login(self):
        try:
            if self.sign.Login(self.get_item()):
                print('Login!')
                self.close()
                self.sub.initUI()
            else:
                self.textboxUp.setText('')
                self.textboxDown.setText('')
                print('Login Failed!')
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_rigister(self):
        try:
            if self.sign.Rigister(self.get_item()):
                print('Rigister!')
            else:
                print('Rigister Failed!')
        except Exception as e:
            print(e)

#功能选择界面；有五个功能：报刊订阅，用户管理，报刊管理，查询统计，数据备份
class SubWindow(QWidget):

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.book = BookWindow(db)
        self.custom = CustomerWindow(db)
        self.Subscribe = SubscribeWindow(db)
        self.count = CountWindow(db)

    def initUI(self):
        self.title = "功能选择"
        self.left = 60
        self.top = 60
        self.width = 500
        self.height = 360
        #self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        # """设置窗体的标题"""
        self.setWindowTitle(self.title)
        # """使用setGeometry(left, top, width, height)方法设置窗体的参数"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.labeltitle = QLabel('欢迎使用报刊管理系统',self)
        self.labeltitle.move(170,10)

        self.buttonUp = QPushButton("报刊管理", self)
        self.buttonUp.setToolTip("This is an example button")
        self.buttonUp.move(50, 320)
        self.buttonUp.clicked.connect(self.on_click_book)

        self.buttonDown = QPushButton("订阅管理", self)
        self.buttonDown.setToolTip("This is an example button")
        self.buttonDown.move(280, 320)
        self.buttonDown.clicked.connect(self.on_click_subscribe)

        self.buttonUp = QPushButton("顾客管理", self)
        self.buttonUp.setToolTip("This is an example button")
        self.buttonUp.move(50, 280)
        self.buttonUp.clicked.connect(self.on_click_custom)

        self.buttonDown = QPushButton("统计功能", self)
        self.buttonDown.setToolTip("This is an example button")
        self.buttonDown.move(280, 280)
        self.buttonDown.clicked.connect(self.on_click_count)

        self.buttoncenter = QPushButton("数据备份", self)
        self.buttoncenter.setToolTip("This is an example button")
        self.buttoncenter.move(320, 30)
        self.buttoncenter.clicked.connect(self.backup_data)


        self.pixmap = QPixmap("image/login.jpg")
        self.lablepix = QLabel(self)
        self.lablepix.setPixmap(self.pixmap)
        self.lablepix.move(150, 50)

        self.show()

    @pyqtSlot()
    def on_click_book(self):
        try:
            #self.close()
            self.book.initUI()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_custom(self):
        try:
            #self.close()
            self.custom.initUI()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_subscribe(self):
        try:
            #self.close()
            self.Subscribe.initUI()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_count(self):
        try:
            #self.close()
            self.count.initUI()
        except Exception as e:
            print(e)

    # 数据库备份
    def backup_data(self):  # 数据库备份
        os.system('mysqldump -u root -pdd20001102 mysql > back_up_mysql.sql')
        QMessageBox.information(self, "消息", "备份成功", QMessageBox.Ok)


'''
CREATE TABLE IF NOT EXISTS `Book`(
   `BNO` INT UNSIGNED AUTO_INCREMENT,
   `BNAME` VARCHAR(100) NOT NULL,
   `BPRICE` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `BNO` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

#报刊管理界面；可以实现报刊增加，报刊查询（通过报刊号），报刊删除，报刊信息修改
class BookWindow(QWidget):

    def __init__(self, db):
        super().__init__()
        self.db = db
        #self.sub = SubWindow(db)

    def initUI(self):
        self.title = "管理报刊相关信息"
        self.left = 80
        self.top = 80
        self.width = 800
        self.height = 500

        # """设置窗体的标题"""
        self.setWindowTitle(self.title)
        # """使用setGeometry(left, top, width, height)方法设置窗体的参数"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create csv
        self.tableWidgetLeft = QTableWidget(self)
        self.tableWidgetLeft.setRowCount(50)
        self.tableWidgetLeft.setColumnCount(3)
        self.tableWidgetLeft.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['报刊号', '报刊名称', '报刊价格']
        self.tableWidgetLeft.setHorizontalHeaderLabels(headers)
        self.tableWidgetLeft.move(400, 30)
        self.tableWidgetLeft.resize(300, 350)

        self.lableLeft = QLabel('显示', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(430, 10)

        self.lableLeft = QLabel('从这里添加或修改', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(30, 10)


        self.tableWidgetRight = QTableWidget(self)
        self.tableWidgetRight.setRowCount(1)
        self.tableWidgetRight.setColumnCount(3)
        self.tableWidgetRight.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['报刊号', '报刊名称', '报刊价格']
        self.tableWidgetRight.setHorizontalHeaderLabels(headers)
        self.tableWidgetRight.move(30, 30)
        self.tableWidgetRight.resize(300, 60)

        self.tableWidgetDown = QTableWidget(self)
        self.tableWidgetDown.setRowCount(3)
        self.tableWidgetDown.setColumnCount(3)
        self.tableWidgetDown.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['报刊号', '报刊名称', '报刊价格']
        self.tableWidgetDown.setHorizontalHeaderLabels(headers)
        self.tableWidgetDown.move(30, 230)
        self.tableWidgetDown.resize(300, 60)

        self.lableLeftn = QLabel('note:' + '\n' +
                                 '输入需要添加的完整报刊信息后点击添加' + '\n' +
                                 '输入需要修改的报刊信息后点击修改' + '\n' +
                                 '输入需要查询或删除的报刊编号点击相关按键'
                                  , self)
        self.lableLeftn.setWordWrap(True)
        self.lableLeftn.move(30, 300)

        self.tabletext1 = QLineEdit(self)
        self.tabletext1.move(30,190)

        self.lableLeft = QLabel('查询或删除从这里', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(30, 170)

        self.buttonshow = QPushButton('显示所有报刊信息',self)
        self.buttonshow.move(400,400)
        self.buttonshow.clicked.connect(self.on_click_show)

        self.buttonFind = QPushButton("查询", self)
        self.buttonFind.move(180, 190)
        self.buttonFind.clicked.connect(self.on_click_find)

        self.buttonInsert = QPushButton("添加", self)
        self.buttonInsert.move(100, 120)
        self.buttonInsert.clicked.connect(self.on_click_insert)

        self.buttonUpdate = QPushButton("修改", self)
        self.buttonUpdate.move(170, 120)
        self.buttonUpdate.clicked.connect(self.on_click_update)

        self.buttonDelete = QPushButton("删除", self)
        self.buttonDelete.move(280, 190)
        self.buttonDelete.clicked.connect(self.on_click_delete)


        self.show()

    def get_item(self):
        item = {}
        thing = self.tableWidgetRight.item(0, 0)
        if thing is not None and thing.text() != '':
            item['BNO'] = thing.text()
        thing = self.tableWidgetRight.item(0, 1)
        if thing is not None and thing.text() != '':
            item['BNAME'] = thing.text()
        thing = self.tableWidgetRight.item(0, 2)
        if thing is not None and thing.text() != '':
            item['BPRICE'] = thing.text()
        return item

    def get_item2(self):
        item = {}
        item['BNO'] = self.tabletext1.text()
        print(item)
        print(item['BNO'])

    @pyqtSlot()
    def on_click_find(self):
        #self.tableWidgetLeft.clearContents()
        item = self.get_item2()
        print(item)
        #content = self.tabletext1.text()
        res = self.db.select_more_old('Book', ' BNAME LIKE "' + self.tabletext1.text() + '%";')
        print(res)
        try:
            # thing = self.tabletext1.text()
            for i in range(len(res)):
                self.tableWidgetDown.setItem(
                    i, 0, QTableWidgetItem(str(res[i]["BNO"])))
                self.tableWidgetDown.setItem(
                    i, 1, QTableWidgetItem(res[i]["BNAME"]))
                self.tableWidgetDown.setItem(
                    i, 2, QTableWidgetItem(res[i]["BPRICE"]))
            self.tableWidgetRight.clearContents()
        except:
            pass
            print('[INFO]', res, sep='\n')

        else:
            print('None')

    @ pyqtSlot()
    def on_click_update(self):
        item = self.get_item()
        self.db.update('Book', item, ' BNO="' + str(item['BNO']) + '" ;')

    @ pyqtSlot()
    def on_click_insert(self):
        item = self.get_item()
        self.db.insert('Book', item)

    @ pyqtSlot()
    def on_click_delete(self):
        #item = self.get_item2()
        self.db.delete1('Book', ' BNO= ' + self.tabletext1.text())

    @ pyqtSlot()
    def on_click_show(self):
        res = self.db.show_all('Book')
        print(res)
        print(len(res))

        try:
            for i in range(len(res)):
                self.tableWidgetLeft.setItem(i, 0, QTableWidgetItem(str(res[i]['BNO'])))
                self.tableWidgetLeft.setItem(i, 1, QTableWidgetItem(res[i]['BNAME']))
                self.tableWidgetLeft.setItem(i, 2, QTableWidgetItem(str(res[i]['BPRICE'])))
        except:
            pass

'''
CREATE TABLE IF NOT EXISTS `Custom`(
   `CNO` INT UNSIGNED AUTO_INCREMENT,
   `CNAME` VARCHAR(100) NOT NULL,
   `CDEPA` VARCHAR(40) NOT NULL,
   `CADDR` VARCHAR(100) NOT NULL,
   `CPHONE` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `CNO` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

#客户信息管理界面；可以实现增添顾客信息，修改顾客信息，删除顾客信息，查询顾客信息（通过顾客编号）
class CustomerWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def initUI(self):
        self.titie = "客户信息管理"
        self.left = 60
        self.top = 60
        self.width = 1200
        self.height = 550

        # """设置窗体的标题"""
        self.setWindowTitle(self.titie)
        # """使用setGeometry(left, top, width, height)方法设置窗体的参数"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create csv
        self.tableWidgetLeft = QTableWidget(self)

        self.tableWidgetLeft.setRowCount(100)
        self.tableWidgetLeft.setColumnCount(5)
        self.tableWidgetLeft.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['工号', '顾客姓名', '部门', '地址', '联系方式']
        self.tableWidgetLeft.setHorizontalHeaderLabels(headers)
        self.tableWidgetLeft.move(600, 30)
        self.tableWidgetLeft.resize(500, 350)

        self.labeltext1 = QLineEdit(self)
        self.labeltext1.move(30,190)

        self.lableLeft = QLabel('查询结果显示', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(600, 10)

        self.lableRight = QLabel('从这里添加或修改', self)
        self.lableRight.setWordWrap(True)
        self.lableRight.move(30, 10)

        self.lableLeft = QLabel('查询或删除从这里', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(30, 170)

        self.lableLeftn = QLabel('note:' + '\n' +
                                 '添加客户信息请输入完整后点击"添加"' + '\n' +
                                 '修改客户信息请输入修改后的完整信息后点击"修改"'+ '\n' +
                                 '查询客户信息请输入客户编号后点击"查询"' + '\n' +
                                 '删除客户信息请输入客户编号后点击"删除"', self)
        self.lableLeftn.setWordWrap(True)
        self.lableLeftn.move(30, 320)

        self.tableWidgetRight = QTableWidget(self)
        self.tableWidgetRight.setRowCount(1)
        self.tableWidgetRight.setColumnCount(5)
        self.tableWidgetRight.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['工号', '顾客姓名', '部门', '地址', '联系方式']
        self.tableWidgetRight.setHorizontalHeaderLabels(headers)
        self.tableWidgetRight.move(30, 30)
        self.tableWidgetRight.resize(500, 65)

        self.tableWidgetDown = QTableWidget(self)
        self.tableWidgetDown.setRowCount(1)
        self.tableWidgetDown.setColumnCount(5)
        self.tableWidgetDown.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['工号', '顾客姓名', '部门', '地址', '联系方式']
        self.tableWidgetDown.setHorizontalHeaderLabels(headers)
        self.tableWidgetDown.move(30, 230)
        self.tableWidgetDown.resize(500, 65)

        self.buttonFind = QPushButton("查询", self)
        self.buttonFind.move(180, 190)
        self.buttonFind.clicked.connect(self.on_click_find)

        self.buttonInsert = QPushButton("添加", self)
        self.buttonInsert.move(100, 110)
        self.buttonInsert.clicked.connect(self.on_click_insert)

        self.buttonUpdate = QPushButton("修改", self)
        self.buttonUpdate.move(220, 110)
        self.buttonUpdate.clicked.connect(self.on_click_update)

        self.buttonDelete = QPushButton("删除", self)
        self.buttonDelete.move(280, 190)
        self.buttonDelete.clicked.connect(self.on_click_delete)

        self.buttonshow = QPushButton("客户信息显示",self)
        self.buttonshow.move(600,400)
        self.buttonshow.clicked.connect(self.on_click_show)

        self.show()

    def get_item(self):
        item = {}
        thing = self.tableWidgetRight.item(0, 0)
        if thing is not None and thing.text() != '':
            item['CNO'] = thing.text()
        thing = self.tableWidgetRight.item(0, 1)
        if thing is not None and thing.text() != '':
            item['CNAME'] = thing.text()
        thing = self.tableWidgetRight.item(0, 2)
        if thing is not None and thing.text() != '':
            item['CDEPA'] = thing.text()
        thing = self.tableWidgetRight.item(0, 3)
        if thing is not None and thing.text() != '':
            item['CADDR'] = thing.text()
        thing = self.tableWidgetRight.item(0, 4)
        if thing is not None and thing.text() != '':
            item['CPHONE'] = thing.text()
        return item

    @pyqtSlot()
    def on_click_find(self):
        res = self.db.select_more_old('Custom', 'CNO=' + self.labeltext1.text())
        #print(res)
        try:
            for i in range(len(res)):
                self.tableWidgetDown.setItem(
                    i, 0, QTableWidgetItem(str(res[i]["CNO"])))
                self.tableWidgetDown.setItem(
                    i, 1, QTableWidgetItem(str(res[i]["CNAME"])))
                self.tableWidgetDown.setItem(
                    i, 2, QTableWidgetItem(str(res[i]["CDEPA"])))
                self.tableWidgetDown.setItem(
                    i, 3, QTableWidgetItem(str(res[i]["CADDR"])))
                self.tableWidgetDown.setItem(
                    i, 4, QTableWidgetItem(str(res[i]["CPHONE"])))
        except:
            pass
        print('[INFO]', res, sep='\n')


    @pyqtSlot()
    def on_click_update(self):
        item = self.get_item()
        self.db.update('Custom', item, ' CNO="' + str(item['CNO']) + '" ;')

    @pyqtSlot()
    def on_click_insert(self):
        item = self.get_item()
        self.db.insert('Custom', item)

    @pyqtSlot()
    def on_click_delete(self):
        #item = self.get_item()
        self.db.delete1('Custom', ' CNO=' + self.labeltext1.text())

    @pyqtSlot()
    def on_click_show(self):
        res = self.db.show_all('Custom')
        print(res)
        print(len(res))

        try:
            for i in range(len(res)):
                self.tableWidgetLeft.setItem(i, 0, QTableWidgetItem(str(res[i]['CNO'])))
                self.tableWidgetLeft.setItem(i, 1, QTableWidgetItem(res[i]['CNAME']))
                self.tableWidgetLeft.setItem(i, 2, QTableWidgetItem(str(res[i]['CDEPA'])))
                self.tableWidgetLeft.setItem(i, 3, QTableWidgetItem(str(res[i]['CADDR'])))
                self.tableWidgetLeft.setItem(i, 4, QTableWidgetItem(str(res[i]['CPHONE'])))
        except:
            pass

'''
CREATE TABLE IF NOT EXISTS `Subscribe`(
   `SNO` INT UNSIGNED AUTO_INCREMENT,
   `CNO` INT NOT NULL,
   `CNAME` VARCHAR(100) NOT NULL,
   `CDATE` VARCHAR(40) NOT NULL,
   `BNAME` VARCHAR(100) NOT NULL,
   `CYEAR` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `SNO` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

#订阅管理界面；顾客通过这个界面订阅，自动结算金额，查询订阅信息（通过订阅号）
class SubscribeWindow(QWidget):

    def __init__(self, db):
        super().__init__()
        self.db = db

    def initUI(self):
        self.titie = "客户订阅管理"
        self.left = 80
        self.top = 80
        self.width = 1300
        self.height = 600

        # """设置窗体的标题"""
        self.setWindowTitle(self.titie)
        # """使用setGeometry(left, top, width, height)方法设置窗体的参数"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create csv
        self.tableWidgetLeft = QTableWidget(self)
        self.tableWidgetLeft.setRowCount(50)
        self.tableWidgetLeft.setColumnCount(6)
        self.tableWidgetLeft.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['订阅号', '工号', '顾客姓名', '订阅日期', '报刊名', '订阅年限']
        self.tableWidgetLeft.setHorizontalHeaderLabels(headers)
        self.tableWidgetLeft.move(650, 30)
        self.tableWidgetLeft.resize(600, 350)

        self.lableRight = QLabel('从这里添加或修改', self)
        self.lableRight.setWordWrap(True)
        self.lableRight.move(30, 10)

        self.lableDown = QLabel('按人员查询',self)
        self.lableDown.setWordWrap(True)
        self.lableDown.move(10,160)

        self.lableLeft = QLabel('总览', self)
        self.lableLeft.setWordWrap(True)
        self.lableLeft.move(650, 10)

        self.tableWidgetRight = QTableWidget(self)
        self.tableWidgetRight.setRowCount(1)
        self.tableWidgetRight.setColumnCount(6)
        self.tableWidgetRight.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['订阅号', '工号', '用户名', '订阅日期', '报刊名', '订阅年限']
        self.tableWidgetRight.setHorizontalHeaderLabels(headers)
        self.tableWidgetRight.move(10, 30)
        self.tableWidgetRight.resize(600, 70)

        self.tableWidgetDown = QTableWidget(self)
        self.tableWidgetDown.setRowCount(1)
        self.tableWidgetDown.setColumnCount(6)
        self.tableWidgetDown.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['订阅号', '工号', '用户名', '订阅日期', '报刊名', '订阅年限']
        self.tableWidgetDown.setHorizontalHeaderLabels(headers)
        self.tableWidgetDown.move(10, 310)
        self.tableWidgetDown.resize(600, 70)

        self.lableLeftn = QLabel('note:' + '\n' +
                                 '添加订阅信息请输入完整后点击"添加"' + '\n' +
                                 '修改订阅信息请输入修改后的完整信息后点击"修改"' + '\n' +
                                 '按订阅号查询订阅信息请输入订阅号后点击"查询"' + '\n' +
                                 '按部门查询订阅信息请输入部门后点击"查询"' +
                                 '取消订阅信息请输入订阅号后点击"取消"', self)
        self.lableLeftn.setWordWrap(True)
        self.lableLeftn.move(30, 380)

        #search
        self.labletext1 = QLineEdit(self)
        self.labletext1.move(10,180)
        self.labletext1.resize(90,20)

        self.buttonFind = QPushButton("查询", self)
        self.buttonFind.move(110, 175)
        self.buttonFind.clicked.connect(self.on_click_find)

        self.buttonInsert = QPushButton("添加", self)
        self.buttonInsert.move(30, 120)
        self.buttonInsert.resize(90, 25)
        self.buttonInsert.clicked.connect(self.on_click_insert)

        self.buttonUpdate = QPushButton("更新", self)
        self.buttonUpdate.move(200, 120)
        self.buttonUpdate.resize(90, 25)
        self.buttonUpdate.clicked.connect(self.on_click_update)

        #price
        self.labeltext2 = QLineEdit(self)
        self.labeltext2.move(420,125)

        self.buttonCount = QPushButton('总价为', self)
        #self.lableDelete.setWordWrap(True)
        self.buttonCount.move(320, 120)
        self.buttonCount.clicked.connect(self.on_click_count)

        self.lableDelete = QLabel('取消订阅', self)
        self.lableDelete.setWordWrap(True)
        self.lableDelete.move(210, 220)

        #delete
        self.textboxDelete = QLineEdit(self)
        self.textboxDelete.move(210, 240)
        self.textboxDelete.resize(90, 20)

        self.buttonDelete = QPushButton("取消", self)
        self.buttonDelete.move(320, 235)
        self.buttonDelete.clicked.connect(self.on_click_delete)

        self.lableDepa = QLabel('按部门查询', self)
        self.lableDepa.setWordWrap(True)
        self.lableDepa.move(210, 160)

        self.textDepa = QLineEdit(self)
        self.textDepa.move(210, 180)
        self.textDepa.resize(90, 20)

        self.buttonDepa = QPushButton("查询", self)
        self.buttonDepa.move(320, 175)
        self.buttonDepa.clicked.connect(self.on_click_find_depa)

        self.buttonShow = QPushButton("显示",self)
        self.buttonShow.move(650,400)
        self.buttonShow.clicked.connect(self.on_click_show)

        self.show()

    def get_item(self):
        try:
            item = {}
            thing = self.tableWidgetRight.item(0, 0)
            if thing is not None and thing.text() != '':
                item['SNO'] = thing.text()
            thing = self.tableWidgetRight.item(0, 1)
            if thing is not None and thing.text() in [str(x["CNO"]) for x in self.db.select_more_old('Custom', '1', 'CNO')]:
                item['CNO'] = thing.text()
            else:
                return {}
            thing = self.tableWidgetRight.item(0, 2)
            if thing is not None and thing.text() == self.db.select_one('Custom', 'CNO=' + item['CNO'] + ' ', 'CNAME')['CNAME']:
                item['CNAME'] = thing.text()
            else:
                return {}
            thing = self.tableWidgetRight.item(0, 3)
            if thing is not None and thing.text() != '':
                item['CDATE'] = thing.text()
            thing = self.tableWidgetRight.item(0, 4)
            if thing is not None and thing.text() in [x["BNAME"] for x in self.db.select_more_old('Book', '1', 'BNAME')]:
                item['BNAME'] = thing.text()
            else:
                return {}
            thing = self.tableWidgetRight.item(0, 5)
            if thing is not None and thing.text() != '':
                item['CYEAR'] = thing.text()
            return item
        except Exception as e:
            print(e)

    def get_item_select(self):
        try:
            item = {}
            thing = self.tableWidgetRight.item(0, 0)
            if thing is not None and thing.text() != '':
                item['SNO'] = thing.text()
            thing = self.tableWidgetRight.item(0, 1)
            if thing is not None and thing.text() != '':
                item['CNO'] = thing.text()
            thing = self.tableWidgetRight.item(0, 2)
            if thing is not None and thing.text() != '':
                item['CNAME'] = thing.text()
            thing = self.tableWidgetRight.item(0, 3)
            if thing is not None and thing.text() != '':
                item['CDATE'] = thing.text()
            thing = self.tableWidgetRight.item(0, 4)
            if thing is not None and thing.text() != '':
                item['BNAME'] = thing.text()
            thing = self.tableWidgetRight.item(0, 5)
            if thing is not None and thing.text() != '':
                item['CYEAR'] = thing.text()
            return item
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_count(self):
        item = self.get_item_select()
        print(item)
        res = self.db.select('Book','Subscribe','BPRICE,CYEAR',
                               'Book.BNAME=Subscribe.BNAME'+' AND '+'Subscribe.BNAME=' + '"'+ item['BNAME'] + '"')
        #print(res)
        totle = int(res[0]['BPRICE']) * int(res[0]['CYEAR'])
        print(totle)
        self.labeltext2.setText(str(totle))


    @pyqtSlot()
    def on_click_find(self):
        #self.tableWidgetLeft.clearContents()
        #item = self.get_item_select()
        res = self.db.select_more_old('Subscribe', ' SNO=' + self.labletext1.text())
        print(res)
        try:
            #thing = self.tableWidgetRight.item(0, 0)
            for i in range(len(res)):
                self.tableWidgetDown.setItem(
                    i, 0, QTableWidgetItem(str(res[i]["SNO"])))
                self.tableWidgetDown.setItem(
                    i, 1, QTableWidgetItem(str(res[i]["CNO"])))
                self.tableWidgetDown.setItem(
                    i, 2, QTableWidgetItem(str(res[i]["CNAME"])))
                self.tableWidgetDown.setItem(
                    i, 3, QTableWidgetItem(str(res[i]["CDATE"])))
                self.tableWidgetDown.setItem(
                    i, 4, QTableWidgetItem(str(res[i]["BNAME"])))
                self.tableWidgetDown.setItem(
                    i, 5, QTableWidgetItem(str(res[i]["CYEAR"])))
            self.tableWidgetRight.clearContents()
        except:
            pass
            print('[INFO]', res, sep='\n')

    @ pyqtSlot()
    def on_click_update(self):
        item = self.get_item()
        if len(item) != 0:
            self.db.update('Subscribe', item, ' SNO="' + str(item['SNO']) + '" ;')

    @ pyqtSlot()
    def on_click_insert(self):
        item = self.get_item()
        if len(item) != 0:
            self.db.insert('Subscribe', item)

    @ pyqtSlot()
    def on_click_delete(self):
        item = {}
        #item['SNO'] = self.textboxDelete.text()
        #if len(item) != 0:
        self.db.delete1('Subscribe', ' SNO=' + self.textboxDelete.text())
    
    # on_click_find_depa
    @pyqtSlot()
    def on_click_find_depa(self):
        self.tableWidgetLeft.clearContents()
        if self.textDepa.text() != '':
            range_str = 'EXISTS (SELECT * FROM Custom WHERE Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME AND Custom.CDEPA="%s") GROUP BY Custom.CNO,Custom.CNAME;'%(self.textDepa.text())
            field = "Subscribe.SNO, Subscribe.CNO, Subscribe.CNAME, Subscribe.CDATE, Subscribe.BNAME, Subscribe.CYEAR"
            table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME) "
            res = self.db.select_more_old(table, range_str, field)
            try:
                thing = self.tableWidgetRight.item(0, 0)
                for i in range(len(res)):
                    self.tableWidgetDown.setItem(
                        i, 0, QTableWidgetItem(str(res[i]["SNO"])))
                    self.tableWidgetDown.setItem(
                        i, 1, QTableWidgetItem(str(res[i]["CNO"])))
                    self.tableWidgetDown.setItem(
                        i, 2, QTableWidgetItem(str(res[i]["CNAME"])))
                    self.tableWidgetDown.setItem(
                        i, 3, QTableWidgetItem(str(res[i]["CDATE"])))
                    self.tableWidgetDown.setItem(
                        i, 4, QTableWidgetItem(str(res[i]["BNAME"])))
                    self.tableWidgetDown.setItem(
                        i, 5, QTableWidgetItem(str(res[i]["CYEAR"])))
                self.tableWidgetRight.clearContents()
            except:
                pass
            print('[INFO]', res, sep='\n')

        else:
            print('None')

    def on_click_show(self):
        res = self.db.show_all('Subscribe')
        print(res)
        print(len(res))

        try:
            for i in range(len(res)):
                self.tableWidgetLeft.setItem(i, 0, QTableWidgetItem(str(res[i]['SNO'])))
                self.tableWidgetLeft.setItem(i, 1, QTableWidgetItem(str(res[i]['CNO'])))
                self.tableWidgetLeft.setItem(i, 2, QTableWidgetItem(res[i]['CNAME']))
                self.tableWidgetLeft.setItem(i, 3, QTableWidgetItem(str(res[i]['CDATE'])))
                self.tableWidgetLeft.setItem(i, 4, QTableWidgetItem(res[i]['BNAME']))
                self.tableWidgetLeft.setItem(i, 5, QTableWidgetItem(str(res[i]['CYEAR'])))
        except:
            pass

#统计界面
class CountWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.graphBook = Main_book(db)
        self.graphDepa = Main_depa(db)
        self.graphCust = Main_cust(db)

    def initUI(self):
        self.titie = "报刊订阅统计"
        self.left = 60
        self.top = 60
        self.width = 900
        self.height = 350

        # """设置窗体的标题"""
        self.setWindowTitle(self.titie)
        # """使用setGeometry(left, top, width, height)方法设置窗体的参数"""
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create csv
        #self.tableWidgetLeft = QTableWidget(self)
        self.lableDepa = QLabel('按部门统计', self)
        self.lableDepa.setWordWrap(True)
        self.lableDepa.move(10, 10)

        self.tableWidgetDepa = QTableWidget(self)
        self.tableWidgetDepa.setRowCount(100)
        self.tableWidgetDepa.setColumnCount(2)
        self.tableWidgetDepa.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['部门', '订阅数量']
        self.tableWidgetDepa.setHorizontalHeaderLabels(headers)
        self.tableWidgetDepa.move(10, 30)
        self.tableWidgetDepa.resize(200, 200)
        self.set_depa()

        self.lableCustom = QLabel('按人员统计', self)
        self.lableCustom.setWordWrap(True)
        self.lableCustom.move(320, 10)

        self.tableWidgetCustom = QTableWidget(self)
        self.tableWidgetCustom.setRowCount(100)
        self.tableWidgetCustom.setColumnCount(2)
        self.tableWidgetCustom.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['顾客', '订阅数量']
        self.tableWidgetCustom.setHorizontalHeaderLabels(headers)
        self.tableWidgetCustom.move(320, 30)
        self.tableWidgetCustom.resize(200, 200)
        self.set_custom()

        self.lableBook = QLabel('按报刊统计', self)
        self.lableBook.setWordWrap(True)
        self.lableBook.move(630, 10)

        self.tableWidgetBook = QTableWidget(self)
        self.tableWidgetBook.setRowCount(100)
        self.tableWidgetBook.setColumnCount(2)
        self.tableWidgetBook.verticalHeader().setVisible(False)  # 隐藏列表头
        headers = ['报刊', '订阅数量']
        self.tableWidgetBook.setHorizontalHeaderLabels(headers)
        self.tableWidgetBook.move(630, 30)
        self.tableWidgetBook.resize(200, 200)
        self.set_book()

        self.buttonGraphBook = QPushButton("报刊柱状图",self)
        self.buttonGraphBook.move(630,300)
        self.buttonGraphBook.clicked.connect(self.on_click_graphbook)

        self.buttonGraphDepa = QPushButton("部门柱状图", self)
        self.buttonGraphDepa.move(10, 300)
        self.buttonGraphDepa.clicked.connect(self.on_click_graphdepa)

        self.buttonGraphCust = QPushButton("客户柱状图", self)
        self.buttonGraphCust.move(320, 300)
        self.buttonGraphCust.clicked.connect(self.on_click_graphcust)

        self.buttonDepa = QPushButton("打印报表", self)
        self.buttonDepa.setToolTip("This is an example button")
        self.buttonDepa.move(10, 240)
        self.buttonDepa.clicked.connect(self.on_click_depa)

        self.buttonCustom = QPushButton("打印报表", self)
        self.buttonCustom.setToolTip("This is an example button")
        self.buttonCustom.move(320, 240)
        self.buttonCustom.clicked.connect(self.on_click_custom)

        self.buttonBook = QPushButton("打印报表", self)
        self.buttonBook.setToolTip("This is an example button")
        self.buttonBook.move(630, 240)
        self.buttonBook.clicked.connect(self.on_click_book)

        self.show()

        # def gen_depa_pie(self):
        #     keyscount = []
        #     valuescount = []
        #     filed = "DISTINCT Custom.CDEPA"
        #     table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
        #     for i in self.db.select_more_old(table, '1', filed):
        #         keyscount.append(i['CDEPA'])
        #         valuescount.append(self.db.select_more_old("Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)",
        #                                         'Custom.CDEPA = "%s"'%(i['CDEPA']),
        #                                         'COUNT(*) AS NUM')[0]['NUM']
        #                                         )
        #     # self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
        #     keyssum = []
        #     valuessum = []
        #     filed = "DISTINCT Custom.CDEPA"
        #     table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
        #     for i in self.db.select_more_old(table, '1', filed):
        #         keyssum.append(i['CDEPA'])
        #         valuessum.append(self.db.select_more_old("(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
        #                                         'Custom.CDEPA = "%s"'%(i['CDEPA']),
        #                                         'SUM(Book.BPRICE) AS NUM')[0]['NUM']
        #                                         )
        #     # self.pic.gen_pie(keyssum, valuessum, 'image/piedepa2.png')
        #     return keyscount, valuescount, keyssum, valuessum

    def set_depa(self):
        keyscount = []
        valuescount = []
        filed = "DISTINCT Custom.CDEPA"
        table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
        for i in self.db.select_more_old(table, '1', filed):
            keyscount.append(i['CDEPA'])
            valuescount.append(self.db.select_more_old(
                "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)",
                'Custom.CDEPA = "%s"' % (i['CDEPA']),
                'COUNT(*) AS NUM')[0]['NUM']
                               )
        # self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
        keyssum = []
        valuessum = []
        filed = "DISTINCT Custom.CDEPA"
        table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
        for i in self.db.select_more_old(table, '1', filed):
            keyssum.append(i['CDEPA'])
            valuessum.append(self.db.select_more_old(
                "(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
                'Custom.CDEPA = "%s"' % (i['CDEPA']),
                'SUM(Book.BPRICE) AS NUM')[0]['NUM'])

        if len(keyscount) != 0:
            try:
                for i in range(len(keyscount)):
                    self.tableWidgetDepa.setItem(
                        i, 0, QTableWidgetItem(str(keyscount[i])))
                    self.tableWidgetDepa.setItem(
                        i, 1, QTableWidgetItem(str(valuescount[i])))
                    #self.tableWidgetDepa.setItem(
                    #    i, 2, QTableWidgetItem(str(valuessum[i])))
            except Exception as e:
                print(e)

    def set_custom(self):
        keyscount = []
        valuescount = []
        filed = "CNAME"
        table = "Custom"
        for i in self.db.select_more_old(table, '1', filed):
            keyscount.append(i['CNAME'])
            valuescount.append(self.db.select_more_old("Subscribe",
                                                       'Subscribe.CNAME = "%s"' % (i['CNAME']),
                                                       'COUNT(*) AS NUM')[0]['NUM']
                               )
        #self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
        keyssum = []
        valuessum = []
        filed = "CNAME"
        table = "Custom"
        for i in self.db.select_more_old(table, '1', filed):
            keyssum.append(i['CNAME'])
            valuessum.append(self.db.select_more_old(
                "(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
                'Subscribe.CNAME = "%s"' % (i['CNAME']),
                'SUM(Book.BPRICE) AS NUM')[0]['NUM'])

        if len(keyscount) != 0:
            try:
                for i in range(len(keyscount)):
                    self.tableWidgetCustom.setItem(
                        i, 0, QTableWidgetItem(str(keyscount[i])))
                    self.tableWidgetCustom.setItem(
                        i, 1, QTableWidgetItem(str(valuescount[i])))
                    #self.tableWidgetCustom.setItem(
                    #    i, 2, QTableWidgetItem(str(valuessum[i])))
            except Exception as e:
                print(e)

    def set_book(self):
        keyscount = []
        valuescount = []
        filed = "BNAME"
        table = "Book"
        for i in self.db.select_more_old(table, '1', filed):
            keyscount.append(i['BNAME'])
            valuescount.append(self.db.select_more_old("Subscribe",
                                                       'Subscribe.BNAME = "%s"' % (i['BNAME']),
                                                       'COUNT(*) AS NUM')[0]['NUM']
                               )
        # self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
        keyssum = []
        valuessum = []
        filed = "BNAME"
        table = "Book"
        for i in self.db.select_more_old(table, '1', filed):
            keyssum.append(i['BNAME'])
            valuessum.append(self.db.select_more_old(
                "(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
                'Subscribe.BNAME = "%s"' % (i['BNAME']),
                'SUM(Book.BPRICE) AS NUM')[0]['NUM']
                             )

        if len(keyscount) != 0:
            try:
                for i in range(len(keyscount)):
                    self.tableWidgetBook.setItem(
                        i, 0, QTableWidgetItem(str(keyscount[i])))
                    self.tableWidgetBook.setItem(
                        i, 1, QTableWidgetItem(str(valuescount[i])))
                    #self.tableWidgetBook.setItem(
                    #    i, 2, QTableWidgetItem(str(valuessum[i])))
            except Exception as e:
                print(e)

    @pyqtSlot()
    def on_click_depa(self):
        try:
            keyscount = []
            valuescount = []
            filed = "DISTINCT Custom.CDEPA"
            table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
            for i in self.db.select_more_old(table, '1', filed):
                keyscount.append(i['CDEPA'])
                valuescount.append(self.db.select_more_old(
                    "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)",
                    'Custom.CDEPA = "%s"' % (i['CDEPA']),
                    'COUNT(*) AS NUM')[0]['NUM']
                                   )
            # self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
            keyssum = []
            valuessum = []
            filed = "DISTINCT Custom.CDEPA"
            table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
            res = self.db.select_more_old(table,'1',filed)
            for i in self.db.select_more_old(table, '1', filed):
                keyssum.append(i['CDEPA'])
                valuessum.append(self.db.select_more_old(
                    "(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
                    'Custom.CDEPA = "%s"' % (i['CDEPA']),
                    'SUM(Book.BPRICE) AS NUM')[0]['NUM'])
            headers = ['部门', '订阅数量', '总价']
            res = []
            #with open('depa.txt', 'w+') as f:
            #    for result in res:
            #        f.write(str(result) + '\n')
            #print('Data write is over!')
            for i in range(len(keyscount)):
                res.append({
                    headers[0]: keyscount[i],
                    headers[1]: valuescount[i],
                    headers[2]: valuessum[i]
                })
            with open('Depa.csv', 'w+') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(res)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_custom(self):
        try:
            keyscount = []
            valuescount = []
            filed = "CNAME"
            table = "Custom"
            for i in self.db.select_more_old(table, '1', filed):
                keyscount.append(i['CNAME'])
                valuescount.append(self.db.select_more_old("Subscribe",
                                                           'Subscribe.CNAME = "%s"' % (i['CNAME']),
                                                           'COUNT(*) AS NUM')[0]['NUM']
                                   )
            # self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
            keyssum = []
            valuessum = []
            filed = "CNAME"
            table = "Custom"
            for i in self.db.select_more_old(table, '1', filed):
                keyssum.append(i['CNAME'])
                valuessum.append(self.db.select_more_old(
                    "(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
                    'Subscribe.CNAME = "%s"' % (i['CNAME']),
                    'SUM(Book.BPRICE) AS NUM')[0]['NUM'])
            headers = ['顾客', '订阅数量', '总价']
            res = []
            for i in range(len(keyscount)):
                res.append({
                    headers[0]: keyscount[i],
                    headers[1]: valuescount[i],
                    headers[2]: valuessum[i]
                })
            with open('Custom.csv', 'w+') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(res)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_book(self):
        try:
            keyscount = []
            valuescount = []
            filed = "BNAME"
            table = "Book"
            for i in self.db.select_more_old(table, '1', filed):
                keyscount.append(i['BNAME'])
                valuescount.append(self.db.select_more_old("Subscribe",
                                                           'Subscribe.BNAME = "%s"' % (i['BNAME']),
                                                           'COUNT(*) AS NUM')[0]['NUM']
                                   )
            # self.pic.gen_pie(keyscount, valuescount, 'image/piedepa1.png')
            keyssum = []
            valuessum = []
            filed = "BNAME"
            table = "Book"
            for i in self.db.select_more_old(table, '1', filed):
                keyssum.append(i['BNAME'])
                valuessum.append(self.db.select_more_old(
                    "(Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)) LEFT OUTER JOIN Book ON (Subscribe.BNAME = Book.BNAME)",
                    'Subscribe.BNAME = "%s"' % (i['BNAME']),
                    'SUM(Book.BPRICE) AS NUM')[0]['NUM']
                                 )
            headers = ['报刊', '订阅数量', '总价']
            res = []
            for i in range(len(keyscount)):
                res.append({
                    headers[0]: keyscount[i],
                    headers[1]: valuescount[i],
                    headers[2]: valuessum[i]
                })
            with open('Book.csv', 'w+') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(res)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_graphbook(self):
        try:
          self.graphBook.show_graph_book()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_graphdepa(self):
        try:
            self.graphDepa.show_graph_depa()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click_graphcust(self):
        try:
            self.graphCust.show_graph_cust()
        except Exception as e:
            print(e)


#book柱状图显示
class Main_book(QMainWindow):
    def __init__(self,db):
        super().__init__()
        self.db = db
        self.setWindowTitle("商品数量显示图")
        self.resize(500,700)
        self.showgraph = QPushButton("查看商品数量柱状图", self)
        self.showgraph.setGeometry(170, 400, 200, 40)
        self.showgraph.clicked.connect(self.show_graph_book)
    def show_graph_book(self):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        keyscount = [] # x
        valuescount = [] # y
        filed = "BNAME"
        table = "Book"
        for i in self.db.select_more_old(table, '1', filed):
            keyscount.append(i['BNAME'])
            valuescount.append(int(self.db.select_more_old("Subscribe",
                                                   'Subscribe.BNAME = "%s"' % (i['BNAME']),
                                                   'COUNT(*) AS NUM')[0]['NUM']))

        print(keyscount)
        print(valuescount)
        #connect.close()
        set1 = set(keyscount)
        m = len(set1)
        plt.bar(range(m), valuescount, align='center', color='steelblue', alpha=0.8)
        plt.ylabel("数量")
        plt.title("商品号")
        plt.xticks(range(m), keyscount)
        plt.ylim([0, 10])
        for x, y in enumerate(valuescount):
            plt.text(x, y + 1, '%s' % round(y, 1), ha='center')
        plt.show()

#depa柱状图显示
class Main_depa(QMainWindow):
    def __init__(self,db):
        super().__init__()
        self.db = db
        self.setWindowTitle("商品数量显示图")
        self.resize(500,700)
        self.showgraph = QPushButton("查看商品数量柱状图", self)
        self.showgraph.setGeometry(170, 400, 200, 40)
        self.showgraph.clicked.connect(self.show_graph_depa)
    def show_graph_depa(self):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        keyscount = [] # x
        valuescount = [] # y
        filed = "DISTINCT Custom.CDEPA"
        table = "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)"
        for i in self.db.select_more_old(table, '1', filed):
            keyscount.append(i['CDEPA'])
            valuescount.append(self.db.select_more_old(
                "Subscribe LEFT OUTER JOIN Custom ON (Custom.CNO=Subscribe.CNO AND Custom.CNAME=Subscribe.CNAME)",
                'Custom.CDEPA = "%s"' % (i['CDEPA']),
                'COUNT(*) AS NUM')[0]['NUM']
                               )
        print(keyscount)
        print(valuescount)
        #connect.close()
        set1 = set(keyscount)
        m = len(set1)
        plt.bar(range(m), valuescount, align='center', color='steelblue', alpha=0.8)
        plt.ylabel("数量")
        plt.title("部门号")
        plt.xticks(range(m), keyscount)
        plt.ylim([0, 10])
        for x, y in enumerate(valuescount):
            plt.text(x, y + 1, '%s' % round(y, 1), ha='center')
        plt.show()

#custom柱状图显示
class Main_cust(QMainWindow):
    def __init__(self,db):
        super().__init__()
        self.db = db
        self.setWindowTitle("商品数量显示图")
        self.resize(500,700)
        self.showgraph = QPushButton("查看商品数量柱状图", self)
        self.showgraph.setGeometry(170, 400, 200, 40)
        self.showgraph.clicked.connect(self.show_graph_cust)
    def show_graph_cust(self):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        keyscount = [] # x
        valuescount = [] # y
        filed = "CNAME"
        table = "Custom"
        for i in self.db.select_more_old(table, '1', filed):
            keyscount.append(i['CNAME'])
            valuescount.append(self.db.select_more_old("Subscribe",
                                                       'Subscribe.CNAME = "%s"' % (i['CNAME']),
                                                       'COUNT(*) AS NUM')[0]['NUM']
                               )
        print(keyscount)
        print(valuescount)
        #connect.close()
        set1 = set(keyscount)
        m = len(set1)
        plt.bar(range(m), valuescount, align='center', color='steelblue', alpha=0.8)
        plt.ylabel("数量")
        plt.title("客户订阅量")
        plt.xticks(range(m), keyscount)
        plt.ylim([0, 10])
        for x, y in enumerate(valuescount):
            plt.text(x, y + 1, '%s' % round(y, 1), ha='center')
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
