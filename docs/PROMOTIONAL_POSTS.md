# Promotional Posts for Clarus

Copy-paste ready posts for different platforms.

---

## 1. Hacker News (Show HN)

**Title:**
```
Show HN: Clarus – Multi-agent debate system that explains why KataGo makes its moves
```

**Text (comment):**
```
Hi HN,

I built Clarus, a system that tries to make superhuman Go AI (KataGo) explain itself.

The problem: KataGo plays better than any human, but it only outputs numbers — winrate, score lead, territory maps. No human can look at those numbers and understand *why* one move is better than another.

The approach: Instead of just having an LLM summarize the numbers, Clarus uses a prediction-based verification loop:

1. KataGo evaluates two moves → raw math vectors
2. A "Scribe" agent (Gemini LLM) writes an explanation
3. A separate "Arbiter" agent reads ONLY the explanation (no board, no coordinates) and tries to predict which move is correct
4. If the Arbiter guesses wrong, it explains what it misunderstood ("I read 'press' as attack, but it meant connect"), and the Scribe rewrites

The key insight: if a student AI can find the right move just by reading the principle, the explanation actually works. If not, it gets rewritten until it does.

Tech: FastAPI + KataGo + Gemini 2.5 Flash, vanilla HTML/CSS/JS frontend.

Go is just the starting domain — the verification framework could extend to any domain where AI makes opaque decisions (medical, finance, autonomous systems).

GitHub: https://github.com/fengxuebailu/clarus

Would love feedback on the verification approach. Is prediction-based validation a viable path for XAI?
```

---

## 2. Reddit r/baduk

**Title:**
```
I built an open-source tool that makes KataGo explain WHY its moves are better, not just show the winrate
```

**Body:**
```
Hey r/baduk,

Like many of you, I've spent hours staring at KataGo's suggested moves thinking "but WHY is this better?"

KataGo tells you Q16 has 56.3% winrate and D4 has 51.1%, but it never explains the reasoning. As a Go player trying to improve, knowing the numbers isn't enough — I need to understand the tactical logic.

So I built **Clarus** — it uses multiple AI agents that debate each other to produce verified explanations:

- **Grandmaster** (KataGo): generates the raw analysis
- **Scribe** (Gemini LLM): writes the explanation using Go concepts (liberty counting, eye formation, connection analysis)
- **Arbiter** (separate LLM): reads the explanation blind and tries to predict the correct move — if it can't, the explanation gets rewritten

Example output:
> "In a double-atari position with 3 liberties each, extend rather than capture the ko. Extending preserves connection to the living group. Consequence: liberties 4 vs 2 = you survive."

The explanations use structured format: Context → Action → Logic. No vague "this develops better influence" — it gives you specific tactical reasoning with liberty counts and eye analysis.

It's open source and free: https://github.com/fengxuebailu/clarus

You need KataGo installed locally + a free Gemini API key. Without KataGo it runs in demo mode with mock data.

Would love to hear from stronger players whether the explanations actually make sense!
```

---

## 3. Reddit r/MachineLearning

**Title:**
```
[P] Prediction-based verification for XAI: if a student model can't find the right answer from the explanation alone, the explanation is rewritten
```

**Body:**
```
I've been working on an approach to Explainable AI that uses prediction-based verification rather than post-hoc attribution methods.

**The problem:** Current XAI methods (SHAP, LIME, attention maps) explain what features the model looked at, but don't verify whether the explanation is actually *useful* — i.e., whether someone could make the correct decision based solely on the explanation.

**The approach:** Using Go/Weiqi as a testbed (KataGo as the superhuman system):

1. KataGo evaluates two candidate moves → ground truth vectors (winrate, territory ownership, score lead)
2. Delta extraction: compute what changed between the two moves
3. A "Scribe" LLM generates a natural language explanation using a structured Context→Action→Logic format
4. **Verification**: A separate "Arbiter" LLM reads ONLY the abstract principle (no coordinates, no board position) and predicts which move is correct
5. If wrong, the Arbiter provides concept-gap analysis ("I interpreted 'press' as aggressive attack, but the context required reading it as 'maintain connection'")
6. The Scribe rewrites with adjusted terminology. Max 3 iterations.

**Key insight:** This is essentially a communication game — if the Arbiter can recover the correct answer from the explanation alone, the explanation has genuinely captured the decision-relevant information. This is a stronger test than reconstruction metrics because it tests functional understanding, not numerical similarity.

**Results so far:** The feedback loop significantly improves explanation quality. The concept-gap analysis (step 5) is particularly valuable — it identifies exactly which terms or concepts are ambiguous, leading to targeted rewrites rather than generic "try again."

**Why Go?** It's an ideal testbed because (a) KataGo is genuinely superhuman, (b) the ground truth is mathematically precise, and (c) Go has a rich vocabulary that can be tested for comprehension.

The framework is domain-agnostic. The same verify-by-prediction approach could work for medical diagnosis AI, financial trading models, or autonomous systems.

Code: https://github.com/fengxuebailu/clarus (FastAPI + KataGo + Gemini, MIT license)

Interested in thoughts on:
- How this compares to other verification approaches in XAI
- Whether the concept-gap feedback mechanism has parallels in the literature
- Potential extensions to other domains
```

---

## 4. 知乎

**标题:**
```
我做了一个让KataGo"说人话"的开源项目：多智能体辩论验证系统
```

**正文:**
```
作为一个围棋爱好者+AI从业者，我一直有一个困惑：

KataGo 能下赢所有人类，但它只会告诉你"Q16的胜率是56.3%，D4是51.1%"。**为什么**Q16更好？它从来不解释。

现有的围棋AI工具都是这样 —— 给你一堆数字和箭头，但你依然不知道背后的战术逻辑。

所以我做了 **Clarus**，一个多智能体辩论系统，让AI不仅要解释，还要**验证**解释是否真的有用。

### 核心机制：预测验证循环

1. **大师** (KataGo) 分析两个候选着法，输出数学向量
2. **书记官** (Gemini LLM) 把数学差异翻译成人话，用"情境→行动→逻辑"的结构
3. **仲裁者** (另一个LLM) 只读解释文字（看不到棋盘、不知道坐标），尝试猜出哪个着法更好
4. 猜错了？仲裁者解释自己哪里理解错了（"我把'压'理解成进攻，但应该是'连接'"），书记官根据反馈重写

**关键洞察**：如果一个"学生AI"能仅凭阅读抽象原则就找到正确着法，说明这个解释真的传达了战术信息。如果找不到，就重写，直到能找到为止。

### 输出示例

> "在双打吃局面中，双方各有3口气时，必须选择长而非提劫。长可以保持与活棋的连接。数学后果：气数4 vs 2 = 你赢。"

不是"此处应注意全局平衡"这种废话，而是具体的气数分析、眼位计算、连接状态判断。

### 技术栈

- 后端：FastAPI + Python
- 围棋引擎：KataGo（本地运行）
- LLM：Google Gemini 2.5 Flash
- 前端：原生HTML/CSS/JS，带北极狐吉祥物 🦊

### 为什么这不只是个围棋工具

围棋只是起点。核心创新是**通过预测来验证AI的解释是否有用**。这个框架可以扩展到：

- **医疗AI**：医生读了解释后，能不能得出同样的诊断？
- **量化交易**：分析师读了推理后，能不能预测同样的仓位？
- **自动驾驶**：工程师读了决策日志后，能不能预测系统的行为？

开源地址：https://github.com/fengxuebailu/clarus

欢迎 Star ⭐ 和提Issue！特别欢迎围棋强手来检验解释的质量。
```

---

## 5. V2EX

**标题:**
```
做了个开源项目 Clarus：用多智能体辩论让围棋 AI 解释自己的决策
```

**正文:**
```
KataGo 比所有人类都强，但它只输出数字（胜率、目差），从不解释"为什么"。

Clarus 用 4 个 AI Agent 协作，把 KataGo 的数学输出翻译成人能理解的战术分析，然后用一个"预测验证"机制确保解释质量：

- 一个"学生AI"只读解释文字（不看棋盘），尝试猜出正确着法
- 猜对 = 解释有效
- 猜错 = 学生反馈哪里没理解，老师重写

技术栈：FastAPI / KataGo / Gemini 2.5 Flash / 原生前端

围棋只是第一个领域，这个验证框架可以扩展到医疗AI、金融AI等任何"黑箱AI"场景。

GitHub: https://github.com/fengxuebailu/clarus

MIT 开源，需要本地 KataGo + Gemini API key。没有 KataGo 也能跑 demo 模式。

欢迎 Star 和反馈 🦊
```

---

## 6. Twitter/X (Thread)

**Tweet 1:**
```
I built an open-source system that makes superhuman Go AI explain itself — and then verifies the explanation actually works.

Meet Clarus 🦊

Thread 🧵👇
```

**Tweet 2:**
```
The problem: KataGo plays better than any human, but it only outputs numbers. No one understands WHY it makes its moves.

Existing tools show what the AI recommends. Never why.
```

**Tweet 3:**
```
The solution: 4 AI agents that debate each other.

🏛️ Grandmaster (KataGo) → ground truth
📊 Delta Hunter → what changed
📝 Scribe (Gemini) → writes explanation
🎓 Arbiter (Gemini) → reads explanation blind, predicts the move
```

**Tweet 4:**
```
The key innovation: prediction-based verification.

If the Arbiter can find the right move just by reading the explanation → it works ✅
If not → it explains what it misunderstood → Scribe rewrites → retry

This is a stronger test than any post-hoc XAI method.
```

**Tweet 5:**
```
Go is just the start. The same framework works for:

🏥 Medical AI — can a doctor reach the same diagnosis from the explanation?
📈 Trading AI — can an analyst predict the same position?
🚗 Autonomous systems — can an engineer predict the action?
```

**Tweet 6:**
```
Open source, MIT license.

FastAPI + KataGo + Gemini 2.5 Flash

⭐ https://github.com/fengxuebailu/clarus

Would love feedback on the verification approach!
```

---

## GitHub Settings (Manual Steps)

Go to https://github.com/fengxuebailu/clarus/settings:

1. **Description**: `Making Superhuman AI Transparent — Multi-agent debate system that explains KataGo's Go/Weiqi decisions through prediction-verified reasoning`

2. **Website**: *(leave empty unless you deploy it)*

3. **Topics** (add these): `explainable-ai`, `xai`, `go-game`, `weiqi`, `katago`, `multi-agent-systems`, `llm`, `gemini`, `fastapi`, `artificial-intelligence`, `machine-learning`

4. **Social Preview**: Upload `assets/demo-workspace-full.png` as the social preview image (Settings → Social Preview → Upload)
