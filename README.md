# DDoSeek 智能DDoS检测防护系统

## 项目概述

DDoSeek是一个基于SDN的智能DDoS检测防护系统，结合DeepSeek技术，面向云平台用户和网络管理员。系统提供完整的DDoS检测、防护、分析和管理功能。

## 系统架构

### 技术栈
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **后端**: Python, Flask
- **网络**: Mininet, Ryu SDN控制器
- **AI模型**: CNN+GRU深度学习模型
- **UI框架**: Ant Design风格
- **数据可视化**: ECharts

## 页面结构

系统包含9个核心页面，采用统一的设计语言和导航结构：

### 1. 登录认证页面 (`login.html`)
- **功能**: 用户身份验证、安全登录
- **特性**: SSL加密提示、记住登录状态、自动跳转、安全检查
- **面包屑**: 无（入口页面）

### 2. 系统仪表盘 (`dashboard.html`) 
- **功能**: 系统概览、KPI监控、实时数据展示
- **特性**: 4个KPI指标卡片、实时网络流量图表、DDoS攻击分布、系统状态监控
- **面包屑**: 首页 / 系统仪表盘

### 3. 网络监测中心 (`network-monitor.html`)
- **功能**: 网络拓扑监控、带宽分析、链路状态管理
- **特性**: 5个网络KPI、实时时延监控、网络拓扑可视化、带宽统计
- **面包屑**: 首页 / 系统仪表盘 / 网络监测中心

### 4. DDoS检测防护 (`ddos-detection.html`)
- **功能**: 威胁检测、攻击防护、实时监控
- **特性**: 威胁态势分析、攻击类型识别、防护策略配置、智能建议
- **面包屑**: 首页 / 系统仪表盘 / DDoS检测防护

### 5. 防火墙管理 (`firewall-management.html`)
- **功能**: 防火墙规则管理、访问控制、流量过滤
- **特性**: 规则CRUD操作、黑白名单管理、实时日志、快速操作面板
- **面包屑**: 首页 / 系统仪表盘 / 防火墙管理

### 6. 智能日志中心 (`log-center.html`)
- **功能**: 日志采集、分析、可视化展示
- **特性**: 实时日志流、智能过滤、AI分析、多维度统计
- **面包屑**: 首页 / 系统仪表盘 / 智能日志中心

### 7. DeepSeek AI助手 (`deepseek-assistant.html`)
- **功能**: AI智能对话、威胁分析、知识问答
- **特性**: 实时聊天界面、智能回复、威胁监控、知识库搜索
- **面包屑**: 首页 / 系统仪表盘 / DeepSeek AI助手

### 8. 规则配置中心 (`rule-config.html`)
- **功能**: 安全规则管理、策略配置、模板编辑
- **特性**: 规则分类管理、可视化编辑器、模板系统、实时预览
- **面包屑**: 首页 / 系统仪表盘 / 规则配置中心

### 9. 系统测试平台 (`system-test.html`)
- **功能**: 系统测试、性能评估、攻击模拟
- **特性**: 多种测试场景、实时监控、结果分析、报告导出
- **面包屑**: 首页 / 系统仪表盘 / 系统测试平台

## 路由功能完善

### 核心组件

#### 1. 路由管理器 (`router.js`)
统一的路由管理系统，提供以下功能：

**身份验证管理**
- 自动检查登录状态
- 24小时登录过期机制
- 未登录自动跳转到登录页面
- 安全退出登录功能

**导航功能**
- 统一的侧边栏导航管理
- 当前页面高亮显示
- 页面状态持久化存储
- 页面切换动画效果

**键盘快捷键**
- `Ctrl/Cmd + 1-8`: 快速导航到对应页面
- `ESC`: 返回系统仪表盘
- `Ctrl/Cmd + Shift + L`: 快速退出登录
- `F5 / Ctrl+R`: 刷新页面（保存状态）

**用户界面增强**
- 用户菜单（个人资料、系统设置、帮助中心）
- 系统通知面板（实时威胁、系统警告、更新信息）
- 快捷键提示（首次访问时显示）
- 页面加载动画效果

**页面生命周期管理**
- 页面可见性检测（标签页切换时暂停更新）
- 自动重新验证身份
- 资源优化管理

### 导航一致性

#### 统一的侧边栏结构
所有页面都采用相同的导航结构，确保用户体验一致性：

```html
<aside class="sidebar">
    <ul class="sidebar-menu">
        <li><a href="dashboard.html"><i class="fas fa-tachometer-alt"></i>系统仪表盘</a></li>
        <li><a href="network-monitor.html"><i class="fas fa-network-wired"></i>网络监测中心</a></li>
        <li><a href="ddos-detection.html"><i class="fas fa-shield-virus"></i>DDoS检测防护</a></li>
        <li><a href="firewall-management.html"><i class="fas fa-fire-extinguisher"></i>防火墙管理</a></li>
        <li><a href="log-center.html"><i class="fas fa-file-alt"></i>智能日志中心</a></li>
        <li><a href="deepseek-assistant.html"><i class="fas fa-robot"></i>DeepSeek AI助手</a></li>
        <li><a href="rule-config.html"><i class="fas fa-cogs"></i>规则配置中心</a></li>
        <li><a href="system-test.html"><i class="fas fa-vial"></i>系统测试平台</a></li>
    </ul>
</aside>
```

#### 面包屑导航
每个页面都包含清晰的面包屑导航，帮助用户了解当前位置：

```html
<nav class="breadcrumb">
    <span><i class="fas fa-home"></i> 首页</span>
    <span>/</span>
    <span><a href="dashboard.html">系统仪表盘</a></span>
    <span>/</span>
    <span>当前页面</span>
</nav>
```

### 设计系统

#### 视觉一致性
- **主题**: 浅色主题，采用浅灰蓝色渐变背景
- **毛玻璃效果**: 所有卡片和面板都使用毛玻璃效果
- **图标系统**: 统一使用FontAwesome图标
- **颜色编码**: 一致的状态和威胁等级颜色方案
- **响应式设计**: 支持各种屏幕尺寸

#### 交互体验
- **页面切换动画**: 平滑的页面过渡效果
- **悬浮反馈**: 按钮和链接的悬浮效果
- **加载状态**: 明确的加载和处理状态指示
- **消息提示**: 统一的成功/错误/警告消息系统

## 使用说明

### 快速开始

1. **登录系统**
   - 访问 `login.html`
   - 使用默认账户：用户名 `admin`，密码 `admin123`
   - 可选择"记住我"功能

2. **导航使用**
   - 点击侧边栏菜单进行页面切换
   - 使用键盘快捷键快速导航
   - 点击面包屑导航快速返回

3. **系统功能**
   - 仪表盘：查看系统概览和实时数据
   - 网络监测：监控网络状态和拓扑结构
   - DDoS防护：配置和管理威胁防护策略
   - 防火墙：管理访问控制规则
   - 日志中心：查看和分析系统日志
   - AI助手：获得智能分析和建议
   - 规则配置：编辑和管理安全规则
   - 系统测试：进行系统性能和安全测试

### 开发部署

1. **文件结构**
   ```
   DDoSeek/
   ├── login.html              # 登录页面
   ├── dashboard.html           # 系统仪表盘
   ├── network-monitor.html     # 网络监测中心
   ├── ddos-detection.html      # DDoS检测防护
   ├── firewall-management.html # 防火墙管理
   ├── log-center.html          # 智能日志中心
   ├── deepseek-assistant.html  # DeepSeek AI助手
   ├── rule-config.html         # 规则配置中心
   ├── system-test.html         # 系统测试平台
   ├── router.js               # 路由管理器
   └── README.md               # 说明文档
   ```

2. **部署要求**
   - 现代Web浏览器（Chrome 80+, Firefox 75+, Safari 13+）
   - HTTP/HTTPS服务器（推荐Nginx或Apache）
   - 支持JavaScript ES6+语法

3. **配置说明**
   - 所有页面都引用 `router.js` 进行路由管理
   - 使用localStorage进行状态持久化
   - CDN资源包括FontAwesome和ECharts

## 技术特性

### 性能优化
- **懒加载**: 图表和数据按需加载
- **资源复用**: 共享的CSS和JavaScript组件
- **缓存策略**: 合理的localStorage使用
- **响应式图表**: 自动适配屏幕尺寸

### 安全特性
- **身份验证**: 完整的登录/登出流程
- **会话管理**: 自动过期和状态检查
- **输入验证**: 表单数据验证和清理
- **XSS防护**: 安全的DOM操作

### 可扩展性
- **模块化设计**: 组件化的页面结构
- **统一API**: 一致的数据接口设计
- **插件架构**: 易于添加新功能模块
- **主题系统**: 支持自定义主题和样式

## 版本信息

- **当前版本**: v2.1.0
- **发布日期**: 2025年
- **开发状态**: 生产就绪
- **维护状态**: 持续更新

## 联系信息

- **项目名称**: DDoSeek 智能DDoS检测防护系统
- **技术支持**: 专业的DDoS检测防护解决方案
- **文档更新**: 随系统版本同步更新

---

*本文档详细介绍了DDoSeek系统的完整路由功能和使用说明。如有疑问，请参考各页面的内置帮助系统或联系技术支持。* 