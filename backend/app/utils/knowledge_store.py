"""
知识积累模块 - Student Knowledge Store
存储和检索学生已学棋理，实现渐进式教学

短期：内存存储 + 文件持久化（JSON）
中期：可迁移到 PostgreSQL
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class KnowledgeStore:
    """
    学生知识库：存储已学棋理，支持按概念检索

    数据结构：每条记录包含
    - general_maxim: 棋理格言
    - situation_context: 局面描述
    - key_concepts: 涉及的围棋概念
    - move_a, move_b: 正解和错手
    - board_state: SGF 棋局
    - timestamp: 学习时间
    - reconstruction_passed: 是否通过验证
    """

    def __init__(self, store_path: str = None):
        """
        Args:
            store_path: JSON 文件路径，用于持久化。为 None 时仅内存存储。
        """
        self.store_path = store_path or os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "knowledge_store.json"
        )
        self.records: List[Dict] = []
        self._load()

    def _load(self):
        """从文件加载已有记录"""
        try:
            if os.path.exists(self.store_path):
                with open(self.store_path, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
                print(f"  [KnowledgeStore] Loaded {len(self.records)} records from {self.store_path}")
        except Exception as e:
            print(f"  [KnowledgeStore] Could not load store: {e}")
            self.records = []

    def _save(self):
        """持久化到文件"""
        try:
            os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  [KnowledgeStore] Could not save store: {e}")

    def add_record(
        self,
        general_maxim: str,
        situation_context: str,
        key_concepts: List[str],
        move_a: str,
        move_b: str,
        board_state: str,
        reconstruction_passed: bool,
        detailed_analysis: str = "",
    ):
        """添加一条教学记录"""
        record = {
            "general_maxim": general_maxim,
            "situation_context": situation_context,
            "key_concepts": key_concepts,
            "move_a": move_a,
            "move_b": move_b,
            "board_state": board_state,
            "detailed_analysis": detailed_analysis,
            "reconstruction_passed": reconstruction_passed,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.records.append(record)
        self._save()
        print(f"  [KnowledgeStore] Added record (concepts: {key_concepts}). Total: {len(self.records)}")

    def find_by_concepts(self, concepts: List[str], max_results: int = 5) -> List[Dict]:
        """
        按概念查找相关的已学棋理

        Args:
            concepts: 要匹配的概念列表（如 ["断点", "厚薄"]）
            max_results: 最多返回几条

        Returns:
            按相关性排序的记录列表（概念重叠越多越靠前）
        """
        scored = []
        for record in self.records:
            record_concepts = set(record.get("key_concepts", []))
            overlap = len(record_concepts & set(concepts))
            if overlap > 0:
                scored.append((overlap, record))

        # 按重叠数量降序，取前 max_results 条
        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored[:max_results]]

    def find_by_keywords(self, keywords: List[str], max_results: int = 5) -> List[Dict]:
        """
        按关键词在 general_maxim 和 situation_context 中搜索

        Args:
            keywords: 搜索关键词
            max_results: 最多返回几条
        """
        results = []
        for record in self.records:
            text = record.get("general_maxim", "") + record.get("situation_context", "")
            if any(kw in text for kw in keywords):
                results.append(record)
                if len(results) >= max_results:
                    break
        return results

    def get_recent(self, n: int = 10) -> List[Dict]:
        """获取最近 n 条记录"""
        return self.records[-n:]

    def get_all(self) -> List[Dict]:
        """获取全部记录"""
        return self.records

    def count(self) -> int:
        """记录总数"""
        return len(self.records)
