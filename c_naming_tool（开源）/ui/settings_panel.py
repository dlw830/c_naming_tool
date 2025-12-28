"""
设置面板
"""

import json
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QComboBox, QCheckBox, QLineEdit,
    QPushButton, QMessageBox, QScrollArea, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class SettingsPanel(QWidget):
    """设置面板"""
    
    # 设置变更信号
    settings_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.settings_file = os.path.join('c_naming_tool', 'config', 'app_settings.json')
        self.settings = {}
        self.init_ui()
        self.load_settings()
    
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
        title = QLabel("⚙️ 设置")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        hint = QLabel("配置工具的行为和外观")
        hint.setProperty("class", "hint")
        layout.addWidget(hint)
        
        # 命名规则预设
        preset_group = QGroupBox("📋 命名规则预设")
        preset_layout = QVBoxLayout(preset_group)
        
        preset_select_layout = QHBoxLayout()
        preset_select_layout.addWidget(QLabel("选择预设:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            '自定义', 'Linux内核风格', 'Google C++风格', 
            'Hungarian命名法', '嵌入式通用'
        ])
        self.preset_combo.currentTextChanged.connect(self.apply_preset)
        preset_select_layout.addWidget(self.preset_combo)
        preset_select_layout.addStretch()
        preset_layout.addLayout(preset_select_layout)
        
        layout.addWidget(preset_group)
        
        # 命名规则设置
        naming_group = QGroupBox("📝 命名规则详细设置")
        naming_layout = QVBoxLayout(naming_group)
        
        # 变量类型前缀配置
        var_prefix_label = QLabel("变量类型前缀:")
        var_prefix_label.setProperty("class", "subtitle")
        naming_layout.addWidget(var_prefix_label)
        
        # 全局变量前缀
        global_prefix_layout = QHBoxLayout()
        global_prefix_layout.addWidget(QLabel("全局变量:"))
        self.global_prefix_edit = QLineEdit()
        self.global_prefix_edit.setPlaceholderText("g_")
        global_prefix_layout.addWidget(self.global_prefix_edit)
        
        self.global_suffix_edit = QLineEdit()
        self.global_suffix_edit.setPlaceholderText("后缀(可选)")
        global_prefix_layout.addWidget(self.global_suffix_edit)
        global_prefix_layout.addStretch()
        naming_layout.addLayout(global_prefix_layout)
        
        # 静态变量前缀
        static_prefix_layout = QHBoxLayout()
        static_prefix_layout.addWidget(QLabel("静态变量:"))
        self.static_prefix_edit = QLineEdit()
        self.static_prefix_edit.setPlaceholderText("s_")
        static_prefix_layout.addWidget(self.static_prefix_edit)
        
        self.static_suffix_edit = QLineEdit()
        self.static_suffix_edit.setPlaceholderText("后缀(可选)")
        static_prefix_layout.addWidget(self.static_suffix_edit)
        static_prefix_layout.addStretch()
        naming_layout.addLayout(static_prefix_layout)
        
        # 局部变量前缀
        local_prefix_layout = QHBoxLayout()
        local_prefix_layout.addWidget(QLabel("局部变量:"))
        self.local_prefix_edit = QLineEdit()
        self.local_prefix_edit.setPlaceholderText("l_")
        local_prefix_layout.addWidget(self.local_prefix_edit)
        
        self.local_suffix_edit = QLineEdit()
        self.local_suffix_edit.setPlaceholderText("后缀(可选)")
        local_prefix_layout.addWidget(self.local_suffix_edit)
        local_prefix_layout.addStretch()
        naming_layout.addLayout(local_prefix_layout)
        
        # 结构体前缀
        struct_prefix_layout = QHBoxLayout()
        struct_prefix_layout.addWidget(QLabel("结构体:"))
        self.struct_prefix_edit = QLineEdit()
        self.struct_prefix_edit.setPlaceholderText("st_")
        struct_prefix_layout.addWidget(self.struct_prefix_edit)
        
        self.struct_suffix_edit = QLineEdit()
        self.struct_suffix_edit.setPlaceholderText("后缀(可选)")
        struct_prefix_layout.addWidget(self.struct_suffix_edit)
        struct_prefix_layout.addStretch()
        naming_layout.addLayout(struct_prefix_layout)
        
        # 联合体前缀
        union_prefix_layout = QHBoxLayout()
        union_prefix_layout.addWidget(QLabel("联合体:"))
        self.union_prefix_edit = QLineEdit()
        self.union_prefix_edit.setPlaceholderText("un_")
        union_prefix_layout.addWidget(self.union_prefix_edit)
        
        self.union_suffix_edit = QLineEdit()
        self.union_suffix_edit.setPlaceholderText("后缀(可选)")
        union_prefix_layout.addWidget(self.union_suffix_edit)
        union_prefix_layout.addStretch()
        naming_layout.addLayout(union_prefix_layout)
        
        # 枚举前缀
        enum_prefix_layout = QHBoxLayout()
        enum_prefix_layout.addWidget(QLabel("枚举:"))
        self.enum_prefix_edit = QLineEdit()
        self.enum_prefix_edit.setPlaceholderText("e_")
        enum_prefix_layout.addWidget(self.enum_prefix_edit)
        
        self.enum_suffix_edit = QLineEdit()
        self.enum_suffix_edit.setPlaceholderText("后缀(可选)")
        enum_prefix_layout.addWidget(self.enum_suffix_edit)
        enum_prefix_layout.addStretch()
        naming_layout.addLayout(enum_prefix_layout)
        
        # 数组前缀
        array_prefix_layout = QHBoxLayout()
        array_prefix_layout.addWidget(QLabel("数组:"))
        self.array_prefix_edit = QLineEdit()
        self.array_prefix_edit.setPlaceholderText("a_")
        array_prefix_layout.addWidget(self.array_prefix_edit)
        
        self.array_suffix_edit = QLineEdit()
        self.array_suffix_edit.setPlaceholderText("后缀(可选)")
        array_prefix_layout.addWidget(self.array_suffix_edit)
        array_prefix_layout.addStretch()
        naming_layout.addLayout(array_prefix_layout)
        
        # 指针前缀
        pointer_prefix_layout = QHBoxLayout()
        pointer_prefix_layout.addWidget(QLabel("指针:"))
        self.pointer_prefix_edit = QLineEdit()
        self.pointer_prefix_edit.setPlaceholderText("p_")
        pointer_prefix_layout.addWidget(self.pointer_prefix_edit)
        
        self.pointer_suffix_edit = QLineEdit()
        self.pointer_suffix_edit.setPlaceholderText("后缀(可选)")
        pointer_prefix_layout.addWidget(self.pointer_suffix_edit)
        pointer_prefix_layout.addStretch()
        naming_layout.addLayout(pointer_prefix_layout)
        
        # 函数前缀
        function_prefix_layout = QHBoxLayout()
        function_prefix_layout.addWidget(QLabel("函数:"))
        self.function_prefix_edit = QLineEdit()
        self.function_prefix_edit.setPlaceholderText("前缀(可选)")
        function_prefix_layout.addWidget(self.function_prefix_edit)
        
        self.function_suffix_edit = QLineEdit()
        self.function_suffix_edit.setPlaceholderText("后缀(可选)")
        function_prefix_layout.addWidget(self.function_suffix_edit)
        function_prefix_layout.addStretch()
        naming_layout.addLayout(function_prefix_layout)
        
        # 类型前缀设置
        type_prefix_label = QLabel("类型前缀设置:")
        type_prefix_label.setProperty("class", "subtitle")
        naming_layout.addWidget(type_prefix_label)
        
        # uint8_t前缀
        uint8_prefix_layout = QHBoxLayout()
        uint8_prefix_layout.addWidget(QLabel("uint8_t:"))
        self.uint8_prefix_edit = QLineEdit()
        self.uint8_prefix_edit.setPlaceholderText("u8_ 或 b_ (可选)")
        uint8_prefix_layout.addWidget(self.uint8_prefix_edit)
        uint8_prefix_layout.addStretch()
        naming_layout.addLayout(uint8_prefix_layout)
        
        # uint16_t前缀
        uint16_prefix_layout = QHBoxLayout()
        uint16_prefix_layout.addWidget(QLabel("uint16_t:"))
        self.uint16_prefix_edit = QLineEdit()
        self.uint16_prefix_edit.setPlaceholderText("u16_ 或 w_ (可选)")
        uint16_prefix_layout.addWidget(self.uint16_prefix_edit)
        uint16_prefix_layout.addStretch()
        naming_layout.addLayout(uint16_prefix_layout)
        
        # uint32_t前缀
        uint32_prefix_layout = QHBoxLayout()
        uint32_prefix_layout.addWidget(QLabel("uint32_t:"))
        self.uint32_prefix_edit = QLineEdit()
        self.uint32_prefix_edit.setPlaceholderText("u32_ 或 dw_ (可选)")
        uint32_prefix_layout.addWidget(self.uint32_prefix_edit)
        uint32_prefix_layout.addStretch()
        naming_layout.addLayout(uint32_prefix_layout)
        
        # 命名风格
        style_label = QLabel("命名风格设置:")
        style_label.setProperty("class", "subtitle")
        naming_layout.addWidget(style_label)
        
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("命名分隔符:"))
        self.naming_style_combo = QComboBox()
        self.naming_style_combo.addItems(['下划线 (_)', '驼峰命名 (camelCase)', '帕斯卡 (PascalCase)'])
        style_layout.addWidget(self.naming_style_combo)
        style_layout.addStretch()
        naming_layout.addLayout(style_layout)
        
        # 大小写风格
        case_layout = QHBoxLayout()
        case_layout.addWidget(QLabel("变量名大小写:"))
        self.case_combo = QComboBox()
        self.case_combo.addItems(['全小写', '全大写', '首字母大写'])
        case_layout.addWidget(self.case_combo)
        case_layout.addStretch()
        naming_layout.addLayout(case_layout)
        
        # 常量命名
        const_case_layout = QHBoxLayout()
        const_case_layout.addWidget(QLabel("常量命名:"))
        self.const_case_combo = QComboBox()
        self.const_case_combo.addItems(['全大写+下划线', '全小写+下划线', 'k前缀+驼峰'])
        const_case_layout.addWidget(self.const_case_combo)
        const_case_layout.addStretch()
        naming_layout.addLayout(const_case_layout)
        
        # 宏命名
        macro_case_layout = QHBoxLayout()
        macro_case_layout.addWidget(QLabel("宏命名:"))
        self.macro_case_combo = QComboBox()
        self.macro_case_combo.addItems(['全大写+下划线', '全小写+下划线'])
        macro_case_layout.addWidget(self.macro_case_combo)
        macro_case_layout.addStretch()
        naming_layout.addLayout(macro_case_layout)
        
        # 命名选项
        naming_options_label = QLabel("命名选项:")
        naming_options_label.setProperty("class", "subtitle")
        naming_layout.addWidget(naming_options_label)
        
        self.use_type_prefix_check = QCheckBox("启用数据类型前缀 (Hungarian风格)")
        naming_layout.addWidget(self.use_type_prefix_check)
        
        self.use_scope_prefix_check = QCheckBox("启用作用域前缀 (g_/s_/l_)")
        self.use_scope_prefix_check.setChecked(True)
        naming_layout.addWidget(self.use_scope_prefix_check)
        
        self.use_module_prefix_check = QCheckBox("启用模块前缀")
        naming_layout.addWidget(self.use_module_prefix_check)
        
        # 模块前缀设置
        module_prefix_layout = QHBoxLayout()
        module_prefix_layout.addWidget(QLabel("  模块前缀:"))
        self.module_prefix_edit = QLineEdit()
        self.module_prefix_edit.setPlaceholderText("例如: UART_")
        module_prefix_layout.addWidget(self.module_prefix_edit)
        module_prefix_layout.addStretch()
        naming_layout.addLayout(module_prefix_layout)
        
        layout.addWidget(naming_group)
        
        # 代码生成设置
        codegen_group = QGroupBox("🔧 代码生成")
        codegen_layout = QVBoxLayout(codegen_group)
        
        # 注释语言
        comment_lang_layout = QHBoxLayout()
        comment_lang_layout.addWidget(QLabel("注释语言:"))
        self.comment_lang_combo = QComboBox()
        self.comment_lang_combo.addItems(['中文', '英文', '中英双语'])
        comment_lang_layout.addWidget(self.comment_lang_combo)
        comment_lang_layout.addStretch()
        codegen_layout.addLayout(comment_lang_layout)
        
        # 缩进方式
        indent_layout = QHBoxLayout()
        indent_layout.addWidget(QLabel("缩进方式:"))
        self.indent_combo = QComboBox()
        self.indent_combo.addItems(['4空格', '2空格', 'Tab'])
        indent_layout.addWidget(self.indent_combo)
        indent_layout.addStretch()
        codegen_layout.addLayout(indent_layout)
        
        # 生成选项
        self.include_range_check = QCheckBox("包含范围注释")
        self.include_range_check.setChecked(True)
        codegen_layout.addWidget(self.include_range_check)
        
        self.include_naming_breakdown_check = QCheckBox("包含命名解析注释")
        self.include_naming_breakdown_check.setChecked(True)
        codegen_layout.addWidget(self.include_naming_breakdown_check)
        
        self.include_memory_layout_check = QCheckBox("包含内存布局注释")
        self.include_memory_layout_check.setChecked(True)
        codegen_layout.addWidget(self.include_memory_layout_check)
        
        self.auto_align_check = QCheckBox("自动对齐注释")
        self.auto_align_check.setChecked(True)
        codegen_layout.addWidget(self.auto_align_check)
        
        layout.addWidget(codegen_group)
        
        # 界面设置
        ui_group = QGroupBox("🎨 界面")
        ui_layout = QVBoxLayout(ui_group)
        
        # 主题
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("主题:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['浅色', '深色', '跟随系统'])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        ui_layout.addLayout(theme_layout)
        
        # 字体大小
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("字体大小:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 20)
        self.font_size_spin.setValue(13)
        self.font_size_spin.setSuffix(" pt")
        font_size_layout.addWidget(self.font_size_spin)
        font_size_layout.addStretch()
        ui_layout.addLayout(font_size_layout)
        
        # 代码字体大小
        code_font_layout = QHBoxLayout()
        code_font_layout.addWidget(QLabel("代码字体大小:"))
        self.code_font_spin = QSpinBox()
        self.code_font_spin.setRange(10, 18)
        self.code_font_spin.setValue(12)
        self.code_font_spin.setSuffix(" pt")
        code_font_layout.addWidget(self.code_font_spin)
        code_font_layout.addStretch()
        ui_layout.addLayout(code_font_layout)
        
        # 语言
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("界面语言:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['简体中文', 'English'])
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        ui_layout.addLayout(lang_layout)
        
        layout.addWidget(ui_group)
        
        # 翻译设置
        translation_group = QGroupBox("🌐 翻译")
        translation_layout = QVBoxLayout(translation_group)
        
        # 翻译引擎
        engine_layout = QHBoxLayout()
        engine_layout.addWidget(QLabel("翻译引擎:"))
        self.translation_engine_combo = QComboBox()
        self.translation_engine_combo.addItems(['本地词库', '在线API (开发中)'])
        engine_layout.addWidget(self.translation_engine_combo)
        engine_layout.addStretch()
        translation_layout.addLayout(engine_layout)
        
        # 翻译选项
        self.auto_translate_check = QCheckBox("自动翻译中文输入")
        self.auto_translate_check.setChecked(True)
        translation_layout.addWidget(self.auto_translate_check)
        
        self.show_pinyin_check = QCheckBox("显示拼音提示")
        self.show_pinyin_check.setChecked(True)
        translation_layout.addWidget(self.show_pinyin_check)
        
        layout.addWidget(translation_group)
        
        # 高级设置
        advanced_group = QGroupBox("🔬 高级")
        advanced_layout = QVBoxLayout(advanced_group)
        
        # 最大数组大小
        max_array_layout = QHBoxLayout()
        max_array_layout.addWidget(QLabel("最大数组大小:"))
        self.max_array_spin = QSpinBox()
        self.max_array_spin.setRange(100, 1000000)
        self.max_array_spin.setValue(65535)
        max_array_layout.addWidget(self.max_array_spin)
        max_array_layout.addStretch()
        advanced_layout.addLayout(max_array_layout)
        
        # 结构体对齐
        align_layout = QHBoxLayout()
        align_layout.addWidget(QLabel("默认结构体对齐:"))
        self.struct_align_combo = QComboBox()
        self.struct_align_combo.addItems(['1字节', '4字节', '8字节', '自然对齐'])
        align_layout.addWidget(self.struct_align_combo)
        align_layout.addStretch()
        advanced_layout.addLayout(align_layout)
        
        # 调试选项
        self.debug_mode_check = QCheckBox("启用调试模式")
        advanced_layout.addWidget(self.debug_mode_check)
        
        self.auto_save_check = QCheckBox("自动保存设置")
        self.auto_save_check.setChecked(True)
        advanced_layout.addWidget(self.auto_save_check)
        
        layout.addWidget(advanced_group)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存设置")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 恢复默认")
        reset_btn.clicked.connect(self.reset_to_defaults)
        btn_layout.addWidget(reset_btn)
        
        export_btn = QPushButton("📤 导出设置")
        export_btn.clicked.connect(self.export_settings)
        btn_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 导入设置")
        import_btn.clicked.connect(self.import_settings)
        btn_layout.addWidget(import_btn)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        # 将内容部件设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.get_default_settings()
            
            self.apply_settings_to_ui()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载设置失败: {str(e)}")
            self.settings = self.get_default_settings()
            self.apply_settings_to_ui()
    
    def get_default_settings(self):
        """获取默认设置"""
        return {
            'preset': '自定义',
            'naming': {
                'global_prefix': 'g_',
                'global_suffix': '',
                'static_prefix': 's_',
                'static_suffix': '',
                'local_prefix': 'l_',
                'local_suffix': '',
                'struct_prefix': 'st_',
                'struct_suffix': '',
                'union_prefix': 'un_',
                'union_suffix': '',
                'enum_prefix': 'e_',
                'enum_suffix': '',
                'array_prefix': 'a_',
                'array_suffix': '',
                'pointer_prefix': 'p_',
                'pointer_suffix': '',
                'function_prefix': '',
                'function_suffix': '',
                'uint8_prefix': '',
                'uint16_prefix': '',
                'uint32_prefix': '',
                'style': '下划线 (_)',
                'case': '全小写',
                'const_case': '全大写+下划线',
                'macro_case': '全大写+下划线',
                'use_type_prefix': False,
                'use_scope_prefix': True,
                'use_module_prefix': False,
                'module_prefix': ''
            },
            'codegen': {
                'comment_lang': '中文',
                'indent': '4空格',
                'include_range': True,
                'include_naming': True,
                'include_memory': True,
                'auto_align': True
            },
            'ui': {
                'theme': '浅色',
                'font_size': 13,
                'code_font_size': 12,
                'language': '简体中文'
            },
            'translation': {
                'engine': '本地词库',
                'auto_translate': True,
                'show_pinyin': True
            },
            'advanced': {
                'max_array_size': 65535,
                'struct_align': '自然对齐',
                'debug_mode': False,
                'auto_save': True
            }
        }
    
    def apply_settings_to_ui(self):
        """将设置应用到UI控件"""
        # 预设
        preset = self.settings.get('preset', '自定义')
        self.preset_combo.setCurrentText(preset)
        
        # 命名规则
        naming = self.settings.get('naming', {})
        self.global_prefix_edit.setText(naming.get('global_prefix', 'g_'))
        self.global_suffix_edit.setText(naming.get('global_suffix', ''))
        self.static_prefix_edit.setText(naming.get('static_prefix', 's_'))
        self.static_suffix_edit.setText(naming.get('static_suffix', ''))
        self.local_prefix_edit.setText(naming.get('local_prefix', 'l_'))
        self.local_suffix_edit.setText(naming.get('local_suffix', ''))
        self.struct_prefix_edit.setText(naming.get('struct_prefix', 'st_'))
        self.struct_suffix_edit.setText(naming.get('struct_suffix', ''))
        self.union_prefix_edit.setText(naming.get('union_prefix', 'un_'))
        self.union_suffix_edit.setText(naming.get('union_suffix', ''))
        self.enum_prefix_edit.setText(naming.get('enum_prefix', 'e_'))
        self.enum_suffix_edit.setText(naming.get('enum_suffix', ''))
        self.array_prefix_edit.setText(naming.get('array_prefix', 'a_'))
        self.array_suffix_edit.setText(naming.get('array_suffix', ''))
        self.pointer_prefix_edit.setText(naming.get('pointer_prefix', 'p_'))
        self.pointer_suffix_edit.setText(naming.get('pointer_suffix', ''))
        self.function_prefix_edit.setText(naming.get('function_prefix', ''))
        self.function_suffix_edit.setText(naming.get('function_suffix', ''))
        self.uint8_prefix_edit.setText(naming.get('uint8_prefix', ''))
        self.uint16_prefix_edit.setText(naming.get('uint16_prefix', ''))
        self.uint32_prefix_edit.setText(naming.get('uint32_prefix', ''))
        self.naming_style_combo.setCurrentText(naming.get('style', '下划线 (_)'))
        self.case_combo.setCurrentText(naming.get('case', '全小写'))
        self.const_case_combo.setCurrentText(naming.get('const_case', '全大写+下划线'))
        self.macro_case_combo.setCurrentText(naming.get('macro_case', '全大写+下划线'))
        self.use_type_prefix_check.setChecked(naming.get('use_type_prefix', False))
        self.use_scope_prefix_check.setChecked(naming.get('use_scope_prefix', True))
        self.use_module_prefix_check.setChecked(naming.get('use_module_prefix', False))
        self.module_prefix_edit.setText(naming.get('module_prefix', ''))
        
        # 代码生成
        codegen = self.settings.get('codegen', {})
        self.comment_lang_combo.setCurrentText(codegen.get('comment_lang', '中文'))
        self.indent_combo.setCurrentText(codegen.get('indent', '4空格'))
        self.include_range_check.setChecked(codegen.get('include_range', True))
        self.include_naming_breakdown_check.setChecked(codegen.get('include_naming', True))
        self.include_memory_layout_check.setChecked(codegen.get('include_memory', True))
        self.auto_align_check.setChecked(codegen.get('auto_align', True))
        
        # 界面
        ui = self.settings.get('ui', {})
        self.theme_combo.setCurrentText(ui.get('theme', '浅色'))
        self.font_size_spin.setValue(ui.get('font_size', 13))
        self.code_font_spin.setValue(ui.get('code_font_size', 12))
        self.lang_combo.setCurrentText(ui.get('language', '简体中文'))
        
        # 翻译
        translation = self.settings.get('translation', {})
        self.translation_engine_combo.setCurrentText(translation.get('engine', '本地词库'))
        self.auto_translate_check.setChecked(translation.get('auto_translate', True))
        self.show_pinyin_check.setChecked(translation.get('show_pinyin', True))
        
        # 高级
        advanced = self.settings.get('advanced', {})
        self.max_array_spin.setValue(advanced.get('max_array_size', 65535))
        self.struct_align_combo.setCurrentText(advanced.get('struct_align', '自然对齐'))
        self.debug_mode_check.setChecked(advanced.get('debug_mode', False))
        self.auto_save_check.setChecked(advanced.get('auto_save', True))
    
    def get_settings_from_ui(self):
        """从UI控件获取设置"""
        return {
            'preset': self.preset_combo.currentText(),
            'naming': {
                'global_prefix': self.global_prefix_edit.text(),
                'global_suffix': self.global_suffix_edit.text(),
                'static_prefix': self.static_prefix_edit.text(),
                'static_suffix': self.static_suffix_edit.text(),
                'local_prefix': self.local_prefix_edit.text(),
                'local_suffix': self.local_suffix_edit.text(),
                'struct_prefix': self.struct_prefix_edit.text(),
                'struct_suffix': self.struct_suffix_edit.text(),
                'union_prefix': self.union_prefix_edit.text(),
                'union_suffix': self.union_suffix_edit.text(),
                'enum_prefix': self.enum_prefix_edit.text(),
                'enum_suffix': self.enum_suffix_edit.text(),
                'array_prefix': self.array_prefix_edit.text(),
                'array_suffix': self.array_suffix_edit.text(),
                'pointer_prefix': self.pointer_prefix_edit.text(),
                'pointer_suffix': self.pointer_suffix_edit.text(),
                'function_prefix': self.function_prefix_edit.text(),
                'function_suffix': self.function_suffix_edit.text(),
                'uint8_prefix': self.uint8_prefix_edit.text(),
                'uint16_prefix': self.uint16_prefix_edit.text(),
                'uint32_prefix': self.uint32_prefix_edit.text(),
                'style': self.naming_style_combo.currentText(),
                'case': self.case_combo.currentText(),
                'const_case': self.const_case_combo.currentText(),
                'macro_case': self.macro_case_combo.currentText(),
                'use_type_prefix': self.use_type_prefix_check.isChecked(),
                'use_scope_prefix': self.use_scope_prefix_check.isChecked(),
                'use_module_prefix': self.use_module_prefix_check.isChecked(),
                'module_prefix': self.module_prefix_edit.text()
            },
            'codegen': {
                'comment_lang': self.comment_lang_combo.currentText(),
                'indent': self.indent_combo.currentText(),
                'include_range': self.include_range_check.isChecked(),
                'include_naming': self.include_naming_breakdown_check.isChecked(),
                'include_memory': self.include_memory_layout_check.isChecked(),
                'auto_align': self.auto_align_check.isChecked()
            },
            'ui': {
                'theme': self.theme_combo.currentText(),
                'font_size': self.font_size_spin.value(),
                'code_font_size': self.code_font_spin.value(),
                'language': self.lang_combo.currentText()
            },
            'translation': {
                'engine': self.translation_engine_combo.currentText(),
                'auto_translate': self.auto_translate_check.isChecked(),
                'show_pinyin': self.show_pinyin_check.isChecked()
            },
            'advanced': {
                'max_array_size': self.max_array_spin.value(),
                'struct_align': self.struct_align_combo.currentText(),
                'debug_mode': self.debug_mode_check.isChecked(),
                'auto_save': self.auto_save_check.isChecked()
            }
        }
    
    def save_settings(self):
        """保存设置"""
        try:
            self.settings = self.get_settings_from_ui()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            
            # 发送设置变更信号
            self.settings_changed.emit(self.settings)
            
            QMessageBox.information(self, "成功", "设置已保存")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存设置失败: {str(e)}")
    
    def reset_to_defaults(self):
        """恢复默认设置"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要恢复默认设置吗？当前设置将丢失。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.settings = self.get_default_settings()
            self.apply_settings_to_ui()
            self.save_settings()
    
    def export_settings(self):
        """导出设置"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出设置", "settings.json", "JSON文件 (*.json)"
        )
        
        if file_path:
            try:
                current_settings = self.get_settings_from_ui()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(current_settings, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "成功", "设置已导出")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")
    
    def import_settings(self):
        """导入设置"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入设置", "", "JSON文件 (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_settings = json.load(f)
                
                self.settings = imported_settings
                self.apply_settings_to_ui()
                self.save_settings()
                
                QMessageBox.information(self, "成功", "设置已导入")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导入失败: {str(e)}")
    
    def apply_preset(self, preset_name):
        """应用预设命名规则"""
        if preset_name == '自定义':
            return
        
        presets = {
            'Linux内核风格': {
                'global_prefix': '',
                'static_prefix': '',
                'local_prefix': '',
                'struct_prefix': '',
                'union_prefix': '',
                'enum_prefix': '',
                'array_prefix': '',
                'pointer_prefix': '',
                'function_prefix': '',
                'style': '下划线 (_)',
                'case': '全小写',
                'const_case': '全大写+下划线',
                'macro_case': '全大写+下划线',
                'use_type_prefix': False,
                'use_scope_prefix': False
            },
            'Google C++风格': {
                'global_prefix': 'g_',
                'static_prefix': 's_',
                'local_prefix': '',
                'struct_prefix': '',
                'union_prefix': '',
                'enum_prefix': '',
                'array_prefix': '',
                'pointer_prefix': '',
                'function_prefix': '',
                'style': '下划线 (_)',
                'case': '全小写',
                'const_case': 'k前缀+驼峰',
                'macro_case': '全大写+下划线',
                'use_type_prefix': False,
                'use_scope_prefix': True
            },
            'Hungarian命名法': {
                'global_prefix': 'g_',
                'static_prefix': 's_',
                'local_prefix': '',
                'struct_prefix': 'st',
                'union_prefix': 'un',
                'enum_prefix': 'e',
                'array_prefix': 'a',
                'pointer_prefix': 'p',
                'function_prefix': 'fn',
                'uint8_prefix': 'b',
                'uint16_prefix': 'w',
                'uint32_prefix': 'dw',
                'style': '驼峰命名 (camelCase)',
                'case': '首字母大写',
                'const_case': 'k前缀+驼峰',
                'macro_case': '全大写+下划线',
                'use_type_prefix': True,
                'use_scope_prefix': True
            },
            '嵌入式通用': {
                'global_prefix': 'g_',
                'static_prefix': 's_',
                'local_prefix': 'l_',
                'struct_prefix': 'st_',
                'union_prefix': 'un_',
                'enum_prefix': 'e_',
                'array_prefix': 'a_',
                'pointer_prefix': 'p_',
                'function_prefix': '',
                'style': '下划线 (_)',
                'case': '全小写',
                'const_case': '全大写+下划线',
                'macro_case': '全大写+下划线',
                'use_type_prefix': False,
                'use_scope_prefix': True
            }
        }
        
        if preset_name in presets:
            preset_config = presets[preset_name]
            
            # 应用预设到UI控件
            self.global_prefix_edit.setText(preset_config.get('global_prefix', ''))
            self.static_prefix_edit.setText(preset_config.get('static_prefix', ''))
            self.local_prefix_edit.setText(preset_config.get('local_prefix', ''))
            self.struct_prefix_edit.setText(preset_config.get('struct_prefix', ''))
            self.union_prefix_edit.setText(preset_config.get('union_prefix', ''))
            self.enum_prefix_edit.setText(preset_config.get('enum_prefix', ''))
            self.array_prefix_edit.setText(preset_config.get('array_prefix', ''))
            self.pointer_prefix_edit.setText(preset_config.get('pointer_prefix', ''))
            self.function_prefix_edit.setText(preset_config.get('function_prefix', ''))
            self.uint8_prefix_edit.setText(preset_config.get('uint8_prefix', ''))
            self.uint16_prefix_edit.setText(preset_config.get('uint16_prefix', ''))
            self.uint32_prefix_edit.setText(preset_config.get('uint32_prefix', ''))
            self.naming_style_combo.setCurrentText(preset_config.get('style', '下划线 (_)'))
            self.case_combo.setCurrentText(preset_config.get('case', '全小写'))
            self.const_case_combo.setCurrentText(preset_config.get('const_case', '全大写+下划线'))
            self.macro_case_combo.setCurrentText(preset_config.get('macro_case', '全大写+下划线'))
            self.use_type_prefix_check.setChecked(preset_config.get('use_type_prefix', False))
            self.use_scope_prefix_check.setChecked(preset_config.get('use_scope_prefix', False))
            
            QMessageBox.information(self, "提示", f"已应用 {preset_name} 预设")
    
    def get_naming_config(self):
        """获取当前命名配置供其他模块使用"""
        naming = self.settings.get('naming', {})
        return {
            'prefixes': {
                'global': naming.get('global_prefix', 'g_'),
                'static': naming.get('static_prefix', 's_'),
                'local': naming.get('local_prefix', 'l_'),
                'struct': naming.get('struct_prefix', 'st_'),
                'union': naming.get('union_prefix', 'un_'),
                'enum': naming.get('enum_prefix', 'e_'),
                'array': naming.get('array_prefix', 'a_'),
                'pointer': naming.get('pointer_prefix', 'p_'),
                'function': naming.get('function_prefix', ''),
                'uint8': naming.get('uint8_prefix', ''),
                'uint16': naming.get('uint16_prefix', ''),
                'uint32': naming.get('uint32_prefix', '')
            },
            'suffixes': {
                'global': naming.get('global_suffix', ''),
                'static': naming.get('static_suffix', ''),
                'local': naming.get('local_suffix', ''),
                'struct': naming.get('struct_suffix', ''),
                'union': naming.get('union_suffix', ''),
                'enum': naming.get('enum_suffix', ''),
                'array': naming.get('array_suffix', ''),
                'pointer': naming.get('pointer_suffix', ''),
                'function': naming.get('function_suffix', '')
            },
            'style': naming.get('style', '下划线 (_)'),
            'case': naming.get('case', '全小写'),
            'const_case': naming.get('const_case', '全大写+下划线'),
            'macro_case': naming.get('macro_case', '全大写+下划线'),
            'use_type_prefix': naming.get('use_type_prefix', False),
            'use_scope_prefix': naming.get('use_scope_prefix', True),
            'use_module_prefix': naming.get('use_module_prefix', False),
            'module_prefix': naming.get('module_prefix', '')
        }
