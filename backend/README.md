# 学程智枢 Backend

数据驱动的教学过程智能诊断平台 · 后端服务

## 技术栈

- Python 3.10+
- FastAPI (Web 框架)
- SQLAlchemy 2.x (ORM)
- Pydantic 2.x (数据验证)
- SQLite (MVP 数据库)
- Pandas + scikit-learn (数据分析)

## 快速开始

```bash
cd backend
pip install -r requirements.txt
python seed_data.py                    # 播种演示数据
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

## 项目结构

```
backend/
├── app/
│   ├── main.py                # FastAPI 入口，CORS + 路由挂载
│   ├── config.py              # 数据库 URL 配置
│   ├── database.py            # SQLAlchemy 引擎 + Session
│   ├── models/teaching.py     # 6 个数据模型
│   ├── schemas/teaching.py    # Pydantic 请求/响应 Schema
│   ├── routers/
│   │   ├── courses.py         # 课程 CRUD
│   │   ├── classes_.py        # 班级 CRUD
│   │   ├── data_import.py     # CSV 批量导入（6个接口）
│   │   └── analysis_routes.py # 画像/指纹/诊断接口
│   └── services/
│       ├── profile.py         # 班级学情画像计算
│       ├── fingerprint.py     # 教学模式指纹识别
│       └── diagnosis.py       # 综合诊断报告生成
├── sample_data/               # 演示数据 CSV（6个文件）
├── seed_data.py               # 数据播种脚本
└── requirements.txt
```

## API 接口一览

### 数据管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/courses` | 课程列表 |
| GET | `/api/courses/{id}` | 课程详情（含班级） |
| POST | `/api/courses` | 创建课程 |
| GET | `/api/classes?course_id=` | 班级列表 |
| GET | `/api/classes/{id}` | 班级详情（含学生） |

### 数据导入
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/import/courses` | CSV 导入课程 |
| POST | `/api/import/classes` | CSV 导入班级 |
| POST | `/api/import/students` | CSV 导入学生 |
| POST | `/api/import/grades` | CSV 导入成绩 |
| POST | `/api/import/observations` | CSV 导入课堂观察 |
| POST | `/api/import/evaluations` | CSV 导入教学评价 |

### 分析引擎
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/analysis/profile/{class_id}` | 六维学情画像 |
| GET | `/api/analysis/fingerprint/{class_id}` | 五维教学模式指纹 |
| GET | `/api/analysis/diagnosis/{class_id}` | 综合诊断报告 |

## 开发约定

1. **路由分层**：路由只做参数校验，业务逻辑在 `services/` 中实现
2. **Schema 复用**：基础 Schema 可嵌套引用（如 `CourseDetail` 包含 `ClassResponse[]`）
3. **数据导入**：统一使用 pandas 解析 CSV，自动跳过重复记录
4. **命名约定**：数据库表名复数（courses, classes），字段名 snake_case

## 生产部署

1. SQLite → PostgreSQL，配置连接池
2. 启用 Gunicorn + Uvicorn workers
3. 环境变量管理敏感信息（`.env`）
4. 添加 API 限流和认证中间件
5. 使用 Alembic 管理数据库迁移
