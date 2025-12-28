"""
Core模块
包含命名生成、翻译、类型信息等核心功能
"""

from .naming import naming_generator
from .translator import translator
from .type_info import type_info_manager

__all__ = ['naming_generator', 'translator', 'type_info_manager']
