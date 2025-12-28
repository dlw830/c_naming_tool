"""
翻译工具面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QScrollArea, QHeaderView
)
from PyQt6.QtCore import Qt
from core.translator import translator


class TranslatorPanel(QWidget):
    """翻译工具面板"""
    
    def __init__(self):
        super().__init__()
        self.translation_history = []
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # 滚动区域的内容部件
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🌐 中英翻译助手")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # 翻译区域
        translate_group = QGroupBox()
        translate_layout = QHBoxLayout(translate_group)
        
        # 中文输入区
        chinese_layout = QVBoxLayout()
        chinese_label = QLabel("🇨🇳 中文输入")
        chinese_label.setProperty("class", "subtitle")
        chinese_layout.addWidget(chinese_label)
        
        self.chinese_input = QLineEdit()
        self.chinese_input.setPlaceholderText("输入中文...")
        self.chinese_input.setMinimumHeight(40)
        self.chinese_input.returnPressed.connect(self.translate_text)
        chinese_layout.addWidget(self.chinese_input)
        
        translate_layout.addLayout(chinese_layout)
        
        # 翻译按钮
        translate_btn = QPushButton("→\n翻译")
        translate_btn.setMinimumSize(80, 80)
        translate_btn.clicked.connect(self.translate_text)
        translate_layout.addWidget(translate_btn)
        
        # 英文输出区
        english_layout = QVBoxLayout()
        english_label = QLabel("🇬🇧 英文输出")
        english_label.setProperty("class", "subtitle")
        english_layout.addWidget(english_label)
        
        self.english_output = QLineEdit()
        self.english_output.setPlaceholderText("翻译结果...")
        self.english_output.setMinimumHeight(40)
        self.english_output.setReadOnly(True)
        english_layout.addWidget(self.english_output)
        
        translate_layout.addLayout(english_layout)
        
        layout.addWidget(translate_group)
        
        # 翻译建议
        suggestions_group = QGroupBox("✨ 其他建议")
        suggestions_layout = QVBoxLayout(suggestions_group)
        
        self.suggestions_label = QLabel("翻译后会显示其他建议")
        self.suggestions_label.setWordWrap(True)
        self.suggestions_label.setProperty("class", "hint")
        suggestions_layout.addWidget(self.suggestions_label)
        
        layout.addWidget(suggestions_group)
        
        # 翻译历史
        history_group = QGroupBox("📚 翻译历史")
        history_layout = QVBoxLayout(history_group)
        
        # 历史记录操作按钮
        history_btn_layout = QHBoxLayout()
        clear_history_btn = QPushButton("🗑️ 清空历史")
        clear_history_btn.clicked.connect(self.clear_history)
        history_btn_layout.addWidget(clear_history_btn)
        history_btn_layout.addStretch()
        history_layout.addLayout(history_btn_layout)
        
        # 历史记录表格
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["中文", "英文"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setMinimumHeight(200)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.itemDoubleClicked.connect(self.on_history_item_double_clicked)
        history_layout.addWidget(self.history_table)
        
        layout.addWidget(history_group)
        
        # 专业术语库
        terms_group = QGroupBox("🔤 专业术语库")
        terms_layout = QVBoxLayout(terms_group)
        
        # 类别选择
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("类别:"))
        self.category_combo = QPushButton("全部")
        self.category_combo.setMaximumWidth(150)
        category_layout.addWidget(self.category_combo)
        category_layout.addStretch()
        terms_layout.addLayout(category_layout)
        
        # 术语表格
        self.terms_table = QTableWidget()
        self.terms_table.setColumnCount(3)
        self.terms_table.setHorizontalHeaderLabels(["中文", "英文", "分类"])
        self.terms_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.terms_table.setMinimumHeight(300)
        self.terms_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        terms_layout.addWidget(self.terms_table)
        
        layout.addWidget(terms_group)
        
        layout.addStretch()
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # 加载术语库
        self.load_terms()
    
    def translate_text(self):
        """翻译文本"""
        chinese = self.chinese_input.text().strip()
        if not chinese:
            return
        
        result = translator.translate(chinese)
        
        # 显示主要翻译
        self.english_output.setText(result['primary'])
        
        # 显示其他建议
        if result.get('alternatives'):
            suggestions_text = "其他建议:\n"
            for i, alt in enumerate(result['alternatives'][:5], 1):
                suggestions_text += f"  {i}. {alt}\n"
            self.suggestions_label.setText(suggestions_text)
        else:
            self.suggestions_label.setText("暂无其他建议")
        
        # 添加到历史记录
        self.add_to_history(chinese, result['primary'])
    
    def add_to_history(self, chinese, english):
        """添加到历史记录"""
        # 避免重复
        for item in self.translation_history:
            if item[0] == chinese and item[1] == english:
                return
        
        self.translation_history.insert(0, (chinese, english))
        
        # 限制历史记录数量
        if len(self.translation_history) > 50:
            self.translation_history = self.translation_history[:50]
        
        # 更新表格
        self.update_history_table()
    
    def update_history_table(self):
        """更新历史记录表格"""
        self.history_table.setRowCount(len(self.translation_history))
        
        for i, (chinese, english) in enumerate(self.translation_history):
            self.history_table.setItem(i, 0, QTableWidgetItem(chinese))
            self.history_table.setItem(i, 1, QTableWidgetItem(english))
    
    def on_history_item_double_clicked(self, item):
        """双击历史记录项"""
        row = item.row()
        chinese = self.history_table.item(row, 0).text()
        english = self.history_table.item(row, 1).text()
        
        self.chinese_input.setText(chinese)
        self.english_output.setText(english)
    
    def clear_history(self):
        """清空历史记录"""
        self.translation_history.clear()
        self.history_table.setRowCount(0)
    
    def load_terms(self):
        """加载术语库"""
        categories = translator.get_all_categories()
        
        terms_list = []
        for category in categories:
            terms = translator.get_terms_by_category(category)
            for chinese, info in terms.items():
                english = info.get('primary', '')
                terms_list.append((chinese, english, category))
        
        # 更新表格
        self.terms_table.setRowCount(len(terms_list))
        
        for i, (chinese, english, category) in enumerate(terms_list):
            self.terms_table.setItem(i, 0, QTableWidgetItem(chinese))
            self.terms_table.setItem(i, 1, QTableWidgetItem(english))
            self.terms_table.setItem(i, 2, QTableWidgetItem(category))
