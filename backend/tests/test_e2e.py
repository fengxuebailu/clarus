"""
端到端测试：Scribe→Arbiter 预测循环
使用真实 Gemini API，验证改进后的教学效果
"""

import asyncio
import json
import sys
import os
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Setup path
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

from app.agents.scribe import ScribeAgent
from app.agents.arbiter import ArbiterAgent
from app.schemas.go_analysis import DeltaVector, ExplanationDraft


# ============================================================
# 测试用例：基于真实名局的关键着法
# ============================================================

TEST_CASES = [
    {
        # AlphaGo vs 李世石 第4局 - 李世石的"神之一手"
        # 白78手挖，打破AlphaGo的中腹大龙连接
        # 简化局面：黑棋中腹有大块棋，白棋找到了断裂点
        "name": "测试1: 李世石vs AlphaGo - 中腹断裂手筋",
        "board_state": "(;GM[1]FF[4]SZ[19];B[pd];W[dp];B[cd];W[qp];B[op];W[oq];B[nq];W[pq];B[cn];W[fq];B[mp];W[qn];B[jq];W[nc];B[pf];W[pb];B[qc];W[kc];B[cj];W[ec];B[df];W[gc];B[dh];W[bp];B[dn];W[em];B[en];W[fn];B[fm];W[fl];B[gm];W[fo];B[gl];W[fk];B[gk];W[fj];B[gj];W[fi];B[gi];W[fh];B[gh];W[fg];B[gg])",
        "move_a": "L8",   # 白棋在黑棋大块棋的连接薄弱处挖入
        "move_b": "Q5",   # 守角（缓手）
        "player_color": "W",
        "delta_vector": DeltaVector(
            delta_winrate=0.15,
            delta_lead=9.5,
            delta_ownership=[[0.0]*19 for _ in range(19)],
            key_differences=[
                "L8挖入黑棋中腹大块的连接处，黑棋的一间跳连接被切断后两块都没有根据地",
                "Q5守角虽然有目数但错过了攻击中腹黑龙的最佳时机",
            ],
            magnitude=9.65,
        ),
        "punisher_sequence": ["L9", "K8", "K9", "J8", "J9"],
    },
    {
        # AlphaGo Master 第60局 vs 朴廷桓 - AI经典的三三侵入时机
        # 现代AI围棋最标志性的着法：在对方外势还没完全围住时侵入三三
        "name": "测试2: AlphaGo Master vs 朴廷桓 - 三三侵入时机",
        "board_state": "(;GM[1]FF[4]SZ[19];B[qd];W[dd];B[pp];W[dp];B[fc];W[cf];B[od];W[qn];B[nq];W[qk];B[jd];W[dj];B[jp])",
        "move_a": "C17",  # 白棋点三三
        "move_b": "R7",   # 右边补强（不急）
        "player_color": "W",
        "delta_vector": DeltaVector(
            delta_winrate=0.08,
            delta_lead=4.2,
            delta_ownership=[[0.0]*19 for _ in range(19)],
            key_differences=[
                "C17侵入时机恰好：黑棋F17和J16还没完全围住角部，三三还能做活并破坏模样",
                "R7方向白棋已经稳定，不急着补",
            ],
            magnitude=4.28,
        ),
        "punisher_sequence": ["C16", "D17", "B16", "C18", "B17"],
    },
    {
        # 申真谞 vs AI复盘 - 典型的封锁外势转换
        # 选择封锁对方逃出中腹，用外势影响全局
        "name": "测试3: 封锁大龙获取外势（中盘转换）",
        "board_state": "(;GM[1]FF[4]SZ[19];B[pd];W[dd];B[pp];W[dp];B[fq];W[cn];B[jp];W[qf];B[qi];W[of];B[nd];W[pi];B[ph];W[qh];B[oh];W[ri];B[pg];W[qj];B[mf])",
        "move_a": "N11",  # 封锁白棋，让白棋在边上委曲做活，黑棋获取中央厚势
        "move_b": "R3",   # 守角（脱离战场）
        "player_color": "B",
        "delta_vector": DeltaVector(
            delta_winrate=0.10,
            delta_lead=6.0,
            delta_ownership=[[0.0]*19 for _ in range(19)],
            key_differences=[
                "N11封锁白棋逃出路线，白棋只能在边上小活，黑棋中腹厚势影响全局",
                "R3脱离战场，白棋从N14逃出后中腹反而变成白棋的势力范围",
            ],
            magnitude=6.10,
        ),
        "punisher_sequence": ["N14", "N13", "O13", "M14", "L13"],
    },
    {
        # 柯洁 vs AlphaGo 第1局 - 经典的碰定式后补断
        # 定式结束后，看似双方都安定，但有一个隐藏的切断点
        "name": "测试4: 碰定式后的隐患补强（高段常识）",
        "board_state": "(;GM[1]FF[4]SZ[19];B[qd];W[dd];B[pq];W[dp];B[fc];W[cf];B[jd];W[qo];B[qp];W[po];B[np];W[qj];B[ql];W[pl];B[qm];W[pm];B[rn];W[pk];B[ro])",
        "move_a": "Q14",  # 黑棋在上边和右边的连接处补强
        "move_b": "D10",  # 大场但忽视了右边棋形的弱点
        "player_color": "B",
        "delta_vector": DeltaVector(
            delta_winrate=0.07,
            delta_lead=3.8,
            delta_ownership=[[0.0]*19 for _ in range(19)],
            key_differences=[
                "Q14补强了Q16黑子和P4一带黑棋的联络，避免白棋从Q13方向切断",
                "D10虽是大场，但白棋Q13一冲，黑棋上下两块被分断，右边战斗不利",
            ],
            magnitude=3.87,
        ),
        "punisher_sequence": ["Q13", "Q12", "R13", "Q15", "R14"],
    },
]


async def run_single_test(test_case: dict, scribe: ScribeAgent, arbiter: ArbiterAgent) -> dict:
    """运行单个测试用例的完整 Scribe→Arbiter 循环"""

    print(f"\n{'='*60}")
    print(f"  {test_case['name']}")
    print(f"  正解: {test_case['move_a']}  错手: {test_case['move_b']}")
    print(f"{'='*60}")

    max_retries = 3
    results = []
    feedback_text = None

    for attempt in range(1, max_retries + 1):
        print(f"\n--- 第 {attempt} 轮 ---")

        # Scribe 生成解说
        print(f"  [Scribe] 生成格言...")
        explanation = await scribe.generate_explanation(
            delta_vector=test_case["delta_vector"],
            move_a=test_case["move_a"],
            move_b=test_case["move_b"],
            player_color=test_case["player_color"],
            version=attempt,
            feedback=feedback_text,
            punisher_sequence=test_case["punisher_sequence"],
            board_state=test_case["board_state"],
        )

        print(f"  [Scribe] situation_context: {explanation.situation_context[:100]}...")
        print(f"  [Scribe] general_maxim: {explanation.general_maxim}")
        print(f"  [Scribe] key_concepts: {explanation.key_concepts}")

        # Arbiter 测试预测
        print(f"  [Arbiter] 测试学生预测...")
        feedback = await arbiter.test_prediction(
            explanation=explanation,
            board_state=test_case["board_state"],
            move_a=test_case["move_a"],
            move_b=test_case["move_b"],
            player_color=test_case["player_color"],
        )

        result = {
            "attempt": attempt,
            "general_maxim": explanation.general_maxim,
            "situation_context": explanation.situation_context,
            "detailed_analysis": explanation.detailed_analysis,
            "predicted_move": feedback.prediction_test.predicted_move if feedback.prediction_test else "N/A",
            "correct_move": test_case["move_a"],
            "passed": feedback.passed,
            "feedback": feedback.specific_feedback[:300],
        }
        results.append(result)

        print(f"  [结果] 预测: {result['predicted_move']}  正解: {result['correct_move']}  {'✓ 通过' if feedback.passed else '✗ 未通过'}")

        if feedback.passed:
            print(f"  [成功] 第 {attempt} 轮通过！")
            break
        else:
            feedback_text = feedback.specific_feedback
            print(f"  [反馈] {feedback.specific_feedback[:200]}...")

    return {
        "test_name": test_case["name"],
        "move_a": test_case["move_a"],
        "move_b": test_case["move_b"],
        "total_attempts": len(results),
        "final_passed": results[-1]["passed"],
        "iterations": results,
    }


async def main():
    print("=" * 60)
    print("  Clarus 端到端测试 - Scribe→Arbiter 预测循环")
    print("  使用真实 Gemini API")
    print("=" * 60)

    # Initialize agents
    scribe = ScribeAgent()
    arbiter = ArbiterAgent()

    all_results = []

    for tc in TEST_CASES:
        result = await run_single_test(tc, scribe, arbiter)
        all_results.append(result)

    # Summary
    print("\n\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)

    for r in all_results:
        status = "✓ 通过" if r["final_passed"] else "✗ 未通过"
        last = r["iterations"][-1]
        print(f"\n  {r['test_name']}")
        print(f"    状态: {status} (共 {r['total_attempts']} 轮)")
        print(f"    正解: {r['move_a']}  预测: {last['predicted_move']}")
        print(f"    最终格言: {last['general_maxim'][:100]}")

    passed_count = sum(1 for r in all_results if r["final_passed"])
    print(f"\n  总计: {passed_count}/{len(all_results)} 通过")

    # Save full results to JSON
    output_path = os.path.join(os.path.dirname(__file__), "test_e2e_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n  详细结果已保存到: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
