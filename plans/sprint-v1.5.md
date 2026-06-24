# v1.5 Sprint Plan — 增强分析

> 父计划: [development-plan.md](./development-plan.md)
> 周期: 4 周 | 目标: 诊断从"描述性"升级为"证据性"

---

## Sprint 1: 对比分析引擎（第1-2周）

### 目标
让平台能回答："这种教学模式比那种教学模式好多少？证据是什么？"

### 任务分解

#### 1.1 后端 — 效应量计算服务（2天）

**文件**: `backend/app/services/comparison.py`

```python
# 核心函数
compute_effect_size(group_a, group_b) -> Cohen's d
compare_modes(class_id_a, class_id_b) -> ComparisonResult
rank_classes_by_metric(metric, course_id) -> RankingResult
```

**指标**:
- Cohen's d 效应量（0.2 小 / 0.5 中 / 0.8 大）
- 成绩均值差异 + 置信区间
- 满意度评分差异

**依赖**: F13（班级画像 ✅）, F16（模式指纹 ✅）

#### 1.2 后端 — 对比分析路由（1天）

**文件**: `backend/app/routers/comparison_routes.py`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/analysis/compare/modes?class_a=1&class_b=2` | 两个班级模式对比 |
| GET | `/api/analysis/compare/cross-teacher?course_id=1` | 同课程跨教师模式对标 |
| GET | `/api/analysis/trend/teacher?course_id=1` | 教师学期效能趋势 |

#### 1.3 数据库变更（0.5天）

- `classes` 表新增 `semester_index` 字段（INT, 用于排序）
- 不引入 Alembic（v1.5 阶段仍用 SQLite create_all 增量）

#### 1.4 前端 — A/B 对比页（2天）

**文件**: `frontend/src/pages/ComparisonAB.tsx`

**布局**:
```
┌─────────────────────────────────────────────┐
│  班级选择器 A  vs  班级选择器 B              │
├──────────────────┬──────────────────────────┤
│  双雷达图叠加     │  效应量指标卡片            │
│  (蓝=A, 紫=B)    │  - Cohen's d = 0.72      │
│                  │  - 成绩差 = +8.3分        │
│                  │  - 满意度差 = +12%        │
├──────────────────┴──────────────────────────┤
│  详细对比表（各维度逐项对比）                  │
└─────────────────────────────────────────────┘
```

**组件**:
- `DualRadarChart` — 双雷达图叠加（echarts 双 series）
- `EffectSizeCard` — 效应量展示（大数字 + 解释文本）
- `DimensionCompareTable` — 维度逐项对比表

#### 1.5 前端 — 效能趋势页（1.5天）

**文件**: `frontend/src/pages/TeacherTrend.tsx`

**布局**: 三线趋势图（ECharts 双 Y 轴）
- X 轴: 学期
- Y1 轴: 成绩（折线）
- Y2 轴: 评教分数（折线）
- 标注点: 教学模式切换时间点

#### 1.6 前端 — 跨班级对比（1.5天）

**文件**: `frontend/src/pages/CrossClassCompare.tsx`

**布局**: 同专业多班级卡片排列 + 差异高亮

### Sprint 1 交付物

- [ ] 3 个新后端接口 + 单元测试
- [ ] 3 个新前端页面（A/B对比 + 趋势 + 跨班对比）
- [ ] 侧边栏新增"对比分析"菜单（二级菜单）

---

## Sprint 2: 教学模式库（第3-4周）

### 目标
让平台成为"教学模式的知识库"，而不仅仅是诊断工具。

### 任务分解

#### 2.1 后端 — 模式库数据模型（1天）

**文件**: `backend/app/models/knowledge.py`

```python
class TeachingModeTemplate(Base):
    id, name, category, description, stages(JSON),
    suitable_scenarios, created_by, usage_count, avg_rating

class KnowledgeGraphNode(Base):
    id, name, course_id, parent_id, difficulty

class KnowledgeGraphEdge(Base):
    id, source_id, target_id, relation_type  # prerequisite/parallel/contains
```

#### 2.2 后端 — 模式库 API（1.5天）

**文件**: `backend/app/routers/modes.py`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/modes/templates` | 内置模式列表（12+） |
| POST | `/api/modes/custom` | 创建自定义模式 |
| GET | `/api/modes/custom?course_id=` | 我的自定义模式 |
| PUT | `/api/modes/custom/{id}` | 编辑自定义模式 |
| DELETE | `/api/modes/custom/{id}` | 删除自定义模式 |
| GET | `/api/modes/recommend?class_id=` | 基于学情推荐模式 |

#### 2.3 后端 — 知识图谱服务（1.5天）

**文件**: `backend/app/services/knowledge_graph.py`

**功能**:
- 从成绩数据自动提取知识点依赖关系
- 计算每个知识点的班级掌握率
- 标注"瓶颈知识点"（影响下游最多的薄弱点）

**算法**: 
- 知识点依赖推断: 基于知识点间成绩相关性矩阵
- 掌握率标注: `count(score >= 60) / count(all)`

#### 2.4 后端 — 种子数据扩展（0.5天）

在 `seed_data.py` 中新增:
- 12 个内置教学模式模板数据
- 3 个自定义模式示例
- 1 门课程的知识图谱依赖关系

#### 2.5 前端 — 模式库浏览页（2天）

**文件**: `frontend/src/pages/ModeLibrary.tsx`

**布局**:
```
┌─────────────────────────────────────────────┐
│  搜索框  [类别筛选下拉]  [适用场景筛选]       │
├─────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ 翻转课堂  │ │  PBL    │ │ BOPPPS  │    │
│  │ ⭐4.8    │ │ ⭐4.5   │ │ ⭐4.2   │    │
│  │ 123次使用 │ │ 89次使用 │ │ 67次使用 │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│  ...                                         │
└─────────────────────────────────────────────┘
```

**组件**: `ModeCard`（带 hover 效果 + 标签）

#### 2.6 前端 — 模式编辑器（1.5天）

**文件**: `frontend/src/pages/ModeEditor.tsx`

**功能**:
- 模式名称 + 描述
- **环节编辑器**: 拖拽式添加/排序教学环节（导入→讲授→讨论→练习→总结）
- 每个环节: 名称、时长（分钟）、活动类型、教师行为、学生行为
- 保存 + 预览

#### 2.7 前端 — 知识图谱页（1.5天）

**文件**: `frontend/src/pages/KnowledgeMap.tsx`

**布局**: ECharts Graph（力导向布局）
- 节点大小 = 掌握率（大=好，小=差）
- 节点颜色 = 难度（绿→黄→红）
- 边 = 依赖关系（箭头方向）
- 点击节点 → 侧边栏显示详情

#### 2.8 前端 — 侧边栏更新（0.5天）

`App.tsx` 侧边栏菜单更新:
```
📊 教师工作台
📥 数据导入
📈 对比分析         ← 新增
   ├─ A/B模式对比
   ├─ 效能趋势
   └─ 跨班级对比
🎯 学情画像
🔍 模式指纹
📚 教学模式库       ← 新增
   ├─ 模板浏览
   ├─ 自定义模式
   └─ 知识图谱
📋 诊断报告
```

### Sprint 2 交付物

- [ ] 2 个新数据模型 + 8 个新接口
- [ ] 4 个新前端页面
- [ ] 侧边栏重构（二级菜单）
- [ ] 种子数据扩展至含 12 个模式模板 + 知识图谱

---

## 技术债务清理（穿插）

| 编号 | 任务 | Sprint |
|------|------|:------:|
| TD-01 | `<LoadingWrapper>` + `<ErrorBoundary>` 组件封装 | S1 |
| TD-02 | `ExceptionMiddleware` 统一异常处理 | S1 |
| TD-04 | Pydantic Field 校验规则补全 | S1 |
| TD-05 | 开启 TS strict unused checks + 清理 | S2 |

---

## v1.5 完成标准

- [ ] 所有 API 接口通过 Swagger 自测
- [ ] 前端 9 个页面无 JS 错误
- [ ] A/B 对比至少覆盖 2 组班级
- [ ] 模式库包含 ≥12 个内置模板
- [ ] 知识图谱至少覆盖 1 门课程
- [ ] 全链路测试: 导入→画像→对比→模式推荐→诊断
- [ ] `lsp_diagnostics` 无 error
