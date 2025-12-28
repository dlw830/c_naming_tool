"""
类型信息管理模块
负责管理C语言数据类型的信息，包括取值范围、内存大小等
"""

import json
import os


class TypeInfo:
    """类型信息管理类"""
    
    def __init__(self):
        """初始化类型信息"""
        self.type_ranges = {}
        self.type_prefixes = {}
        self.array_prefixes = {}
        self.load_type_data()
    
    def load_type_data(self):
        """从配置文件加载类型数据"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'type_ranges.json'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.type_ranges = data.get('type_ranges', {})
                self.type_prefixes = data.get('type_prefixes', {})
                self.array_prefixes = data.get('array_prefixes', {})
        except Exception as e:
            print(f"加载类型数据失败: {e}")
    
    def get_type_info(self, type_name):
        """
        获取指定类型的详细信息
        
        Args:
            type_name: 类型名称，如 'uint16_t'
            
        Returns:
            dict: 类型信息字典
        """
        return self.type_ranges.get(type_name, {})
    
    def get_type_prefix(self, type_name, is_array=False):
        """
        获取类型前缀
        
        Args:
            type_name: 类型名称
            is_array: 是否为数组
            
        Returns:
            str: 类型前缀
        """
        if is_array:
            return self.array_prefixes.get(type_name, 'a')
        return self.type_prefixes.get(type_name, '')
    
    def get_range_str(self, type_name):
        """
        获取类型的取值范围字符串
        
        Args:
            type_name: 类型名称
            
        Returns:
            str: 取值范围字符串
        """
        info = self.get_type_info(type_name)
        if not info:
            return "未知范围"
        
        if 'min' in info and 'max' in info:
            min_val = info['min']
            max_val = info['max']
            
            # 格式化大数字，添加千位分隔符
            if isinstance(min_val, int) and isinstance(max_val, int):
                if abs(min_val) > 999 or abs(max_val) > 999:
                    return f"{min_val:,} ~ {max_val:,}"
                return f"{min_val} ~ {max_val}"
            else:
                # 浮点数使用科学计数法
                return f"{min_val:.6e} ~ {max_val:.6e}"
        
        return "未知范围"
    
    def get_memory_size(self, type_name, array_size=None):
        """
        计算内存占用大小
        
        Args:
            type_name: 类型名称
            array_size: 数组大小（如果是数组）
            
        Returns:
            tuple: (字节数, 格式化字符串)
        """
        info = self.get_type_info(type_name)
        if not info:
            return (0, "未知")
        
        bytes_per_element = info.get('bytes', 0)
        
        if array_size:
            total_bytes = bytes_per_element * array_size
        else:
            total_bytes = bytes_per_element
        
        # 格式化输出
        if total_bytes < 1024:
            return (total_bytes, f"{total_bytes} bytes")
        elif total_bytes < 1024 * 1024:
            kb = total_bytes / 1024
            return (total_bytes, f"{total_bytes} bytes ({kb:.4f} KB)")
        else:
            mb = total_bytes / (1024 * 1024)
            return (total_bytes, f"{total_bytes} bytes ({mb:.4f} MB)")
    
    def get_all_types(self):
        """获取所有可用的类型列表"""
        return list(self.type_ranges.keys())
    
    def is_float_type(self, type_name):
        """判断是否为浮点类型"""
        return type_name in ['float', 'double']
    
    def is_signed_type(self, type_name):
        """判断是否为有符号类型"""
        info = self.get_type_info(type_name)
        return info.get('signed', False)
    
    def get_type_description(self, type_name):
        """获取类型描述"""
        info = self.get_type_info(type_name)
        return info.get('description', '')
    
    def get_type_notes(self, type_name):
        """获取类型注意事项"""
        info = self.get_type_info(type_name)
        return info.get('notes', [])
    
    def format_type_display(self, type_name):
        """
        格式化类型显示信息（用于UI展示）
        
        Returns:
            dict: 格式化后的显示信息
        """
        info = self.get_type_info(type_name)
        if not info:
            return {
                'type': type_name,
                'description': '未知类型',
                'range': '未知',
                'bytes': 0,
                'notes': []
            }
        
        display_info = {
            'type': type_name,
            'description': info.get('description', ''),
            'range': self.get_range_str(type_name),
            'bytes': info.get('bytes', 0),
            'signed': info.get('signed', False),
            'notes': info.get('notes', [])
        }
        
        # 浮点类型的额外信息
        if self.is_float_type(type_name):
            display_info['precision'] = info.get('precision', 0)
            display_info['decimal_places'] = info.get('decimal_places', '')
            if 'min_positive' in info:
                display_info['min_positive'] = f"{info['min_positive']:.6e}"
        
        return display_info


# 全局实例
type_info_manager = TypeInfo()
