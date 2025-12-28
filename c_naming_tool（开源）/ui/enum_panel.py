"""
枚举定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QGroupBox, QMessageBox,
    QScrollArea, QListWidget, QDialog, QDialogButtonBox, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from core.naming import naming_generator
from core.translator import translator


class EnumValueDialog(QDialog):
    """枚举值编辑对话框"""
    
    def __init__(self, parent=None, value_data=None):
        super().__init__(parent)
        self.value_data = value_data or {}
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("添加/编辑枚举值")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 枚举值名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("名称:"))
        self.name_input = QLineEdit()
        self.name_input.setText(self.value_data.get('name', ''))
        self.name_input.setPlaceholderText("例如: STATE_IDLE")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # 是否指定值
        self.specify_value_check = QCheckBox("指定枚举值")
        self.specify_value_check.setChecked(self.value_data.get('value') is not None)
        self.specify_value_check.toggled.connect(self.on_specify_toggled)
        layout.addWidget(self.specify_value_check)
        
        # 枚举值
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("值:"))
        self.value_spinbox = QSpinBox()
        self.value_spinbox.setMinimum(-2147483648)
        self.value_spinbox.setMaximum(2147483647)
        self.value_spinbox.setValue(self.value_data.get('value', 0) if self.value_data.get('value') is not None else 0)
        self.value_spinbox.setEnabled(self.specify_value_check.isChecked())
        value_layout.addWidget(self.value_spinbox)
        layout.addLayout(value_layout)
        
        # 注释
        comment_layout = QHBoxLayout()
        comment_layout.addWidget(QLabel("注释:"))
        self.comment_input = QLineEdit()
        self.comment_input.setText(self.value_data.get('comment', ''))
        self.comment_input.setPlaceholderText("例如: 空闲状态")
        comment_layout.addWidget(self.comment_input)
        layout.addLayout(comment_layout)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def on_specify_toggled(self, checked):
        """指定值复选框切换"""
        self.value_spinbox.setEnabled(checked)
    
    def get_value_data(self):
        """获取枚举值数据"""
        return {
            'name': self.name_input.text().strip(),
            'value': self.value_spinbox.value() if self.specify_value_check.isChecked() else None,
            'comment': self.comment_input.text().strip()
        }


class EnumPanel(QWidget):
    """枚举定义面板"""
    
    code_generated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.enum_values = []
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
        title = QLabel("📋 枚举定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # 枚举名称输入
        name_group = QGroupBox("枚举配置")
        name_layout = QVBoxLayout(name_group)
        
        enum_name_layout = QHBoxLayout()
        enum_name_layout.addWidget(QLabel("枚举名称:"))
        self.enum_name_input = QLineEdit()
        self.enum_name_input.setPlaceholderText("例如：system_state 或 系统状态")
        self.enum_name_input.textChanged.connect(self.update_preview)
        enum_name_layout.addWidget(self.enum_name_input)
        
        self.enum_translate_btn = QPushButton("🌐 翻译")
        self.enum_translate_btn.setMaximumWidth(80)
        self.enum_translate_btn.clicked.connect(self.translate_enum_name)
        enum_name_layout.addWidget(self.enum_translate_btn)
        name_layout.addLayout(enum_name_layout)
        
        self.enum_suggestions = QLabel()
        self.enum_suggestions.setWordWrap(True)
        self.enum_suggestions.setProperty("class", "hint")
        self.enum_suggestions.hide()
        name_layout.addWidget(self.enum_suggestions)
        
        layout.addWidget(name_group)
        
        # 枚举值列表
        values_group = QGroupBox("枚举值列表")
        values_layout = QVBoxLayout(values_group)
        
        # 枚举值操作按钮
        value_btn_layout = QHBoxLayout()
        add_value_btn = QPushButton("➕ 添加枚举值")
        add_value_btn.clicked.connect(self.add_value)
        value_btn_layout.addWidget(add_value_btn)
        
        edit_value_btn = QPushButton("✏️ 编辑枚举值")
        edit_value_btn.clicked.connect(self.edit_value)
        value_btn_layout.addWidget(edit_value_btn)
        
        remove_value_btn = QPushButton("🗑️ 删除枚举值")
        remove_value_btn.clicked.connect(self.remove_value)
        value_btn_layout.addWidget(remove_value_btn)
        
        move_up_btn = QPushButton("↑ 上移")
        move_up_btn.clicked.connect(self.move_up)
        value_btn_layout.addWidget(move_up_btn)
        
        move_down_btn = QPushButton("↓ 下移")
        move_down_btn.clicked.connect(self.move_down)
        value_btn_layout.addWidget(move_down_btn)
        
        value_btn_layout.addStretch()
        values_layout.addLayout(value_btn_layout)
        
        # 枚举值列表
        self.values_list = QListWidget()
        self.values_list.setMinimumHeight(200)
        values_layout.addWidget(self.values_list)
        
        layout.addWidget(values_group)
        
        # 枚举信息显示
        self.enum_info_group = QGroupBox("📊 枚举信息")
        self.enum_info_layout = QVBoxLayout(self.enum_info_group)
        self.enum_info_display = QLabel()
        self.enum_info_display.setWordWrap(True)
        self.enum_info_layout.addWidget(self.enum_info_display)
        layout.addWidget(self.enum_info_group)
        
        # 预览区域
        preview_group = QGroupBox("🎯 枚举类型名")
        preview_layout = QVBoxLayout(preview_group)
        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #007AFF;")
        preview_layout.addWidget(self.preview_label)
        layout.addWidget(preview_group)
        
        # 代码显示区域
        code_group = QGroupBox("📋 生成的代码")
        code_layout = QVBoxLayout(code_group)
        self.code_display = QTextEdit()
        self.code_display.setProperty("class", "code")
        self.code_display.setReadOnly(True)
        self.code_display.setMinimumHeight(250)
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
        
        # 初始化
        self.update_enum_info()
    
    def add_value(self):
        """添加枚举值"""
        dialog = EnumValueDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            value_data = dialog.get_value_data()
            if value_data['name']:
                self.enum_values.append(value_data)
                self.update_values_list()
                self.update_enum_info()
    
    def edit_value(self):
        """编辑枚举值"""
        current_row = self.values_list.currentRow()
        if current_row >= 0:
            dialog = EnumValueDialog(self, self.enum_values[current_row])
            if dialog.exec() == QDialog.DialogCode.Accepted:
                value_data = dialog.get_value_data()
                if value_data['name']:
                    self.enum_values[current_row] = value_data
                    self.update_values_list()
                    self.update_enum_info()
    
    def remove_value(self):
        """删除枚举值"""
        current_row = self.values_list.currentRow()
        if current_row >= 0:
            del self.enum_values[current_row]
            self.update_values_list()
            self.update_enum_info()
    
    def move_up(self):
        """上移枚举值"""
        current_row = self.values_list.currentRow()
        if current_row > 0:
            self.enum_values[current_row], self.enum_values[current_row - 1] = \
                self.enum_values[current_row - 1], self.enum_values[current_row]
            self.update_values_list()
            self.values_list.setCurrentRow(current_row - 1)
    
    def move_down(self):
        """下移枚举值"""
        current_row = self.values_list.currentRow()
        if current_row >= 0 and current_row < len(self.enum_values) - 1:
            self.enum_values[current_row], self.enum_values[current_row + 1] = \
                self.enum_values[current_row + 1], self.enum_values[current_row]
            self.update_values_list()
            self.values_list.setCurrentRow(current_row + 1)
    
    def update_values_list(self):
        """更新枚举值列表显示"""
        self.values_list.clear()
        current_value = 0
        
        for i, value in enumerate(self.enum_values):
            if value['value'] is not None:
                current_value = value['value']
                value_str = f" = {current_value}"
            else:
                value_str = f" (= {current_value})"
            
            item_text = f"{i+1}. {value['name']}{value_str}"
            if value['comment']:
                item_text += f" - {value['comment']}"
            
            self.values_list.addItem(item_text)
            current_value += 1
    
    def update_enum_info(self):
        """更新枚举信息"""
        if not self.enum_values:
            info_text = "<p>暂无枚举值，请添加枚举值</p>"
            self.enum_info_display.setText(info_text)
            return
        
        # 统计信息
        specified_count = sum(1 for v in self.enum_values if v['value'] is not None)
        auto_count = len(self.enum_values) - specified_count
        
        info_text = f"""
<p><b>枚举值数量:</b> {len(self.enum_values)}</p>
<p><b>指定值:</b> {specified_count}</p>
<p><b>自动编号:</b> {auto_count}</p>
<p><b>存储大小:</b> 通常为 4 bytes (int)</p>
<p style="color: #007AFF;"><b>💡 提示:</b> 枚举值建议使用全大写命名，用下划线分隔</p>
"""
        
        self.enum_info_display.setText(info_text)
    
    def translate_enum_name(self):
        """翻译枚举名称"""
        chinese = self.enum_name_input.text().strip()
        if not chinese:
            return
            
        result = translator.translate(chinese)
        self.enum_name_input.setText(result['primary'])
        
        if result.get('alternatives'):
            suggestions_text = "✨ 其他建议: " + ", ".join(result['alternatives'][:3])
            self.enum_suggestions.setText(suggestions_text)
            self.enum_suggestions.show()
        else:
            self.enum_suggestions.hide()
    
    def update_preview(self):
        """更新预览"""
        enum_name = self.enum_name_input.text().strip()
        if enum_name:
            type_name = naming_generator.generate_enum_name(enum_name)
            self.preview_label.setText(type_name)
        else:
            self.preview_label.setText("请输入枚举名称")
    
    def generate_code(self):
        """生成代码"""
        enum_name = self.enum_name_input.text().strip()
        
        if not enum_name:
            QMessageBox.warning(self, "提示", "请输入枚举名称")
            return
        
        if not self.enum_values:
            QMessageBox.warning(self, "提示", "请至少添加一个枚举值")
            return
        
        # 生成枚举类型名
        enum_name_en = translator.translate(enum_name)['primary']
        
        # 生成代码
        from utils.code_generator import code_generator
        code = code_generator.generate_enum_code(enum_name_en, self.enum_values, enum_name)
        
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
        self.enum_name_input.clear()
        self.enum_values.clear()
        self.update_values_list()
        self.update_enum_info()
        self.code_display.clear()
        self.preview_label.setText("")
        self.enum_suggestions.hide()
