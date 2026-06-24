# 学程智枢 Frontend

数据驱动的教学过程智能诊断平台 · 前端 · v1.5

## 技术栈

- React 18 + TypeScript
- Ant Design 5.x (UI 组件)
- ECharts 5 + echarts-for-react (数据可视化)
- Vite 5 (构建工具)
- React Router v6 (路由)

## 快速开始

```bash
cd frontend
npm install
npm run dev          # http://localhost:5173
```

## 页面清单（11 页）

| 路由 | 页面 | 版本 |
|------|------|:----:|
| `/` | 教师工作台 Dashboard | v1.0 |
| `/import` | 数据导入 DataImport | v1.0 |
| `/compare/ab` | A/B 模式对比 ComparisonAB | v1.5 |
| `/compare/trend` | 效能趋势 TeacherTrend | v1.5 |
| `/compare/cross` | 跨班级对比 CrossClassCompare | v1.5 |
| `/profile` | 学情画像 ClassProfile | v1.0 |
| `/fingerprint` | 模式指纹 ModeFingerprint | v1.0 |
| `/modes/library` | 模式库浏览 ModeLibrary | v1.5 |
| `/modes/editor` | 模式编辑器 ModeEditor | v1.5 |
| `/modes/knowledge` | 知识图谱 KnowledgeMap | v1.5 |
| `/diagnosis` | 诊断报告 DiagnosisReport | v1.0 |

## 目录结构

```
src/
├── api/               # API 调用层
│   ├── client.ts      # Axios 实例（baseURL: /api）
│   └── endpoints.ts   # 全部接口函数
├── components/        # 通用组件（待扩展）
├── pages/             # 11 个页面组件
├── types/             # TypeScript 类型
├── App.tsx            # 根组件（二级菜单 + 路由）
├── main.tsx           # 入口
└── index.css          # 全局样式
```

## 开发约定

1. **组件命名**：页面组件 PascalCase，文件名与组件同名
2. **API 调用**：统一通过 `src/api/endpoints.ts` 导出
3. **状态管理**：useState + useEffect，不引入额外状态库
4. **样式**：优先使用 Ant Design 内置样式

## 构建部署

```bash
npm run build        # 输出到 dist/
npm run preview      # 预览构建结果
```
