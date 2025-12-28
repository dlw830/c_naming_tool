"""
变量解析面板
"""

import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QGroupBox, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt
from core.type_info import type_info_manager


class ParserPanel(QWidget):
    """变量解析面板"""
    
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
        title = QLabel("🔍 变量解析器")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        hint = QLabel("粘贴C语言代码，自动解析变量定义、结构体、联合体、枚举等")
        hint.setProperty("class", "hint")
        layout.addWidget(hint)
        
        # 输入区域
        input_group = QGroupBox("📥 输入区域")
        input_layout = QVBoxLayout(input_group)
        
        # 操作按钮
        input_btn_layout = QHBoxLayout()
        paste_btn = QPushButton("📋 粘贴")
        paste_btn.clicked.connect(self.paste_code)
        input_btn_layout.addWidget(paste_btn)
        
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.clicked.connect(self.clear_input)
        input_btn_layout.addWidget(clear_btn)
        
        input_btn_layout.addStretch()
        input_layout.addLayout(input_btn_layout)
        
        # 代码输入框
        self.code_input = QTextEdit()
        self.code_input.setProperty("class", "code")
        self.code_input.setPlaceholderText("""粘贴代码示例:

typedef struct {
    uint8_t channel;
    uint32_t sample_rate;
    uint8_t resolution;
    uint8_t enable;
} adc_config_t;

adc_config_t g_st_adc_config;
uint16_t gu16_temperature_value;
float gfa_calibration_table[10];
""")
        self.code_input.setMinimumHeight(200)
        input_layout.addWidget(self.code_input)
        
        layout.addWidget(input_group)
        
        # 解析按钮
        parse_btn_layout = QHBoxLayout()
        self.parse_btn = QPushButton("🔍 开始解析")
        self.parse_btn.setMinimumHeight(40)
        self.parse_btn.clicked.connect(self.parse_code)
        parse_btn_layout.addWidget(self.parse_btn)
        layout.addLayout(parse_btn_layout)
        
        # 解析结果区域
        result_group = QGroupBox("📊 解析结果")
        result_layout = QVBoxLayout(result_group)
        
        # 结果操作按钮
        result_btn_layout = QHBoxLayout()
        export_btn = QPushButton("📄 导出报告")
        export_btn.clicked.connect(self.export_report)
        result_btn_layout.addWidget(export_btn)
        
        copy_result_btn = QPushButton("📋 复制结果")
        copy_result_btn.clicked.connect(self.copy_result)
        result_btn_layout.addWidget(copy_result_btn)
        
        result_btn_layout.addStretch()
        result_layout.addLayout(result_btn_layout)
        
        # 结果显示
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(400)
        result_layout.addWidget(self.result_display)
        
        layout.addWidget(result_group)
        
        layout.addStretch()
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def paste_code(self):
        """粘贴代码"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        self.code_input.setPlainText(clipboard.text())
    
    def clear_input(self):
        """清空输入"""
        self.code_input.clear()
        self.result_display.clear()
    
    def parse_code(self):
        """解析代码"""
        code = self.code_input.toPlainText().strip()
        
        if not code:
            QMessageBox.warning(self, "提示", "请先输入代码")
            return
        
        # 解析结果
        result_html = "<h2>解析结果</h2>"
        
        # 解析结构体定义
        structs = self.parse_structs(code)
        if structs:
            result_html += "<h3>✅ 识别到结构体定义</h3>"
            for struct in structs:
                result_html += self.format_struct_result(struct)
        
        # 解析联合体定义
        unions = self.parse_unions(code)
        if unions:
            result_html += "<h3>✅ 识别到联合体定义</h3>"
            for union in unions:
                result_html += self.format_union_result(union)
        
        # 解析枚举定义
        enums = self.parse_enums(code)
        if enums:
            result_html += "<h3>✅ 识别到枚举定义</h3>"
            for enum in enums:
                result_html += self.format_enum_result(enum)
        
        # 解析变量定义
        variables = self.parse_variables(code)
        if variables:
            result_html += "<h3>✅ 识别到变量定义</h3>"
            for var in variables:
                result_html += self.format_variable_result(var)
        
        # 优化建议
        suggestions = self.generate_suggestions(structs, variables)
        if suggestions:
            result_html += "<h3>💡 优化建议</h3><ul>"
            for suggestion in suggestions:
                result_html += f"<li>{suggestion}</li>"
            result_html += "</ul>"
        
        self.result_display.setHtml(result_html)
    
    def parse_structs(self, code):
        """解析结构体定义"""
        structs = []
        # 匹配 typedef struct { ... } name_t;
        pattern = r'typedef\s+struct\s*\{([^}]+)\}\s*(\w+)\s*;'
        matches = re.finditer(pattern, code, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            members_text = match.group(1)
            struct_name = match.group(2)
            
            # 解析成员
            members = []
            member_pattern = r'(\w+)\s+(\w+)\s*;'
            for m in re.finditer(member_pattern, members_text):
                member_type = m.group(1)
                member_name = m.group(2)
                members.append({'type': member_type, 'name': member_name})
            
            structs.append({
                'name': struct_name,
                'members': members
            })
        
        return structs
    
    def parse_unions(self, code):
        """解析联合体定义"""
        unions = []
        pattern = r'typedef\s+union\s*\{([^}]+)\}\s*(\w+)\s*;'
        matches = re.finditer(pattern, code, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            members_text = match.group(1)
            union_name = match.group(2)
            
            members = []
            member_pattern = r'(\w+)\s+(\w+)\s*;'
            for m in re.finditer(member_pattern, members_text):
                member_type = m.group(1)
                member_name = m.group(2)
                members.append({'type': member_type, 'name': member_name})
            
            unions.append({
                'name': union_name,
                'members': members
            })
        
        return unions
    
    def parse_enums(self, code):
        """解析枚举定义"""
        enums = []
        pattern = r'typedef\s+enum\s*\{([^}]+)\}\s*(\w+)\s*;'
        matches = re.finditer(pattern, code, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            values_text = match.group(1)
            enum_name = match.group(2)
            
            values = []
            value_pattern = r'(\w+)\s*(?:=\s*(\d+))?\s*,?'
            for v in re.finditer(value_pattern, values_text):
                value_name = v.group(1)
                value_num = v.group(2)
                values.append({'name': value_name, 'value': value_num})
            
            enums.append({
                'name': enum_name,
                'values': values
            })
        
        return enums
    
    def parse_variables(self, code):
        """解析变量定义"""
        variables = []
        # 匹配变量定义
        pattern = r'(?:^|\n)\s*(?:(static|const|volatile)\s+)?(\w+)\s+(\w+)(?:\[(\d+)\])?\s*(?:=\s*[^;]+)?;'
        matches = re.finditer(pattern, code, re.MULTILINE)
        
        for match in matches:
            modifier = match.group(1)
            var_type = match.group(2)
            var_name = match.group(3)
            array_size = match.group(4)
            
            # 跳过结构体、联合体、枚举内部的成员
            variables.append({
                'modifier': modifier,
                'type': var_type,
                'name': var_name,
                'array_size': array_size
            })
        
        return variables
    
    def format_struct_result(self, struct):
        """格式化结构体解析结果"""
        html = f"""
<div style="border: 1px solid #E8E8ED; border-radius: 8px; padding: 16px; margin: 10px 0; background: #FAFAFA;">
    <h4>📋 结构体: {struct['name']}</h4>
    <p><b>成员数量:</b> {len(struct['members'])}</p>
"""
        
        offset = 0
        for i, member in enumerate(struct['members']):
            type_info = type_info_manager.get_type_info(member['type'])
            if type_info:
                range_str = type_info_manager.get_range_str(member['type'])
                bytes_info = type_info.get('bytes', 0)
                
                html += f"""
    <p><b>成员{i+1}:</b> {member['name']}<br>
    • 类型: {member['type']}<br>
    • 大小: {bytes_info} bytes<br>
    • 偏移: {offset}<br>
    • 取值范围: {range_str}</p>
"""
                offset += bytes_info
            else:
                html += f"""
    <p><b>成员{i+1}:</b> {member['name']}<br>
    • 类型: {member['type']}<br>
    • 大小: 未知类型</p>
"""
        
        html += f"""
    <p><b>总大小:</b> 约 {offset} bytes (未考虑对齐)</p>
</div>
"""
        return html
    
    def format_union_result(self, union):
        """格式化联合体解析结果"""
        html = f"""
<div style="border: 1px solid #E8E8ED; border-radius: 8px; padding: 16px; margin: 10px 0; background: #FAFAFA;">
    <h4>🔀 联合体: {union['name']}</h4>
    <p><b>成员数量:</b> {len(union['members'])}</p>
"""
        
        max_size = 0
        for i, member in enumerate(union['members']):
            type_info = type_info_manager.get_type_info(member['type'])
            if type_info:
                bytes_info = type_info.get('bytes', 0)
                max_size = max(max_size, bytes_info)
                html += f"<p><b>成员{i+1}:</b> {member['name']} ({member['type']}, {bytes_info} bytes)</p>"
            else:
                html += f"<p><b>成员{i+1}:</b> {member['name']} ({member['type']})</p>"
        
        html += f"<p><b>联合体大小:</b> {max_size} bytes (最大成员)</p></div>"
        return html
    
    def format_enum_result(self, enum):
        """格式化枚举解析结果"""
        html = f"""
<div style="border: 1px solid #E8E8ED; border-radius: 8px; padding: 16px; margin: 10px 0; background: #FAFAFA;">
    <h4>📋 枚举: {enum['name']}</h4>
    <p><b>枚举值数量:</b> {len(enum['values'])}</p>
"""
        
        for i, value in enumerate(enum['values']):
            if value['value']:
                html += f"<p><b>{i+1}.</b> {value['name']} = {value['value']}</p>"
            else:
                html += f"<p><b>{i+1}.</b> {value['name']}</p>"
        
        html += "</div>"
        return html
    
    def format_variable_result(self, var):
        """格式化变量解析结果"""
        html = f"""
<div style="border: 1px solid #E8E8ED; border-radius: 8px; padding: 16px; margin: 10px 0; background: #FAFAFA;">
    <h4>📌 变量: {var['name']}</h4>
"""
        
        # 解析命名
        name_parts = self.parse_variable_name(var['name'])
        if name_parts:
            html += "<p><b>命名解析:</b></p><ul>"
            for part in name_parts:
                html += f"<li>{part}</li>"
            html += "</ul>"
        
        type_info = type_info_manager.get_type_info(var['type'])
        if type_info:
            range_str = type_info_manager.get_range_str(var['type'])
            bytes_info = type_info.get('bytes', 0)
            
            html += f"""
    <p><b>类型:</b> {var['type']}<br>
    <b>取值范围:</b> {range_str}<br>
    <b>内存占用:</b> {bytes_info} bytes
"""
            
            if var['array_size']:
                total_bytes = bytes_info * int(var['array_size'])
                html += f"<br><b>数组大小:</b> [{var['array_size']}]<br>"
                html += f"<b>总内存:</b> {total_bytes} bytes"
            
            html += "</p>"
        
        html += "</div>"
        return html
    
    def parse_variable_name(self, name):
        """解析变量命名"""
        parts = []
        
        # 解析前缀
        if name.startswith('g'):
            parts.append("g: 全局变量 (Global)")
            name = name[1:]
        elif name.startswith('s'):
            parts.append("s: 静态变量 (Static)")
            name = name[1:]
        
        # 解析类型前缀
        type_prefixes = {
            'u8': 'uint8_t', 'i8': 'int8_t',
            'u16': 'uint16_t', 'i16': 'int16_t',
            'u32': 'uint32_t', 'i32': 'int32_t',
            'u64': 'uint64_t', 'i64': 'int64_t',
            'f': 'float', 'd': 'double',
            'st': '结构体', 'un': '联合体'
        }
        
        for prefix, type_name in type_prefixes.items():
            if name.startswith(prefix + '_'):
                parts.append(f"{prefix}: {type_name}")
                name = name[len(prefix)+1:]
                break
        
        # 剩余部分
        if name:
            parts.append(f"名称: {name}")
        
        return parts
    
    def generate_suggestions(self, structs, variables):
        """生成优化建议"""
        suggestions = []
        
        # 检查结构体
        for struct in structs:
            if len(struct['members']) > 10:
                suggestions.append(f"结构体 {struct['name']} 成员较多({len(struct['members'])}个)，考虑拆分")
        
        # 检查变量命名
        for var in variables:
            if not var['name'].startswith(('g', 's', 'l')):
                suggestions.append(f"变量 {var['name']} 建议添加作用域前缀(g/s/l)")
        
        return suggestions
    
    def export_report(self):
        """导出报告"""
        QMessageBox.information(self, "提示", "导出功能开发中...")
    
    def copy_result(self):
        """复制结果"""
        text = self.result_display.toPlainText()
        if text:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "成功", "结果已复制到剪贴板")
