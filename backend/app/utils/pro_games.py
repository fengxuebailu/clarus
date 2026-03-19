"""
现代围棋参考语料 - Pro Games Reference Corpus
经典现代围棋局面，用于 Scribe 的 few-shot 参考

包含 10 个经典场景，每个场景有：
- SGF 片段
- 关键着法
- 棋理要点（中文）
"""

from typing import List, Dict


class ProGameReference:
    """单个参考局面"""

    def __init__(
        self,
        title: str,
        title_en: str,
        sgf_fragment: str,
        key_move: str,
        principle: str,
        principle_en: str,
        category: str,
        concepts: List[str],
    ):
        self.title = title
        self.title_en = title_en
        self.sgf_fragment = sgf_fragment
        self.key_move = key_move
        self.principle = principle
        self.principle_en = principle_en
        self.category = category
        self.concepts = concepts

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "title_en": self.title_en,
            "sgf_fragment": self.sgf_fragment,
            "key_move": self.key_move,
            "principle": self.principle,
            "principle_en": self.principle_en,
            "category": self.category,
            "concepts": self.concepts,
        }


# ============================================================
# 10 个经典现代围棋场景
# ============================================================

PRO_GAME_REFERENCES: List[ProGameReference] = [
    # 1. 点三三侵入时机
    ProGameReference(
        title="点三三侵入时机",
        title_en="3-3 Invasion Timing",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[fq];W[cn];B[qc])",
        key_move="R17 (qc)",
        principle=(
            "当对方的外势还没有完全围住中腹时，是点三三的最佳时机。"
            "太早进去，对方外势价值还不大，等于帮对方围了模样；"
            "太晚进去，对方补强之后角里可能做不活。"
            "关键判断：对方的模样是否已经有弱点可以消减？如果有，先不急着点三三。"
        ),
        principle_en="Invade 3-3 when the opponent's framework still has weaknesses that reduce its value.",
        category="fuseki",
        concepts=["点三三", "时机判断", "模样", "布局"],
    ),

    # 2. 大飞守角 vs 小飞守角
    ProGameReference(
        title="大飞守角与小飞守角的选择",
        title_en="Large Knight vs Small Knight Corner Enclosure",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pj];W[dp];B[qn])",
        key_move="R6 (qn) - 大飞守角",
        principle=(
            "大飞守角重视速度和外势，适合配合已有的边上子力形成模样；"
            "小飞守角重视实地和坚实，适合对方有打入可能时先稳固角部。"
            "AI 时代的新认识：大飞守角被点三三后虽然角上损失大，"
            "但如果外势方向有配合，整体效率反而更高。"
        ),
        principle_en="Large knight enclosure prioritizes speed; small knight prioritizes solidity. AI favors the large knight when side stones provide synergy.",
        category="fuseki",
        concepts=["守角", "大飞", "小飞", "模样配合"],
    ),

    # 3. AI 流行的肩冲定式
    ProGameReference(
        title="肩冲——AI 时代的急所",
        title_en="Shoulder Hit - AI Era's Key Move",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[cf];W[dj])",
        key_move="D10 (dj) - 肩冲",
        principle=(
            "肩冲是 AI 最爱用的削减手段。它的妙处在于：不直接接触对方的强子，"
            "而是在对方势力的'腰部'落子，让对方进退两难。"
            "对方如果压，你就退回来获得实地；对方如果退，你就顺势扩张。"
            "肩冲的要诀：选在对方模样最薄的方向，让对方无法同时兼顾两边。"
        ),
        principle_en="Shoulder hit at the waist of the opponent's influence creates a dilemma - push gains territory, pull back yields expansion.",
        category="joseki",
        concepts=["肩冲", "削减", "薄味", "进退两难"],
    ),

    # 4. 中腹厚薄判断
    ProGameReference(
        title="中腹厚薄——何时该补强",
        title_en="Center Thickness Judgment",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[qf];W[nc];B[oc];W[nd];B[pf];W[jc])",
        key_move="K17 (jc) - 拆边兼顾厚味",
        principle=(
            "判断中腹厚薄的关键：看断点和眼位。"
            "如果一块棋有两个以上的断点且没有明确的两只眼，这块棋就是薄的。"
            "薄棋附近不能脱先——对方一旦攻击，你会陷入被动，"
            "不仅失去主动权（先手），还可能连带周围的子力贬值。"
            "补强的原则：选择既能消除断点又能扩张势力的一手。"
        ),
        principle_en="A group is thin if it has multiple cutting points and no clear eyes. Reinforce before the opponent attacks.",
        category="middle_game",
        concepts=["厚薄", "断点", "眼位", "补强", "先手"],
    ),

    # 5. 收束阶段的先手利
    ProGameReference(
        title="收束阶段的先手利",
        title_en="Endgame Sente Profit",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[qj];W[dj];B[jd];W[jp])",
        key_move="先手收官的优先级",
        principle=(
            "收官阶段，先手利比绝对目数更重要。"
            "一手棋如果是先手（对方必须应），就算只值3目，也要优先于后手6目的大官子。"
            "因为先手收完还能继续收下一个，而后手之后主动权就交给对方了。"
            "判断先手的标准：如果我不走这里，对方走了是否是先手？如果是，那我走就也是先手。"
        ),
        principle_en="In endgame, sente moves worth 3 points outweigh gote moves worth 6 points because you keep the initiative.",
        category="endgame",
        concepts=["先手利", "收官", "主动权", "目数计算"],
    ),

    # 6. 对杀（攻め合い）中的气数计算
    ProGameReference(
        title="对杀中的气数计算",
        title_en="Liberty Counting in Capturing Races",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[qf];B[qe];W[pf];B[rf];W[rg];B[re];W[qh])",
        key_move="紧外气优先",
        principle=(
            "对杀（攻め合い）的铁律：先紧对方的外气，再考虑里面。"
            "走里面往往是自己填气（自撞一气），反而让自己少一气。"
            "气数计算口诀：数对方的外气，数自己的外气，多的一方赢。"
            "有眼杀无眼——如果你有一只眼对方没有，你的内部气不用算，你稳赢。"
        ),
        principle_en="In capturing races, fill opponent's outside liberties first. Playing inside is self-atari. Eyes beat no eyes.",
        category="life_and_death",
        concepts=["对杀", "攻め合い", "气数", "外气", "有眼杀无眼"],
    ),

    # 7. 弃子战术（捨て石）
    ProGameReference(
        title="弃子战术——舍小取大",
        title_en="Sacrifice Strategy",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[qn];W[fq];B[cf];W[fc])",
        key_move="主动弃子获取外势",
        principle=(
            "弃子的时机：当救回几颗子的代价大于它们的价值时，果断放弃。"
            "好的弃子不是被动丢子，而是故意让对方去吃，"
            "趁对方忙着吃子的时候，在外面构筑更大的势力或实地。"
            "判断标准：被吃的子值多少目？放弃之后我能获得多少目？"
            "如果弃子后的收获大于损失两倍以上，这就是好的弃子。"
        ),
        principle_en="Sacrifice when the cost of saving stones exceeds their value. Good sacrifice creates more outside profit than the stones are worth.",
        category="strategy",
        concepts=["弃子", "捨て石", "外势", "损益判断", "效率"],
    ),

    # 8. 打入时机判断
    ProGameReference(
        title="打入时机——什么时候该进去搅局",
        title_en="Invasion Timing",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[qj];W[dj];B[jj])",
        key_move="打入对方模样",
        principle=(
            "打入的时机取决于三个条件："
            "1. 对方的模样是否已经大到不打入就要输？"
            "2. 打入之后能否做活或逃出？看附近有没有接应的子力。"
            "3. 打入会不会让自己的弱棋更弱？如果自己也有孤棋，先补强再打入。"
            "打入的位置选择：在对方阵势最薄的地方进去，通常是在对方两块棋之间的缝隙。"
        ),
        principle_en="Invade when: (1) opponent's framework is too large to ignore, (2) you can live or escape, (3) your own groups are secure.",
        category="middle_game",
        concepts=["打入", "模样", "做活", "接应", "薄味"],
    ),

    # 9. 封锁 vs 实地的平衡
    ProGameReference(
        title="封锁与实地的平衡",
        title_en="Sealing vs Territory Balance",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[fq];W[cn];B[jp];W[qn])",
        key_move="封锁对方还是围实地",
        principle=(
            "封锁和实地是围棋永恒的平衡。"
            "封锁对方的好处：把对方压低，自己的外势变厚，为后续攻击创造条件。"
            "围实地的好处：确定的利益，不依赖后续战斗。"
            "选择的原则：如果外势方向还有大场可以配合，选封锁；"
            "如果外势方向已经没什么发展空间，选实地。"
            "AI 的新认识：封锁的价值常常被低估，厚味的潜力可以影响全局。"
        ),
        principle_en="Seal in the opponent when your influence has room to grow; take territory when influence cannot develop further.",
        category="strategy",
        concepts=["封锁", "实地", "外势", "厚味", "全局判断"],
    ),

    # 10. 大型转换的损益判断
    ProGameReference(
        title="大型转换——得失计算",
        title_en="Large-Scale Trade Evaluation",
        sgf_fragment="(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[qf];W[nc];B[oc];W[nd];B[qc];W[kc])",
        key_move="角部实地换外势的转换",
        principle=(
            "大型转换是高手的必修课。核心问题只有一个：谁赚了？"
            "计算方法：把双方得到的东西都换算成目数。"
            "实地好算——数空就行；外势难算——看它能影响多大范围。"
            "AI 时代的经验法则：外势的价值约等于它能'罩住'的空间面积的30-40%。"
            "转换之后要问自己：我的棋是否变厚了？如果只换到了薄棋，即使目数持平也是亏的。"
        ),
        principle_en="In large trades, convert everything to points. Influence is worth ~30-40% of the area it covers. Thickness matters beyond raw points.",
        category="strategy",
        concepts=["转换", "损益计算", "实地", "外势", "厚薄"],
    ),
]


def get_reference_by_category(category: str) -> List[ProGameReference]:
    """获取指定分类的参考局面"""
    return [ref for ref in PRO_GAME_REFERENCES if ref.category == category]


def get_reference_by_concept(concept: str) -> List[ProGameReference]:
    """获取包含指定概念的参考局面"""
    return [ref for ref in PRO_GAME_REFERENCES if concept in ref.concepts]


def get_all_references() -> List[Dict]:
    """获取所有参考局面（字典格式）"""
    return [ref.to_dict() for ref in PRO_GAME_REFERENCES]


def get_few_shot_examples(n: int = 3) -> str:
    """
    生成用于 Scribe few-shot 的参考文本

    Args:
        n: 返回的示例数量

    Returns:
        格式化的 few-shot 参考文本
    """
    examples = []
    for ref in PRO_GAME_REFERENCES[:n]:
        example = f"""### {ref.title} ({ref.title_en})
棋理要点：{ref.principle}
涉及概念：{', '.join(ref.concepts)}
"""
        examples.append(example)

    return "\n".join(examples)
