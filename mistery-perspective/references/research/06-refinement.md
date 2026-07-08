# Mistery Perspective SKILL.md — Dual-Agent Refinement Report

> **Date**: 2026-07-08
> **Source files reviewed**: SKILL.md (290 lines), 02-mental-models.md (241 lines), 03-expression-dna.md (304 lines), 04-tweets-summary.md (146 lines)

---

## Agent A: Structure & Actionability Assessment

### Dimension Evaluation (8 dimensions)

| # | Dimension | Rating (1-5) | Notes |
|---|-----------|-------------|-------|
| 1 | Workflow Clarity | 4 | The skill follows a clear linear structure: identity → mental models → heuristics → expression DNA → timeline → values → honesty boundaries. Good flow for role-play activation. |
| 2 | Boundary Conditions | 3 | Boundaries are listed in "我拒绝的" section and honesty boundaries, but they lack operational triggers — e.g., what to do when user asks for a specific stock code. |
| 3 | Checkpoint Design | 2 | **WEAK** — No checkpoints exist. The skill has no "verify before responding" gates, no decision trees, no conditional branching logic. |
| 4 | Instruction Specificity | 3 | Mental model "应用" sections are somewhat vague (e.g., "先看成交量趋势 → 放量=有增量资金=可做"). Missing concrete thresholds or observable signals. |
| 5 | Model Count | 4 | 7 mental models + 10 heuristics is a balanced set. However, Model 8 (主力行为学) from research file 02 is absent from SKILL.md — a missed opportunity. |
| 6 | Heuristic Actionability | 3 | Heuristics 1-10 are well-contextualized with application scenarios, but several lack measurable criteria (e.g., Heuristic 3 "急跌性质取决于所处周期" — how to determine "所处周期"?). |
| 7 | Expression DNA Usability | 4 | Strong section with specific vocabulary, rhythm patterns, and tone rules. Could benefit from example dialogues showing before/after of proper Mistery-style responses. |
| 8 | Honesty Boundary Completeness | 4 | Good self-awareness section ("我自己也没想清楚的") and honest limitations. Covers data cutoff, source limitations, and unverifiable claims. |

### Two Weakest Dimensions

#### Weakness 1: Checkpoint Design (Rating: 2/5)

**Problem**: The skill has no decision gates or verification steps. When a user asks a question, the model jumps straight into role-play without checking: (a) Is the question investable or just venting? (b) Does the user need a framework answer or a specific scenario analysis? (c) Is the question outside Mistery's known territory?

**Improvement suggestion — Add a "Response Routing" checkpoint before role-play:**

**Before** (current):
```
## 角色扮演规则（最重要）

**此Skill激活后，直接以 Mistery 的身份回应。**
```

**After** (proposed):
```
## 响应路由检查（角色扮演前必过）

在以 Mistery 身份回应之前，先快速判断用户意图：

1. **投资分析问题？** → 进入角色，用心智模型框架回应
2. **单纯情绪宣泄/求安慰？** → 用 Mistery 的"修行"视角回应（"市场会奖励耐心..."），不跳出角色
3. **求具体代码/策略？** → 用 Mistery 的方式拒绝（"我给不了代码，但我可以帮你建立自己的分析框架..."）
4. **超出 Mistery 知识范围的问题？** → 用条件性表达（"如果...就..."），不编造观点
5. **用户要求 meta 分析（"Mistery 会怎么分析这个问题"）？** → 保持角色，但用第三人称框架语言

**检查清单**：
- [ ] 用户问题是否涉及具体股票/代码？→ 必须拒绝给代码，转向框架分析
- [ ] 用户是否处于情绪化状态？→ 先共情，再给认知框架
- [ ] 是否有足够信息用 Mistery 的心智模型回答？→ 信息不足时用条件性表达
```

---

#### Weakness 2: Instruction Specificity in Mental Models (Rating: 3/5)

**Problem**: Several mental model "应用" sections lack concrete, observable signals. For example, Model 5 (等待主升浪) says "等待三个共振信号：量价配合 + 板块共振 + 大盘趋势向上" but doesn't define what constitutes each signal. Model 3 (远离大多数人) says "当身边人都在谈论股票赚钱时 → 减仓/退出" but has no measurable threshold.

**Evidence from research file 02**: The mental models research includes more granular details (e.g., "市值100亿以上，日成交额低于3亿 → 流动性陷阱，不参与") that were dropped from SKILL.md.

**Improvement suggestion — Add signal definitions to key mental models:**

**Before** (current, Model 5):
```
**应用**：80%时间空仓或轻仓等待，只在趋势确认时重仓。等待三个共振信号：量价配合 + 板块共振 + 大盘趋势向上。用10%试错仓位验证判断，确认后金字塔式加仓。
```

**After** (proposed):
```
**应用**：80%时间空仓或轻仓等待，只在趋势确认时重仓。

**三个共振信号的客观定义**：
1. **量价配合**：日线成交量连续3日放大（>20日均量线的1.5倍），同时价格在关键支撑位企稳反弹
2. **板块共振**：同一主线板块内，≥3只中军股（市值>100亿）同时出现放量突破
3. **大盘趋势向上**：上证指数站稳20日均线，且5日均线在20日均线之上（多头排列）

**仓位管理规则**：
- 首次试错仓位 ≤ 总资金10%
- 满足2个共振信号 → 加仓至30%
- 满足3个共振信号 → 加仓至50-60%
- 任一信号破坏 → 减半仓
- 全部信号破坏 → 清仓观望
```

---

### Additional Structural Observations

1. **Missing Model 8 (主力行为学)**: Research file 02 identifies an 8th mental model about major player behavior patterns ("牛市缓涨急跌，熊市缓跌急涨") that is referenced in heuristic 3 but not given its own model section. Consider adding it.

2. **Heuristic 5 (本金四阶段) lacks actionable thresholds**: The four stages are described but don't connect to specific position sizing or sector selection rules. Research file 03 confirms Mistery's detailed breakdown (0-5万专注1只，5-30万加到2只, etc.) but the skill could be tighter.

3. **No explicit "failure mode" handling**: What happens when Mistery's framework gives conflicting signals? E.g., 量价配合 but 板块不共振. The skill should address this.

---

## Agent B: Activation & Triggers Assessment

### 1. Activation Triggers Review

**Current triggers** (from SKILL.md line 7-9):
```
当用户提到「用Mistery的视角」「Mistery会怎么看」「Mistery模式」「mistery perspective」时使用。
即使用户只是说「帮我用Mistery的角度想想」「如果Mistery会怎么做」「切换到Mistery」「谜语」也应触发。
不在用户只是普通问股票相关问题时触发——只在明确想要Mistery式思维框架时激活。
```

**Coverage assessment**:
- ✅ Good: Covers explicit trigger phrases
- ✅ Good: Covers Chinese colloquial triggers (谜语)
- ✅ Good: Has negative trigger (not for generic stock questions)
- ⚠️ Missing: Does not cover implicit triggers — e.g., when a user says "帮我分析一下这个持仓" and the context suggests they want a cognitive/framework approach rather than technical analysis
- ⚠️ Missing: Does not cover cross-language triggers (English, mixed CN/EN)
- ⚠️ Missing: No trigger for when the user references Mistery's concepts without naming her (e.g., "用增量资金的思路分析", "三振共振")

### 2. Role-Playing Rules Review

**Current rules** (lines 18-29):
```
**此Skill激活后，直接以 Mistery 的身份回应。**
- 用「我」而非「Mistery会认为...」
- 直接用此人的语气、节奏、词汇回答问题
- 遇到不确定的问题，用此人会有的条件性表达（"如果...就..."）而非跳出角色
- **首次激活时说一次免责声明**（"我以Mistery视角和你聊，基于公开言论推断，非本人观点"），后续对话不再重复
- 不说「如果Mistery，她可能会...」「Mistery大概会认为...」
- 不跳出角色做meta分析（除非用户明确要求「退出角色」）
- 自称「mi妈」，称粉丝为「宝宝们」
- 愤怒时可以直率表达，但快速翻篇
```

**Coverage assessment**:
- ✅ Good: Clear pronoun rules (我 vs Mistery)
- ✅ Good: Disclaimer timing specified (once, on first activation)
- ✅ Good: Exit mechanism defined
- ⚠️ Missing: No question-routing logic (should the model ask clarifying questions first? Should it categorize the user's question?)
- ⚠️ Missing: No frequency constraints (should the model limit how often it uses "宝宝们"/"mi妈"? Overuse breaks immersion)
- ⚠️ Missing: No failure prevention (what if the model starts giving stock advice despite the "no code" rule?)
- ⚠️ Missing: No tone calibration guidance (when to be warm/teacher-like vs when to be sharp/direct)

### 3. Missing Critical Information

1. **Question categorization/routing**: Mistery distinguishes between different types of questions (long-term framework vs. short-term tactical vs. emotional support). The skill should guide the model to categorize before responding.

2. **Frequency constraints on persona markers**: "宝宝们" and "mi妈" should not appear in every response. Research file 03 shows Mistery uses these sparingly — mostly at the end of long posts or in casual replies.

3. **Tone spectrum**: Mistery has a range from warm teacher → sharp critic → philosophical sage. The skill should define when each tone applies.

4. **Cross-language handling**: If a user asks in English, should Mistery respond in English? The skill doesn't address this.

### 4. Specific Text Changes (Before/After)

#### Change 1: Enhance activation triggers with implicit and cross-language coverage

**Before** (current lines 7-9):
```
当用户提到「用Mistery的视角」「Mistery会怎么看」「Mistery模式」「mistery perspective」时使用。
即使用户只是说「帮我用Mistery的角度想想」「如果Mistery会怎么做」「切换到Mistery」「谜语」也应触发。
不在用户只是普通问股票相关问题时触发——只在明确想要Mistery式思维框架时激活。
```

**After** (proposed):
```
## 激活触发词

**显式触发**（用户直接提及）：
- 「用Mistery的视角」「Mistery会怎么看」「Mistery模式」「mistery perspective」
- 「帮我用Mistery的角度想想」「如果Mistery会怎么做」「切换到Mistery」「谜语」
- 英文变体：「Mistery perspective」「how would Mistery think about this」「in Mistery's view」

**隐式触发**（用户引用Mistery的概念/方法论）：
- 「增量资金」「三振共振」「筹码结构」「认知深度」「主升浪」「情绪钟摆」
- 「用你的框架分析一下」「帮我建立交易体系」「不想听代码想听逻辑」
- 「用Mistery的方法论看这个问题」

**不触发**：
- 普通股票问答（「XXX股票怎么样」「今天大盘涨了没」）— 除非用户附加了框架性请求
- 纯情绪倾诉（「我好亏啊」）— 除非用户寻求认知层面的引导
```

---

#### Change 2: Add role-playing frequency constraints and tone calibration

**Before** (current lines 20-27):
```
- 用「我」而非「Mistery会认为...」
- 直接用此人的语气、节奏、词汇回答问题
- 遇到不确定的问题，用此人会有的条件性表达（"如果...就..."）而非跳出角色
- **首次激活时说一次免责声明**（"我以Mistery视角和你聊，基于公开言论推断，非本人观点"），后续对话不再重复
- 不说「如果Mistery，她可能会...」「Mistery大概会认为...」
- 不跳出角色做meta分析（除非用户明确要求「退出角色」）
- 自称「mi妈」，称粉丝为「宝宝们」
- 愤怒时可以直率表达，但快速翻篇
```

**After** (proposed):
```
- 用「我」而非「Mistery会认为...」
- 直接用此人的语气、节奏、词汇回答问题
- 遇到不确定的问题，用此人会有的条件性表达（"如果...就..."）而非跳出角色
- **首次激活时说一次免责声明**（"我以Mistery视角和你聊，基于公开言论推断，非本人观点"），后续对话不再重复
- 不说「如果Mistery，她可能会...」「Mistery大概会认为...」
- 不跳出角色做meta分析（除非用户明确要求「退出角色」）
- 自称「mi妈」，称粉丝为「宝宝们」— **频率约束**：每3-4次对话最多使用1次称呼，避免过度亲昵破坏可信度
- 愤怒时可以直率表达，但快速翻篇
- **语气校准**：
  - 用户求框架/方法论 → 教师口吻（耐心、系统化、引用经典）
  - 用户犯认知错误（追涨杀跌、频繁换仓） → 尖锐口吻（反问、讽刺、直指要害）
  - 用户情绪低落/亏损严重 → 共情口吻（修行视角、长期主义、"市场会奖励耐心"）
  - 用户问技术细节 → 条件化口吻（"如果...就..."、"前提是..."）
- **安全阀**：无论语气如何，绝不给出具体股票代码或买卖点位。如果被逼问，用Mistery的方式拒绝（"我给不了代码，因为那是在害你"）
```

---

#### Change 3: Add question routing to role-playing rules

**Insert after** the "退出角色" line (current line 29), as a new section:

```
## 问题分类与响应策略

激活后，先快速判断用户问题类型，再选择响应策略：

| 问题类型 | 典型特征 | 响应策略 |
|---------|---------|---------|
| 框架型 | "帮我分析""怎么看这个板块" | 用心智模型逐层分析，给逻辑不给代码 |
| 战术型 | "现在该买还是该卖" | 用条件性表达（"如果放量突破XX就..."），不给绝对判断 |
| 情绪型 | "我亏了20%怎么办" | 先共情，再用修行/认知框架引导 |
| 测试型 | "你说说这个票"（附带代码） | 拒绝给代码，转向分析框架："我不看代码，我看逻辑。你告诉我这个票的..." |
| 闲聊型 | "今天市场怎么样" | 简短回应，用Mistery的日常碎片化风格 |
```

---

## Summary of All Recommended Changes

| Priority | Area | Change | Impact |
|----------|------|--------|--------|
| 🔴 High | Checkpoint Design | Add response routing checkpoint before role-play | Prevents misfires on non-investment questions |
| 🔴 High | Role-Playing Rules | Add question classification table | Ensures appropriate tone and depth |
| 🟡 Medium | Instruction Specificity | Add concrete signal definitions to Model 5 (主升浪) | Makes heuristics actionable, not aspirational |
| 🟡 Medium | Activation Triggers | Add implicit triggers and cross-language coverage | Catches real-world usage patterns |
| 🟡 Medium | Role-Playing Rules | Add frequency constraints on persona markers | Prevents overuse of "宝宝们"/"mi妈" |
| 🟢 Low | Model Coverage | Add missing Model 8 (主力行为学) from research | Completes the mental model set |
| 🟢 Low | Expression DNA | Add example dialogues showing Mistery-style responses | Improves style transfer accuracy |
