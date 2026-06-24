# v2.0 Sprint Plan — 生态闭环

> 父计划: [development-plan.md](./development-plan.md)
> 周期: 6 周 | 目标: 教学模式从"一次性诊断"升级为"可复用数据资产"

---

## 里程碑总览

```
Sprint 3 (3周)          Sprint 4 (3周)
模式迁移 + 智能备课      数据资产 + 平台运营
─────────────────────────────────────────→
个体画像                 数据资产目录
跨课迁移引擎             数据血缘追踪
智能备课助手             效果仪表盘
课后反思助手             操作审计日志
                         消息通知
                         SQLite → PostgreSQL
```

---

## Sprint 3: 模式迁移引擎（第1-3周）

### 目标
让平台从"告诉你现在是什么模式"升级为"建议你用什么模式，并把好模式自动推荐给其他课程"。

### 3.1 后端 — 个体学情画像服务（2天）

**文件**: `backend/app/services/individual_profile.py`

**功能**: 为每个学生构建学习画像

**计算指标**:
- 知识掌握热力图: 按知识点 × 时间维度的成绩变化
- 学习投入度: 基于成绩波动 + 课堂参与度的综合评分
- 优势/薄弱知识点: 个人成绩排名前3和后3
- 学习风格标签: 视觉/听觉/动手/阅读型（基于选修课程+参与度推断）
- 进步趋势: 近3次考试成绩变化率

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/analysis/student/{student_id}/profile` | 个体学情画像 |
| GET | `/api/analysis/class/{class_id}/students` | 班级学生画像列表 |

**数据库变更**: 无需新表，基于已有 Grade + Observation 计算。

---

### 3.2 后端 — 模式迁移可行性评估（2天）

**文件**: `backend/app/services/migration.py`

**核心算法**: 余弦相似度计算两个课程的知识结构相似度

```python
def course_similarity(course_a_id, course_b_id) -> float:
    """基于知识图谱结构 + 成绩分布 + 学情特征计算课程相似度 (0-1)"""
    
def recommend_mode_migration(target_class_id) -> list[dict]:
    """
    1. 找到目标班级的学情画像
    2. 搜索所有"相似课程"中验证有效的教学模式
    3. 按相似度 × 效果量排序返回
    """
    
def assess_migration_risk(source_mode, target_class) -> dict:
    """评估模式迁移的风险等级 + 注意事项"""
```

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/migration/candidate-classes?source_class_id=` | 查找相似班级 |
| GET | `/api/migration/recommend?target_class_id=` | 推荐可迁移的优质模式 |
| GET | `/api/migration/assess?mode_id=&target_class_id=` | 迁移可行性评估 |

**前端新增**: `src/pages/ModeMigration.tsx`
- 左侧: 目标班级学情卡片
- 右侧: 相似课程列表 + 模式匹配度进度条
- 底部: 迁移风险提示（⚠️ 知识点差异 / ✅ 学情相似）

---

### 3.3 后端 — 智能备课助手（2天）

**文件**: `backend/app/services/lesson_plan.py`

**功能**: 基于学情数据自动生成教案框架

**生成逻辑**（规则引擎+LLM增强）:
1. 分析班级学情画像 → 确定教学目标和重难点
2. 匹配教学模式 → 确定教学环节结构
3. 填充知识点掌握率 → 标注"需重点讲解"和"可快速通过"
4. 可选的LLM增强：生成活动设计建议、板书设计、提问设计

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/lesson-plan/generate` | 生成教案框架 |
| GET | `/api/lesson-plan/{id}` | 获取已生成教案 |
| PUT | `/api/lesson-plan/{id}` | 编辑修改教案 |

**请求体**:
```json
{
  "class_id": 1,
  "lesson_topic": "二叉树遍历",
  "duration": 50,
  "use_llm_enhance": false
}
```

**响应**:
```json
{
  "lesson_plan": {
    "topic": "二叉树遍历",
    "objectives": ["掌握前序遍历", "理解中序遍历", "了解后序遍历"],
    "key_points": [{"name": "递归实现", "mastery": 0.45, "flag": "重点讲解"}],
    "quick_pass": [{"name": "树的基本概念", "mastery": 0.88}],
    "stages": [
      {"name": "导入", "duration": 5, "activity": "复习链表结构，引出树的非线性"},
      {"name": "讲授", "duration": 20, "activity": "三种遍历算法的递归实现"},
      {"name": "练习", "duration": 15, "activity": "课堂练习 + 小组讨论"},
      {"name": "总结", "duration": 5, "activity": "对比三种遍历异同"}
    ]
  }
}
```

**前端新增**: `src/pages/LessonPlanGenerator.tsx`
- 左侧: 输入表单（班级、课题、时长）
- 右侧: 实时生成的教案框架预览
- 重难点按掌握率标色（红=薄弱需重点讲，绿=已掌握可快速过）

---

### 3.4 后端 — 课后反思助手（1.5天）

**文件**: `backend/app/services/reflection.py`

**功能**: 课后自动汇总课堂数据，辅助教学反思

**输入**: 课堂观察记录 + 教案 + 课后即时反馈

**产出**:
- 教学目标达成度估算
- 与模式预期的偏差分析
- 学生互动热力图（哪些环节参与度高/低）
- 改进建议自动生成

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/reflection/generate` | 生成反思报告 |
| GET | `/api/reflection/{id}` | 查看反思报告 |

**前端新增**: `src/pages/ReflectionReport.tsx`
- 达成度仪表盘（圆形进度条）
- 环节参与度柱状图
- 偏差分析卡片（预期 vs 实际）
- AI改进建议列表

---

### 3.5 前端 — 页面开发（4天）

| 文件 | 说明 | 工作量 |
|------|------|:------:|
| `src/pages/StudentProfile.tsx` | 个体学情画像（知识热力图 + 趋势 + 标签） | 1.5天 |
| `src/pages/ModeMigration.tsx` | 模式迁移推荐页 | 1天 |
| `src/pages/LessonPlanGenerator.tsx` | 智能备课助手 | 1天 |
| `src/pages/ReflectionReport.tsx` | 课后反思报告 | 0.5天 |

### Sprint 3 交付物

- [ ] 5 个新后端模块
- [ ] 7 个新 API 接口
- [ ] 4 个新前端页面
- [ ] 侧边栏新增"教学工具"二级菜单（备课助手 + 课后反思 + 模式迁移）

---

## Sprint 4: 数据资产管理（第4-6周）

### 目标
让平台从"单机工具"升级为"可运营的数据资产平台"。

### 4.1 数据库升级（2天）

**SQLite → PostgreSQL 迁移**

| 步骤 | 说明 |
|------|------|
| 1. 引入 Alembic | `alembic init migrations` |
| 2. 自动生成初始迁移 | `alembic revision --autogenerate -m "init"` |
| 3. 配置多环境 | development / production 两套数据库 URL |
| 4. 引入 Redis | 缓存画像计算结果（10分钟 TTL），减少重复计算 |
| 5. 连接池配置 | PostgreSQL: pool_size=10, max_overflow=20 |
| 6. 写入 `docker-compose.yml` | 一键启动 PostgreSQL + Redis + App |

**文件变更**:
- `backend/app/config.py` → 新增 `DATABASE_URL`、`REDIS_URL` 环境变量读取
- `backend/alembic/` → 自动生成
- `backend/docker-compose.yml` → 新增

---

### 4.2 数据资产目录（2天）

**文件**: `backend/app/services/data_catalog.py`

**功能**: 平台数据资产的全景可视化

**资产统计维度**:
- 数据类型: 课程/学生/成绩/观察/评价/模式
- 数据量: 各表行数、存储大小
- 更新频率: 最近更新时间
- 质量评分: 缺失率 + 异常率 + 完整性综合评分（0-100）
- 使用次数: 被查询/被引用的次数

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/catalog/summary` | 数据资产总览 |
| GET | `/api/catalog/{entity_type}` | 某类资产详情 |
| GET | `/api/catalog/quality-report` | 数据质量报告 |

**前端新增**: `src/pages/DataCatalog.tsx`
- 资产统计卡片行（6类数据各一张卡片）
- 数据质量仪表盘
- 资产更新日历时间线

---

### 4.3 数据血缘追踪（1.5天）

**文件**: `backend/app/services/data_lineage.py`

**功能**: 记录和展示每条分析结论的完整数据来源链路

**血缘记录格式**:
```json
{
  "analysis_id": "diagnosis_2024_1",
  "analysis_type": "diagnosis",
  "inputs": [
    {"source": "grades", "filters": {"class_id": 1}, "row_count": 50},
    {"source": "observations", "filters": {"class_id": 1}, "row_count": 3},
    {"source": "evaluations", "filters": {"class_id": 1}, "row_count": 5}
  ],
  "transformations": ["profile_compute", "fingerprint_compute", "diagnosis_build"],
  "output": {"type": "diagnosis_report", "class_id": 1},
  "timestamp": "2026-06-24T10:00:00"
}
```

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/catalog/lineage/{analysis_id}` | 分析结论的数据血缘 |

**前端新增**: `src/pages/DataLineage.tsx`
- Sankey 图展示数据流（CSV → DB → Profile → Diagnosis）
- 点击节点展开详情

---

### 4.4 效果仪表盘（1.5天）

**文件**: `frontend/src/pages/EffectivenessDashboard.tsx`

**功能**: 平台使用成效的可视化看板

**指标**:
- 已诊断课程数、已识别模式数
- 模式应用后的平均成绩提升率
- 最受欢迎的教学模式 TOP5
- 教师使用频率趋势（日/周/月）
- "数据资产价值"估算（模式复用次数 × 平均效应量）

**前端**: 独立页面，使用 ECharts Dashboard 风格布局

**后端 API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/dashboard/effectiveness` | 效果指标汇总 |

---

### 4.5 操作审计日志（1天）

**文件**: `backend/app/models/audit.py`

**模型**: `AuditLog(id, user_id, action, entity_type, entity_id, details, ip, created_at)`

**记录的操作**:
- 数据导入（谁导入了什么数据）
- 分析查看（谁查看了哪个班级的画像/诊断）
- 模式创建/编辑/删除
- 教案生成

**API**:
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/audit/logs?user_id=&action=&page=&size=` | 审计日志分页查询 |

**前端新增**: `src/pages/AuditLog.tsx`（管理后台，仅管理员可见）

---

### 4.6 消息通知（1天）

**功能**: 关键事件自动通知

**通知类型**:
| 事件 | 通知方式 | 接收人 |
|------|----------|--------|
| 诊断报告生成完毕 | 站内信 | 任课教师 |
| 新模式被验证为高效 | 站内信 | 模式创建者 |
| 数据质量下降预警 | 站内信+邮件 | 管理员 |

**实现**: 站内信存数据库（`notifications` 表），邮件通过 SMTP 发送

**前端**: 顶部 Header 新增🔔通知图标 + 未读红点 + 下拉列表

---

### 4.7 前端 — 页面开发（4天）

| 文件 | 说明 | 工作量 |
|------|------|:------:|
| `src/pages/DataCatalog.tsx` | 数据资产目录总览 | 1天 |
| `src/pages/DataLineage.tsx` | 数据血缘 Sankey 图 | 1天 |
| `src/pages/EffectivenessDashboard.tsx` | 效果仪表盘 | 1天 |
| `src/pages/AuditLog.tsx` | 审计日志管理 | 0.5天 |
| `src/components/NotificationBell.tsx` | 通知铃铛组件 | 0.5天 |

### Sprint 4 交付物

- [ ] PostgreSQL + Redis 基础设施
- [ ] Alembic 迁移管理
- [ ] 4 个新后端模块 + 5 个新 API
- [ ] 5 个新前端功能（4 页面 + 通知组件）
- [ ] `docker-compose.yml`

---

## v2.0 新增 API 一览（12 个）

### 个体画像 & 迁移
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/analysis/student/{student_id}/profile` | 个体学情画像 |
| GET | `/api/migration/recommend?target_class_id=` | 模式迁移推荐 |
| GET | `/api/migration/assess?mode_id=&target_class_id=` | 迁移风险评估 |

### 智能备课 & 反思
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/lesson-plan/generate` | 生成教案框架 |
| GET | `/api/lesson-plan/{id}` | 获取教案 |
| POST | `/api/reflection/generate` | 生成反思报告 |

### 数据资产
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/catalog/summary` | 数据资产总览 |
| GET | `/api/catalog/quality-report` | 数据质量报告 |
| GET | `/api/catalog/lineage/{analysis_id}` | 数据血缘 |
| GET | `/api/dashboard/effectiveness` | 效果仪表盘 |

### 管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/audit/logs` | 审计日志 |

---

## v2.0 前端新增页面（9 个）

| 路由 | 页面 | Sprint |
|------|------|:------:|
| `/tools/student-profile` | 个体学情画像 StudentProfile | S3 |
| `/tools/migration` | 模式迁移 ModeMigration | S3 |
| `/tools/lesson-plan` | 智能备课 LessonPlanGenerator | S3 |
| `/tools/reflection` | 课后反思 ReflectionReport | S3 |
| `/assets/catalog` | 数据资产目录 DataCatalog | S4 |
| `/assets/lineage` | 数据血缘 DataLineage | S4 |
| `/assets/dashboard` | 效果仪表盘 EffectivenessDashboard | S4 |
| `/admin/audit` | 审计日志 AuditLog | S4 |
| — | 通知铃铛 NotificationBell (组件) | S4 |

---

## 侧边栏重构（v2.0）

```
📊 教师工作台          → /
📥 数据导入            → /import
📈 对比分析            → /compare/*
🎯 学情画像            → /profile
🔍 模式指纹            → /fingerprint
📚 教学模式库          → /modes/*
🛠️ 教学工具            → /tools/*        ← 新增
   ├─ 个体画像
   ├─ 模式迁移
   ├─ 智能备课
   └─ 课后反思
📋 诊断报告            → /diagnosis
📦 数据资产            → /assets/*        ← 新增
   ├─ 资产目录
   ├─ 数据血缘
   └─ 效果仪表盘
```

---

## 基础设施升级

### docker-compose.yml

```yaml
version: '3.8'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: xczs
      POSTGRES_USER: xczs
      POSTGRES_PASSWORD: xczs_dev
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

volumes:
  pgdata:
```

### 环境变量（.env）

```
DATABASE_URL=postgresql://xczs:xczs_dev@localhost:5432/xczs
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=change-in-production
```

---

## 团队分工建议

| 角色 | Sprint 3 | Sprint 4 | 总工作量 |
|------|----------|----------|:------:|
| 后端 ×2 | 个体画像 + 迁移引擎 + 备课助手 | 数据资产 + 血缘 + 审计 + 通知 | 各 3 周 |
| 前端 ×2 | StudentProfile + Migration + LessonPlan + Reflection | DataCatalog + Lineage + Dashboard + AuditLog + Notification | 各 3 周 |
| DevOps | — | PostgreSQL + Redis + Alembic + Docker | 1 周 |
| 测试 | S3 集成测试 | S4 集成测试 + 性能测试 | 各 0.5 周 |

---

## v2.0 完成标准

- [ ] PostgreSQL 替换 SQLite，Alembic 迁移可用
- [ ] 个体画像至少覆盖 80 名学生
- [ ] 跨课程模式迁移至少 2 组课程可用
- [ ] 智能备课助手可生成完整教案框架
- [ ] 数据资产目录展示 6 类数据资产
- [ ] 数据血缘可追踪至少 2 条分析链路
- [ ] 效果仪表盘含 ≥5 个核心指标
- [ ] 审计日志记录全部关键操作
- [ ] Docker 一键启动全部服务
- [ ] 前端 20 页面全部零 JS 错误
- [ ] 全链路测试: 导入→画像→对比→迁移→备课→反思→数据资产
