"""
数组定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QGroupBox, QMessageBox,
    QScrollArea, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from core.naming import naming_generator
from core.type_info import type_info_manager
from core.translator import translator
from utils.code_generator import code_generator


class ArrayPanel(QWidget):
    """数组定义面板"""
    
    code_generated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
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
        title = QLabel("📊 数组定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # 输入区域
        input_group = QGroupBox("数组配置")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(16)
        
        # 1. 修饰类型
        modifier_layout = QHBoxLayout()
        modifier_layout.addWidget(QLabel("① 修饰类型:"))
        self.modifier_combo = QComboBox()
        self.modifier_combo.addItems(["全局数组", "静态数组", "局部数组", "常量数组"])
        self.modifier_combo.setMinimumWidth(200)
        modifier_layout.addWidget(self.modifier_combo)
        modifier_layout.addStretch()
        input_layout.addLayout(modifier_layout)
        
        # 2. 元素类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("② 元素类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(type_info_manager.get_all_types())
        self.type_combo.setMinimumWidth(200)
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        input_layout.addLayout(type_layout)
        
        # 3. 数组大小
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("③ 数组大小:"))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setMinimum(1)
        self.size_spinbox.setMaximum(65535)
        self.size_spinbox.setValue(64)
        self.size_spinbox.setMinimumWidth(200)
        self.size_spinbox.valueChanged.connect(self.on_size_changed)
        size_layout.addWidget(self.size_spinbox)
        size_layout.addStretch()
        input_layout.addLayout(size_layout)
        
        # 4. 功能模块
        module_layout = QVBoxLayout()
        module_input_layout = QHBoxLayout()
        module_input_layout.addWidget(QLabel("④ 功能模块:"))
        self.module_input = QLineEdit()
        self.module_input.setPlaceholderText("例如：缓冲区 或 buffer")
        self.module_input.setMinimumWidth(300)
        self.module_input.textChanged.connect(self.on_input_changed)
        module_input_layout.addWidget(self.module_input)
        
        self.module_translate_btn = QPushButton("🌐 翻译")
        self.module_translate_btn.setMaximumWidth(80)
        self.module_translate_btn.clicked.connect(self.translate_module)
        module_input_layout.addWidget(self.module_translate_btn)
        module_input_layout.addStretch()
        module_layout.addLayout(module_input_layout)
        
        self.module_suggestions = QLabel()
        self.module_suggestions.setWordWrap(True)
        self.module_suggestions.setProperty("class", "hint")
        self.module_suggestions.hide()
        module_layout.addWidget(self.module_suggestions)
        input_layout.addLayout(module_layout)
        
        # 5. 使用目的
        purpose_layout = QVBoxLayout()
        purpose_input_layout = QHBoxLayout()
        purpose_input_layout.addWidget(QLabel("⑤ 使用目的:"))
        self.purpose_input = QLineEdit()
        self.purpose_input.setPlaceholderText("例如：数据存储 或 data_storage")
        self.purpose_input.setMinimumWidth(300)
        self.purpose_input.textChanged.connect(self.on_input_changed)
        purpose_input_layout.addWidget(self.purpose_input)
        
        self.purpose_translate_btn = QPushButton("🌐 翻译")
        self.purpose_translate_btn.setMaximumWidth(80)
        self.purpose_translate_btn.clicked.connect(self.translate_purpose)
        purpose_input_layout.addWidget(self.purpose_translate_btn)
        purpose_input_layout.addStretch()
        purpose_layout.addLayout(purpose_input_layout)
        
        self.purpose_suggestions = QLabel()
        self.purpose_suggestions.setWordWrap(True)
        self.purpose_suggestions.setProperty("class", "hint")
        self.purpose_suggestions.hide()
        purpose_layout.addWidget(self.purpose_suggestions)
        input_layout.addLayout(purpose_layout)
        
        layout.addWidget(input_group)
        
        # 数组信息显示区域
        self.array_info_group = QGroupBox("📊 数组信息")
        self.array_info_layout = QVBoxLayout(self.array_info_group)
        self.array_info_display = QLabel()
        self.array_info_display.setWordWrap(True)
        self.array_info_layout.addWidget(self.array_info_display)
        layout.addWidget(self.array_info_group)
        
        # 预览区域
        preview_group = QGroupBox("🎯 生成的数组名")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #007AFF;")
        preview_layout.addWidget(self.preview_label)
        
        self.breakdown_label = QLabel()
        self.breakdown_label.setWordWrap(True)
        preview_layout.addWidget(self.breakdown_label)
        layout.addWidget(preview_group)
        
        # 代码显示区域
        code_group = QGroupBox("📋 生成的代码")
        code_layout = QVBoxLayout(code_group)
        self.code_display = QTextEdit()
        self.code_display.setProperty("class", "code")
        self.code_display.setReadOnly(True)
        self.code_display.setMinimumHeight(200)
        code_layout.addWidget(self.code_display)
        layout.addWidget(code_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("📋 生成代码")
        self.generate_btn.clicked.connect(self.generate_code)
        button_layout.addWidget(self.generate_btn)
        
        self.copy_btn = QPushButton("📄 复制代码")
        self.copy_btn.clicked.connect(self.copy_code)
        button_layout.addWidget(self.copy_btn)
        
        self.reset_btn = QPushButton("🔄 重置")
        self.reset_btn.setProperty("class", "secondary")
        self.reset_btn.clicked.connect(self.reset_fields)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # 初始化显示
        self.on_type_changed(self.type_combo.currentText())
        self.on_size_changed(self.size_spinbox.value())
    
    def on_type_changed(self, type_name):
        """类型改变时更新显示"""
        self.update_array_info()
    
    def on_size_changed(self, size):
        """数组大小改变时更新显示"""
        self.update_array_info()
        self.on_input_changed()
    
    def update_array_info(self):
        """更新数组信息显示"""
        element_type = self.type_combo.currentText()
        array_size = self.size_spinbox.value()
        
        display_info = type_info_manager.format_type_display(element_type)
        total_bytes, memory_str = type_info_manager.get_memory_size(element_type, array_size)
        
        info_text = f"""
<p><b>元素类型:</b> {element_type} - {display_info['description']}</p>
<p><b>元素范围:</b> {display_info['range']}</p>
<p><b>数组大小:</b> {array_size}</p>
<p><b>总内存:</b> {memory_str}</p>
<p><b>总元素数:</b> {array_size}</p>
"""
        
        # 添加建议
        if array_size >= 1024:
            info_text += """
<p style="color: #FF9500;"><b>💡 建议:</b> 数组较大，考虑使用动态内存分配</p>
"""
        else:
            info_text += """
<p><b>💡 建议:</b> 考虑使用宏定义数组大小便于维护</p>
"""
        
        self.array_info_display.setText(info_text)
    
    def on_input_changed(self):
        """输入改变时更新预览"""
        modifier = self.modifier_combo.currentText()
        element_type = self.type_combo.currentText()
        module = self.module_input.text().strip()
        purpose = self.purpose_input.text().strip()
        array_size = self.size_spinbox.value()
        
        if not module and not purpose:
            self.preview_label.setText("请输入功能模块和使用目的")
            self.breakdown_label.setText("")
            return
        
        # 生成数组名
        result = naming_generator.generate_array_name(
            modifier, element_type, module, purpose, array_size
        )
        
        self.preview_label.setText(f"{result['name']}[{array_size}]")
        
        # 显示命名解析
        breakdown_text = "<p><b>命名解析:</b></p>"
        for part in result['breakdown']:
            breakdown_text += f"<p>• <b>{part['part']}</b>: {part['description']}</p>"
        
        self.breakdown_label.setText(breakdown_text)
    
    def translate_module(self):
        """翻译功能模块"""
        chinese = self.module_input.text().strip()
        if not chinese:
            return
            
        result = translator.translate(chinese)
        self.module_input.setText(result['primary'])
        
        if result.get('alternatives'):
            suggestions_text = "✨ 其他建议: " + ", ".join(result['alternatives'][:3])
            self.module_suggestions.setText(suggestions_text)
            self.module_suggestions.show()
        else:
            self.module_suggestions.hide()
    
    def translate_purpose(self):
        """翻译使用目的"""
        chinese = self.purpose_input.text().strip()
        if not chinese:
            return
            
        result = translator.translate(chinese)
        self.purpose_input.setText(result['primary'])
        
        if result.get('alternatives'):
            suggestions_text = "✨ 其他建议: " + ", ".join(result['alternatives'][:3])
            self.purpose_suggestions.setText(suggestions_text)
            self.purpose_suggestions.show()
        else:
            self.purpose_suggestions.hide()
    
    def generate_code(self):
        """生成代码"""
        modifier = self.modifier_combo.currentText()
        element_type = self.type_combo.currentText()
        module = self.module_input.text().strip()
        purpose = self.purpose_input.text().strip()
        array_size = self.size_spinbox.value()
        
        if not module and not purpose:
            QMessageBox.warning(self, "提示", "请至少输入功能模块或使用目的")
            return
        
        # 生成数组名
        result = naming_generator.generate_array_name(
            modifier, element_type, module, purpose, array_size
        )
        
        # 生成代码
        code = code_generator.generate_array_code(
            result['name'], element_type, array_size, modifier, module, purpose
        )
        
        self.code_display.setPlainText(code)
        self.code_generated.emit(code)
    
    def copy_code(self):
        """复制代码到剪贴板"""
        code = self.code_display.toPlainText()
        if code:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(code)
            QMessageBox.information(self, "成功", "代码已复制到剪贴板")
    
    def reset_fields(self):
        """重置所有字段"""
        self.modifier_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.size_spinbox.setValue(64)
        self.module_input.clear()
        self.purpose_input.clear()
        self.code_display.clear()
        self.preview_label.setText("")
        self.breakdown_label.setText("")
        self.module_suggestions.hide()
        self.purpose_suggestions.hide()
