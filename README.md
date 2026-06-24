# 学程智枢 (XueCheng ZhiShu)

> 数据驱动的教学过程智能诊断与模式重构平台

2026年"数据要素×"大赛山东分赛 · 教育创新赛道 · 教育教学应用与模式创新 参赛项目

---

## 项目简介

学程智枢是一款面向高校教师的教学过程智能诊断平台。通过对教务数据、课堂行为、学生评教、学业成果和教学资源五源数据的融合分析，自动生成**班级学情画像**、**教学模式指纹**和**诊断报告**，帮助教师从经验驱动转向数据驱动的循证教学决策。

### 核心功能

| 功能 | 说明 |
|------|------|
| 📥 **数据导入** | 支持 CSV 批量导入课程、班级、学生、成绩、课堂观察、教学评价六类数据 |
| 📊 **教师工作台** | 课程卡片概览、班级/学生统计、一键跳转诊断 |
| 🎯 **学情画像** | 六维雷达图（知识掌握/参与度/互动质量/提问深度/实践均衡/满意度）+ 薄弱/优势知识点 |
| 🔍 **模式指纹** | 五维教学模式雷达图 + 模式自动识别（讲授型/互动型/实践型/混合型）+ 改进建议 |
| 📋 **诊断报告** | 综合诊断 + 教学模式适配建议 + 可打印导出 |

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
| 数据处理 | Pandas + scikit-learn |

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 9+

### 1. 克隆项目

```bash
git clone <repo-url>
cd xczs-platform
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python seed_data.py                    # 播种演示数据
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
│   │   ├── main.py                # FastAPI 入口
│   │   ├── config.py              # 配置（数据库URL等）
│   │   ├── database.py            # SQLAlchemy 引擎
│   │   ├── models/teaching.py     # 数据模型（6个实体）
│   │   ├── schemas/teaching.py    # Pydantic 请求/响应
│   │   ├── routers/
│   │   │   ├── courses.py         # 课程 CRUD
│   │   │   ├── classes_.py        # 班级 CRUD
│   │   │   ├── data_import.py     # CSV 导入
│   │   │   └── analysis_routes.py # 分析接口
│   │   └── services/
│   │       ├── profile.py         # 学情画像引擎
│   │       ├── fingerprint.py     # 模式指纹引擎
│   │       └── diagnosis.py       # 诊断报告引擎
│   ├── sample_data/               # 演示数据 CSV
│   ├── seed_data.py               # 数据播种
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx                # 布局 + 路由
│   │   ├── types/index.ts         # TypeScript 类型
│   │   ├── api/
│   │   │   ├── client.ts          # Axios 实例
│   │   │   └── endpoints.ts       # API 调用
│   │   └── pages/
│   │       ├── Dashboard.tsx       # 教师工作台
│   │       ├── DataImport.tsx      # 数据导入
│   │       ├── ClassProfile.tsx    # 学情画像
│   │       ├── ModeFingerprint.tsx # 模式指纹
│   │       └── DiagnosisReport.tsx # 诊断报告
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── docs/
│   └── screenshots/               # 界面截图
├── .gitignore
├── README.md
└── LICENSE
```

---

## API 接口

### 数据管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/courses` | 课程列表 |
| GET | `/api/courses/{id}` | 课程详情（含班级） |
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
| GET | `/api/analysis/profile/{class_id}` | 班级学情画像 |
| GET | `/api/analysis/fingerprint/{class_id}` | 教学模式指纹 |
| GET | `/api/analysis/diagnosis/{class_id}` | 综合诊断报告 |

> 完整 API 文档：启动后端后访问 http://localhost:8000/docs

---

## 演示数据说明

运行 `python seed_data.py` 后，数据库包含：

- **4 门课程**：数据结构、操作系统、计算机网络、软件工程
- **8 个班级**：每门课 2 个班
- **80 名学生**
- **100 条成绩记录**：涵盖期中/期末、多个知识点
- **12 条课堂观察**：覆盖不同教学模式（讲授型/互动型/实践型/混合型）
- **20 条教学评价**：5 个维度 × 4 个班

### 推荐演示路径

1. **Dashboard** → 查看课程总览
2. **数据导入** → 上传新的 CSV 文件体验导入流程
3. **学情画像** → 选择 2024级软件工程1班（class_id=1），查看六维雷达图
4. **模式指纹** → 选择 2024级软件工程2班（class_id=2），查看实践驱动型模式
5. **诊断报告** → 选择 2024级软件工程1班，查看综合诊断建议

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

---

## 许可证

MIT License

---

## 联系方式

- 项目负责人：[姓名]
- 邮箱：[email]
- 团队：[团队名称]
