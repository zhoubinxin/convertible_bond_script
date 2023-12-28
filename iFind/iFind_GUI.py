import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QGroupBox, \
    QCheckBox, QMessageBox
from PyQt5.QtCore import pyqtSignal


class DataWindow(QWidget):
    data_ready = pyqtSignal(dict)  # 定义信号

    def __init__(self):
        super().__init__()
        self.setWindowTitle('可转债数据')
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        value_group = QGroupBox("转股价值筛选")
        value_layout = QGridLayout()
        self.value_check = QCheckBox('是否筛选转股价值')
        value_layout.addWidget(self.value_check, 0, 0, 1, 2)
        self.max_value_label = QLabel('最大价值')
        self.max_value_input = QLineEdit()
        self.max_value_input.setEnabled(False)  # 初始禁用输入框
        value_layout.addWidget(self.max_value_label, 1, 0)
        value_layout.addWidget(self.max_value_input, 1, 1)
        self.min_value_label = QLabel('最小价值')
        self.min_value_input = QLineEdit()
        self.min_value_input.setEnabled(False)  # 初始禁用输入框
        value_layout.addWidget(self.min_value_label, 2, 0)
        value_layout.addWidget(self.min_value_input, 2, 1)
        value_group.setLayout(value_layout)
        layout.addWidget(value_group)

        balance_group = QGroupBox("债券余额筛选")
        balance_layout = QGridLayout()
        self.balance_check = QCheckBox('是否筛选债券余额')
        balance_layout.addWidget(self.balance_check, 0, 0, 1, 2)
        self.max_balance_label = QLabel('最大值')
        self.max_balance_input = QLineEdit()
        self.max_balance_input.setEnabled(False)  # 初始禁用输入框
        balance_layout.addWidget(self.max_balance_label, 1, 0)
        balance_layout.addWidget(self.max_balance_input, 1, 1)
        self.min_balance_label = QLabel('最小值')
        self.min_balance_input = QLineEdit()
        self.min_balance_input.setEnabled(False)  # 初始禁用输入框
        balance_layout.addWidget(self.min_balance_label, 2, 0)
        balance_layout.addWidget(self.min_balance_input, 2, 1)
        balance_group.setLayout(balance_layout)
        layout.addWidget(balance_group)

        issue_group = QGroupBox("债券评级筛选")
        issue_layout = QGridLayout()
        self.issue_check = QCheckBox('是否筛选债券评级')
        issue_layout.addWidget(self.issue_check, 0, 0, 1, 2)
        self.issue_label = QLabel('债券评级')
        self.issue_input = QLineEdit()
        self.issue_input.setEnabled(False)  # 初始禁用输入框
        issue_layout.addWidget(self.issue_label, 1, 0)
        issue_layout.addWidget(self.issue_input, 1, 1)
        issue_group.setLayout(issue_layout)
        layout.addWidget(issue_group)

        get_data_button = QPushButton('确定')
        get_data_button.clicked.connect(self.on_button_click)
        layout.addWidget(get_data_button)

        self.setLayout(layout)

        # 连接复选框信号与槽函数
        self.value_check.stateChanged.connect(self.on_value_check_changed)
        self.balance_check.stateChanged.connect(self.on_balance_check_changed)
        self.issue_check.stateChanged.connect(self.on_issue_check_changed)

    # 复选框状态变化时的槽函数
    def on_value_check_changed(self, state):
        checked = state == 2  # 2 表示选中状态
        self.max_value_input.setEnabled(checked)
        self.min_value_input.setEnabled(checked)

    def on_balance_check_changed(self, state):
        checked = state == 2
        self.max_balance_input.setEnabled(checked)
        self.min_balance_input.setEnabled(checked)

    def on_issue_check_changed(self, state):
        checked = state == 2
        self.issue_input.setEnabled(checked)

    # 数据验证函数
    def validate_data(self):
        error_message = ""

        # 在处理数据之前进行数据验证
        # 例如，检查最大/最小值和余额是否为数字
        if self.value_check.isChecked():
            max_value = self.max_value_input.text()
            min_value = self.min_value_input.text()
            if not (max_value.isdigit() and min_value.isdigit()):
                # 显示错误消息或高亮显示无效数据的字段
                error_message += "请输入有效的最大/最小价值数值。\n"

        if self.balance_check.isChecked():
            max_balance = self.max_balance_input.text()
            min_balance = self.min_balance_input.text()
            if not (max_balance.isdigit() and min_balance.isdigit()):
                # 显示错误消息或高亮显示无效数据的字段
                error_message += "请输入有效的最大/最小余额数值。\n"

        # 如果有错误消息，则显示提示框
        if error_message:
            self.show_error_message(error_message)
            return False
        else:
            return True

    def show_error_message(self, message):
        # 显示错误消息框
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("错误")
        msg.setInformativeText(message)
        msg.setWindowTitle("错误提示")
        msg.exec_()

    def on_button_click(self):
        if not self.validate_data():
            return  # 如果数据验证失败，则停止处理数据

        data = {
            'consider_value': self.value_check.isChecked(),
            'max_value': self.max_value_input.text(),
            'min_value': self.min_value_input.text(),
            'consider_balance': self.balance_check.isChecked(),
            'max_balance': self.max_balance_input.text(),
            'min_balance': self.min_balance_input.text(),
            'consider_issue': self.issue_check.isChecked(),
            'issue': self.issue_input.text()
        }
        self.data_ready.emit(data)  # 发送数据到槽函数
        self.close()  # 关闭窗口

    def start(self):
        app = QApplication(sys.argv)
        self.show()
        sys.exit(app.exec_())
