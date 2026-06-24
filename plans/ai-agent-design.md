# 学程智枢 — AI Agent 扩展需求分析与架构设计

> 版本: v1.0 | 日期: 2026-06-24 | 基于现有 v2.0 平台

---

## 一、需求分析

### 1.1 现有功能与智能体映射

| 现有功能 | 当前实现 | 痛点 | Agent 化后 |
|----------|----------|------|-----------|
| 学情画像 `profile.py` | 触发式 API 调用 | 被动等待教师查看 | **Diagnosis Agent** 定时自主分析 + 主动推送 |
| 模式指纹 `fingerprint.py` | 规则 + 模板匹配 | 一次诊断，无持续追踪 | **Diagnosis Agent** 持续监控模式变化趋势 |
| 智能备课 `lesson_plan.py` | 单次模板加载 | 不关联历史数据 | **Planning Agent** 结合历史学情 + 迁移推荐生成教案 |
| 课后反思 `reflection.py` | 规则偏差分析 | 没有与备课计划对比 | **Reflection Agent** 对比教案预期 vs 实际执行 |
| 模式迁移 `migration.py` | 相似度计算 | 需要教师主动查找 | **Planning Agent** 在备课时自动推荐迁移模式 |
| 诊断报告 `diagnosis.py` | LLM 增强文本 | 固定格式输出 | **Diagnosis Agent** 对话式输出 + 追问能力 |
| — | 无 | 教师需切换多个页面拼凑信息 | **Query Agent** 自然语言问答"哪个班二叉树最差?" |

### 1.2 智能体使用场景（5个核心场景）

```
场景1: 自动诊断与预警
  每周一 8:00 → Diagnosis Agent 扫描全部班级 → 发现异常 → 推送到通知中心

场景2: 智能备课辅助
  教师输入"下节课讲二叉树遍历" → Planning Agent 调取画像 + 迁移推荐 + 模板库
  → 生成教案框架 → 教师确认/修改

场景3: 课后反思闭环
  教师完成课堂观察录入 → Reflection Agent 读取教案预期 vs 实际数据
  → 生成对比反思 → 更新班级模式历史

场景4: 自然语言查询
  教师问"哪些学生图算法最弱?" → Query Agent 检索数据 → 返回排名 + 建议

场景5: 一键综合诊断
  教师点击"全面诊断" → Orchestrator 编排 Diagnosis + Planning + Reflection
  → 生成综合诊断报告（含教案建议）
```

### 1.3 参考项目分析

| 项目 | 架构 | 可借鉴点 |
|------|------|----------|
| **VidyaAI** | 7-Agent LangGraph Pipeline | 教学备课的多智能体串行流程设计 |
| **MAIC/OpenMAIC** | Director + Teacher + Student Agents | 教育场景的角色定义方法论 |
| **Multi-Agent-Learning-System** | 18 Agent + Supervisor 编排 | Fan-out 并行生成 + 意图路由 |
| **EduGPT** | 3-Agent 角色协作 | 备课 Agent 的双人讨论模式 |
| **hi-paris/teaching-assistant** | Router → RAG/Web → Synthesis | 多路召回 + 合成 Agent 模式 |

---

## 二、架构设计

### 2.1 总体架构

```
┌────────────────────────────────────────────────────────────┐
│                      前端 (React)                           │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐ │
│  │ Agent聊天│ │ 自动报告 │ │ 备课助手 │ │ 综合诊断按钮   │ │
│  └────┬────┘ └────┬─────┘ └────┬─────┘ └───────┬───────┘ │
├───────┼───────────┼───────────┼─────────────────┼─────────┤
│       ▼           ▼           ▼                 ▼         │
│  ┌────────────────────────────────────────────────────┐   │
│  │              FastAPI 路由层 (新增 /api/agent/*)     │   │
│  │  POST /agent/chat       对话式查询                  │   │
│  │  POST /agent/diagnose   综合诊断                    │   │
│  │  POST /agent/plan       智能备课（Agent版）          │   │
│  │  POST /agent/reflect    课后反思（Agent版）          │   │
│  │  GET  /agent/schedule   触发定时任务                 │   │
│  └──────────────────────┬─────────────────────────────┘   │
│                         ▼                                  │
│  ┌────────────────────────────────────────────────────┐   │
│  │           Agent 编排层 (LangGraph)                   │   │
│  │                                                     │   │
│  │  ┌──────────────┐                                  │   │
│  │  │ Orchestrator │ ← Supervisor Agent               │   │
│  │  │  (调度中心)   │    意图识别 + 任务分发             │   │
│  │  └──┬───┬───┬──┘                                  │   │
│  │     │   │   │                                       │   │
│  │  ┌──▼─┐ ┌▼──┐ ┌▼──────┐ ┌▼─────┐                 │   │
│  │  │Diag│ │Plan│ │Reflect│ │Query │ 5 个专业 Agent   │   │
│  │  │nosis│ │ning│ │ion    │ │      │                 │   │
│  │  └──┬─┘ └┬──┘ └┬──────┘ └┬─────┘                 │   │
│  │     │     │      │         │                        │   │
│  └─────┼─────┼──────┼─────────┼────────────────────────┘   │
│        │     │      │         │                             │
│        ▼     ▼      ▼         ▼                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │              现有服务层 (复用)                        │   │
│  │  profile.py  fingerprint.py  lesson_plan.py         │   │
│  │  reflection.py  migration.py  llm.py                │   │
│  │  comparison.py  data_catalog.py                     │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### 2.2 技术选型

| 维度 | 选择 | 理由 |
|------|------|------|
| **Agent 框架** | **LangGraph** (`langgraph`) | 与现有 FastAPI 天然集成；状态图模型匹配教学流程；原生 Human-in-the-Loop 支持；LangSmith 可观测性 |
| **LLM** | 复用现有 `llm.py`（DeepSeek/通义） | 不引入新依赖 |
| **状态存储** | SQLite `SqliteSaver`（开发）/ PostgreSQL（生产） | 复用现有数据库 |
| **定时任务** | `APScheduler` | 轻量级，FastAPI 集成简单 |
| **RAG（可选 v2）** | ChromaDB + 现有知识图谱 | 增强 Query Agent 精度 |

**为什么不用 CrewAI/AutoGen**：

| 框架 | 不适合原因 |
|------|-----------|
| CrewAI | 角色抽象层过重；缺乏状态持久化；不适合生产级 FastAPI 集成 |
| AutoGen | 微软生态绑定；对话循环成本不可控；v2.0 仍不稳定 |
| LangGraph | ✅ 图式状态机适合教学流程；Pydantic 原生状态校验；FastAPI 一等公民 |

### 2.3 编排模式

采用 **Hierarchical Supervisor + Sequential Pipeline** 混合模式：

```
Orchestrator (Supervisor)
  │
  ├── 场景A (简单查询): 直接路由到 Query Agent
  │
  ├── 场景B (备课): Planning Agent (串行)
  │     └── 内部调用: profile → migration → lesson_plan
  │
  └── 场景C (综合诊断): fan-out 并行
        ├── Diagnosis Agent ────┐
        ├── Planning Agent ─────┼──→ Synthesis ──→ 综合报告
        └── Reflection Agent ───┘
```

---

## 三、详细设计

### 3.1 Agent 定义

#### Agent 0: Orchestrator（调度中心）

```python
# backend/app/agents/orchestrator.py
class OrchestratorAgent:
    """意图识别 + 任务分发。所有 agent 请求的入口。"""

    def route(self, intent: str, context: dict) -> str:
        """
        意图 → Agent 路由:
          "diagnose"      → Diagnosis Agent
          "plan"          → Planning Agent
          "reflect"       → Reflection Agent
          "query"         → Query Agent
          "comprehensive" → Fan-out → Synthesis
        """

    def fan_out_diagnose(self, class_ids: list[int]) -> dict:
        """并行诊断多个班级，汇总结果。"""
```

#### Agent 1: Diagnosis Agent（诊断智能体）

```python
# backend/app/agents/diagnosis_agent.py
class DiagnosisAgent:
    """
    职责: 自主诊断 + 趋势监控 + 预警
    工具: profile.py, fingerprint.py, comparison.py
    LLM: 增强描述 + 生成预警文本
    """

    def analyze_class(self, class_id: int) -> DiagnosisResult:
        """单班综合诊断"""
        profile = compute_profile(db, cls)
        fingerprint = compute_fingerprint(db, cls)
        trend = get_trend_data(db, class_id)  # 新增: 历史对比
        alert = self._check_anomalies(profile, trend)
        suggestion = call_llm(system_prompt, user_prompt)
        return DiagnosisResult(...)

    def batch_scan(self) -> list[Alert]:
        """批量扫描所有班级，发现异常"""
        for cls in all_classes:
            if self._is_grade_declining(cls):     # 成绩连续下降
                yield Alert(cls, "成绩下降预警")
            if self._is_participation_low(cls):   # 参与度持续低
                yield Alert(cls, "参与度预警")

    def _check_anomalies(self, profile, trend) -> list[str]:
        """异常检测: 成绩突降、参与度骤减、知识断层"""
```

#### Agent 2: Planning Agent（备课智能体）

```python
# backend/app/agents/planning_agent.py
class PlanningAgent:
    """
    职责: 智能备课 + 模式推荐
    工具: lesson_plan.py, migration.py, 教学模式库
    LLM: 生成教案文本 + 教学提示
    """

    def generate_plan(self, class_id: int, topic: str, duration: int = 50) -> LessonPlan:
        """多步串行生成教案"""
        # Step 1: 获取班级画像
        profile = compute_profile(db, cls)

        # Step 2: 查找可迁移的优质模式
        migrations = recommend_migration(db, class_id)

        # Step 3: 匹配最佳模板
        template = _get_class_mode_template(db, class_id)

        # Step 4: 从模板加载环节 + 等比缩放
        stages = self._scale_stages(template.stages, duration)

        # Step 5: LLM 增强描述
        description = call_llm(...)

        return LessonPlan(...)
```

#### Agent 3: Reflection Agent（反思智能体）

```python
# backend/app/agents/reflection_agent.py
class ReflectionAgent:
    """
    职责: 对比教案预期 vs 实际执行 → 生成复盘报告
    工具: reflection.py, 上次教案记录
    LLM: 生成反思文本 + 改进建议
    """

    def reflect(self, class_id: int, observation_id: int,
                last_plan_id: int = None) -> ReflectionReport:
        """闭环反思: 教案 → 执行 → 偏差分析"""
        # 1. 读取上次教案（如果存在）
        last_plan = get_last_plan(class_id) if last_plan_id else None

        # 2. 读取课堂观察
        obs = get_observation(observation_id)

        # 3. 对比预期 vs 实际
        deviations = []
        if last_plan:
            deviations = self._compare_plan_vs_actual(last_plan, obs)

        # 4. LLM 生成反思
        suggestion = call_llm(...)

        return ReflectionReport(deviations, suggestion)
```

#### Agent 4: Query Agent（查询智能体）

```python
# backend/app/agents/query_agent.py
class QueryAgent:
    """
    职责: 自然语言 → SQL/API 查询 → 结果解读
    工具: 所有分析 API
    LLM: 理解问题 → 选择工具 → 解读结果
    """

    def answer(self, question: str, user_id: int) -> str:
        """自然语言问答"""
        # 1. LLM 解析意图
        intent = self._parse_intent(question)
        # "哪些学生图算法最弱?" → intent: rank_students, kp: "图算法"

        # 2. 调用对应 API
        if intent == "rank_students":
            data = get_class_students_profile(class_id)
            weak = [s for s in data if kp in s["weak_points"]]
            result = sorted(weak, key=lambda s: s["avg_grade"])

        # 3. LLM 解读结果
        answer = call_llm(f"根据以下数据回答: {question}\n数据: {result}")
        return answer
```

### 3.2 LangGraph 状态图

```python
# backend/app/agents/graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    intent: str                    # "diagnose" | "plan" | "reflect" | "query" | "comprehensive"
    class_ids: list[int]
    user_id: int
    user_role: str
    messages: Annotated[list, operator.add]  # 对话历史
    diagnosis_result: dict | None
    plan_result: dict | None
    reflection_result: dict | None
    query_result: str | None
    final_output: dict | None

def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("diagnosis", diagnosis_node)
    graph.add_node("planning", planning_node)
    graph.add_node("reflection", reflection_node)
    graph.add_node("query", query_node)
    graph.add_node("synthesis", synthesis_node)       # 综合诊断时汇总

    # Entry
    graph.set_entry_point("orchestrator")

    # Conditional routing
    graph.add_conditional_edges(
        "orchestrator",
        route_by_intent,
        {
            "diagnose": "diagnosis",
            "plan": "planning",
            "reflect": "reflection",
            "query": "query",
            "comprehensive": "diagnosis",  # starts parallel chain
        }
    )

    # Diagnose → END or → synthesis (if comprehensive)
    graph.add_conditional_edges("diagnosis", should_synthesize, {True: "synthesis", False: END})

    # Fan-out: diagnose → planning (comprehensive mode)
    graph.add_edge("diagnosis", "planning")
    graph.add_edge("planning", "reflection")
    graph.add_edge("reflection", "synthesis")
    graph.add_edge("synthesis", END)

    # Simple paths
    graph.add_edge("planning", END)
    graph.add_edge("reflection", END)
    graph.add_edge("query", END)

    return graph.compile()
```

### 3.3 Agent 状态持久化

```python
# backend/app/models/agent_state.py
class AgentSession(Base):
    __tablename__ = "agent_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    intent = Column(String(50))
    state_json = Column(Text)          # LangGraph checkpoint
    created_at = Column(DateTime)

class LessonPlanRecord(Base):
    __tablename__ = "lesson_plan_records"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer)
    topic = Column(String(200))
    plan_json = Column(Text)           # 教案内容
    template_id = Column(Integer)       # 使用的模板
    created_at = Column(DateTime)
    # 供 Reflection Agent 做预期 vs 实际对比
```

---

## 四、与现有代码的集成点

### 4.1 目录结构

```
backend/app/
├── agents/                          ← 新增
│   ├── __init__.py
│   ├── orchestrator.py              # 调度中心
│   ├── diagnosis_agent.py           # 诊断 Agent
│   ├── planning_agent.py            # 备课 Agent
│   ├── reflection_agent.py          # 反思 Agent
│   ├── query_agent.py               # 查询 Agent
│   └── graph.py                     # LangGraph 状态图
├── models/
│   ├── agent_state.py               ← 新增: 会话 + 教案记录
│   └── ... (现有)
├── routers/
│   └── agent_routes.py              ← 新增: /api/agent/* 路由
├── services/
│   ├── llm.py                       → 复用
│   ├── profile.py                   → Agent 内部调用
│   ├── fingerprint.py               → Agent 内部调用
│   └── ... (其余不变)
└── ...
```

### 4.2 现有代码修改

| 文件 | 修改 | 原因 |
|------|------|------|
| `main.py` | 注册 `agent_routes` + 初始化 APScheduler | Agent 入口 + 定时任务 |
| `requirements.txt` | 新增 `langgraph`, `apscheduler` | 新依赖 |
| `llm.py` | 无修改 | Agent 直接 `from app.services.llm import call_llm` |
| `models/__init__.py` | 导入 `agent_state` | 自动建表 |
| `seed_data.py` | 新增教案记录示例数据 | 演示用 |

### 4.3 前端新增页面

| 路由 | 页面 | 说明 |
|------|------|------|
| `/agent/chat` | AgentChat | 对话式查询界面（Query Agent） |
| `/agent/diagnose` | AgentDiagnose | 一键综合诊断（Orchestrator fan-out） |
| `/agent/plan` | AgentPlan | Agent 增强版备课（Planning Agent） |

---

## 五、实施路线

### Phase 1: 基础设施（1 周）

- [ ] 安装 LangGraph + APScheduler
- [ ] 创建 `models/agent_state.py`（会话 + 教案记录表）
- [ ] 搭建 `agents/graph.py` 基础图框架
- [ ] 创建 `routers/agent_routes.py` 路由骨架
- [ ] 初始化 APScheduler 定时任务框架

### Phase 2: Diagnosis Agent（1 周）

- [ ] 实现 `diagnosis_agent.py`（单班诊断 + 批量扫描）
- [ ] 定时任务：每周一 8:00 全量扫描
- [ ] 异常检测逻辑（成绩下降/参与度低/知识断层）
- [ ] 主动推送通知到 Notification 表

### Phase 3: Planning + Reflection Agent（1 周）

- [ ] 实现 `planning_agent.py`（多步串行备课）
- [ ] 教案存入 `lesson_plan_records` 表
- [ ] 实现 `reflection_agent.py`（预期 vs 实际对比）
- [ ] 闭环：上次教案 → 本次观察 → 反思建议

### Phase 4: Query Agent + 前端（1 周）

- [ ] 实现 `query_agent.py`（NL → API → 解读）
- [ ] 前端 AgentChat 页面
- [ ] 前端 AgentDiagnose 一键诊断按钮
- [ ] 端到端集成测试

---

## 六、风险评估

| 风险 | 缓解 |
|------|------|
| LangGraph 学习曲线 | Phase 1 先用最简单的 Sequential 图，逐步加条件路由 |
| LLM 调用成本 | Query Agent 用本地 SQL 查询兜底，LLM 只做意图解析和结果解读 |
| 定时任务稳定性 | APScheduler 内存调度，Phase 1 仅单次触发，逐步升级 |
| Agent 幻觉 | 所有 Agent 输出都基于 API 真实数据，LLM 只做文本润色 |
