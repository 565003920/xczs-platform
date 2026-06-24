# 学程智枢 (XueCheng ZhiShu) · v2.0

> 数据驱动的教学过程智能诊断与模式重构平台

2026年"数据要素×"大赛山东分赛 · 教育创新赛道 · 教育教学应用与模式创新 参赛项目

[开发计划](./plans/development-plan.md) · [GitHub](https://github.com/565003920/xczs-platform)

---

## 项目简介

学程智枢是一款面向高校教师的教学过程智能诊断平台。通过**五源数据融合分析**，构建从数据采集到数据资产化的完整闭环。支持 **DeepSeek / 通义千问** 大模型增强文本输出，未配置时自动回退规则引擎。

### 数据闭环

```
采集 ──→ 融合 ──→ 画像 ──→ 诊断 ──→ 对比 ──→ 推荐 ──→ 应用 ──→ 反馈 ──→ 资产化
 ✅       ✅       ✅       ✅        ✅       ✅       ✅       ✅        ✅
```

### 核心功能

| 功能 | 说明 |
|------|------|
| 🔐 **用户认证** | JWT 登录，教师/管理员双角色，数据按用户隔离 |
| 📥 **数据导入** | CSV 批量导入 6 类教学数据 |
| 📊 **教师工作台** | 课程卡片 → 点击展开该课所有授课班级 |
| 🎯 **学情画像** | 六维雷达图 + 薄弱/优势知识点 + 成绩分布 |
| 🔍 **模式指纹** | 五维雷达图 + 匹配 12 内置模板 + LLM 增强描述 |
| 📈 **对比分析** | A/B 双雷达图 + Cohen's d + 效能趋势 + 跨班排名 |
| 📚 **教学模式库** | 12 内置模板 + 创建/编辑/删除 + 详情弹窗 |
| 🗺️ **知识图谱** | 力导向依赖图 + 掌握率 + 瓶颈预警 |
| 👤 **个体画像** | 学生知识热力图 + 趋势 + 薄弱/优势 |
| 🔄 **模式迁移** | 跨课程相似度 + 优质模式推荐 |
| 📝 **智能备课** | 模板加载环节 + 等比缩放时长 + LLM 增强提示 |
| 💡 **课后反思** | 达成度 + 偏差分析 + LLM 增强建议 |
| 📦 **数据资产** | 资产目录 + 质量 + 血缘 + 仪表盘 + 审计日志 |
| 🔔 **通知中心** | 诊断/验证/预警通知 |
| 📋 **诊断报告** | 综合诊断 + LLM 增强建议 |

### AI 增强

| 模块 | LLM 增强 | 无 LLM 时 |
|------|----------|-----------|
| 诊断报告 | 综合建议文本 | 规则拼接 |
| 模式指纹 | 模式描述 + 建议 | 模板匹配 |
| 智能备课 | 教学提示 | 模板 strengths |
| 课后反思 | 改进建议 | 规则建议 |

```bash
# 配置方式：backend/.env
LLM_PROVIDER=deepseek     # 或 tongyi
LLM_API_KEY=sk-your-key
# 不配置 → 自动回退规则引擎，零影响
```

---

## 快速开始

```bash
git clone https://github.com/565003920/xczs-platform.git && cd xczs-platform

# 后端
cd backend && pip install -r requirements.txt && python seed_data.py
uvicorn app.main:app --reload --port 8000    # → http://localhost:8000/docs

# 前端
cd frontend && npm install && npm run dev     # → http://localhost:5173
```

**演示账号**：

| 用户 | 密码 | 角色 | 可见数据 |
|------|------|------|----------|
| `zhang` | `123456` | 教师 | 数据结构、软件工程（6 班） |
| `li` | `123456` | 教师 | 操作系统、数据库原理（6 班） |
| `wang` | `123456` | 教师 | 计算机网络、AI导论（5 班） |
| `admin` | `admin` | 管理员 | **全部 6 课 17 班** + 数据资产管理 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + TS + Ant Design 5 + ECharts 5 + Vite 5 |
| 后端 | Python FastAPI + SQLAlchemy + Pydantic |
| 认证 | HMAC-SHA256 JWT + 密码哈希 |
| AI | DeepSeek / 通义千问（可选） |
| 数据库 | SQLite（开发） |
| 分析 | Pandas + Cohen's d + 协同过滤 |

---

## 项目结构

```
xczs-platform/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口 (43 接口)
│   │   ├── config.py            # .env 加载 + DB URL
│   │   ├── models/              # 10 数据模型 (teaching/knowledge/audit/user)
│   │   ├── routers/             # 9 路由模块
│   │   └── services/            # 12 业务服务 (含 llm.py)
│   ├── sample_data/
│   ├── seed_data.py             # 程序化种子数据 (6课17班204生)
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.tsx              # 路由守卫 + 角色菜单
│       ├── contexts/AuthContext  # JWT 管理
│       ├── pages/               # 20 页面
│       └── components/          # NotificationBell
├── plans/                       # 开发计划
├── 学程智枢_项目申报书.md
└── README.md
```

---

## API 一览（43 个）

| 分类 | 数量 | 说明 |
|------|:----:|------|
| 认证 | 2 | 登录 + 当前用户 |
| 数据管理 | 5 | 课程/班级 CRUD |
| 导入 | 6 | CSV 批量导入 |
| 分析 | 6 | 画像/指纹/诊断 + A/B 对比 |
| 模式库 | 8 | 模板 CRUD + 推荐 + 知识图谱 |
| v2.0 | 16 | 个体画像/迁移/备课/反思/资产/血缘/仪表盘/审计/通知 |

---

## 许可证

MIT — [GitHub](https://github.com/565003920/xczs-platform)
