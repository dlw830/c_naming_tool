"""
主窗口
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QStackedWidget, QStatusBar, QLabel, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .variable_panel import VariablePanel
from .array_panel import ArrayPanel
from .struct_panel import StructPanel
from .translator_panel import TranslatorPanel
from .union_panel import UnionPanel
from .enum_panel import EnumPanel
from .parser_panel import ParserPanel
from .template_panel import TemplatePanel
from .settings_panel import SettingsPanel
from .pointer_panel import PointerPanel
from .function_panel import FunctionPanel


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🔧 C Variable Naming Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 侧边栏
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(200)
        self.sidebar.setMinimumWidth(200)
        
        # 添加侧边栏项目
        sidebar_items = [
            "📝 变量定义",
            "📊 数组定义",
            "🏗️ 结构体",
            "🔀 联合体",
            "📋 枚举",
            "👉 指针定义",
            "⚡ 函数定义",
            "🔍 变量解析",
            "🌐 翻译工具",
            "",  # 分隔符
            "📚 模板库",
            "⚙️ 设置"
        ]
        
        for item_text in sidebar_items:
            if item_text:
                self.sidebar.addItem(item_text)
        
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.on_sidebar_changed)
        
        splitter.addWidget(self.sidebar)
        
        # 内容区域
        self.content_stack = QStackedWidget()
        
        # 添加各个面板
        self.variable_panel = VariablePanel()
        self.content_stack.addWidget(self.variable_panel)
        
        self.array_panel = ArrayPanel()
        self.content_stack.addWidget(self.array_panel)
        
        self.struct_panel = StructPanel()
        self.content_stack.addWidget(self.struct_panel)
        
        self.union_panel = UnionPanel()
        self.content_stack.addWidget(self.union_panel)
        
        self.enum_panel = EnumPanel()
        self.content_stack.addWidget(self.enum_panel)
        
        self.pointer_panel = PointerPanel()
        self.content_stack.addWidget(self.pointer_panel)
        
        self.function_panel = FunctionPanel()
        self.content_stack.addWidget(self.function_panel)
        
        self.parser_panel = ParserPanel()
        self.content_stack.addWidget(self.parser_panel)
        
        self.translator_panel = TranslatorPanel()
        self.content_stack.addWidget(self.translator_panel)
        
        self.template_panel = TemplatePanel()
        self.content_stack.addWidget(self.template_panel)
        
        self.settings_panel = SettingsPanel()
        self.content_stack.addWidget(self.settings_panel)
        
        splitter.addWidget(self.content_stack)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        status_label = QLabel("🔔 就绪")
        self.status_bar.addWidget(status_label)
        
        self.status_bar.addPermanentWidget(QLabel("v1.0.0"))
        
        from datetime import datetime
        date_label = QLabel(datetime.now().strftime("%Y-%m-%d"))
        self.status_bar.addPermanentWidget(date_label)
    
    def on_sidebar_changed(self, index):
        """侧边栏选项改变"""
        # 直接使用index，因为侧边栏添加时已过滤空项
        if index >= 0 and index < self.content_stack.count():
            self.content_stack.setCurrentIndex(index)
    
    def apply_styles(self):
        """应用样式"""
        import os
        style_path = os.path.join(
            os.path.dirname(__file__),
            'styles',
            'macos_light.qss'
        )
        
        try:
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"加载样式失败: {e}")
