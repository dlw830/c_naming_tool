"""
变量定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QGroupBox, QMessageBox,
    QScrollArea, QListWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from core.naming import naming_generator
from core.type_info import type_info_manager
from core.translator import translator
from utils.code_generator import code_generator


class VariablePanel(QWidget):
    """变量定义面板"""
    
    code_generated = pyqtSignal(str)  # 代码生成信号
    
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
        title = QLabel("📝 基础变量定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # 输入区域
        input_group = QGroupBox("变量配置")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(16)
        
        # 1. 修饰类型
        modifier_layout = QHBoxLayout()
        modifier_layout.addWidget(QLabel("① 修饰类型:"))
        self.modifier_combo = QComboBox()
        self.modifier_combo.addItems(["全局变量", "静态变量", "局部变量", "常量", "volatile"])
        self.modifier_combo.setMinimumWidth(200)
        modifier_layout.addWidget(self.modifier_combo)
        modifier_layout.addStretch()
        input_layout.addLayout(modifier_layout)
        
        # 2. 变量类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("② 变量类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(type_info_manager.get_all_types())
        self.type_combo.setMinimumWidth(200)
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        input_layout.addLayout(type_layout)
        
        # 3. 功能模块
        module_layout = QVBoxLayout()
        module_input_layout = QHBoxLayout()
        module_input_layout.addWidget(QLabel("③ 功能模块:"))
        self.module_input = QLineEdit()
        self.module_input.setPlaceholderText("例如：温度传感器 或 temperature_sensor")
        self.module_input.setMinimumWidth(300)
        self.module_input.textChanged.connect(self.on_input_changed)
        module_input_layout.addWidget(self.module_input)
        
        self.module_translate_btn = QPushButton("🌐 翻译")
        self.module_translate_btn.setMaximumWidth(80)
        self.module_translate_btn.clicked.connect(self.translate_module)
        module_input_layout.addWidget(self.module_translate_btn)
        module_input_layout.addStretch()
        module_layout.addLayout(module_input_layout)
        
        # 翻译建议
        self.module_suggestions = QLabel()
        self.module_suggestions.setWordWrap(True)
        self.module_suggestions.setProperty("class", "hint")
        self.module_suggestions.hide()
        module_layout.addWidget(self.module_suggestions)
        input_layout.addLayout(module_layout)
        
        # 4. 使用目的
        purpose_layout = QVBoxLayout()
        purpose_input_layout = QHBoxLayout()
        purpose_input_layout.addWidget(QLabel("④ 使用目的:"))
        self.purpose_input = QLineEdit()
        self.purpose_input.setPlaceholderText("例如：数据采集 或 data_sample")
        self.purpose_input.setMinimumWidth(300)
        self.purpose_input.textChanged.connect(self.on_input_changed)
        purpose_input_layout.addWidget(self.purpose_input)
        
        self.purpose_translate_btn = QPushButton("🌐 翻译")
        self.purpose_translate_btn.setMaximumWidth(80)
        self.purpose_translate_btn.clicked.connect(self.translate_purpose)
        purpose_input_layout.addWidget(self.purpose_translate_btn)
        purpose_input_layout.addStretch()
        purpose_layout.addLayout(purpose_input_layout)
        
        # 翻译建议
        self.purpose_suggestions = QLabel()
        self.purpose_suggestions.setWordWrap(True)
        self.purpose_suggestions.setProperty("class", "hint")
        self.purpose_suggestions.hide()
        purpose_layout.addWidget(self.purpose_suggestions)
        input_layout.addLayout(purpose_layout)
        
        # 5. 初始值
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("⑤ 初始值:"))
        self.value_input = QLineEdit()
        self.value_input.setText("0")
        self.value_input.setMinimumWidth(200)
        value_layout.addWidget(self.value_input)
        value_layout.addStretch()
        input_layout.addLayout(value_layout)
        
        layout.addWidget(input_group)
        
        # 取值范围显示区域
        self.range_group = QGroupBox("📊 取值范围")
        self.range_layout = QVBoxLayout(self.range_group)
        self.range_display = QLabel()
        self.range_display.setWordWrap(True)
        self.range_layout.addWidget(self.range_display)
        layout.addWidget(self.range_group)
        
        # 预览区域
        preview_group = QGroupBox("🎯 生成的变量名")
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
    
    def on_type_changed(self, type_name):
        """类型改变时更新取值范围显示"""
        display_info = type_info_manager.format_type_display(type_name)
        
        range_text = f"""
<p><b>类型:</b> {display_info['type']} - {display_info['description']}</p>
<p><b>字节数:</b> {display_info['bytes']} bytes</p>
<p><b>取值范围:</b> {display_info['range']}</p>
"""
        
        # 如果是浮点类型，显示额外信息
        if type_info_manager.is_float_type(type_name):
            range_text += f"""
<p><b>精度:</b> {display_info.get('precision', 0)}位有效数字</p>
<p><b>小数位数:</b> {display_info.get('decimal_places', '')}</p>
<p><b>最小正数:</b> {display_info.get('min_positive', '')}</p>
"""
            
            if display_info.get('notes'):
                range_text += "<p><b>⚠️ 注意事项:</b></p><ul>"
                for note in display_info['notes']:
                    range_text += f"<li>{note}</li>"
                range_text += "</ul>"
        
        self.range_display.setText(range_text)
        self.on_input_changed()
    
    def on_input_changed(self):
        """输入改变时更新预览"""
        modifier = self.modifier_combo.currentText()
        var_type = self.type_combo.currentText()
        module = self.module_input.text().strip()
        purpose = self.purpose_input.text().strip()
        
        if not module and not purpose:
            self.preview_label.setText("请输入功能模块和使用目的")
            self.breakdown_label.setText("")
            return
        
        # 生成变量名
        result = naming_generator.generate_variable_name(
            modifier, var_type, module, purpose
        )
        
        self.preview_label.setText(result['name'])
        
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
        
        # 显示其他翻译建议
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
        
        # 显示其他翻译建议
        if result.get('alternatives'):
            suggestions_text = "✨ 其他建议: " + ", ".join(result['alternatives'][:3])
            self.purpose_suggestions.setText(suggestions_text)
            self.purpose_suggestions.show()
        else:
            self.purpose_suggestions.hide()
    
    def generate_code(self):
        """生成代码"""
        modifier = self.modifier_combo.currentText()
        var_type = self.type_combo.currentText()
        module = self.module_input.text().strip()
        purpose = self.purpose_input.text().strip()
        initial_value = self.value_input.text().strip()
        
        if not module and not purpose:
            QMessageBox.warning(self, "提示", "请至少输入功能模块或使用目的")
            return
        
        # 生成变量名
        result = naming_generator.generate_variable_name(
            modifier, var_type, module, purpose
        )
        
        # 生成代码
        code = code_generator.generate_variable_code(
            result['name'], var_type, modifier, module, purpose, initial_value
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
        self.module_input.clear()
        self.purpose_input.clear()
        self.value_input.setText("0")
        self.code_display.clear()
        self.preview_label.setText("")
        self.breakdown_label.setText("")
