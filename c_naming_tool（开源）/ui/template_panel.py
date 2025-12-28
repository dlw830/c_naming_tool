"""
模板库面板
"""

import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGroupBox, QListWidget, QListWidgetItem,
    QDialog, QLineEdit, QTextEdit, QMessageBox, QScrollArea,
    QFileDialog
)
from PyQt6.QtCore import Qt


class TemplateDialog(QDialog):
    """模板编辑对话框"""
    
    def __init__(self, parent=None, template_data=None):
        super().__init__(parent)
        self.template_data = template_data or {}
        self.init_ui()
        self.load_template()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("模板编辑")
        self.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 模板名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("模板名称:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如: ADC配置模板")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # 分类
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("模板分类:"))
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("例如: 外设配置")
        category_layout.addWidget(self.category_edit)
        layout.addLayout(category_layout)
        
        # 描述
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("模板描述:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("描述这个模板的用途和使用场景...")
        self.desc_edit.setMinimumHeight(100)
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)
        
        # 代码内容
        code_layout = QVBoxLayout()
        code_layout.addWidget(QLabel("代码内容:"))
        self.code_edit = QTextEdit()
        self.code_edit.setProperty("class", "code")
        self.code_edit.setPlaceholderText("""粘贴模板代码，例如：

typedef struct {
    uint8_t channel;
    uint32_t sample_rate;
} adc_config_t;

adc_config_t g_st_adc_config;
""")
        self.code_edit.setMinimumHeight(200)
        code_layout.addWidget(self.code_edit)
        layout.addLayout(code_layout)
        
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
    
    def load_template(self):
        """加载模板数据"""
        if self.template_data:
            self.name_edit.setText(self.template_data.get('name', ''))
            self.category_edit.setText(self.template_data.get('category', ''))
            self.desc_edit.setPlainText(self.template_data.get('description', ''))
            self.code_edit.setPlainText(self.template_data.get('code', ''))
    
    def get_template(self):
        """获取模板数据"""
        return {
            'name': self.name_edit.text().strip(),
            'category': self.category_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip(),
            'code': self.code_edit.toPlainText().strip(),
            'created_at': self.template_data.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }


class TemplatePanel(QWidget):
    """模板库面板"""
    
    def __init__(self):
        super().__init__()
        self.templates_file = os.path.join('c_naming_tool', 'config', 'templates.json')
        self.templates = []
        self.init_ui()
        self.load_templates()
    
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
        title = QLabel("📚 模板库")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        hint = QLabel("保存常用的变量定义模板，快速复用代码")
        hint.setProperty("class", "hint")
        layout.addWidget(hint)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ 新建模板")
        add_btn.clicked.connect(self.add_template)
        btn_layout.addWidget(add_btn)
        
        import_btn = QPushButton("📥 导入模板")
        import_btn.clicked.connect(self.import_templates)
        btn_layout.addWidget(import_btn)
        
        export_btn = QPushButton("📤 导出模板")
        export_btn.clicked.connect(self.export_templates)
        btn_layout.addWidget(export_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 模板列表
        list_group = QGroupBox("📋 模板列表")
        list_layout = QVBoxLayout(list_group)
        
        self.template_list = QListWidget()
        self.template_list.setMinimumHeight(300)
        self.template_list.itemDoubleClicked.connect(self.view_template)
        list_layout.addWidget(self.template_list)
        
        # 列表操作按钮
        list_btn_layout = QHBoxLayout()
        
        view_btn = QPushButton("👁️ 查看")
        view_btn.clicked.connect(self.view_selected_template)
        list_btn_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("✏️ 编辑")
        edit_btn.clicked.connect(self.edit_template)
        list_btn_layout.addWidget(edit_btn)
        
        use_btn = QPushButton("📋 使用")
        use_btn.clicked.connect(self.use_template)
        list_btn_layout.addWidget(use_btn)
        
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.clicked.connect(self.delete_template)
        list_btn_layout.addWidget(delete_btn)
        
        list_btn_layout.addStretch()
        list_layout.addLayout(list_btn_layout)
        
        layout.addWidget(list_group)
        
        # 预览区域
        preview_group = QGroupBox("👁️ 模板预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_display = QTextEdit()
        self.preview_display.setReadOnly(True)
        self.preview_display.setMinimumHeight(200)
        preview_layout.addWidget(self.preview_display)
        
        layout.addWidget(preview_group)
        
        layout.addStretch()
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def load_templates(self):
        """加载模板列表"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            else:
                # 创建默认模板
                self.templates = self.create_default_templates()
                self.save_templates()
            
            self.refresh_template_list()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载模板失败: {str(e)}")
            self.templates = []
    
    def create_default_templates(self):
        """创建默认模板"""
        return [
            {
                'name': 'ADC配置模板',
                'category': '外设配置',
                'description': 'ADC外设的基本配置结构',
                'code': '''typedef struct {
    uint8_t channel;        // 通道号 [0-15]
    uint32_t sample_rate;   // 采样率(Hz) [1K-1M]
    uint8_t resolution;     // 分辨率(bit) [8/10/12]
} adc_config_t;

adc_config_t g_st_adc_config;''',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'name': 'UART配置模板',
                'category': '外设配置',
                'description': 'UART串口配置结构',
                'code': '''typedef struct {
    uint32_t baud_rate;     // 波特率 [9600-115200]
    uint8_t data_bits;      // 数据位 [5-8]
    uint8_t stop_bits;      // 停止位 [1-2]
    uint8_t parity;         // 校验位 [0:无, 1:奇, 2:偶]
} uart_config_t;

uart_config_t g_st_uart_config;''',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'name': 'PID控制器模板',
                'category': '算法',
                'description': 'PID控制器参数结构',
                'code': '''typedef struct {
    float kp;               // 比例系数
    float ki;               // 积分系数
    float kd;               // 微分系数
    float setpoint;         // 目标值
    float output;           // 输出值
} pid_controller_t;

pid_controller_t g_st_pid_controller;''',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]
    
    def save_templates(self):
        """保存模板列表"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
            
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存模板失败: {str(e)}")
    
    def refresh_template_list(self):
        """刷新模板列表显示"""
        self.template_list.clear()
        
        for i, template in enumerate(self.templates):
            item = QListWidgetItem(f"📄 {template['name']}")
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.template_list.addItem(item)
    
    def add_template(self):
        """新建模板"""
        dialog = TemplateDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            template = dialog.get_template()
            
            if not template['name']:
                QMessageBox.warning(self, "提示", "请输入模板名称")
                return
            
            self.templates.append(template)
            self.save_templates()
            self.refresh_template_list()
            QMessageBox.information(self, "成功", "模板已添加")
    
    def edit_template(self):
        """编辑模板"""
        current_item = self.template_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个模板")
            return
        
        index = current_item.data(Qt.ItemDataRole.UserRole)
        template = self.templates[index]
        
        dialog = TemplateDialog(self, template)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_template = dialog.get_template()
            self.templates[index] = updated_template
            self.save_templates()
            self.refresh_template_list()
            QMessageBox.information(self, "成功", "模板已更新")
    
    def view_selected_template(self):
        """查看选中的模板"""
        current_item = self.template_list.currentItem()
        if current_item:
            self.view_template(current_item)
    
    def view_template(self, item):
        """查看模板详情"""
        index = item.data(Qt.ItemDataRole.UserRole)
        template = self.templates[index]
        
        html = f"""
<h3>{template['name']}</h3>
<p><b>分类:</b> {template.get('category', '未分类')}</p>
<p><b>描述:</b> {template.get('description', '无描述')}</p>
<p><b>创建时间:</b> {template.get('created_at', '未知')}</p>
<p><b>更新时间:</b> {template.get('updated_at', '未知')}</p>
<h4>代码内容:</h4>
<pre style="background: #F5F5F7; padding: 16px; border-radius: 8px;">{template.get('code', '')}</pre>
"""
        
        self.preview_display.setHtml(html)
    
    def use_template(self):
        """使用模板"""
        current_item = self.template_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个模板")
            return
        
        index = current_item.data(Qt.ItemDataRole.UserRole)
        template = self.templates[index]
        
        # 复制代码到剪贴板
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(template['code'])
        
        QMessageBox.information(self, "成功", 
            f"模板代码已复制到剪贴板\n\n可以在变量解析面板中粘贴使用")
    
    def delete_template(self):
        """删除模板"""
        current_item = self.template_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个模板")
            return
        
        index = current_item.data(Qt.ItemDataRole.UserRole)
        template = self.templates[index]
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除模板 '{template['name']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.templates.pop(index)
            self.save_templates()
            self.refresh_template_list()
            self.preview_display.clear()
            QMessageBox.information(self, "成功", "模板已删除")
    
    def import_templates(self):
        """导入模板"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入模板", "", "JSON文件 (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported = json.load(f)
                
                if isinstance(imported, list):
                    self.templates.extend(imported)
                    self.save_templates()
                    self.refresh_template_list()
                    QMessageBox.information(self, "成功", f"成功导入 {len(imported)} 个模板")
                else:
                    QMessageBox.warning(self, "错误", "文件格式不正确")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导入失败: {str(e)}")
    
    def export_templates(self):
        """导出模板"""
        if not self.templates:
            QMessageBox.warning(self, "提示", "没有可导出的模板")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出模板", "templates.json", "JSON文件 (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.templates, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "成功", f"已导出 {len(self.templates)} 个模板")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")
