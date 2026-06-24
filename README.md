# 学程智枢 (XueCheng ZhiShu)

> 数据驱动的教学过程智能诊断与模式重构平台

2026年"数据要素×"大赛山东分赛 · 教育创新赛道 · 教育教学应用与模式创新 参赛项目

**当前版本：v1.5** | [开发计划](./plans/development-plan.md)

---

## 项目简介

学程智枢是一款面向高校教师的教学过程智能诊断平台。通过对教务数据、课堂行为、学生评教、学业成果和教学资源五源数据的融合分析，自动生成**班级学情画像**、**教学模式指纹**、**A/B 对比分析**和**诊断报告**，内置 **12 种教学模式模板**和**课程知识图谱**，帮助教师从经验驱动转向数据驱动的循证教学决策。

### 核心功能

| 功能 | 说明 | 版本 |
|------|------|:----:|
| 📥 **数据导入** | 支持 CSV 批量导入课程、班级、学生、成绩、课堂观察、教学评价六类数据 | v1.0 |
| 📊 **教师工作台** | 课程卡片概览、班级/学生统计、一键跳转诊断 | v1.0 |
| 🎯 **学情画像** | 六维雷达图（知识掌握/参与度/互动质量/提问深度/实践均衡/满意度）+ 薄弱/优势知识点 | v1.0 |
| 🔍 **模式指纹** | 五维教学模式雷达图 + 模式自动识别（讲授型/互动型/实践型/混合型）+ 改进建议 | v1.0 |
| 📈 **对比分析** | A/B 模式双雷达图叠加 + Cohen's d 效应量 + 效能趋势 + 跨班级排名 | v1.5 |
| 📚 **教学模式库** | 12 种内置教学模式模板（翻转课堂/PBL/BOPPPS/对分/5E…）+ 自定义模式创建 | v1.5 |
| 🗺️ **知识图谱** | 力导向知识点依赖图 + 掌握率可视化 + 瓶颈知识点自动预警 | v1.5 |
| 📋 **诊断报告** | 综合诊断 + 教学模式适配建议 + 可打印导出 | v1.0 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | React 18 + TypeScript |
| UI 组件 | Ant Design 5.x |
| 图表 | ECharts 5 + echarts-for-react |
| 构建工具 | Vite 5 |
| 后端框架 | Python FastAPI |
| ORM | SQLAlchemy 2.x |
| 数据库 | SQLite（MVP）/ PostgreSQL（生产） |
| 数据分析 | Pandas + scikit-learn + Cohen's d |

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 9+

### 1. 克隆项目

```bash
git clone https://github.com/565003920/xczs-platform.git
cd xczs-platform
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python seed_data.py                    # 播种演示数据（含12模式模板+知识图谱）
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev                            # → http://localhost:5173
```

### 4. 访问

打开浏览器访问 http://localhost:5173

---

## 项目结构

```
xczs-platform/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI 入口
│   │   ├── config.py                # 配置（数据库URL等）
│   │   ├── database.py              # SQLAlchemy 引擎
│   │   ├── models/
│   │   │   ├── teaching.py          # 教学数据模型（6个实体）
│   │   │   └── knowledge.py         # 模式模板 + 知识图谱模型（v1.5）
│   │   ├── schemas/teaching.py      # Pydantic 请求/响应
│   │   ├── routers/
│   │   │   ├── courses.py           # 课程 CRUD
│   │   │   ├── classes_.py          # 班级 CRUD
│   │   │   ├── data_import.py       # CSV 导入
│   │   │   ├── analysis_routes.py   # 画像/指纹/诊断接口
│   │   │   ├── comparison_routes.py # 对比分析接口（v1.5）
│   │   │   └── modes.py             # 模式库 + 知识图谱接口（v1.5）
│   │   └── services/
│   │       ├── profile.py           # 学情画像引擎
│   │       ├── fingerprint.py       # 模式指纹引擎
│   │       ├── diagnosis.py         # 诊断报告引擎
│   │       ├── comparison.py        # A/B对比 + Cohen's d（v1.5）
│   │       └── knowledge_graph.py   # 知识图谱分析（v1.5）
│   ├── sample_data/                 # 演示数据 CSV
│   ├── seed_data.py                 # 数据播种（含模式+图谱）
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx                  # 布局 + 二级菜单路由（v1.5）
│   │   ├── types/index.ts           # TypeScript 类型
│   │   ├── api/
│   │   │   ├── client.ts            # Axios 实例
│   │   │   └── endpoints.ts         # API 调用（v1.5扩展）
│   │   └── pages/
│   │       ├── Dashboard.tsx         # 教师工作台
│   │       ├── DataImport.tsx        # 数据导入
│   │       ├── ClassProfile.tsx      # 学情画像
│   │       ├── ModeFingerprint.tsx   # 模式指纹
│   │       ├── DiagnosisReport.tsx   # 诊断报告
│   │       ├── ComparisonAB.tsx      # A/B模式对比（v1.5）
│   │       ├── TeacherTrend.tsx      # 效能趋势（v1.5）
│   │       ├── CrossClassCompare.tsx # 跨班级对比（v1.5）
│   │       ├── ModeLibrary.tsx       # 模式库浏览（v1.5）
│   │       ├── ModeEditor.tsx        # 模式编辑器（v1.5）
│   │       └── KnowledgeMap.tsx      # 知识图谱（v1.5）
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── plans/
│   ├── development-plan.md          # 完整开发计划（v1.0→v3.0）
│   └── sprint-v1.5.md               # v1.5增量Sprint计划
├── .gitignore
├── README.md
└── LICENSE
```

---

## API 接口（23 个）

### 数据管理

| 方法 | 路径 | 说明 | 版本 |
|------|------|------|:----:|
| GET | `/api/courses` | 课程列表 | v1.0 |
| GET | `/api/courses/{id}` | 课程详情（含班级） | v1.0 |
| POST | `/api/courses` | 创建课程 | v1.0 |
| GET | `/api/classes?course_id=` | 班级列表 | v1.0 |
| GET | `/api/classes/{id}` | 班级详情（含学生） | v1.0 |

### 数据导入

| 方法 | 路径 | 说明 | 版本 |
|------|------|------|:----:|
| POST | `/api/import/courses` | CSV 导入课程 | v1.0 |
| POST | `/api/import/classes` | CSV 导入班级 | v1.0 |
| POST | `/api/import/students` | CSV 导入学生 | v1.0 |
| POST | `/api/import/grades` | CSV 导入成绩 | v1.0 |
| POST | `/api/import/observations` | CSV 导入课堂观察 | v1.0 |
| POST | `/api/import/evaluations` | CSV 导入教学评价 | v1.0 |

### 分析引擎

| 方法 | 路径 | 说明 | 版本 |
|------|------|------|:----:|
| GET | `/api/analysis/profile/{class_id}` | 六维班级学情画像 | v1.0 |
| GET | `/api/analysis/fingerprint/{class_id}` | 五维教学模式指纹 | v1.0 |
| GET | `/api/analysis/diagnosis/{class_id}` | 综合诊断报告 | v1.0 |
| GET | `/api/analysis/compare/modes?class_a=&class_b=` | A/B 模式对比（Cohen's d 效应量） | v1.5 |
| GET | `/api/analysis/compare/cross-teacher?course_id=` | 跨教师班级排名 | v1.5 |
| GET | `/api/analysis/trend/teacher?course_id=` | 学期效能趋势 | v1.5 |

### 教学模式库

| 方法 | 路径 | 说明 | 版本 |
|------|------|------|:----:|
| GET | `/api/modes/templates` | 内置模式模板列表 | v1.5 |
| GET | `/api/modes/templates/{id}` | 模板详情 | v1.5 |
| GET | `/api/modes/custom?course_id=` | 自定义模式列表 | v1.5 |
| POST | `/api/modes/custom` | 创建自定义模式 | v1.5 |
| PUT | `/api/modes/custom/{id}` | 编辑自定义模式 | v1.5 |
| DELETE | `/api/modes/custom/{id}` | 删除自定义模式 | v1.5 |
| GET | `/api/modes/recommend?class_id=` | 基于学情推荐模式 | v1.5 |
| GET | `/api/modes/knowledge-graph?course_id=` | 课程知识图谱 | v1.5 |

> 完整 API 文档：启动后端后访问 http://localhost:8000/docs

---

## 演示数据说明

运行 `python seed_data.py` 后，数据库包含：

| 实体 | 数量 | 说明 |
|------|:----:|------|
| 课程 | 4 | 数据结构、操作系统、计算机网络、软件工程 |
| 班级 | 8 | 每门课 2 个班 |
| 学生 | 80 | 每个班 10 人 |
| 成绩记录 | 100 | 期中/期末 + 多知识点 |
| 课堂观察 | 12 | 覆盖讲授型/互动型/实践型/混合型 |
| 教学评价 | 20 | 5 维度 × 4 班 |
| 教学模式模板 | 12 | 翻转课堂/PBL/BOPPPS/对分/5E/案例/混合/探究/讲练/同伴/游戏/研讨 |
| 知识图谱节点 | 15 | 数据结构课程知识点 |
| 知识图谱边 | 10 | 前置/并列依赖关系 |

### 推荐演示路径

1. **Dashboard** → 查看课程总览
2. **A/B 模式对比** → 选择 class_id=1 vs class_id=2，查看双雷达图 + Cohen's d
3. **学情画像** → 查看六维雷达图 + 薄弱知识点
4. **模式指纹** → 查看实践驱动型班级 (class_id=2)
5. **教学模式库** → 浏览 12 种内置教学模板
6. **知识图谱** → 选择"数据结构"课程，查看知识点依赖图 + 瓶颈预警
7. **诊断报告** → 综合诊断 + 模式适配建议

---

## 赛事信息

| 项目 | 内容 |
|------|------|
| 赛事 | 2026年"数据要素×"大赛山东分赛 |
| 赛道 | 教育创新赛道 |
| 赛题 | 教育教学应用与模式创新 |
| 参赛单位 | [填写学校名称] |

### 相关文档

- [项目申报书](./学程智枢_项目申报书.md)
- [上下文分析与推演过程](./学程智枢_上下文分析与讨论输出.md)
- [完整开发计划](./plans/development-plan.md)
- [v1.5 Sprint 计划](./plans/sprint-v1.5.md)

---

## 版本历史

| 版本 | 日期 | 提交 | 核心变更 |
|------|------|------|----------|
| **v1.5** | 2026-06-24 | `0a519eb` | A/B 对比引擎 + 12 模式模板库 + 知识图谱 + 6 新页面 + 侧边栏重构 |
| v1.0 | 2026-06-24 | `89e8a7d` | MVP：数据导入→画像→指纹→诊断核心闭环 |

---

## 许可证

MIT License

---

## 联系方式

- 项目负责人：[姓名]
- 邮箱：[email]
- 团队：[团队名称]
- GitHub：https://github.com/565003920/xczs-platform
