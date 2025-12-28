"""
结构体定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QGroupBox, QMessageBox,
    QScrollArea, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from core.naming import naming_generator
from core.type_info import type_info_manager
from core.translator import translator
from utils.code_generator import code_generator


class MemberDialog(QDialog):
    """成员编辑对话框"""
    
    def __init__(self, parent=None, member_data=None):
        super().__init__(parent)
        self.member_data = member_data or {}
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("添加/编辑成员")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 成员类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(type_info_manager.get_all_types())
        if self.member_data.get('type'):
            index = self.type_combo.findText(self.member_data['type'])
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # 成员名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("名称:"))
        self.name_input = QLineEdit()
        self.name_input.setText(self.member_data.get('name', ''))
        self.name_input.setPlaceholderText("例如: temperature")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # 注释
        comment_layout = QHBoxLayout()
        comment_layout.addWidget(QLabel("注释:"))
        self.comment_input = QLineEdit()
        self.comment_input.setText(self.member_data.get('comment', ''))
        self.comment_input.setPlaceholderText("例如: 温度值(℃)")
        comment_layout.addWidget(self.comment_input)
        layout.addLayout(comment_layout)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_member_data(self):
        """获取成员数据"""
        return {
            'type': self.type_combo.currentText(),
            'name': self.name_input.text().strip(),
            'comment': self.comment_input.text().strip()
        }


class StructPanel(QWidget):
    """结构体定义面板"""
    
    code_generated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.members = []
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
        title = QLabel("🏗️ 结构体定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # 结构体名称输入
        name_group = QGroupBox("结构体配置")
        name_layout = QVBoxLayout(name_group)
        
        struct_name_layout = QHBoxLayout()
        struct_name_layout.addWidget(QLabel("结构体名称:"))
        self.struct_name_input = QLineEdit()
        self.struct_name_input.setPlaceholderText("例如：sensor_data 或 传感器数据")
        self.struct_name_input.textChanged.connect(self.update_preview)
        struct_name_layout.addWidget(self.struct_name_input)
        
        self.struct_translate_btn = QPushButton("🌐 翻译")
        self.struct_translate_btn.setMaximumWidth(80)
        self.struct_translate_btn.clicked.connect(self.translate_struct_name)
        struct_name_layout.addWidget(self.struct_translate_btn)
        name_layout.addLayout(struct_name_layout)
        
        self.struct_suggestions = QLabel()
        self.struct_suggestions.setWordWrap(True)
        self.struct_suggestions.setProperty("class", "hint")
        self.struct_suggestions.hide()
        name_layout.addWidget(self.struct_suggestions)
        
        layout.addWidget(name_group)
        
        # 成员列表
        members_group = QGroupBox("成员列表")
        members_layout = QVBoxLayout(members_group)
        
        # 成员操作按钮
        member_btn_layout = QHBoxLayout()
        add_member_btn = QPushButton("➕ 添加成员")
        add_member_btn.clicked.connect(self.add_member)
        member_btn_layout.addWidget(add_member_btn)
        
        edit_member_btn = QPushButton("✏️ 编辑成员")
        edit_member_btn.clicked.connect(self.edit_member)
        member_btn_layout.addWidget(edit_member_btn)
        
        remove_member_btn = QPushButton("🗑️ 删除成员")
        remove_member_btn.clicked.connect(self.remove_member)
        member_btn_layout.addWidget(remove_member_btn)
        
        move_up_btn = QPushButton("↑ 上移")
        move_up_btn.clicked.connect(self.move_up)
        member_btn_layout.addWidget(move_up_btn)
        
        move_down_btn = QPushButton("↓ 下移")
        move_down_btn.clicked.connect(self.move_down)
        member_btn_layout.addWidget(move_down_btn)
        
        member_btn_layout.addStretch()
        members_layout.addLayout(member_btn_layout)
        
        # 成员列表
        self.members_list = QListWidget()
        self.members_list.setMinimumHeight(200)
        members_layout.addWidget(self.members_list)
        
        layout.addWidget(members_group)
        
        # 结构体信息显示
        self.struct_info_group = QGroupBox("📦 结构体信息")
        self.struct_info_layout = QVBoxLayout(self.struct_info_group)
        self.struct_info_display = QLabel()
        self.struct_info_display.setWordWrap(True)
        self.struct_info_layout.addWidget(self.struct_info_display)
        layout.addWidget(self.struct_info_group)
        
        # 预览区域
        preview_group = QGroupBox("🎯 结构体类型名")
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
        self.update_struct_info()
    
    def add_member(self):
        """添加成员"""
        dialog = MemberDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            member_data = dialog.get_member_data()
            if member_data['name']:
                self.members.append(member_data)
                self.update_members_list()
                self.update_struct_info()
    
    def edit_member(self):
        """编辑成员"""
        current_row = self.members_list.currentRow()
        if current_row >= 0:
            dialog = MemberDialog(self, self.members[current_row])
            if dialog.exec() == QDialog.DialogCode.Accepted:
                member_data = dialog.get_member_data()
                if member_data['name']:
                    self.members[current_row] = member_data
                    self.update_members_list()
                    self.update_struct_info()
    
    def remove_member(self):
        """删除成员"""
        current_row = self.members_list.currentRow()
        if current_row >= 0:
            del self.members[current_row]
            self.update_members_list()
            self.update_struct_info()
    
    def move_up(self):
        """上移成员"""
        current_row = self.members_list.currentRow()
        if current_row > 0:
            self.members[current_row], self.members[current_row - 1] = \
                self.members[current_row - 1], self.members[current_row]
            self.update_members_list()
            self.members_list.setCurrentRow(current_row - 1)
            self.update_struct_info()
    
    def move_down(self):
        """下移成员"""
        current_row = self.members_list.currentRow()
        if current_row >= 0 and current_row < len(self.members) - 1:
            self.members[current_row], self.members[current_row + 1] = \
                self.members[current_row + 1], self.members[current_row]
            self.update_members_list()
            self.members_list.setCurrentRow(current_row + 1)
            self.update_struct_info()
    
    def update_members_list(self):
        """更新成员列表显示"""
        self.members_list.clear()
        for i, member in enumerate(self.members):
            type_info = type_info_manager.get_type_info(member['type'])
            range_str = type_info_manager.get_range_str(member['type'])
            
            item_text = f"{i+1}. {member['name']} ({member['type']})"
            if member['comment']:
                item_text += f" - {member['comment']}"
            item_text += f"\n   范围: {range_str}"
            
            self.members_list.addItem(item_text)
    
    def update_struct_info(self):
        """更新结构体信息"""
        if not self.members:
            info_text = "<p>暂无成员，请添加成员</p>"
            self.struct_info_display.setText(info_text)
            return
        
        # 计算结构体大小
        unaligned, aligned, padding = self.calculate_struct_size()
        
        info_text = f"""
<p><b>成员数量:</b> {len(self.members)}</p>
<p><b>总大小:</b> {unaligned} bytes (未对齐)</p>
<p><b>对齐后:</b> {aligned} bytes (4字节对齐)</p>
"""
        
        if padding > 0:
            info_text += f"<p><b>填充字节:</b> {padding} bytes</p>"
            info_text += """
<p style="color: #FF9500;"><b>⚠️ 建议:</b> 调整成员顺序可能减少填充字节</p>
"""
        
        self.struct_info_display.setText(info_text)
    
    def calculate_struct_size(self):
        """计算结构体大小"""
        offset = 0
        max_alignment = 1
        
        for member in self.members:
            type_info = type_info_manager.get_type_info(member['type'])
            member_bytes = type_info.get('bytes', 0)
            
            if member_bytes > 0:
                alignment = min(member_bytes, 4)
                max_alignment = max(max_alignment, alignment)
                
                if offset % alignment != 0:
                    offset += alignment - (offset % alignment)
                
                offset += member_bytes
        
        unaligned_size = offset
        if offset % max_alignment != 0:
            aligned_size = offset + (max_alignment - offset % max_alignment)
        else:
            aligned_size = offset
        
        padding = aligned_size - unaligned_size
        
        return unaligned_size, aligned_size, padding
    
    def translate_struct_name(self):
        """翻译结构体名称"""
        chinese = self.struct_name_input.text().strip()
        if not chinese:
            return
            
        result = translator.translate(chinese)
        self.struct_name_input.setText(result['primary'])
        
        if result.get('alternatives'):
            suggestions_text = "✨ 其他建议: " + ", ".join(result['alternatives'][:3])
            self.struct_suggestions.setText(suggestions_text)
            self.struct_suggestions.show()
        else:
            self.struct_suggestions.hide()
    
    def update_preview(self):
        """更新预览"""
        struct_name = self.struct_name_input.text().strip()
        if struct_name:
            type_name = naming_generator.generate_struct_name(struct_name)
            self.preview_label.setText(type_name)
        else:
            self.preview_label.setText("请输入结构体名称")
    
    def generate_code(self):
        """生成代码"""
        struct_name = self.struct_name_input.text().strip()
        
        if not struct_name:
            QMessageBox.warning(self, "提示", "请输入结构体名称")
            return
        
        if not self.members:
            QMessageBox.warning(self, "提示", "请至少添加一个成员")
            return
        
        # 生成代码
        code = code_generator.generate_struct_code(struct_name, self.members)
        
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
        self.struct_name_input.clear()
        self.members.clear()
        self.update_members_list()
        self.update_struct_info()
        self.code_display.clear()
        self.preview_label.setText("")
        self.struct_suggestions.hide()
