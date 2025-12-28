"""
C语言变量定义和命名工具
主程序入口
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("C Variable Naming Tool")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Embedded Tools")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
