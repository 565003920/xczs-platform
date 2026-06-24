# 学程智枢 Frontend · v2.0

数据驱动的教学过程智能诊断平台 · 前端 · 生态闭环

## 快速开始

```bash
cd frontend && npm install && npm run dev   # http://localhost:5173
```

## 页面清单（19 页）

| 分类 | 路由 | 页面 | 版本 |
|------|------|------|:----:|
| 核心 | `/` | 教师工作台 Dashboard | v1.0 |
| | `/import` | 数据导入 DataImport | v1.0 |
| | `/profile` | 学情画像 ClassProfile | v1.0 |
| | `/fingerprint` | 模式指纹 ModeFingerprint | v1.0 |
| | `/diagnosis` | 诊断报告 DiagnosisReport | v1.0 |
| 对比 | `/compare/ab` | A/B 对比 ComparisonAB | v1.5 |
| | `/compare/trend` | 效能趋势 TeacherTrend | v1.5 |
| | `/compare/cross` | 跨班对比 CrossClassCompare | v1.5 |
| 模式 | `/modes/library` | 模板浏览 ModeLibrary | v1.5 |
| | `/modes/editor` | 模式编辑器 ModeEditor | v1.5 |
| | `/modes/knowledge` | 知识图谱 KnowledgeMap | v1.5 |
| 工具 | `/tools/student` | 个体画像 StudentProfile | v2.0 |
| | `/tools/migration` | 模式迁移 ModeMigration | v2.0 |
| | `/tools/lesson-plan` | 智能备课 LessonPlanGenerator | v2.0 |
| | `/tools/reflection` | 课后反思 ReflectionReport | v2.0 |
| 资产 | `/assets/catalog` | 资产目录 DataCatalog | v2.0 |
| | `/assets/lineage` | 数据血缘 DataLineage | v2.0 |
| | `/assets/dashboard` | 效果仪表盘 EffectivenessDashboard | v2.0 |
| | `/assets/audit` | 审计日志 AuditLog | v2.0 |

## 技术栈

- React 18 + TypeScript
- Ant Design 5.x + ECharts 5
- Vite 5 + React Router v6

## 构建

```bash
npm run build && npm run preview
```
