# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\scrapy.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import os.path
import threading
import json
import pandas
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from spiders.tieba_gather_users import GatherSpider
from spiders.tieba_user_info import UserInfoSpider

class Ui_MainWindow(object):

    status = {
        'max_get': 9999999,
        'counter': 0,
        'msg': '',
        'forums': [],
        'running': False,
    }

    data_exists = False

    def setupUi(self, MainWindow):

        MainWindow.setFixedSize(400, 440)
        MainWindow.closeEvent = self.shutdown

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateUI)
        self.timer.start(50)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 400, 415))
        self.tab_1 = QtWidgets.QWidget()
        self.tab_2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_1, '贴吧用户获取')
        self.tabWidget.addTab(self.tab_2, '用户信息聚合')

        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_1)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 30, 320, 350))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setText("")
        self.lineEdit.returnPressed.connect(self.addForum)
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.clicked.connect(self.addForum)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.doubleClicked.connect(self.deleteForum)
        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setText('数据量上限(0表示无上限)')
        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setMaximum(self.status['max_get'])
        self.spinBox.valueChanged.connect(self.statusChanged)
        self.horizontalLayout_2.addWidget(self.spinBox)

        self.start_crawl = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.start_crawl.clicked.connect(self.start_gather)

        self.horizontalLayout_2.addWidget(self.start_crawl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        #---------------------------------------------------------------------------------------

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 30, 320, 350))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.btnImportFile = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnImportFile.clicked.connect(lambda _: self.label_filename.setText(QtWidgets.QFileDialog.getOpenFileName()[0]))
        self.horizontalLayout_3.addWidget(self.btnImportFile)

        self.label_filename = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_filename.setAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.horizontalLayout_3.addWidget(self.label_filename)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.btnStartGet = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnStartGet.clicked.connect(self.get_user_info)
        self.verticalLayout_2.addWidget(self.btnStartGet)

        self.treeWidget = QtWidgets.QTreeWidget(self.verticalLayoutWidget_2)
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.treeWidget.setHeaderItem(QtWidgets.QTreeWidgetItem(['项', '值']))

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.btnExportRaw = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnExportRaw.clicked.connect(self.exportRaw)

        self.horizontalLayout_4.addWidget(self.btnExportRaw)
        self.btnExportPcd = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btnExportPcd.clicked.connect(self.exportPcd)

        self.horizontalLayout_4.addWidget(self.btnExportPcd)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setVisible(False)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setFixedHeight(20)
        self.statusbar.addPermanentWidget(self.progressBar)
        self.statusbar.addPermanentWidget(self.label)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小爬虫-百度贴吧"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "输入贴吧名称"))
        self.pushButton.setText(_translate("MainWindow", "添加"))
        self.start_crawl.setText(_translate("MainWindow", "开始"))
        self.btnImportFile.setText(_translate("MainWindow", "选择文件..."))
        self.label_filename.setText(_translate("MainWindow", "选择需要聚合的用户列表文件"))
        self.btnStartGet.setText(_translate("MainWindow", "开始获取"))
        self.btnExportRaw.setText(_translate("MainWindow", "导出原始数据..."))
        self.btnExportPcd.setText(_translate("MainWindow", "导出已处理数据..."))

    def updateUI(self):
        if self.status['msg']:
            self.label.setVisible(True)
            self.label.setText(self.status['msg'])
        else:
            self.label.setVisible(False)
        if self.status.get('pct'):
            self.progressBar.setVisible(True)
            self.progressBar.setValue(self.status.get('pct'))
        else:
            self.progressBar.setVisible(False)
        if self.status.get('running'):
            self.tabWidget.setDisabled(True)
        else:
            self.tabWidget.setDisabled(False)
        if not self.data_exists and self.status.get('data'):
            self.data_exists = True
            self.process_data(self.status['data'])
        elif self.data_exists and not self.status.get('data'):
            self.treeWidget.clear()
            self.data_exists = False

    def addForum(self):
        if not self.lineEdit.text():
            return
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).text() == self.lineEdit.text():
                return
        self.listWidget.addItem(self.lineEdit.text())
        self.lineEdit.setText('')
        self.statusChanged()

    def deleteForum(self, item):
        self.listWidget.takeItem(item.row())
        self.statusChanged()

    def statusChanged(self):
        self.status['max_get'] = self.spinBox.value() or 9999999
        self.status['forums'].clear()
        for i in range(self.listWidget.count()):
            self.status['forums'].append(self.listWidget.item(i).text())

    def exportRaw(self):
        if self.on_missing_data():
            return
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self.tabWidget,
            "保存原始数据",
            "./用户原始数据.json",
            "JSON数据文件 (*.json)"
        )[0]
        if filename:
            open(filename, 'w').write(json.dumps(self.status['data']))

    def exportPcd(self):
        if self.on_missing_data():
            return
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self.tabWidget,
            "保存处理数据",
            "./自动处理的数据.csv",
            "逗号分隔值文档 (*.csv)"
        )[0]
        if not filename:
            return
        f = open(filename, 'w', encoding='gb18030')
        f.write('!!!本文档为自动生成的文档,请勿将此文档作为主文档编写!!!\n')
        Ui_MainWindow.write_tree_to_file(f, self.status['pcd_data'])
        f.close()

    def start_gather(self):
        if not self.listWidget.count():
            return
        CrawlingThread(GatherSpider, self.status).start()

    def get_user_info(self):
        if not os.path.isfile(self.label_filename.text()):
            QtWidgets.QMessageBox.warning(self.tabWidget, '文件查找失败', '无法找到指定文件')
            return
        self.status['data'] = None
        self.status['file'] = self.label_filename.text()
        if self.status['file'].lower().endswith('.json'):
            self.status['data'] = json.loads(open(self.status['file'], 'r').read())
        else:
            CrawlingThread(UserInfoSpider, self.status).start()

    def on_missing_data(self):
        if not self.status.get('data') or not self.status.get('pcd_data'):
            QtWidgets.QMessageBox.warning(self.tabWidget, '数据不存在', '还未完成分析文件操作，请先获取用户信息')
            return True
        return False

    def shutdown(self, e):
        e.accept()
        self.status['running'] = False

    def process_data(self, raw_data):
        pcd_data = {
            '性别': {
                '男': 0,
                '女': 0,
            },
            '吧龄': {
                '均值': 0,
                '中值': 0,
            },
            '发帖量': {
                '均值': 0,
                '中值': 0,
            },
            '关注贴吧情况': {
                '!EXTRA_INFO!': '人数  占比  平均等级',
                '具体关注贴吧': {},
                '人均贴吧总等级': 0,
            }
        }
        age_list = []
        postnum_list = []
        forums = {}
        total_level = 0
        for user in raw_data:
            if raw_data[user]['gender'] == 'male':
                pcd_data['性别']['男'] += 1
            else:
                pcd_data['性别']['女'] += 1
            age_list.append(raw_data[user]['age'])
            postnum_list.append(raw_data[user]['postNum'])
            for forum in raw_data[user]['forums']:
                if forum not in forums:
                    forums[forum] = []
                level = int(raw_data[user]['forums'][forum])
                forums[forum].append(level)
                total_level += level

        top_forums = sorted(forums, key=lambda k: len(forums[k]), reverse=True)
        pcd_data['吧龄']['!HIDDEN_DATA!'] = age_list
        pcd_data['发帖量']['!HIDDEN_DATA!'] = postnum_list

        pcd_data['性别']['男'] = '{}人 / {:.2f}%'.format(pcd_data['性别']['男'], pcd_data['性别']['男'] / len(raw_data) * 100)
        pcd_data['性别']['女'] = '{}人 / {:.2f}%'.format(pcd_data['性别']['女'], pcd_data['性别']['女'] / len(raw_data) * 100)
        series_age = pandas.Series(age_list)
        series_postnum = pandas.Series(postnum_list)
        pcd_data['吧龄']['均值'] = '{:.2f}年'.format(series_age.mean())
        pcd_data['吧龄']['中值'] = '{:.2f}年'.format(series_age.median())
        pcd_data['发帖量']['均值'] = '{:.2f}'.format(series_postnum.mean())
        pcd_data['发帖量']['中值'] = '{:.2f}'.format(series_postnum.median())
        pcd_data['关注贴吧情况']['人均贴吧总等级'] = '{:.2f}'.format(total_level / len(raw_data))
        for forum in top_forums:
            series = pandas.Series(forums[forum])
            pcd_data['关注贴吧情况']['具体关注贴吧'][forum] = '{}  {:.2f}%  {:.2f}'.format(len(forums[forum]), len(forums[forum]) / len(raw_data) * 100, series.mean())

        Ui_MainWindow.generate_tree(self.treeWidget, pcd_data)
        self.status['pcd_data'] = pcd_data

    @staticmethod
    def generate_tree(root, data):
        if type(data) is dict:
            for s, i in enumerate(data):
                if s >= 20:
                    break
                if i == '!HIDDEN_DATA!':
                    continue
                if i == '!EXTRA_INFO!':
                    root.setData(1, Qt.DisplayRole, data[i])
                else:
                    branch = QtWidgets.QTreeWidgetItem(root, [i])
                    Ui_MainWindow.generate_tree(branch, data[i])
        else:
            root.setData(1, Qt.DisplayRole, data)

    @staticmethod
    def write_tree_to_file(f, data, indent=0):
        if type(data) is list:
            for i in data:
                f.write('\n' + ',' * indent + str(i))
        elif type(data) is dict:
            for i in data:
                f.write('\n' + ',' * indent + str(i))
                Ui_MainWindow.write_tree_to_file(f, data[i], indent + 1)
        else:
            f.write(str(data).replace('  ', ',') + '\n')

class CrawlingThread(threading.Thread):

    def __init__(self, spider, status):
        threading.Thread.__init__(self)
        self.spider = spider
        self.status = status

    def run(self):
        self.spider(self.status)
