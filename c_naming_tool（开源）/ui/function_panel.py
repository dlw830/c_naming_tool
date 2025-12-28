"""
函数定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QGroupBox, QTextEdit, QCheckBox,
    QMessageBox, QScrollArea, QListWidget, QListWidgetItem, QDialog
)
from PyQt6.QtCore import Qt
from core.translator import translator


class ParameterDialog(QDialog):
    """参数编辑对话框"""
    
    def __init__(self, parent=None, param_data=None):
        super().__init__(parent)
        self.param_data = param_data or {}
        self.init_ui()
        self.load_param()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("参数编辑")
        self.setMinimumSize(500, 300)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 参数类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("参数类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            'uint8_t', 'int8_t', 'uint16_t', 'int16_t',
            'uint32_t', 'int32_t', 'uint64_t', 'int64_t',
            'float', 'double', 'char', 'void',
            'char*', 'void*', 'const char*'
        ])
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # 中文名称
        cn_name_layout = QVBoxLayout()
        cn_name_layout.addWidget(QLabel("中文名称:"))
        
        cn_input_layout = QHBoxLayout()
        self.chinese_name_edit = QLineEdit()
        self.chinese_name_edit.setPlaceholderText("例如：缓冲区")
        cn_input_layout.addWidget(self.chinese_name_edit)
        
        translate_btn = QPushButton("🌐 翻译")
        translate_btn.clicked.connect(self.translate_param)
        cn_input_layout.addWidget(translate_btn)
        
        cn_name_layout.addLayout(cn_input_layout)
        layout.addLayout(cn_name_layout)
        
        # 英文名称
        en_name_layout = QVBoxLayout()
        en_name_layout.addWidget(QLabel("参数名:"))
        self.english_name_edit = QLineEdit()
        self.english_name_edit.setPlaceholderText("例如：buffer")
        en_name_layout.addWidget(self.english_name_edit)
        layout.addLayout(en_name_layout)
        
        # 修饰符
        modifier_layout = QHBoxLayout()
        self.const_check = QCheckBox("const")
        modifier_layout.addWidget(self.const_check)
        
        self.pointer_check = QCheckBox("指针 (*)")
        modifier_layout.addWidget(self.pointer_check)
        
        modifier_layout.addStretch()
        layout.addLayout(modifier_layout)
        
        # 描述
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("参数说明:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        self.desc_edit.setPlaceholderText("参数的详细说明...")
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("💾 保存")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def translate_param(self):
        """翻译参数名"""
        chinese_text = self.chinese_name_edit.text().strip()
        if chinese_text:
            result = translator.translate(chinese_text)
            self.english_name_edit.setText(result['primary'])
    
    def load_param(self):
        """加载参数数据"""
        if self.param_data:
            self.type_combo.setCurrentText(self.param_data.get('type', 'uint8_t'))
            self.chinese_name_edit.setText(self.param_data.get('chinese_name', ''))
            self.english_name_edit.setText(self.param_data.get('name', ''))
            self.const_check.setChecked(self.param_data.get('const', False))
            self.pointer_check.setChecked(self.param_data.get('pointer', False))
            self.desc_edit.setPlainText(self.param_data.get('description', ''))
    
    def get_param(self):
        """获取参数数据"""
        return {
            'type': self.type_combo.currentText(),
            'chinese_name': self.chinese_name_edit.text().strip(),
            'name': self.english_name_edit.text().strip(),
            'const': self.const_check.isChecked(),
            'pointer': self.pointer_check.isChecked(),
            'description': self.desc_edit.toPlainText().strip()
        }


class FunctionPanel(QWidget):
    """函数定义面板"""
    
    def __init__(self):
        super().__init__()
        self.parameters = []
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
        title = QLabel("🔧 函数定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        hint = QLabel("定义C语言函数，支持参数配置、返回值设置、注释生成等")
        hint.setProperty("class", "hint")
        layout.addWidget(hint)
        
        # 基本信息组
        basic_group = QGroupBox("📋 基本信息")
        basic_layout = QVBoxLayout(basic_group)
        
        # 函数中文名
        cn_name_layout = QVBoxLayout()
        cn_name_layout.addWidget(QLabel("函数中文名:"))
        
        cn_input_layout = QHBoxLayout()
        self.chinese_name_edit = QLineEdit()
        self.chinese_name_edit.setPlaceholderText("例如：初始化串口")
        self.chinese_name_edit.textChanged.connect(self.on_chinese_name_changed)
        cn_input_layout.addWidget(self.chinese_name_edit)
        
        translate_btn = QPushButton("🌐 翻译")
        translate_btn.clicked.connect(self.translate_name)
        cn_input_layout.addWidget(translate_btn)
        
        cn_name_layout.addLayout(cn_input_layout)
        basic_layout.addLayout(cn_name_layout)
        
        # 翻译建议
        self.suggestion_label = QLabel("")
        self.suggestion_label.setProperty("class", "hint")
        self.suggestion_label.setWordWrap(True)
        basic_layout.addWidget(self.suggestion_label)
        
        # 函数英文名
        en_name_layout = QVBoxLayout()
        en_name_layout.addWidget(QLabel("函数英文名:"))
        self.english_name_edit = QLineEdit()
        self.english_name_edit.setPlaceholderText("例如：init_uart")
        self.english_name_edit.textChanged.connect(self.update_preview)
        en_name_layout.addWidget(self.english_name_edit)
        basic_layout.addLayout(en_name_layout)
        
        # 返回类型
        ret_type_layout = QHBoxLayout()
        ret_type_layout.addWidget(QLabel("返回类型:"))
        self.return_type_combo = QComboBox()
        self.return_type_combo.addItems([
            'void', 'uint8_t', 'int8_t', 'uint16_t', 'int16_t',
            'uint32_t', 'int32_t', 'uint64_t', 'int64_t',
            'float', 'double', 'bool', 'char*'
        ])
        self.return_type_combo.currentTextChanged.connect(self.update_preview)
        ret_type_layout.addWidget(self.return_type_combo)
        ret_type_layout.addStretch()
        basic_layout.addLayout(ret_type_layout)
        
        # 函数属性
        attr_layout = QHBoxLayout()
        self.static_check = QCheckBox("static (静态)")
        self.static_check.stateChanged.connect(self.update_preview)
        attr_layout.addWidget(self.static_check)
        
        self.inline_check = QCheckBox("inline (内联)")
        self.inline_check.stateChanged.connect(self.update_preview)
        attr_layout.addWidget(self.inline_check)
        
        attr_layout.addStretch()
        basic_layout.addLayout(attr_layout)
        
        # 函数说明
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("函数说明:"))
        self.function_desc_edit = QTextEdit()
        self.function_desc_edit.setMaximumHeight(80)
        self.function_desc_edit.setPlaceholderText("函数的功能描述...")
        self.function_desc_edit.textChanged.connect(self.update_preview)
        desc_layout.addWidget(self.function_desc_edit)
        basic_layout.addLayout(desc_layout)
        
        layout.addWidget(basic_group)
        
        # 参数管理组
        param_group = QGroupBox("📝 参数列表")
        param_layout = QVBoxLayout(param_group)
        
        # 参数列表
        self.param_list = QListWidget()
        self.param_list.setMinimumHeight(150)
        param_layout.addWidget(self.param_list)
        
        # 参数操作按钮
        param_btn_layout = QHBoxLayout()
        
        add_param_btn = QPushButton("➕ 添加参数")
        add_param_btn.clicked.connect(self.add_parameter)
        param_btn_layout.addWidget(add_param_btn)
        
        edit_param_btn = QPushButton("✏️ 编辑")
        edit_param_btn.clicked.connect(self.edit_parameter)
        param_btn_layout.addWidget(edit_param_btn)
        
        del_param_btn = QPushButton("🗑️ 删除")
        del_param_btn.clicked.connect(self.delete_parameter)
        param_btn_layout.addWidget(del_param_btn)
        
        clear_param_btn = QPushButton("🧹 清空")
        clear_param_btn.clicked.connect(self.clear_parameters)
        param_btn_layout.addWidget(clear_param_btn)
        
        param_btn_layout.addStretch()
        param_layout.addLayout(param_btn_layout)
        
        layout.addWidget(param_group)
        
        # 代码生成选项
        gen_opt_group = QGroupBox("⚙️ 生成选项")
        gen_opt_layout = QVBoxLayout(gen_opt_group)
        
        opt_layout = QHBoxLayout()
        self.gen_declaration_check = QCheckBox("生成声明")
        self.gen_declaration_check.setChecked(True)
        self.gen_declaration_check.stateChanged.connect(self.update_preview)
        opt_layout.addWidget(self.gen_declaration_check)
        
        self.gen_definition_check = QCheckBox("生成定义")
        self.gen_definition_check.setChecked(True)
        self.gen_definition_check.stateChanged.connect(self.update_preview)
        opt_layout.addWidget(self.gen_definition_check)
        
        self.gen_doxygen_check = QCheckBox("Doxygen格式注释")
        self.gen_doxygen_check.stateChanged.connect(self.update_preview)
        opt_layout.addWidget(self.gen_doxygen_check)
        
        opt_layout.addStretch()
        gen_opt_layout.addLayout(opt_layout)
        
        layout.addWidget(gen_opt_group)
        
        # 预览和生成
        preview_group = QGroupBox("👁️ 代码预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_display = QTextEdit()
        self.preview_display.setReadOnly(True)
        self.preview_display.setMinimumHeight(250)
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
        """翻译函数名"""
        chinese_text = self.chinese_name_edit.text().strip()
        if not chinese_text:
            QMessageBox.warning(self, "提示", "请先输入中文名称")
            return
        
        result = translator.translate(chinese_text)
        self.english_name_edit.setText(result['primary'])
        self.update_preview()
    
    def add_parameter(self):
        """添加参数"""
        dialog = ParameterDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            param = dialog.get_param()
            if not param['name']:
                QMessageBox.warning(self, "提示", "参数名不能为空")
                return
            
            self.parameters.append(param)
            self.refresh_param_list()
            self.update_preview()
    
    def edit_parameter(self):
        """编辑参数"""
        current_item = self.param_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个参数")
            return
        
        index = self.param_list.currentRow()
        param = self.parameters[index]
        
        dialog = ParameterDialog(self, param)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_param = dialog.get_param()
            self.parameters[index] = updated_param
            self.refresh_param_list()
            self.update_preview()
    
    def delete_parameter(self):
        """删除参数"""
        current_item = self.param_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个参数")
            return
        
        index = self.param_list.currentRow()
        self.parameters.pop(index)
        self.refresh_param_list()
        self.update_preview()
    
    def clear_parameters(self):
        """清空参数"""
        self.parameters.clear()
        self.refresh_param_list()
        self.update_preview()
    
    def refresh_param_list(self):
        """刷新参数列表"""
        self.param_list.clear()
        for i, param in enumerate(self.parameters):
            modifiers = []
            if param.get('const'):
                modifiers.append('const')
            
            param_type = param['type']
            if param.get('pointer'):
                param_type += '*'
            
            modifier_str = ' '.join(modifiers) + ' ' if modifiers else ''
            
            display_text = f"{i+1}. {modifier_str}{param_type} {param['name']}"
            if param.get('chinese_name'):
                display_text += f" ({param['chinese_name']})"
            
            self.param_list.addItem(display_text)
    
    def update_preview(self):
        """更新预览"""
        func_name = self.english_name_edit.text().strip()
        if not func_name:
            self.preview_display.clear()
            return
        
        code = ""
        
        # 生成注释
        chinese_name = self.chinese_name_edit.text().strip() or func_name
        func_desc = self.function_desc_edit.toPlainText().strip()
        
        if self.gen_doxygen_check.isChecked():
            # Doxygen格式
            code += "/**\n"
            code += f" * @brief {chinese_name}\n"
            if func_desc:
                code += f" * \n"
                code += f" * {func_desc}\n"
            
            if self.parameters:
                code += " * \n"
                for param in self.parameters:
                    param_desc = param.get('description', param.get('chinese_name', ''))
                    code += f" * @param {param['name']} {param_desc}\n"
            
            ret_type = self.return_type_combo.currentText()
            if ret_type != 'void':
                code += " * \n"
                code += f" * @return {ret_type}\n"
            
            code += " */\n"
        else:
            # 普通注释
            code += "/*\n"
            code += f" * {chinese_name}\n"
            if func_desc:
                code += f" * \n"
                code += f" * 功能: {func_desc}\n"
            
            if self.parameters:
                code += " * \n"
                code += " * 参数:\n"
                for param in self.parameters:
                    param_desc = param.get('description', param.get('chinese_name', ''))
                    code += f" *   {param['name']}: {param_desc}\n"
            
            ret_type = self.return_type_combo.currentText()
            if ret_type != 'void':
                code += " * \n"
                code += f" * 返回: {ret_type}\n"
            
            code += " */\n"
        
        # 函数签名
        attributes = []
        if self.static_check.isChecked():
            attributes.append("static")
        if self.inline_check.isChecked():
            attributes.append("inline")
        
        attr_str = " ".join(attributes) + " " if attributes else ""
        ret_type = self.return_type_combo.currentText()
        
        # 参数列表
        if self.parameters:
            params = []
            for param in self.parameters:
                modifiers = []
                if param.get('const'):
                    modifiers.append('const')
                
                param_type = param['type']
                if param.get('pointer'):
                    param_type += '*'
                
                modifier_str = ' '.join(modifiers) + ' ' if modifiers else ''
                params.append(f"{modifier_str}{param_type} {param['name']}")
            
            param_str = ", ".join(params)
        else:
            param_str = "void"
        
        # 生成声明
        if self.gen_declaration_check.isChecked():
            code += f"{attr_str}{ret_type} {func_name}({param_str});\n"
        
        # 生成定义
        if self.gen_definition_check.isChecked():
            if self.gen_declaration_check.isChecked():
                code += "\n"
            
            code += f"{attr_str}{ret_type} {func_name}({param_str})\n"
            code += "{\n"
            code += "    // TODO: 实现函数功能\n"
            if ret_type != 'void':
                if 'int' in ret_type or ret_type == 'bool':
                    code += "    return 0;\n"
                elif ret_type in ['float', 'double']:
                    code += "    return 0.0;\n"
                elif ret_type == 'char*':
                    code += "    return NULL;\n"
            code += "}\n"
        
        self.preview_display.setPlainText(code)
    
    def generate_code(self):
        """生成代码"""
        if not self.english_name_edit.text().strip():
            QMessageBox.warning(self, "提示", "请先输入函数英文名")
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
