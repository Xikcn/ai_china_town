import sys
import os

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QMessageBox
from PySide6.QtGui import QFont

class FileBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件浏览器')
        self.setGeometry(100, 100, 1200, 800)

        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout()

        # 创建输入框
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText('请输入文件路径')
        layout.addWidget(self.path_input)

        # 创建按钮
        self.browse_button = QPushButton('打开文件', self)
        self.browse_button.clicked.connect(self.open_file)
        layout.addWidget(self.browse_button)

        # 创建文本编辑器
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Arial", 14))  # 设置字体大小为14
        layout.addWidget(self.text_edit)

        # 设置布局
        central_widget.setLayout(layout)

    @Slot()
    def open_file(self):
        file_path = self.path_input.text().strip()
        file_path = "D:/Python_workspace/rag_qwen/test/" + file_path
        if not file_path:
            QMessageBox.warning(self, "警告", "请输入有效的文件路径")
            return

        if not os.path.isfile(file_path):
            QMessageBox.warning(self, "警告", "输入的路径不是一个有效的文件")
            return

        self.read_and_display_file(file_path)
        self.path_input.clear()  # 清除输入框中的文件路径

    def read_and_display_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.clear()  # 清除之前的文本
                self.text_edit.append(f"{content}")
        except Exception as e:
            self.text_edit.clear()
            self.text_edit.append(f"无法读取文件 {file_path}: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileBrowserApp()
    window.show()
    sys.exit(app.exec())