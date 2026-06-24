# 学程智枢 Backend · v2.0

数据驱动的教学过程智能诊断平台 · 后端服务 · 生态闭环

## 快速开始

```bash
cd backend
pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

## 项目结构

```
app/
├── main.py                   # FastAPI 入口 (37 接口)
├── models/                   # 8 个数据模型
│   ├── teaching.py           # Course, Class, Student, Observation, Grade, Evaluation
│   ├── knowledge.py          # TeachingModeTemplate, KnowledgeNode, KnowledgeEdge
│   └── audit.py              # AuditLog, Notification
├── routers/                  # 9 个路由模块
│   ├── courses.py            # 课程 CRUD (3)
│   ├── classes_.py           # 班级 CRUD (3)
│   ├── data_import.py        # CSV 导入 (6)
│   ├── analysis_routes.py    # 画像/指纹/诊断 (3)
│   ├── comparison_routes.py  # A/B 对比 (3)
│   ├── modes.py              # 模式库+知识图谱 (8)
│   └── v2_routes.py          # v2.0 统一路由 (14)
└── services/                 # 10 个业务服务
    ├── profile.py            # 学情画像
    ├── fingerprint.py        # 模式指纹
    ├── diagnosis.py          # 诊断报告
    ├── comparison.py         # Cohen's d 效应量
    ├── knowledge_graph.py    # 知识图谱分析
    ├── individual_profile.py # 个体画像
    ├── migration.py          # 模式迁移推荐
    ├── lesson_plan.py        # 智能备课
    ├── reflection.py         # 课后反思
    └── data_catalog.py       # 数据资产目录
```

## API 一览（37 个）

| 分类 | 数量 | 前缀 |
|------|:---:|------|
| 数据管理 | 5 | `/api/courses`, `/api/classes` |
| 数据导入 | 6 | `/api/import/*` |
| 分析引擎 | 6 | `/api/analysis/*` |
| 教学模式库 | 8 | `/api/modes/*` |
| v2.0 闭环 | 12 | `/api/v2/*` |

## 生产部署

1. SQLite → PostgreSQL，配置连接池
2. Gunicorn + Uvicorn workers
3. `.env` 管理敏感信息
4. Alembic 管理数据库迁移
