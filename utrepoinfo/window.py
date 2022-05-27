import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QTextBrowser, QHeaderView, QPushButton, QLabel, QWidget, \
    QTableWidgetItem, QTableWidget, QDesktopWidget, QMainWindow, QAbstractItemView, QHBoxLayout, QStyle, \
    QStyleOptionButton
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication, QEvent, QObject, pyqtSignal

try:
    from dnf_utils import UtBase

    rpmpkgs = UtBase().get_available_update_pkgs_details()
except Exception as e:
    print(e)
    rpmpkgs = [{'name': 'python-qt5-rpm-macros', 'release': '6.uel20', 'version': '5.11.3', 'arch': 'noarch',
                'downloadsize': 12276, 'downloadsize_human_readable': '12 k',
                'srpm': 'python-qt5-5.11.3-6.uel20.src.rpm', 'repo': 'aa', 'summary': 'RPM macros python-qt5',
                'url': 'http://www.riverbankcomputing.com/software/pyqt/', 'license': 'GPLv3',
                'desc': 'RPM macros python-qt5.'},
               {'name': 'python3-qt5', 'release': '6.uel20', 'version': '5.11.3', 'arch': 'x86_64',
                'downloadsize': 1104320, 'downloadsize_human_readable': '1.1 M',
                'srpm': 'python-qt5-5.11.3-6.uel20.src.rpm', 'repo': 'aa', 'summary': 'Python 3 bindings for Qt5',
                'url': 'http://www.riverbankcomputing.com/software/pyqt/', 'license': 'GPLv3',
                'desc': 'Python 3 bindings for Qt5.'},
               {'name': 'python3-qt5-base', 'release': '6.uel20', 'version': '5.11.3', 'arch': 'x86_64',
                'downloadsize': 2731180, 'downloadsize_human_readable': '2.6 M',
                'srpm': 'python-qt5-5.11.3-6.uel20.src.rpm', 'repo': 'aa', 'summary': 'Python 3 bindings for Qt5 base',
                'url': 'http://www.riverbankcomputing.com/software/pyqt/', 'license': 'GPLv3',
                'desc': 'Python 3 bindings for Qt5 base.'}]
qssStyle = '''
QPushButton#close{
    border-style:none;
    background-image: url(img/window_close_normal_light.png);
    background-position:center;
    background-repeat:no-repeat;
}
QPushButton#close::hover
{
	background-color: #E6E6E6;

}
QPushButton#hide{
    border-style:none;
    background-image: url(img/window_min_normal_light.png);
    background-position:center;
    background-repeat:no-repeat;
}
QPushButton#hide::hover
{
	background-color: #E6E6E6;

}
QPushButton[name~='btn']{
    width: 170px;
    height: 36px;
    background: rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.03);
    border-radius: 8px;
    box-shadow: 0px 4px 4px 0px rgba(0,145,255,0.30); 
}
QPushButton#update
{
	background-color: #0091FF;
	color: #FFFFFF;
}


QTextBrowser{
    background: rgba(255,255,255,0.50);
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
    font-size: 12px;
    font-family: Noto Mono;
}
QTableWidget{
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 8px;
    alternate-background-color: rgb(244,244,244);text-align:right;
}
QHeaderView::section
{
    border-width:6;
}
'''
"""
QHeaderView::section
{
    border: 1px solid red;
    margin: 1px;
    text-align: right;
    font-family: arial;
}
QPushButton[name~='btn']::hover
{
	background-color: #0091FF;
}
QCheckBox::indicator:unchecked{  
    image:url(img/checkbox_unchecked_insensitive.png);  
}  
  
QCheckBox::indicator:checked{  
    image:url(img/checkbox_checked_insensitive.png);  
}  
  
QCheckBox::indicator:checked:disabled{  
    image:url(img/checkbox_unchecked_insensitive.png);  
}  
"""


class Ui_rpm_update(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 移动到屏幕中心
        self.center()
        # 无边框设置
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TintedBackground)
        self.setObjectName("rpm_update")
        self.resize(640, 561)
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.setMouseTracking(False)

        # 左上角logo设置
        self.logo = QLabel(self)
        self.logo.setGeometry(15, 25, 80, 76)
        self.logo.setObjectName("logo")
        logo_pic = QPixmap('/home/weidong/Desktop/repo/rpmupdate/img/notify.png')
        self.logo.setPixmap(logo_pic.scaled(80, 76))

        self.title = QLabel(self)
        self.title.setGeometry(QRect(113, 26, 396, 25))
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.desc = QLabel(self)
        self.desc.setGeometry(QRect(113, 61, 396, 40))
        self.desc.setTextFormat(Qt.AutoText)
        self.desc.setScaledContents(False)
        self.desc.setWordWrap(True)
        self.desc.setObjectName("desc")

        self.hidebutton = QPushButton(self)
        self.hidebutton.setGeometry(QRect(542, 0, 50, 50))
        self.hidebutton.setObjectName("hide")
        self.hidebutton.clicked.connect(self.hide)

        self.closebutton = QPushButton(self)
        self.closebutton.setGeometry(QRect(592, 0, 50, 50))
        self.closebutton.setObjectName("close")
        self.closebutton.clicked.connect(QApplication.instance().quit)

        self.rpm_table_widget = QTableWidget(self)
        self.rpm_table_widget.setGeometry(QRect(10, 125, 620, 226))
        self.rpm_table_widget.setObjectName("rpm_table_widget")
        self.rpm_table_widget.viewport().installEventFilter(self)
        self.set_rpm_table_widget_header()
        self.init_rpm_info()

        self.output_console = QTextBrowser(self)
        self.output_console.setGeometry(QRect(10, 362, 620, 103))
        self.output_console.setObjectName("output_console")
        self.output_console.setReadOnly(True)

        self.rpm_status = QLabel(self)
        self.rpm_status.setGeometry(QRect(19, 475, 601, 20))
        font = QFont()
        font.setPointSize(12)
        self.rpm_status.setFont(font)
        self.rpm_status.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.rpm_status.setObjectName("rpm_status")

        self.cancle = QPushButton(self)
        self.cancle.setGeometry(QRect(140, 512, 170, 36))
        self.cancle.setObjectName("cancle")
        self.cancle.setProperty("name", 'btn')
        self.cancle.clicked.connect(self.clean_rpm)

        self.update = QPushButton(self)
        self.update.setGeometry(QRect(330, 512, 170, 36))
        self.update.setObjectName("update")
        self.update.setProperty("name", 'btn')
        self.update.clicked.connect(self.update_rpmpkges)

        self.setStyleSheet(qssStyle)
        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

    def set_rpm_table_widget_header(self):
        # 取消选中单元格的特效
        self.rpm_table_widget.setFocusPolicy(Qt.NoFocus)
        # 将表格变为禁止编辑
        self.rpm_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格为整行选择
        self.rpm_table_widget.setSelectionMode((QAbstractItemView.SingleSelection))
        self.rpm_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 设置交替色
        self.rpm_table_widget.setAlternatingRowColors(True)

        # 不显示表格单元格的分割线
        self.rpm_table_widget.setShowGrid(False)
        # 不显示垂直表头
        self.rpm_table_widget.verticalHeader().setVisible(False)
        # 设置行高36
        self.rpm_table_widget.verticalHeader().setDefaultSectionSize(36)
        # 设置表格高度
        self.rpm_table_widget.horizontalHeader().setFixedHeight(36)
        # 设置表头显示方式
        self.rpm_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 四列数据
        self.rpm_table_widget.setColumnCount(4)
        # 设置头
        header_checkbox = CheckBoxHeader()
        self.rpm_table_widget.setHorizontalHeader(header_checkbox)
        # self.rpm_table_widget.setHorizontalHeaderLabels(['Install', 'Software', 'Version', "Size"])
        self.rpm_table_widget.setHorizontalHeaderLabels(['', 'Software', 'Version', "Size"])
        # 设置表头显示方式
        self.rpm_table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_checkbox.select_all_clicked.connect(self.select_all_action)

        # 前三列固定宽度
        self.rpm_table_widget.setColumnWidth(0, 60)
        self.rpm_table_widget.setColumnWidth(1, 196)
        self.rpm_table_widget.setColumnWidth(2, 260)
        # 最后一列自适应宽度
        self.rpm_table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

    def init_rpm_info(self):
        self.check_status = []
        for i in rpmpkgs:
            ck = self.add_rpm_item("{name}({arch})".format(name=i["name"], arch=i["arch"]),
                                   "{version}-{release}".format(version=i["version"], release=i["release"]),
                                   i["downloadsize_human_readable"])
            self.check_status.append([ck, i["name"]])

    def select_all_action(self, event):
        if event:
            # 将所有的复选框都设为勾选状态
            for i in self.check_status:
                i[0].setCheckState(Qt.Checked)
        else:
            for i in self.check_status:
                i[0].setCheckState(Qt.Unchecked)

    def add_rpm_item(self, name, version, size):
        row = self.rpm_table_widget.rowCount()
        self.rpm_table_widget.setRowCount(row + 1)
        ck = QCheckBox()
        ck.toggled.connect(self.update_rpm_status)
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)
        self.rpm_table_widget.setCellWidget(row, 0, w)
        self.rpm_table_widget.setItem(row, 1, QTableWidgetItem(name))
        self.rpm_table_widget.setItem(row, 2, QTableWidgetItem(version))
        self.rpm_table_widget.setItem(row, 3, QTableWidgetItem(size))
        return ck

    def update_rpmpkges(self):
        select_rpm_list = []
        for i in range(self.rpm_table_widget.rowCount()):
            if self.check_status[i][0].isChecked():
                select_rpm_list.append(self.check_status[i][1])
        with UtBase() as base:
            base.update_rpmpkgs(select_rpm_list)

    def eventFilter(self, source, event):
        if self.rpm_table_widget.selectedIndexes() != []:
            if event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
                    row = self.rpm_table_widget.currentRow()
                    self.show_rpm_info(row)
        return QObject.event(source, event)

    def show_rpm_info(self, row):
        def get_rpm_info(rpmpkg):
            output_list = []
            name = "{0:<12}: {1}".format("Name", rpmpkg["name"])
            output_list.append(name)
            version = "{0:<12}: {1}".format("Version", rpmpkg["version"])
            output_list.append(version)
            release = "{0:<12}: {1}".format("Release", rpmpkg["release"])
            output_list.append(release)
            arch = "{0:<12}: {1}".format("Arch", rpmpkg["arch"])
            output_list.append(arch)
            size = "{0:<12}: {1}".format("Size", rpmpkg["downloadsize_human_readable"])
            output_list.append(size)
            srpm = "{0:<12}: {1}".format("Srpm", rpmpkg["srpm"])
            output_list.append(srpm)
            repo = "{0:<12}: {1}".format("Repository", rpmpkg["repo"])
            output_list.append(repo)
            summary = "{0:<12}: {1}".format("Summary", rpmpkg["summary"])
            output_list.append(summary)
            url = "{0:<12}: {1}".format("URL", rpmpkg["url"])
            output_list.append(url)
            license = "{0:<12}: {1}".format("License", rpmpkg["license"])
            output_list.append(license)
            desc = "{0:<12}: {1}".format("Description", rpmpkg["desc"])
            output_list.append(desc)
            return "\n".join(output_list)

        self.output_console.clear()
        try:
            rpminfo = get_rpm_info(rpmpkgs[row])
        except Exception as e:
            print(e)
        self.output_console.clear()
        self.output_console.append(rpminfo)

    def update_rpm_status(self):
        # return
        select_count = 0
        for i in range(self.rpm_table_widget.rowCount()):
            if self.check_status[i][0].isChecked():
                select_count += 1

        self.rpm_status.setText("{0} updates selected".format(str(select_count)))

    # 清空rpm信息展示列表
    def clean_rpm(self):
        self.rpm_table_widget.clearContents()
        self.rpm_table_widget.setRowCount(0)

    # 移动到屏幕中心
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def retranslateUi(self, rpm_update):
        _translate = QCoreApplication.translate
        rpm_update.setWindowTitle(_translate("rpm_update", "testReviewtitle"))
        self.cancle.setText(_translate("rpm_update", "cancle"))
        self.update.setText(_translate("rpm_update", "update"))
        self.rpm_status.setText(_translate("rpm_update", "0 update selected"))
        self.title.setText(_translate("rpm_update", "There are some updates available"))
        self.desc.setText(_translate("rpm_update",
                                     "Software updates correct errors，eliminate security vulnerabilities and provide new features"))
        self.hidebutton.setToolTip(_translate("rpm_update", "hide"))
        self.closebutton.setToolTip(_translate("rpm_update", "close"))

    # 实现窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    # 实现窗口拖动
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    # 实现窗口拖动
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


class CheckBoxHeader(QHeaderView):
    """自定义表头类"""

    # 自定义 复选框全选信号
    select_all_clicked = pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 23
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2.)

        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    ex = Ui_rpm_update()
    ex.setWindowOpacity(0.5)
    ex.show()
    app.exec_()