"""
指针定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QGroupBox, QTextEdit, QCheckBox,
    QMessageBox, QScrollArea, QSpinBox
)
from PyQt6.QtCore import Qt
from core.type_info import type_info_manager
from core.translator import translator
from core.naming import naming_generator
from utils.code_generator import code_generator


class PointerPanel(QWidget):
    """指针定义面板"""
    
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
        title = QLabel("👉 指针定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        hint = QLabel("定义C语言指针变量，支持多级指针、函数指针、数组指针等")
        hint.setProperty("class", "hint")
        layout.addWidget(hint)
        
        # 基本信息组
        basic_group = QGroupBox("📋 基本信息")
        basic_layout = QVBoxLayout(basic_group)
        
        # 指针类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("指针类型:"))
        self.pointer_type_combo = QComboBox()
        self.pointer_type_combo.addItems([
            "普通指针",
            "函数指针",
            "数组指针",
            "结构体指针",
            "void指针"
        ])
        self.pointer_type_combo.currentTextChanged.connect(self.on_pointer_type_changed)
        type_layout.addWidget(self.pointer_type_combo)
        type_layout.addStretch()
        basic_layout.addLayout(type_layout)
        
        # 基础类型
        base_type_layout = QHBoxLayout()
        base_type_layout.addWidget(QLabel("基础类型:"))
        self.base_type_combo = QComboBox()
        self.base_type_combo.addItems([
            'uint8_t', 'int8_t', 'uint16_t', 'int16_t',
            'uint32_t', 'int32_t', 'uint64_t', 'int64_t',
            'float', 'double', 'char', 'void'
        ])
        self.base_type_combo.currentTextChanged.connect(self.update_preview)
        base_type_layout.addWidget(self.base_type_combo)
        base_type_layout.addStretch()
        basic_layout.addLayout(base_type_layout)
        
        # 指针级别
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("指针级别:"))
        self.pointer_level_spin = QSpinBox()
        self.pointer_level_spin.setRange(1, 3)
        self.pointer_level_spin.setValue(1)
        self.pointer_level_spin.setSuffix(" 级")
        self.pointer_level_spin.valueChanged.connect(self.update_preview)
        level_layout.addWidget(self.pointer_level_spin)
        self.level_hint = QLabel("(* 一级指针)")
        level_layout.addWidget(self.level_hint)
        level_layout.addStretch()
        basic_layout.addLayout(level_layout)
        
        layout.addWidget(basic_group)
        
        # 函数指针配置（默认隐藏）
        self.func_ptr_group = QGroupBox("🔧 函数指针配置")
        func_ptr_layout = QVBoxLayout(self.func_ptr_group)
        
        # 返回类型
        ret_type_layout = QHBoxLayout()
        ret_type_layout.addWidget(QLabel("返回类型:"))
        self.return_type_combo = QComboBox()
        self.return_type_combo.addItems([
            'void', 'uint8_t', 'int8_t', 'uint16_t', 'int16_t',
            'uint32_t', 'int32_t', 'float', 'double'
        ])
        self.return_type_combo.currentTextChanged.connect(self.update_preview)
        ret_type_layout.addWidget(self.return_type_combo)
        ret_type_layout.addStretch()
        func_ptr_layout.addLayout(ret_type_layout)
        
        # 参数列表
        params_layout = QVBoxLayout()
        params_layout.addWidget(QLabel("参数列表:"))
        self.params_edit = QLineEdit()
        self.params_edit.setPlaceholderText("例如: uint8_t param1, uint16_t param2")
        self.params_edit.textChanged.connect(self.update_preview)
        params_layout.addWidget(self.params_edit)
        func_ptr_layout.addLayout(params_layout)
        
        self.func_ptr_group.setVisible(False)
        layout.addWidget(self.func_ptr_group)
        
        # 数组指针配置（默认隐藏）
        self.array_ptr_group = QGroupBox("📊 数组指针配置")
        array_ptr_layout = QVBoxLayout(self.array_ptr_group)
        
        # 数组大小
        array_size_layout = QHBoxLayout()
        array_size_layout.addWidget(QLabel("数组大小:"))
        self.array_size_spin = QSpinBox()
        self.array_size_spin.setRange(1, 65535)
        self.array_size_spin.setValue(10)
        self.array_size_spin.valueChanged.connect(self.update_preview)
        array_size_layout.addWidget(self.array_size_spin)
        array_size_layout.addStretch()
        array_ptr_layout.addLayout(array_size_layout)
        
        self.array_ptr_group.setVisible(False)
        layout.addWidget(self.array_ptr_group)
        
        # 命名信息组
        naming_group = QGroupBox("✏️ 命名信息")
        naming_layout = QVBoxLayout(naming_group)
        
        # 中文名称
        name_layout = QVBoxLayout()
        name_layout.addWidget(QLabel("中文名称:"))
        
        name_input_layout = QHBoxLayout()
        self.chinese_name_edit = QLineEdit()
        self.chinese_name_edit.setPlaceholderText("输入中文描述，例如：缓冲区指针")
        self.chinese_name_edit.textChanged.connect(self.on_chinese_name_changed)
        name_input_layout.addWidget(self.chinese_name_edit)
        
        translate_btn = QPushButton("🌐 翻译")
        translate_btn.clicked.connect(self.translate_name)
        name_input_layout.addWidget(translate_btn)
        
        name_layout.addLayout(name_input_layout)
        naming_layout.addLayout(name_layout)
        
        # 翻译建议
        self.suggestion_label = QLabel("")
        self.suggestion_label.setProperty("class", "hint")
        self.suggestion_label.setWordWrap(True)
        naming_layout.addWidget(self.suggestion_label)
        
        # 英文名称
        en_name_layout = QVBoxLayout()
        en_name_layout.addWidget(QLabel("英文名称:"))
        self.english_name_edit = QLineEdit()
        self.english_name_edit.setPlaceholderText("翻译后的英文名称")
        self.english_name_edit.textChanged.connect(self.update_preview)
        en_name_layout.addWidget(self.english_name_edit)
        naming_layout.addLayout(en_name_layout)
        
        # 作用域
        scope_layout = QHBoxLayout()
        scope_layout.addWidget(QLabel("作用域:"))
        self.scope_combo = QComboBox()
        self.scope_combo.addItems(['全局 (g_)', '静态 (s_)', '局部 (l_)'])
        self.scope_combo.currentTextChanged.connect(self.update_preview)
        scope_layout.addWidget(self.scope_combo)
        scope_layout.addStretch()
        naming_layout.addLayout(scope_layout)
        
        # 修饰符
        modifier_layout = QHBoxLayout()
        self.const_check = QCheckBox("const (常量指针)")
        self.const_check.stateChanged.connect(self.update_preview)
        modifier_layout.addWidget(self.const_check)
        
        self.volatile_check = QCheckBox("volatile (易变)")
        self.volatile_check.stateChanged.connect(self.update_preview)
        modifier_layout.addWidget(self.volatile_check)
        
        modifier_layout.addStretch()
        naming_layout.addLayout(modifier_layout)
        
        layout.addWidget(naming_group)
        
        # 预览和生成
        preview_group = QGroupBox("👁️ 代码预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_display = QTextEdit()
        self.preview_display.setReadOnly(True)
        self.preview_display.setMinimumHeight(200)
        preview_layout.addWidget(self.preview_display)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        generate_btn = QPushButton("⚡ 生成代码")
        generate_btn.setMinimumHeight(40)
        generate_btn.clicked.connect(self.generate_code)
        btn_layout.addWidget(generate_btn)
        
        copy_btn = QPushButton("📋 复制")
        copy_btn.clicked.connect(self.copy_code)
        btn_layout.addWidget(copy_btn)
        
        preview_layout.addLayout(btn_layout)
        
        layout.addWidget(preview_group)
        
        layout.addStretch()
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def on_pointer_type_changed(self, ptr_type):
        """指针类型改变"""
        self.func_ptr_group.setVisible(ptr_type == "函数指针")
        self.array_ptr_group.setVisible(ptr_type == "数组指针")
        
        if ptr_type == "void指针":
            self.base_type_combo.setCurrentText("void")
        elif ptr_type == "结构体指针":
            self.base_type_combo.setCurrentText("uint8_t")
        
        self.update_preview()
    
    def on_chinese_name_changed(self):
        """中文名称改变"""
        chinese_text = self.chinese_name_edit.text().strip()
        if chinese_text:
            suggestions = translator.get_translation_suggestions(chinese_text, 3)
            if suggestions:
                suggestion_text = "建议: " + ", ".join([s['text'] for s in suggestions[:3]])
                self.suggestion_label.setText(suggestion_text)
            else:
                self.suggestion_label.setText("")
    
    def translate_name(self):
        """翻译名称"""
        chinese_text = self.chinese_name_edit.text().strip()
        if not chinese_text:
            QMessageBox.warning(self, "提示", "请先输入中文名称")
            return
        
        result = translator.translate(chinese_text)
        self.english_name_edit.setText(result['primary'])
        self.update_preview()
    
    def update_preview(self):
        """更新预览"""
        level = self.pointer_level_spin.value()
        stars = '*' * level
        self.level_hint.setText(f"({stars} {level}级指针)")
        
        english_name = self.english_name_edit.text().strip()
        if not english_name:
            self.preview_display.clear()
            return
        
        # 生成变量名
        scope = self.scope_combo.currentText()
        scope_prefix = scope.split('(')[1].strip(')')
        
        ptr_type = self.pointer_type_combo.currentText()
        
        if ptr_type == "函数指针":
            var_name = f"{scope_prefix}p_func_{english_name}"
        else:
            var_name = f"{scope_prefix}p_{english_name}"
        
        # 构建声明
        base_type = self.base_type_combo.currentText()
        
        modifiers = []
        if self.const_check.isChecked():
            modifiers.append("const")
        if self.volatile_check.isChecked():
            modifiers.append("volatile")
        
        modifier_str = " ".join(modifiers) + " " if modifiers else ""
        
        if ptr_type == "函数指针":
            ret_type = self.return_type_combo.currentText()
            params = self.params_edit.text().strip() or "void"
            declaration = f"{ret_type} (*{var_name})({params});"
        elif ptr_type == "数组指针":
            array_size = self.array_size_spin.value()
            declaration = f"{modifier_str}{base_type} (*{var_name})[{array_size}];"
        else:
            declaration = f"{modifier_str}{base_type} {stars}{var_name};"
        
        # 生成注释
        chinese_name = self.chinese_name_edit.text().strip() or english_name
        
        code = f"""/*
 * {chinese_name}
 * 类型: {ptr_type}
 * 基础类型: {base_type}
 * 指针级别: {level}级
"""
        
        if modifiers:
            code += f" * 修饰符: {', '.join(modifiers)}\n"
        
        if ptr_type == "函数指针":
            code += f" * 返回类型: {ret_type}\n"
            code += f" * 参数: {params}\n"
        elif ptr_type == "数组指针":
            code += f" * 数组大小: {array_size}\n"
        
        code += f" * 命名解析:\n"
        code += f" *   {scope_prefix.rstrip('_')}: {scope.split('(')[0].strip()}\n"
        code += f" *   p: 指针 (Pointer)\n"
        code += f" *   {english_name}: {chinese_name}\n"
        code += f" */\n"
        code += declaration
        
        self.preview_display.setPlainText(code)
    
    def generate_code(self):
        """生成代码"""
        if not self.english_name_edit.text().strip():
            QMessageBox.warning(self, "提示", "请先输入英文名称")
            return
        
        self.update_preview()
        QMessageBox.information(self, "成功", "代码已生成到预览区域")
    
    def copy_code(self):
        """复制代码"""
        code = self.preview_display.toPlainText()
        if code:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(code)
            QMessageBox.information(self, "成功", "代码已复制到剪贴板")
        else:
            QMessageBox.warning(self, "提示", "没有可复制的代码")
