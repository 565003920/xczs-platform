# 前端开发规范

## 技术栈

- React 18 + TypeScript (strict mode)
- Ant Design 5.x (UI 组件库)
- ECharts 5 (数据可视化)
- Vite 5 (构建工具)
- React Router v6 (路由)

## 目录结构

```
src/
├── api/           # API 调用层
│   ├── client.ts  # Axios 实例配置
│   └── endpoints.ts # 接口函数
├── components/    # 通用组件（待扩展）
├── pages/         # 页面组件
│   ├── Dashboard.tsx
│   ├── DataImport.tsx
│   ├── ClassProfile.tsx
│   ├── ModeFingerprint.tsx
│   └── DiagnosisReport.tsx
├── types/         # TypeScript 类型定义
│   └── index.ts
├── App.tsx        # 根组件（布局 + 路由）
├── main.tsx       # 入口
└── index.css      # 全局样式
```

## 开发约定

1. **组件命名**：页面组件 PascalCase，文件名与组件同名
2. **API 调用**：统一通过 `src/api/endpoints.ts` 导出，禁止页面直接使用 axios
3. **类型定义**：所有接口响应类型定义在 `src/types/index.ts`
4. **状态管理**：使用 React `useState` + `useEffect`，不引入额外状态库
5. **样式**：优先使用 Ant Design 组件内置样式，必要时使用内联 `style`
6. **中文文案**：所有面向用户的文案使用中文

## 本地开发

```bash
npm install
npm run dev          # http://localhost:5173
```

Vite 自动代理 `/api` 请求到 `http://localhost:8000`。

## 构建部署

```bash
npm run build        # 输出到 dist/
npm run preview      # 预览构建结果
```
