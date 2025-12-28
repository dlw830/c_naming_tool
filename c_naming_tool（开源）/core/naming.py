"""
命名生成器模块
负责根据规则生成C语言变量名
"""

import json
import os
from .type_info import type_info_manager
from .translator import translator


class NamingGenerator:
    """命名生成器"""
    
    def __init__(self):
        """初始化命名生成器"""
        self.modifier_prefixes = {}
        self.struct_prefix = "st"
        self.union_prefix = "un"
        self.enum_prefix = "e"
        self.separator = "_"
        self.load_naming_rules()
    
    def load_naming_rules(self):
        """加载命名规则配置"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'settings.json'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                naming_rules = data.get('naming_rules', {})
                self.modifier_prefixes = naming_rules.get('modifier_prefixes', {})
                self.struct_prefix = naming_rules.get('struct_prefix', 'st')
                self.union_prefix = naming_rules.get('union_prefix', 'un')
                self.enum_prefix = naming_rules.get('enum_prefix', 'e')
                self.separator = naming_rules.get('separator', '_')
        except Exception as e:
            print(f"加载命名规则失败: {e}")
    
    def generate_variable_name(self, modifier, var_type, module, purpose, is_array=False):
        """
        生成变量名
        
        Args:
            modifier: 修饰类型（全局变量/静态变量/局部变量等）
            var_type: 变量类型（uint16_t等）
            module: 功能模块（可以是中文或英文）
            purpose: 使用目的（可以是中文或英文）
            is_array: 是否为数组
            
        Returns:
            dict: 生成的变量名及相关信息
        """
        parts = []
        
        # 1. 添加修饰前缀
        modifier_prefix = self.modifier_prefixes.get(modifier, '')
        if modifier_prefix:
            parts.append(modifier_prefix)
        
        # 2. 添加类型前缀
        type_prefix = type_info_manager.get_type_prefix(var_type, is_array)
        if type_prefix:
            parts.append(type_prefix)
        
        # 3. 翻译并添加功能模块
        if module:
            module_en = translator.translate(module)
            parts.append(module_en['primary'])
        
        # 4. 翻译并添加使用目的
        if purpose:
            purpose_en = translator.translate(purpose)
            parts.append(purpose_en['primary'])
        
        # 5. 组合成完整变量名
        variable_name = self.separator.join(parts)
        
        # 6. 生成命名解析
        naming_breakdown = self._generate_naming_breakdown(
            modifier, var_type, module, purpose, is_array
        )
        
        return {
            'name': variable_name,
            'breakdown': naming_breakdown,
            'parts': parts
        }
    
    def generate_array_name(self, modifier, element_type, module, purpose, array_size):
        """
        生成数组名
        
        Args:
            modifier: 修饰类型
            element_type: 元素类型
            module: 功能模块
            purpose: 使用目的
            array_size: 数组大小
            
        Returns:
            dict: 生成的数组名及相关信息
        """
        result = self.generate_variable_name(
            modifier, element_type, module, purpose, is_array=True
        )
        
        # 添加数组特定信息
        result['array_size'] = array_size
        result['element_type'] = element_type
        
        return result
    
    def generate_struct_name(self, struct_name):
        """
        生成结构体类型名
        
        Args:
            struct_name: 结构体名称（可以是中文或英文）
            
        Returns:
            str: 结构体类型名
        """
        # 翻译结构体名称
        name_en = translator.translate(struct_name)
        
        # 添加 _t 后缀
        return f"{name_en['primary']}_t"
    
    def generate_struct_variable_name(self, modifier, struct_type_name, module, purpose):
        """
        生成结构体变量名
        
        Args:
            modifier: 修饰类型
            struct_type_name: 结构体类型名（不含_t后缀）
            module: 功能模块
            purpose: 使用目的
            
        Returns:
            dict: 生成的结构体变量名及相关信息
        """
        parts = []
        
        # 1. 添加修饰前缀
        modifier_prefix = self.modifier_prefixes.get(modifier, '')
        if modifier_prefix:
            parts.append(modifier_prefix)
        
        # 2. 添加结构体前缀
        parts.append(self.struct_prefix)
        
        # 3. 翻译并添加功能模块（如果提供）
        if module:
            module_en = translator.translate(module)
            parts.append(module_en['primary'])
        
        # 4. 如果没有提供模块，使用结构体类型名
        if not module:
            type_en = translator.translate(struct_type_name)
            parts.append(type_en['primary'])
        
        # 5. 翻译并添加使用目的（如果提供）
        if purpose:
            purpose_en = translator.translate(purpose)
            parts.append(purpose_en['primary'])
        
        variable_name = self.separator.join(parts)
        
        return {
            'name': variable_name,
            'struct_type': f"{struct_type_name}_t",
            'parts': parts
        }
    
    def generate_enum_name(self, enum_name):
        """
        生成枚举类型名
        
        Args:
            enum_name: 枚举名称（可以是中文或英文）
            
        Returns:
            str: 枚举类型名
        """
        # 翻译枚举名称
        name_en = translator.translate(enum_name)
        
        # 添加 _e 后缀
        return f"{name_en['primary']}_e"
    
    def generate_union_name(self, union_name):
        """
        生成联合体类型名
        
        Args:
            union_name: 联合体名称（可以是中文或英文）
            
        Returns:
            str: 联合体类型名
        """
        # 翻译联合体名称
        name_en = translator.translate(union_name)
        
        # 添加 _u 后缀
        return f"{name_en['primary']}_u"
    
    def _generate_naming_breakdown(self, modifier, var_type, module, purpose, is_array):
        """
        生成命名解析说明
        
        Returns:
            list: 命名解析列表
        """
        breakdown = []
        
        # 修饰符
        modifier_prefix = self.modifier_prefixes.get(modifier, '')
        if modifier_prefix:
            modifier_desc = {
                'g': '全局变量 (Global)',
                's': '静态变量 (Static)',
                'c': '常量 (Constant)',
                'v': 'Volatile变量'
            }.get(modifier_prefix, modifier)
            
            breakdown.append({
                'part': modifier_prefix,
                'description': modifier_desc
            })
        
        # 类型前缀
        type_prefix = type_info_manager.get_type_prefix(var_type, is_array)
        if type_prefix:
            type_desc = f"{var_type}"
            if is_array:
                type_desc += " 数组"
            
            type_info = type_info_manager.get_type_info(var_type)
            if type_info:
                range_str = type_info_manager.get_range_str(var_type)
                type_desc += f" ({range_str})"
            
            breakdown.append({
                'part': type_prefix,
                'description': type_desc
            })
        
        # 功能模块
        if module:
            module_en = translator.translate(module)
            breakdown.append({
                'part': module_en['primary'],
                'description': f"功能模块: {module}"
            })
        
        # 使用目的
        if purpose:
            purpose_en = translator.translate(purpose)
            breakdown.append({
                'part': purpose_en['primary'],
                'description': f"使用目的: {purpose}"
            })
        
        return breakdown
    
    def validate_name(self, name):
        """
        验证变量名是否符合C语言命名规范
        
        Args:
            name: 变量名
            
        Returns:
            dict: 验证结果
        """
        issues = []
        
        # 检查是否为空
        if not name:
            issues.append("变量名不能为空")
            return {'valid': False, 'issues': issues}
        
        # 检查首字符是否为字母或下划线
        if not (name[0].isalpha() or name[0] == '_'):
            issues.append("变量名必须以字母或下划线开头")
        
        # 检查是否只包含字母、数字和下划线
        if not all(c.isalnum() or c == '_' for c in name):
            issues.append("变量名只能包含字母、数字和下划线")
        
        # 检查是否为C语言关键字
        c_keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'int', 'long', 'register', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
            'unsigned', 'void', 'volatile', 'while'
        ]
        
        if name.lower() in c_keywords:
            issues.append(f"'{name}' 是C语言关键字，不能用作变量名")
        
        # 检查长度
        if len(name) > 63:
            issues.append("变量名过长，建议不超过63个字符")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }


# 全局实例
naming_generator = NamingGenerator()
