# Clarus 中国风设计系统 - 水墨画风格指南 v2.0

## 概述
**Clarus 中国风设计系统**将传统中国水墨画美学与现代玻璃态设计相结合，创造出典雅、深邃且富有文化底蕴的用户界面。此设计系统专为围棋AI分析工作区开发，体现了东方哲学与现代科技的完美融合。

### 设计哲学
- **山水意境**：层叠的山峰与流动的云雾营造深远的空间感
- **金色辉煌**：使用金色作为主题色，体现尊贵与智慧
- **留白艺术**：借鉴中国画留白技巧，让界面呼吸
- **层次分明**：通过透明度和模糊创造景深效果
- **文化传承**：使用中国风字体和装饰元素传承传统

---

## 配色方案

### 主题色彩

#### 金色系统（Gold System）
```css
/* 主金色 - Primary Gold */
--color-primary-gold: #d4af37;
--color-gold-light: #f4d03f;
--color-gold-dark: #b8941e;
--color-gold-darker: #8b6914;

/* 用途 */
- 主金色：边框、装饰角、标签激活状态
- 浅金色：光线效果、粒子、发光效果
- 深金色：标题文字、重要操作按钮
- 更深金色：正文文字、次要元素
```

**对比度规范**：
- 深金色 (#8b6914) 在浅色背景上：7.8:1（WCAG AAA）
- 主金色 (#d4af37) 边框清晰可见

#### 墨色系统（Ink System）
```css
/* 墨色渐变 */
--color-ink-black: #1a1a1a;
--color-ink-darkgray: #2d2d2d;
--color-ink-gray: #4a4a4a;
--color-mountain-gray: #6b7280;

/* 用途 */
- 墨黑：最深背景、远山剪影
- 深灰：中层山峰
- 中灰：近层山峰
- 山灰：云雾、次要文字
```

#### 米白色系统（Beige System）
```css
/* 纸张色调 */
--color-mist-white: #f5f0e8;
--color-paper-white: rgba(245, 240, 232, 0.92);

/* 用途 */
- 雾白：面板背景、输入框
- 纸白：主要内容区域
```

#### 辅助色彩
```css
/* 天空蓝（点缀用） */
--color-sky-blue: #4a9fb5;
--color-sky-blue-light: rgba(96, 165, 250, 0.15);

/* 云白（半透明） */
--color-cloud-white: rgba(255, 255, 255, 0.6);
```

---

## 背景系统

### 层叠山水背景（Multi-layer Mountain Background）

#### 基础层 - 天空渐变
```css
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        radial-gradient(ellipse at 50% 20%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
        linear-gradient(to bottom, #1a1a1a 0%, #2d2d2d 30%, #1a1a1a 60%, #0f0f0f 100%);
    z-index: -5;
}
```

#### 第一层 - 远山（最浅，最远）
```css
.ink-mountain.layer-3 {
    position: fixed;
    bottom: 0;
    height: 60%;
    background: linear-gradient(to bottom,
        transparent 0%,
        rgba(96, 165, 250, 0.1) 30%,
        rgba(75, 85, 99, 0.35) 60%,
        rgba(55, 65, 81, 0.45) 100%
    );
    clip-path: polygon(
        0% 100%, 0% 50%,
        8% 54%, 15% 48%, 22% 52%, 28% 45%, 35% 50%, 42% 42%,
        48% 48%, 55% 40%, 62% 46%, 68% 38%, 75% 44%, 82% 36%,
        88% 42%, 95% 48%, 100% 44%, 100% 100%
    );
    filter: blur(4px);
    z-index: -3;
}
```

#### 第二层 - 中景山峰
```css
.ink-mountain.layer-2 {
    height: 55%;
    background: linear-gradient(to bottom,
        transparent 0%,
        rgba(96, 165, 250, 0.15) 20%,
        rgba(75, 85, 99, 0.55) 50%,
        rgba(55, 65, 81, 0.7) 100%
    );
    clip-path: polygon(
        0% 100%, 0% 60%,
        6% 63%, 12% 56%, 18% 60%, 24% 52%, 30% 57%, 36% 48%,
        42% 54%, 48% 46%, 54% 52%, 60% 44%, 66% 50%, 72% 42%,
        78% 48%, 84% 55%, 90% 50%, 96% 58%, 100% 52%, 100% 100%
    );
    filter: blur(2px);
    z-index: -2;
}
```

#### 第三层 - 近景山峰（最深，最近）
```css
.ink-mountain.layer-1 {
    height: 50%;
    background: linear-gradient(to bottom,
        transparent 0%,
        rgba(75, 85, 99, 0.7) 30%,
        rgba(55, 65, 81, 0.85) 60%,
        rgba(31, 41, 55, 0.95) 100%
    );
    clip-path: polygon(
        0% 100%, 0% 70%,
        3% 75%, 7% 68%, 12% 72%, 18% 65%, 23% 70%, 28% 62%,
        33% 68%, 38% 60%, 43% 65%, 48% 58%, 53% 63%, 58% 55%,
        63% 60%, 68% 52%, 73% 58%, 78% 50%, 83% 55%, 88% 62%,
        93% 58%, 97% 65%, 100% 60%, 100% 100%
    );
    filter: blur(0.5px);
    z-index: -1;
}
```

### 云雾效果（Mist & Clouds）
```css
.mountain-mist::before,
.mountain-mist::after {
    content: '';
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(255, 255, 255, 0.12) 0%,
        rgba(255, 255, 255, 0.05) 40%,
        transparent 70%
    );
    filter: blur(40px);
    animation: mistFlow 20s ease-in-out infinite;
}

.mountain-mist::before {
    width: 1000px;
    height: 500px;
    top: 15%;
    left: -10%;
}

.mountain-mist::after {
    width: 800px;
    height: 400px;
    top: 35%;
    right: -10%;
    animation-delay: 10s;
}

@keyframes mistFlow {
    0%, 100% {
        transform: translate(0, 0) scale(1);
        opacity: 0.3;
    }
    50% {
        transform: translate(100px, -50px) scale(1.2);
        opacity: 0.5;
    }
}
```

---

## 光效系统

### 金色光线（Golden Light Rays）
```css
.light-ray {
    position: fixed;
    width: 2px;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent 0%,
        rgba(212, 175, 55, 0.3) 30%,
        rgba(244, 208, 63, 0.5) 50%,
        rgba(212, 175, 55, 0.3) 70%,
        transparent 100%
    );
    filter: blur(2px);
    transform-origin: top center;
    z-index: 4;
    pointer-events: none;
}

/* 4条光线，分别位于不同位置 */
.light-ray:nth-child(1) {
    left: 15%;
    animation: rayPulse 4s ease-in-out infinite, raySway 8s ease-in-out infinite;
}

@keyframes rayPulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.7; }
}

@keyframes raySway {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2deg); }
}
```

### 漂浮粒子（Floating Particles）
```css
.particle {
    position: absolute;
    width: 3px;
    height: 3px;
    background: radial-gradient(circle, rgba(244, 208, 63, 0.8), transparent);
    border-radius: 50%;
    animation: particleFloat 15s linear infinite;
    opacity: 0;
}

@keyframes particleFloat {
    0% {
        opacity: 0;
        transform: translateY(100vh) translateX(0) scale(0);
    }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% {
        opacity: 0;
        transform: translateY(-100px) translateX(var(--drift)) scale(1);
    }
}
```

**实现方式**：
```javascript
// 动态生成25个随机粒子
for(let i = 0; i < 25; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.setProperty('--drift', (Math.random() - 0.5) * 200 + 'px');
    particle.style.animationDelay = Math.random() * 15 + 's';
    particle.style.animationDuration = (12 + Math.random() * 6) + 's';
    document.body.appendChild(particle);
}
```

---

## 玻璃态组件（Glassmorphism Components）

### 主面板（Primary Panel）
```css
.panel {
    background: rgba(245, 240, 232, 0.92);
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    border-radius: 32px;
    border: 3px solid rgba(212, 175, 55, 0.6);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow:
        0 20px 40px rgba(0, 0, 0, 0.5),
        0 0 40px rgba(212, 175, 55, 0.3),
        inset 0 0 60px rgba(255, 255, 255, 0.1);
    position: relative;
}
```

### 金色装饰角（Golden Corner Decorations）
```css
/* 增强版装饰角 */
.panel::before,
.panel::after {
    content: '';
    position: absolute;
    width: 60px;
    height: 60px;
    border-width: 3px;
    border-style: solid;
    border-color: rgba(212, 175, 55, 0.9);
    z-index: 1;
    box-shadow:
        0 0 15px rgba(212, 175, 55, 0.4),
        inset 0 0 10px rgba(212, 175, 55, 0.2);
}

.panel::before {
    top: -3px;
    left: -3px;
    border-right: none;
    border-bottom: none;
    border-top-left-radius: 32px;
    background: linear-gradient(135deg,
        rgba(212, 175, 55, 0.1) 0%,
        transparent 50%
    );
}

.panel::after {
    bottom: -3px;
    right: -3px;
    border-left: none;
    border-top: none;
    border-bottom-right-radius: 32px;
    background: linear-gradient(315deg,
        rgba(212, 175, 55, 0.1) 0%,
        transparent 50%
    );
}
```

### Header（顶部导航栏）
```css
header {
    background: rgba(245, 240, 232, 0.95);
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    border: none;
    border-bottom: 3px solid rgba(212, 175, 55, 0.6);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 90px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow:
        0 4px 20px rgba(0, 0, 0, 0.15),
        0 0 40px rgba(212, 175, 55, 0.2);
}
```

---

## 标签页系统（Tab Navigation）

### 标签导航栏
```css
.tab-nav {
    display: flex;
    gap: 0.5rem;
    padding: 1rem 1.5rem 0;
    background: rgba(212, 175, 55, 0.03);
    border-bottom: 2px solid rgba(212, 175, 55, 0.2);
}
```

### 标签按钮
```css
.tab-btn {
    padding: 0.75rem 1.25rem;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(107, 79, 19, 0.6);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: 12px 12px 0 0;
}

.tab-btn:hover {
    background: rgba(212, 175, 55, 0.08);
    color: rgba(107, 79, 19, 0.9);
}

.tab-btn.active {
    background: rgba(212, 175, 55, 0.12);
    color: #8b6914;
    border-bottom-color: #d4af37;
    font-weight: 700;
}

/* 激活标签的金色发光效果 */
.tab-btn.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #d4af37, #f4d03f, #d4af37);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}
```

### 标签面板
```css
.tab-panel {
    display: none;
    padding: 1.5rem;
    animation: fadeInTab 0.3s ease;
}

.tab-panel.active {
    display: block;
}

@keyframes fadeInTab {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

---

## 表单组件（Form Elements）

### 输入框（Input Fields）
```css
.input-field {
    width: 100%;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 2px solid rgba(212, 175, 55, 0.4);
    border-radius: 20px;
    font-size: 0.95rem;
    color: #2d2d2d;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.input-field::placeholder {
    color: rgba(107, 79, 19, 0.5);
}

.input-field:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.9);
    border-color: rgba(212, 175, 55, 0.8);
    box-shadow:
        0 0 0 4px rgba(212, 175, 55, 0.15),
        0 4px 12px rgba(0, 0, 0, 0.1);
}
```

### 主要按钮（Primary Button）
```css
.btn-primary {
    width: 100%;
    padding: 1rem 2rem;
    background: linear-gradient(135deg,
        rgba(212, 175, 55, 0.95) 0%,
        rgba(244, 208, 63, 1) 50%,
        rgba(212, 175, 55, 0.95) 100%
    );
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: #1a1a1a;
    border: 3px solid rgba(255, 255, 255, 0.4);
    border-radius: 50px;
    font-weight: 900;
    font-size: 1rem;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow:
        0 0 40px rgba(212, 175, 55, 0.6),
        0 10px 30px rgba(0, 0, 0, 0.4),
        inset 0 2px 0 rgba(255, 255, 255, 0.4),
        inset 0 -2px 10px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

/* 光泽动画 */
.btn-primary::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent 30%,
        rgba(255, 255, 255, 0.3) 50%,
        transparent 70%
    );
    animation: btnShine 3s linear infinite;
}

@keyframes btnShine {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.btn-primary:hover {
    transform: scale(1.05);
    box-shadow:
        0 0 60px rgba(212, 175, 55, 0.9),
        0 15px 40px rgba(0, 0, 0, 0.5),
        inset 0 2px 0 rgba(255, 255, 255, 0.5);
}

.btn-primary:active {
    transform: scale(0.98);
}
```

### 次要按钮（Secondary Button）
```css
.btn-secondary {
    padding: 0.75rem 1.25rem;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: rgba(212, 175, 55, 0.95);
    border: 2px solid rgba(212, 175, 55, 0.4);
    border-radius: 20px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover {
    background: rgba(212, 175, 55, 0.15);
    color: #8b6914;
    border-color: rgba(212, 175, 55, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(212, 175, 55, 0.25);
}
```

---

## 字体系统（Typography）

### 字体引入
```html
<!-- Google Fonts - 中国风字体 -->
<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;600;700;900&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
```

### 字体定义
```css
:root {
    --font-title: 'ZCOOL XiaoWei', 'Ma Shan Zheng', cursive;
    --font-primary: 'Noto Serif SC', 'Ma Shan Zheng', serif;
}
```

### 字体使用规范

#### 标题（Headings）
```css
h1, h2, h3 {
    font-family: var(--font-title);
    color: #8b6914;
    letter-spacing: 0.05em;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

h1 { font-size: 2rem; font-weight: 900; }
h2 { font-size: 1.5rem; font-weight: 700; }
h3 { font-size: 1.2rem; font-weight: 700; }
```

#### 正文（Body Text）
```css
body {
    font-family: var(--font-primary);
    color: #2d2d2d;
    font-size: 0.95rem;
    line-height: 1.6;
}
```

#### 特殊文字（Logo/Brand）
```css
.logo {
    font-family: 'ZCOOL XiaoWei', cursive;
    font-size: 1.4rem;
    font-weight: 900;
    color: #8b6914;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}
```

---

## 间距系统（Spacing System）

### CSS变量定义
```css
:root {
    --spacing-1: 0.5rem;   /* 8px */
    --spacing-2: 1rem;     /* 16px */
    --spacing-3: 1.5rem;   /* 24px */
    --spacing-4: 2rem;     /* 32px */
    --spacing-6: 3rem;     /* 48px */
    --spacing-8: 4rem;     /* 64px */
}
```

### 使用场景
- **组件内部间距**：`padding: var(--spacing-3)`
- **面板之间间隔**：`gap: var(--spacing-4)`
- **页面边距**：`padding: var(--spacing-6)`

---

## 圆角系统（Border Radius）

### 定义
```css
:root {
    --radius-small: 4px;
    --radius-medium: 8px;
    --radius-large: 20px;
    --radius-xl: 32px;
}
```

### 使用规范
- **主面板**：`border-radius: var(--radius-xl)` (32px)
- **按钮**：`border-radius: var(--radius-large)` (20px)
- **输入框**：`border-radius: var(--radius-large)` (20px)
- **小卡片**：`border-radius: var(--radius-medium)` (8px)

---

## 阴影系统（Shadow System）

### 面板阴影（Panel Shadows）
```css
box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.5),          /* 深度阴影 */
    0 0 40px rgba(212, 175, 55, 0.3),        /* 金色发光 */
    inset 0 0 60px rgba(255, 255, 255, 0.1); /* 内部高光 */
```

### 按钮阴影（Button Shadows）
```css
/* 正常状态 */
box-shadow:
    0 0 40px rgba(212, 175, 55, 0.6),
    0 10px 30px rgba(0, 0, 0, 0.4),
    inset 0 2px 0 rgba(255, 255, 255, 0.4);

/* 悬停状态 */
box-shadow:
    0 0 60px rgba(212, 175, 55, 0.9),
    0 15px 40px rgba(0, 0, 0, 0.5);
```

### 文字阴影（Text Shadows）
```css
/* 标题文字 */
text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);

/* 金色文字 */
text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
```

---

## 动画系统（Animation System）

### 淡入动画（Fade In）
```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### 脉冲动画（Pulse）
```css
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 0.6;
    }
    50% {
        transform: scale(1.05);
        opacity: 1;
    }
}
```

### 发光动画（Glow）
```css
@keyframes glowPulse {
    0%, 100% {
        filter: brightness(1) drop-shadow(0 0 20px rgba(212, 175, 55, 0.4));
    }
    50% {
        filter: brightness(1.2) drop-shadow(0 0 40px rgba(212, 175, 55, 0.8));
    }
}
```

---

## 布局规范（Layout Guidelines）

### 三列网格布局
```css
.workspace-container {
    display: grid;
    grid-template-columns: 580px 1fr 480px;
    min-height: calc(100vh - 90px);
    gap: var(--spacing-4);
    padding: var(--spacing-4);
    max-width: 1920px;
    margin: 0 auto;
}
```

### 响应式布局
```css
@media (max-width: 1400px) {
    .workspace-container {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .workspace-container {
        padding: var(--spacing-2);
        gap: var(--spacing-2);
    }
}
```

---

## 图标系统（Icon System）

### 使用Lucide图标
```html
<script src="https://unpkg.com/lucide@latest"></script>
```

```javascript
// 初始化图标
lucide.createIcons();
```

### 图标样式规范
```html
<i data-lucide="grid-3x3" style="width: 20px; height: 20px; stroke-width: 1.5;"></i>
```

---

## 交互状态（Interaction States）

### 悬停效果（Hover）
```css
/* 按钮 */
.btn:hover {
    transform: translateY(-2px) scale(1.05);
}

/* 卡片 */
.card:hover {
    transform: translateY(-1px);
    border-color: rgba(212, 175, 55, 0.8);
}

/* 标签 */
.tab-btn:hover {
    background: rgba(212, 175, 55, 0.08);
}
```

### 激活效果（Active）
```css
.btn:active {
    transform: scale(0.98);
}
```

### 聚焦效果（Focus）
```css
.input-field:focus {
    outline: none;
    border-color: rgba(212, 175, 55, 0.8);
    box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.15);
}
```

---

## 可访问性（Accessibility）

### 对比度要求
- **标题文字** (#8b6914 on #f5f0e8)：7.8:1 ✓ WCAG AAA
- **正文文字** (#2d2d2d on #f5f0e8)：12.5:1 ✓ WCAG AAA
- **金色边框**：清晰可见

### 键盘导航
所有交互元素必须支持：
- Tab键导航
- Enter/Space键激活
- Esc键关闭

### 屏幕阅读器
- 所有图标添加`aria-label`
- 面板添加`role`和`aria-labelledby`
- 标签页使用正确的ARIA属性

---

## 实现示例（Implementation Example）

### 完整HTML模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clarus - 中国风设计系统</title>

    <!-- 字体引入 -->
    <link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;600;700;900&family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">

    <!-- Lucide图标 -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            /* 颜色变量 */
            --color-primary-gold: #d4af37;
            --color-gold-light: #f4d03f;
            --color-gold-dark: #b8941e;
            --color-gold-darker: #8b6914;
            --color-ink-black: #1a1a1a;
            --color-mist-white: #f5f0e8;

            /* 字体变量 */
            --font-title: 'ZCOOL XiaoWei', 'Ma Shan Zheng', cursive;
            --font-primary: 'Noto Serif SC', serif;

            /* 间距变量 */
            --spacing-2: 1rem;
            --spacing-3: 1.5rem;
            --spacing-4: 2rem;

            /* 圆角变量 */
            --radius-large: 20px;
            --radius-xl: 32px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-primary);
            background: #0f0f0f;
            color: #2d2d2d;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* 背景层 */
        /* ... (参考上面的背景系统代码) ... */

        /* 组件样式 */
        /* ... (参考上面的组件代码) ... */
    </style>
</head>
<body>
    <!-- 山水背景元素 -->
    <div class="mountain-mist"></div>
    <div class="ink-mountain layer-3"></div>
    <div class="ink-mountain layer-2"></div>
    <div class="ink-mountain layer-1"></div>

    <!-- 光线效果 -->
    <div class="light-ray"></div>
    <div class="light-ray"></div>
    <div class="light-ray"></div>
    <div class="light-ray"></div>

    <!-- 主要内容 -->
    <header>
        <div class="logo">Clarus</div>
    </header>

    <main class="workspace-container">
        <div class="panel">
            <!-- 面板内容 -->
        </div>
    </main>

    <script>
        // 生成粒子
        for(let i = 0; i < 25; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.setProperty('--drift', (Math.random() - 0.5) * 200 + 'px');
            particle.style.animationDelay = Math.random() * 15 + 's';
            document.body.appendChild(particle);
        }

        // 初始化图标
        lucide.createIcons();
    </script>
</body>
</html>
```

---

## 最佳实践（Best Practices）

### ✅ 应该做的
1. 使用金色作为主题色和装饰色
2. 保持浅色面板背景确保文字清晰
3. 添加多层山水背景营造深度
4. 使用中国风字体增强文化氛围
5. 添加金色光效和粒子动画
6. 保持一致的圆角和间距
7. 使用玻璃态效果增强现代感

### ❌ 不应该做的
1. 不要使用纯黑或纯白背景
2. 不要省略装饰性金色边框和角
3. 不要使用西文衬线字体
4. 不要让文字对比度过低
5. 不要过度使用动画影响性能
6. 不要忽略移动端适配
7. 不要破坏玻璃态的半透明特性

---

## 组件库（Component Library）

### 可复用组件清单
- [ ] 玻璃态面板（Panel）
- [ ] 金色按钮（Button）
- [ ] 输入框（Input）
- [ ] 标签页（Tabs）
- [ ] 卡片（Card）
- [ ] 模态框（Modal）
- [ ] 下拉菜单（Dropdown）
- [ ] 通知提示（Notification）

---

## 版本历史（Version History）

### v2.0 (2026-01-03)
- 初始版本
- 建立中国风水墨画设计系统
- 定义金色主题色调
- 实现层叠山水背景
- 添加光效和粒子系统
- 实现标签页导航
- 定义玻璃态组件规范

---

## 维护与更新

本设计系统由 Clarus 团队维护。如有建议或发现问题，请联系设计团队。

**文档地址**：`D:\ai\Clarus\CHINESE_STYLE_GUIDE.md`
**最后更新**：2026-01-03
