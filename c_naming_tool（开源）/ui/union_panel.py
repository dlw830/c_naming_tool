"""
联合体定义面板
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QGroupBox, QMessageBox,
    QScrollArea, QListWidget, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from core.naming import naming_generator
from core.type_info import type_info_manager
from core.translator import translator
from utils.code_generator import code_generator


class UnionMemberDialog(QDialog):
    """联合体成员编辑对话框"""
    
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
        self.name_input.setPlaceholderText("例如: int_value")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # 注释
        comment_layout = QHBoxLayout()
        comment_layout.addWidget(QLabel("注释:"))
        self.comment_input = QLineEdit()
        self.comment_input.setText(self.member_data.get('comment', ''))
        self.comment_input.setPlaceholderText("例如: 整数值")
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


class UnionPanel(QWidget):
    """联合体定义面板"""
    
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
        title = QLabel("🔀 联合体定义")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # 联合体名称输入
        name_group = QGroupBox("联合体配置")
        name_layout = QVBoxLayout(name_group)
        
        union_name_layout = QHBoxLayout()
        union_name_layout.addWidget(QLabel("联合体名称:"))
        self.union_name_input = QLineEdit()
        self.union_name_input.setPlaceholderText("例如：data_buffer 或 数据缓冲")
        self.union_name_input.textChanged.connect(self.update_preview)
        union_name_layout.addWidget(self.union_name_input)
        
        self.union_translate_btn = QPushButton("🌐 翻译")
        self.union_translate_btn.setMaximumWidth(80)
        self.union_translate_btn.clicked.connect(self.translate_union_name)
        union_name_layout.addWidget(self.union_translate_btn)
        name_layout.addLayout(union_name_layout)
        
        self.union_suggestions = QLabel()
        self.union_suggestions.setWordWrap(True)
        self.union_suggestions.setProperty("class", "hint")
        self.union_suggestions.hide()
        name_layout.addWidget(self.union_suggestions)
        
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
        
        member_btn_layout.addStretch()
        members_layout.addLayout(member_btn_layout)
        
        # 成员列表
        self.members_list = QListWidget()
        self.members_list.setMinimumHeight(200)
        members_layout.addWidget(self.members_list)
        
        layout.addWidget(members_group)
        
        # 联合体信息显示
        self.union_info_group = QGroupBox("📦 联合体信息")
        self.union_info_layout = QVBoxLayout(self.union_info_group)
        self.union_info_display = QLabel()
        self.union_info_display.setWordWrap(True)
        self.union_info_layout.addWidget(self.union_info_display)
        layout.addWidget(self.union_info_group)
        
        # 预览区域
        preview_group = QGroupBox("🎯 联合体类型名")
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
        self.update_union_info()
    
    def add_member(self):
        """添加成员"""
        dialog = UnionMemberDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            member_data = dialog.get_member_data()
            if member_data['name']:
                self.members.append(member_data)
                self.update_members_list()
                self.update_union_info()
    
    def edit_member(self):
        """编辑成员"""
        current_row = self.members_list.currentRow()
        if current_row >= 0:
            dialog = UnionMemberDialog(self, self.members[current_row])
            if dialog.exec() == QDialog.DialogCode.Accepted:
                member_data = dialog.get_member_data()
                if member_data['name']:
                    self.members[current_row] = member_data
                    self.update_members_list()
                    self.update_union_info()
    
    def remove_member(self):
        """删除成员"""
        current_row = self.members_list.currentRow()
        if current_row >= 0:
            del self.members[current_row]
            self.update_members_list()
            self.update_union_info()
    
    def update_members_list(self):
        """更新成员列表显示"""
        self.members_list.clear()
        for i, member in enumerate(self.members):
            type_info = type_info_manager.get_type_info(member['type'])
            range_str = type_info_manager.get_range_str(member['type'])
            bytes_info = type_info.get('bytes', 0)
            
            item_text = f"{i+1}. {member['name']} ({member['type']}, {bytes_info} bytes)"
            if member['comment']:
                item_text += f" - {member['comment']}"
            item_text += f"\n   范围: {range_str}"
            
            self.members_list.addItem(item_text)
    
    def update_union_info(self):
        """更新联合体信息"""
        if not self.members:
            info_text = "<p>暂无成员，请添加成员</p>"
            self.union_info_display.setText(info_text)
            return
        
        # 计算联合体大小（取最大成员的大小）
        max_size = 0
        max_member = None
        
        for member in self.members:
            type_info = type_info_manager.get_type_info(member['type'])
            member_bytes = type_info.get('bytes', 0)
            if member_bytes > max_size:
                max_size = member_bytes
                max_member = member
        
        info_text = f"""
<p><b>成员数量:</b> {len(self.members)}</p>
<p><b>联合体大小:</b> {max_size} bytes (取最大成员)</p>
<p><b>最大成员:</b> {max_member['name']} ({max_member['type']})</p>
<p style="color: #FF9500;"><b>💡 提示:</b> 联合体所有成员共享同一块内存，大小由最大成员决定</p>
<p style="color: #FF9500;"><b>⚠️ 注意:</b> 同一时刻只能使用一个成员</p>
"""
        
        self.union_info_display.setText(info_text)
    
    def translate_union_name(self):
        """翻译联合体名称"""
        chinese = self.union_name_input.text().strip()
        if not chinese:
            return
            
        result = translator.translate(chinese)
        self.union_name_input.setText(result['primary'])
        
        if result.get('alternatives'):
            suggestions_text = "✨ 其他建议: " + ", ".join(result['alternatives'][:3])
            self.union_suggestions.setText(suggestions_text)
            self.union_suggestions.show()
        else:
            self.union_suggestions.hide()
    
    def update_preview(self):
        """更新预览"""
        union_name = self.union_name_input.text().strip()
        if union_name:
            type_name = naming_generator.generate_union_name(union_name)
            self.preview_label.setText(type_name)
        else:
            self.preview_label.setText("请输入联合体名称")
    
    def generate_code(self):
        """生成代码"""
        union_name = self.union_name_input.text().strip()
        
        if not union_name:
            QMessageBox.warning(self, "提示", "请输入联合体名称")
            return
        
        if not self.members:
            QMessageBox.warning(self, "提示", "请至少添加一个成员")
            return
        
        # 生成联合体类型名
        union_name_en = translator.translate(union_name)['primary']
        
        # 计算最大成员大小
        max_size = 0
        for member in self.members:
            type_info = type_info_manager.get_type_info(member['type'])
            member_bytes = type_info.get('bytes', 0)
            max_size = max(max_size, member_bytes)
        
        # 生成代码
        code = f"""/*******************************************************************************
 * 联合体名称: {union_name_en}_u
 * 功能描述: {union_name}
 * 大小: {max_size} bytes
 * 成员数量: {len(self.members)}
 * 
 * 注意: 联合体所有成员共享同一块内存空间
 ******************************************************************************/
typedef union {{
"""
        
        # 添加成员
        for member in self.members:
            type_info = type_info_manager.get_type_info(member['type'])
            range_str = type_info_manager.get_range_str(member['type'])
            bytes_info = type_info.get('bytes', 0)
            
            if member['comment']:
                code += f"    {member['type']:<12} {member['name']};  // {member['comment']}, Range: {range_str}, {bytes_info} bytes\n"
            else:
                code += f"    {member['type']:<12} {member['name']};  // Range: {range_str}, {bytes_info} bytes\n"
        
        code += f"}} {union_name_en}_u;\n\n"
        
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
        self.union_name_input.clear()
        self.members.clear()
        self.update_members_list()
        self.update_union_info()
        self.code_display.clear()
        self.preview_label.setText("")
        self.union_suggestions.hide()
