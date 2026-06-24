# 学程智枢 Backend

数据驱动的教学过程智能诊断平台 · 后端服务 · v1.5

## 技术栈

- Python 3.10+
- FastAPI (Web 框架)
- SQLAlchemy 2.x (ORM)
- Pydantic 2.x (数据验证)
- SQLite (MVP 数据库)
- Pandas + scikit-learn (数据分析)
- Cohen's d (效应量计算)

## 快速开始

```bash
cd backend
pip install -r requirements.txt
python seed_data.py                    # 播种演示数据（4课程+12模式模板+知识图谱）
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

## 项目结构

```
backend/
├── app/
│   ├── main.py                  # FastAPI 入口，路由注册
│   ├── config.py                # 数据库 URL 配置
│   ├── database.py              # SQLAlchemy 引擎 + Session
│   ├── models/
│   │   ├── teaching.py          # Course, ClassModel, Student, Observation, Grade, Evaluation
│   │   └── knowledge.py         # TeachingModeTemplate, KnowledgeNode, KnowledgeEdge (v1.5)
│   ├── schemas/teaching.py      # Pydantic Schema
│   ├── routers/
│   │   ├── courses.py           # 课程 CRUD (3 endpoints)
│   │   ├── classes_.py          # 班级 CRUD (3 endpoints)
│   │   ├── data_import.py       # CSV 批量导入 (6 endpoints)
│   │   ├── analysis_routes.py   # 画像/指纹/诊断 (3 endpoints)
│   │   ├── comparison_routes.py # 对比分析 (3 endpoints) (v1.5)
│   │   └── modes.py             # 模式库 + 知识图谱 (8 endpoints) (v1.5)
│   └── services/
│       ├── profile.py           # 学情画像计算
│       ├── fingerprint.py       # 教学模式指纹识别
│       ├── diagnosis.py         # 诊断报告生成
│       ├── comparison.py        # Cohen's d + A/B对比 + 跨教师对标 (v1.5)
│       └── knowledge_graph.py   # 知识图谱构建 + 瓶颈识别 (v1.5)
├── sample_data/                 # 演示数据 CSV（6个文件）
├── seed_data.py                 # 数据播种（含12模式+知识图谱）
└── requirements.txt
```

## API 接口一览（23 个）

### 数据管理（5）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/courses` | 课程列表 |
| GET | `/api/courses/{id}` | 课程详情 |
| POST | `/api/courses` | 创建课程 |
| GET | `/api/classes?course_id=` | 班级列表 |
| GET | `/api/classes/{id}` | 班级详情 |

### 数据导入（6）
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/import/courses` | CSV 导入课程 |
| POST | `/api/import/classes` | CSV 导入班级 |
| POST | `/api/import/students` | CSV 导入学生 |
| POST | `/api/import/grades` | CSV 导入成绩 |
| POST | `/api/import/observations` | CSV 导入课堂观察 |
| POST | `/api/import/evaluations` | CSV 导入教学评价 |

### 分析引擎（6）
| 方法 | 路径 | 说明 | 版本 |
|------|------|------|:----:|
| GET | `/api/analysis/profile/{class_id}` | 六维学情画像 | v1.0 |
| GET | `/api/analysis/fingerprint/{class_id}` | 教学模式指纹 | v1.0 |
| GET | `/api/analysis/diagnosis/{class_id}` | 综合诊断报告 | v1.0 |
| GET | `/api/analysis/compare/modes?class_a=&class_b=` | A/B 对比（Cohen's d） | v1.5 |
| GET | `/api/analysis/compare/cross-teacher?course_id=` | 跨教师排名 | v1.5 |
| GET | `/api/analysis/trend/teacher?course_id=` | 学期效能趋势 | v1.5 |

### 教学模式库（8）
| 方法 | 路径 | 说明 | 版本 |
|------|------|------|:----:|
| GET | `/api/modes/templates` | 内置模式列表 | v1.5 |
| GET | `/api/modes/templates/{id}` | 模式详情 | v1.5 |
| GET | `/api/modes/custom?course_id=` | 自定义模式列表 | v1.5 |
| POST | `/api/modes/custom` | 创建自定义模式 | v1.5 |
| PUT | `/api/modes/custom/{id}` | 更新自定义模式 | v1.5 |
| DELETE | `/api/modes/custom/{id}` | 删除自定义模式 | v1.5 |
| GET | `/api/modes/recommend?class_id=` | 推荐模式 | v1.5 |
| GET | `/api/modes/knowledge-graph?course_id=` | 知识图谱 | v1.5 |

## 开发约定

1. **路由分层**：路由只做参数校验，业务逻辑在 `services/` 中实现
2. **命名约定**：表名复数（courses），字段名 snake_case，中文 comment
3. **数据导入**：统一用 pandas 解析 CSV，自动跳过重复记录
4. **分析计算**：核心统计（Cohen's d、均值、分布）用纯 Python，不依赖重量级库

## 生产部署

1. SQLite → PostgreSQL，配置连接池
2. 启用 Gunicorn + Uvicorn workers
3. 环境变量管理敏感信息（`.env`）
4. 添加 API 限流和认证中间件
5. 使用 Alembic 管理数据库迁移
