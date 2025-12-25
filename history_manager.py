#!/usr/bin/env python3
"""
历史记录管理器
用于保存和管理用户的分析历史记录
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class HistoryRecord:
    """历史记录数据结构"""
    id: str
    query: str
    status: str  # completed, failed, running
    created_at: str
    updated_at: str
    report_file_path: Optional[str] = None
    report_html: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict] = None


class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, history_dir: str = "history"):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)
        
    def save_record(self, record: HistoryRecord) -> bool:
        """保存历史记录"""
        try:
            record_file = self.history_dir / f"{record.id}.json"
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(record), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存历史记录失败: {str(e)}")
            return False
            
    def get_record(self, record_id: str) -> Optional[HistoryRecord]:
        """获取单条历史记录"""
        try:
            record_file = self.history_dir / f"{record_id}.json"
            if not record_file.exists():
                return None
                
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return HistoryRecord(**data)
        except Exception as e:
            print(f"获取历史记录失败: {str(e)}")
            return None
            
    def get_all_records(self, sort_by: str = "created_at", reverse: bool = True) -> List[HistoryRecord]:
        """获取所有历史记录"""
        records = []
        try:
            for record_file in self.history_dir.glob("*.json"):
                with open(record_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                records.append(HistoryRecord(**data))
                
            # 排序
            records.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)
            return records
        except Exception as e:
            print(f"获取所有历史记录失败: {str(e)}")
            return []
            
    def delete_record(self, record_id: str) -> bool:
        """删除历史记录"""
        try:
            record_file = self.history_dir / f"{record_id}.json"
            if record_file.exists():
                record_file.unlink()
            return True
        except Exception as e:
            print(f"删除历史记录失败: {str(e)}")
            return False
            
    def clear_all_records(self) -> bool:
        """清空所有历史记录"""
        try:
            for record_file in self.history_dir.glob("*.json"):
                record_file.unlink()
            return True
        except Exception as e:
            print(f"清空历史记录失败: {str(e)}")
            return False


# 全局实例
history_manager = HistoryManager()