"""
Translation engine module with pinyin conversion, smart segmentation, multi-strategy translation
"""

import json
import os
import re
from typing import Dict, List, Tuple


class PinyinConverter:
    """Pinyin converter for Chinese characters"""
    
    # Common Chinese character to pinyin mapping (simplified, covering common characters)
    PINYIN_MAP = {
        # Numbers
        '零': 'ling', '一': 'yi', '二': 'er', '三': 'san', '四': 'si',
        '五': 'wu', '六': 'liu', '七': 'qi', '八': 'ba', '九': 'jiu', '十': 'shi',
        
        # Common verbs
        '开': 'kai', '关': 'guan', '启': 'qi', '停': 'ting', '动': 'dong',
        '静': 'jing', '始': 'shi', '终': 'zhong', '入': 'ru', '出': 'chu',
        '上': 'shang', '下': 'xia', '左': 'zuo', '右': 'you', '前': 'qian',
        '后': 'hou', '中': 'zhong', '增': 'zeng', '减': 'jian', '加': 'jia',
        '乘': 'cheng', '除': 'chu', '读': 'du', '写': 'xie',
        '发': 'fa', '收': 'shou', '送': 'song', '接': 'jie', '传': 'chuan',
        '输': 'shu', '存': 'cun', '取': 'qu', '查': 'cha', '检': 'jian',
        '测': 'ce', '试': 'shi', '置': 'zhi', '设': 'she', '配': 'pei',
        
        # Common nouns
        '值': 'value', '数': 'number', '量': 'count', '率': 'rate', '度': 'degree',
        '温': 'temperature', '湿': 'humidity', '压': 'pressure', '速': 'speed',
        '力': 'force', '光': 'light', '声': 'sound', '电': 'electric',
        '流': 'current', '阻': 'resistance', '容': 'capacity',
        '感': 'sensor', '器': 'device', '机': 'machine', '表': 'table',
        '计': 'counter', '时': 'time', '钟': 'clock', '秒': 'second',
        '分': 'minute', '日': 'day', '月': 'month', '年': 'year',
        '位': 'bit', '字': 'word', '节': 'byte', '段': 'segment',
        '块': 'block', '页': 'page', '行': 'line', '列': 'column',
        '队': 'queue', '栈': 'stack', '链': 'link', '树': 'tree',
        '图': 'graph', '网': 'network', '系': 'system', '统': 'system',
        
        # Status adjectives
        '高': 'high', '低': 'low', '大': 'big', '小': 'small',
        '长': 'long', '短': 'short', '宽': 'wide', '窄': 'narrow',
        '快': 'fast', '慢': 'slow', '新': 'new', '旧': 'old',
        '好': 'good', '坏': 'bad', '正': 'positive', '负': 'negative',
        '有': 'has', '无': 'no', '空': 'empty', '满': 'full',
        '真': 'true', '假': 'false', '是': 'yes', '否': 'no',
        '成': 'success', '败': 'fail', '对': 'correct', '错': 'error',
        
        # Colors
        '红': 'red', '橙': 'orange', '黄': 'yellow', '绿': 'green',
        '青': 'cyan', '蓝': 'blue', '紫': 'purple', '黑': 'black',
        '白': 'white', '灰': 'gray',
        
        # Directions
        '东': 'east', '南': 'south', '西': 'west', '北': 'north',
        '内': 'inner', '外': 'outer', '顶': 'top', '底': 'bottom',
        
        # Other common words
        '当': 'dang', '主': 'main', '次': 'sub', '总': 'total',
        '平': 'ping', '均': 'average', '最': 'most', '初': 'init',
        '末': 'end', '首': 'first', '尾': 'last', '单': 'single',
        '双': 'double', '多': 'multi', '少': 'few', '全': 'all',
        '半': 'half', '部': 'part', '整': 'whole', '零': 'zero',
    }
    
    @classmethod
    def to_pinyin(cls, char: str) -> str:
        """Convert single Chinese character to pinyin"""
        return cls.PINYIN_MAP.get(char, char)
    
    @classmethod
    def text_to_pinyin(cls, text: str) -> str:
        """Convert text to pinyin"""
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # is Chinese character
                result.append(cls.to_pinyin(char))
            else:
                result.append(char)
        return '_'.join(result)


class TranslationEngine:
    """Powerful offline translation engine"""
    
    def __init__(self):
        """Initialize translation engine"""
        self.term_db = {}
        self.translation_cache = {}
        self.pinyin_converter = PinyinConverter()
        self.load_term_database()
        self._init_common_patterns()
    
    def _init_common_patterns(self):
        """Initialize common translation patterns"""
        self.common_patterns = [
            # verb+noun pattern
            (r'^(读|写|发送|接收|获取|设置|检测|测量|采集|计算)(.*)', self._translate_verb_noun),
            # adjective+noun pattern
            (r'^(最大|最小|当前|平均|总|初始|默认)(.*)', self._translate_adj_noun),
            # number+unit pattern
            (r'(\d+)(米|秒|度|次|个|位|字节)', self._translate_number_unit),
        ]
    
    def load_term_database(self):
        """Load term database from config file"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'term_database.json'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.term_db = json.load(f)
        except Exception as e:
            print(f"Failed to load term database: {e}")
    
    def translate(self, chinese_text: str, context: str = 'general') -> Dict:
        """
        Powerful multi-strategy translation
        
        Strategy order:
        1. Exact match in term database
        2. Pattern matching (verb+noun, etc.)
        3. Smart segmentation translation
        4. Pinyin fallback
        
        Args:
            chinese_text: Chinese text
            context: Context type
            
        Returns:
            dict: Translation result {
                'primary': main translation,
                'alternatives': alternative translations list,
                'pinyin': pinyin form,
                'confidence': confidence (0-1),
                'source': translation source,
                'parts': segmentation info (if any)
            }
        """
        # Remove whitespace
        chinese_text = chinese_text.strip()
        
        if not chinese_text:
            return {
                'primary': '',
                'alternatives': [],
                'pinyin': '',
                'confidence': 0,
                'source': 'empty'
            }
        
        # Check if already English
        if self._is_english(chinese_text):
            formatted = self._format_for_c_naming(chinese_text)
            return {
                'primary': formatted,
                'alternatives': [],
                'pinyin': formatted,
                'confidence': 1.0,
                'source': 'already_english'
            }
        
        # Check cache
        cache_key = f"{chinese_text}_{context}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        # Strategy 1: Exact match in term database
        result = self._query_term_database(chinese_text, context)
        if result['confidence'] >= 1.0:
            self.translation_cache[cache_key] = result
            return result
        
        # Strategy 2: Pattern matching
        pattern_result = self._try_pattern_match(chinese_text)
        if pattern_result and pattern_result['confidence'] >= 0.8:
            self.translation_cache[cache_key] = pattern_result
            return pattern_result
        
        # Strategy 3: Smart segmentation translation
        parts_result = self._translate_by_smart_segmentation(chinese_text)
        if parts_result['confidence'] >= 0.6:
            self.translation_cache[cache_key] = parts_result
            return parts_result
        
        # Strategy 4: Pinyin fallback
        pinyin_result = self._translate_to_pinyin(chinese_text)
        self.translation_cache[cache_key] = pinyin_result
        
        return pinyin_result
    
    def _is_english(self, text: str) -> bool:
        """Check if text is English"""
        # If text is mainly composed of English letters, numbers and underscores, consider it English
        english_chars = re.findall(r'[a-zA-Z0-9_]', text)
        return len(english_chars) / len(text) > 0.8 if text else False
    
    def _query_term_database(self, chinese_text: str, context: str) -> Dict:
        """
        Query term database (supports exact and partial matching)
        
        Args:
            chinese_text: Chinese text
            context: Context
            
        Returns:
            dict: Translation result
        """
        # 1. Exact match
        for category, terms in self.term_db.items():
            if chinese_text in terms:
                term_info = terms[chinese_text]
                primary = term_info.get('primary', '')
                alternatives = term_info.get('alternatives', [])
                pinyin = self.pinyin_converter.text_to_pinyin(chinese_text)
                
                return {
                    'primary': primary,
                    'alternatives': alternatives,
                    'pinyin': pinyin,
                    'confidence': 1.0,
                    'source': 'term_db_exact',
                    'category': category
                }
        
        # 2. Partial matching (text contains terms)
        best_partial = self._find_best_partial_match(chinese_text)
        if best_partial:
            return best_partial
        
        # 3. No match
        pinyin = self.pinyin_converter.text_to_pinyin(chinese_text)
        return {
            'primary': '',
            'alternatives': [],
            'pinyin': pinyin,
            'confidence': 0,
            'source': 'not_found'
        }
    
    def _find_best_partial_match(self, chinese_text: str) -> Dict:
        """Find best partial match"""
        matches = []
        
        for category, terms in self.term_db.items():
            for term_cn, term_info in terms.items():
                if term_cn in chinese_text and len(term_cn) > 1:
                    matches.append({
                        'term_cn': term_cn,
                        'term_en': term_info.get('primary', ''),
                        'length': len(term_cn),
                        'category': category
                    })
        
        if not matches:
            return None
        
        # Select longest match
        best = max(matches, key=lambda x: x['length'])
        
        # Build partial translation result
        parts = chinese_text.split(best['term_cn'])
        result_parts = []
        for part in parts:
            if part:
                part_trans = self._translate_by_smart_segmentation(part)
                result_parts.append(part_trans['primary'])
            result_parts.append(best['term_en'])
        
        result_parts = [p for p in result_parts if p]
        primary = '_'.join(result_parts)
        primary = self._format_for_c_naming(primary)
        
        return {
            'primary': primary,
            'alternatives': [],
            'pinyin': self.pinyin_converter.text_to_pinyin(chinese_text),
            'confidence': 0.7,
            'source': 'term_db_partial',
            'matched_term': best['term_cn']
        }
    
    def _try_pattern_match(self, chinese_text: str) -> Dict:
        """Try pattern matching"""
        for pattern, handler in self.common_patterns:
            match = re.match(pattern, chinese_text)
            if match:
                return handler(match)
        return None
    
    def _translate_verb_noun(self, match) -> Dict:
        """Translate verb+noun pattern"""
        verb_map = {
            '读': 'read', '写': 'write', '发送': 'send', '接收': 'receive',
            '获取': 'get', '设置': 'set', '检测': 'detect', '测量': 'measure',
            '采集': 'collect', '计算': 'calculate'
        }
        
        verb = match.group(1)
        noun = match.group(2)
        
        verb_en = verb_map.get(verb, self.pinyin_converter.to_pinyin(verb))
        noun_result = self.translate(noun) if noun else {'primary': ''}
        
        primary = f"{verb_en}_{noun_result['primary']}" if noun_result['primary'] else verb_en
        primary = self._format_for_c_naming(primary)
        
        return {
            'primary': primary,
            'alternatives': [],
            'pinyin': self.pinyin_converter.text_to_pinyin(verb + noun),
            'confidence': 0.8,
            'source': 'pattern_verb_noun'
        }
    
    def _translate_adj_noun(self, match) -> Dict:
        """Translate adjective+noun pattern"""
        adj_map = {
            '最大': 'max', '最小': 'min', '当前': 'current', '平均': 'average',
            '总': 'total', '初始': 'initial', '默认': 'default'
        }
        
        adj = match.group(1)
        noun = match.group(2)
        
        adj_en = adj_map.get(adj, self.pinyin_converter.to_pinyin(adj))
        noun_result = self.translate(noun) if noun else {'primary': ''}
        
        primary = f"{adj_en}_{noun_result['primary']}" if noun_result['primary'] else adj_en
        primary = self._format_for_c_naming(primary)
        
        return {
            'primary': primary,
            'alternatives': [],
            'pinyin': self.pinyin_converter.text_to_pinyin(adj + noun),
            'confidence': 0.8,
            'source': 'pattern_adj_noun'
        }
    
    def _translate_number_unit(self, match) -> Dict:
        """Translate number+unit pattern"""
        unit_map = {
            '米': 'meter', '秒': 'second', '度': 'degree',
            '次': 'times', '个': 'count', '位': 'bit', '字节': 'byte'
        }
        
        number = match.group(1)
        unit = match.group(2)
        
        unit_en = unit_map.get(unit, self.pinyin_converter.to_pinyin(unit))
        primary = f"{number}_{unit_en}"
        
        return {
            'primary': primary,
            'alternatives': [],
            'pinyin': f"{number}_{self.pinyin_converter.to_pinyin(unit)}",
            'confidence': 0.9,
            'source': 'pattern_number_unit'
        }
    
    def _translate_by_smart_segmentation(self, chinese_text: str) -> Dict:
        """
        Smart segmentation translation
        
        Strategy:
        1. Try 2-3 character word combinations
        2. Single character translation
        3. Pinyin fallback
        """
        text_len = len(chinese_text)
        parts = []
        alternatives_list = []
        i = 0
        
        while i < text_len:
            found = False
            
            # Try 3-character word
            if i + 3 <= text_len:
                three_char = chinese_text[i:i+3]
                result = self._query_term_database(three_char, 'general')
                if result['confidence'] >= 1.0:
                    parts.append(result['primary'])
                    if result.get('alternatives'):
                        alternatives_list.append(result['alternatives'][0])
                    i += 3
                    found = True
                    continue
            
            # Try 2-character word
            if i + 2 <= text_len:
                two_char = chinese_text[i:i+2]
                result = self._query_term_database(two_char, 'general')
                if result['confidence'] >= 1.0:
                    parts.append(result['primary'])
                    if result.get('alternatives'):
                        alternatives_list.append(result['alternatives'][0])
                    i += 2
                    found = True
                    continue
            
            # Single character processing
            char = chinese_text[i]
            char_result = self._query_term_database(char, 'general')
            if char_result['confidence'] >= 1.0:
                parts.append(char_result['primary'])
                if char_result.get('alternatives'):
                    alternatives_list.append(char_result['alternatives'][0])
            else:
                # Use pinyin
                parts.append(self.pinyin_converter.to_pinyin(char))
            
            i += 1
        
        # Combine results
        primary = '_'.join(parts) if parts else chinese_text
        primary = self._format_for_c_naming(primary)
        
        alternatives = []
        if alternatives_list and len(alternatives_list) == len(parts):
            alt = '_'.join(alternatives_list)
            alternatives.append(self._format_for_c_naming(alt))
        
        return {
            'primary': primary,
            'alternatives': alternatives,
            'pinyin': self.pinyin_converter.text_to_pinyin(chinese_text),
            'confidence': 0.6,
            'source': 'smart_segmentation',
            'parts': parts
        }
    
    def _translate_to_pinyin(self, chinese_text: str) -> Dict:
        """Use pinyin translation (fallback strategy)"""
        pinyin = self.pinyin_converter.text_to_pinyin(chinese_text)
        formatted = self._format_for_c_naming(pinyin)
        
        return {
            'primary': formatted,
            'alternatives': [],
            'pinyin': pinyin,
            'confidence': 0.3,
            'source': 'pinyin_fallback'
        }
    
    def _format_for_c_naming(self, text: str) -> str:
        """
        Format for C naming conventions
        
        Args:
            text: Original text
            
        Returns:
            str: Formatted text
        """
        # To lowercase
        text = text.lower()
        # Replace spaces with underscores
        text = text.replace(' ', '_')
        text = text.replace('-', '_')
        # Remove special characters, keep only letters, numbers and underscores
        text = re.sub(r'[^a-z0-9_]', '_', text)
        # Remove consecutive underscores
        text = re.sub(r'_+', '_', text)
        # Remove leading/trailing underscores
        text = text.strip('_')
        
        return text
    
    def get_translation_suggestions(self, chinese_text: str, max_suggestions: int = 5) -> List[Dict]:
        """
        Get multiple translation suggestions (enhanced version)
        
        Args:
            chinese_text: Chinese text
            max_suggestions: Maximum number of suggestions
            
        Returns:
            list: Suggestion list, each suggestion contains {'text': str, 'source': str, 'confidence': float}
        """
        suggestions = []
        seen = set()
        
        # Main translation
        result = self.translate(chinese_text)
        if result['primary'] and result['primary'] not in seen:
            suggestions.append({
                'text': result['primary'],
                'source': result.get('source', 'unknown'),
                'confidence': result.get('confidence', 0)
            })
            seen.add(result['primary'])
        
        # Alternative translations
        for alt in result.get('alternatives', []):
            if alt and alt not in seen:
                suggestions.append({
                    'text': alt,
                    'source': 'alternative',
                    'confidence': result.get('confidence', 0) * 0.9
                })
                seen.add(alt)
                if len(suggestions) >= max_suggestions:
                    break
        
        # Pinyin form (if not yet reached quantity limit)
        if len(suggestions) < max_suggestions:
            pinyin = result.get('pinyin', '')
            if pinyin and pinyin not in seen:
                suggestions.append({
                    'text': pinyin,
                    'source': 'pinyin',
                    'confidence': 0.3
                })
                seen.add(pinyin)
        
        # Abbreviation form
        if len(suggestions) < max_suggestions and result['primary']:
            abbr = self._generate_abbreviation(result['primary'])
            if abbr and abbr not in seen:
                suggestions.append({
                    'text': abbr,
                    'source': 'abbreviation',
                    'confidence': 0.5
                })
                seen.add(abbr)
        
        return suggestions[:max_suggestions]
    
    def _generate_abbreviation(self, text: str) -> str:
        """Generate abbreviation"""
        parts = text.split('_')
        if len(parts) <= 1:
            return ''
        
        # Take first letter of each word
        abbr = ''.join([p[0] for p in parts if p])
        return abbr if len(abbr) > 1 else ''
    
    def batch_translate(self, text_list: List[str]) -> List[Dict]:
        """Batch translation"""
        return [self.translate(text) for text in text_list]
    
    def get_all_categories(self) -> List[str]:
        """Get all term categories"""
        return list(self.term_db.keys())
    
    def get_terms_by_category(self, category: str) -> Dict:
        """
        Get all terms in specified category
        
        Args:
            category: Category name
            
        Returns:
            dict: Term dictionary
        """
        return self.term_db.get(category, {})
    
    def search_terms(self, keyword: str) -> List[Dict]:
        """
        Search terms (supports both Chinese and English)
        
        Args:
            keyword: Search keyword
            
        Returns:
            list: List of matching terms
        """
        results = []
        keyword_lower = keyword.lower()
        
        for category, terms in self.term_db.items():
            for term_cn, term_info in terms.items():
                # Chinese match
                if keyword in term_cn:
                    results.append({
                        'chinese': term_cn,
                        'english': term_info.get('primary', ''),
                        'category': category,
                        'match_type': 'chinese'
                    })
                # English match
                elif keyword_lower in term_info.get('primary', '').lower():
                    results.append({
                        'chinese': term_cn,
                        'english': term_info.get('primary', ''),
                        'category': category,
                        'match_type': 'english'
                    })
                # Alternative translation match
                elif any(keyword_lower in alt.lower() for alt in term_info.get('alternatives', [])):
                    results.append({
                        'chinese': term_cn,
                        'english': term_info.get('primary', ''),
                        'category': category,
                        'match_type': 'alternative'
                    })
        
        return results
    
    def add_custom_term(self, chinese: str, english: str, category: str = 'custom', 
                       alternatives: List[str] = None):
        """
        Add custom term
        
        Args:
            chinese: Chinese
            english: English
            category: Category
            alternatives: Alternative translations
        """
        if category not in self.term_db:
            self.term_db[category] = {}
        
        self.term_db[category][chinese] = {
            'primary': english,
            'alternatives': alternatives or [],
            'context': category,
            'custom': True
        }
        
        # Clear related cache
        self.translation_cache.clear()
    
    def get_statistics(self) -> Dict:
        """Get term database statistics"""
        stats = {
            'total_categories': len(self.term_db),
            'total_terms': 0,
            'categories': {}
        }
        
        for category, terms in self.term_db.items():
            term_count = len(terms)
            stats['total_terms'] += term_count
            stats['categories'][category] = term_count
        
        return stats


# Global instance
translator = TranslationEngine()
