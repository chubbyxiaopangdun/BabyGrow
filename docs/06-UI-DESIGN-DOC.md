# BabyGrow · UI 设计文档

> 更新日期：2026-05-01 | 状态：定稿
> 用途：UI 设计规范，设计系统，高保真原型参考

---

## 一、设计系统

### 1.1 色彩体系

**主色（柔和薄荷绿）：**
```
--mint:   #7EC8B8  （主色，按钮/链接/强调）
--mint-l: #D4EDE5  （浅薄荷，卡片背景）
--mint-xl:#EDF7F3  （极浅薄荷，标签选中）
```

**辅助色（柔和暖色）：**
```
--peach:   #E8A87C  （桃色，温暖强调）
--peach-l: #F5DCC8  （浅桃色）
--peach-xl:#FDF0E6  （极浅桃色）

--sky:     #8BB8D6  （天蓝色，信息/辅助）
--sky-l:   #CEE0F0  （浅天蓝）
--sky-xl:  #EAF3FA  （极浅天蓝）

--lav:     #B5A3CC  （薰衣草，AI/特殊）
--lav-l:   #DDD4EB  （浅薰衣草）
--lav-xl:  #F0EBF6  （极浅薰衣草）

--rose:    #D4A0A0  （玫瑰色，警告/删除）
--rose-l:  #F0D4D4  （浅玫瑰）
--rose-xl: #FAEAEA  （极浅玫瑰）
```

**中性色：**
```
--cream:  #FDF9F3  （主背景，温暖奶油白）
--cream2: #F5EFE6  （次级背景）
--cream3: #EDE6DA  （分隔线/分割）
--card:   #FFFFFF  （卡片背景）
```

**文字色：**
```
--ink:  #3C3C3C  （主文字，近黑）
--ink2: #6E6E73  （次要文字）
--ink3: #A0A0A5  （辅助文字）
--ink4: #C7C7CC  （最浅文字）
```

**语义色：**
```
--ok:   #8CC5A0  （成功/正常）
--warn: #E8C76A  （警告/关注）
--err:  #D48A8A  （错误/危险）
```

### 1.2 字体规范

```css
/* 字体栈 */
--font: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;

/* 字体层级 */
font-size: 34px  /* 大标题（页面标题） */
font-size: 28px  /* 页面标题 */
font-size: 24px  /* 个人中心名字 */
font-size: 20px  /* 卡片标题 */
font-size: 17px  /* 正文/列表标题 */
font-size: 16px  /* 按钮文字 */
font-size: 15px  /* 次要内容 */
font-size: 14px  /* 描述文字 */
font-size: 13px  /* 标签/辅助文字 */
font-size: 12px  /* 小标签 */
font-size: 11px  /* 最小文字 */
font-size: 10px  /* Tab Bar 标签 */
```

### 1.3 间距系统（8pt 网格）

```css
--sp-1:  4px   /* 极小间距 */
--sp-2:  8px   /* 小间距 */
--sp-3:  12px  /* 中小间距 */
--sp-4:  16px  /* 标准间距（卡片内边距） */
--sp-5:  20px  /* 中等间距 */
--sp-6:  24px  /* 大间距 */
--sp-8:  32px  /* 超大间距 */
--sp-10: 40px  /* 页面顶部留白 */
```

### 1.4 圆角规范

```css
--r-xs:  6px    /* 标签、小按钮 */
--r-sm:  10px   /* 输入框、次级卡片 */
--r-md:  14px   /* 主卡片、列表 */
--r-lg:  16px   /* 大卡片 */
--r-xl:  22px   /* 超大圆角元素 */
--r-full: 9999px /* 胶囊按钮、头像 */
```

### 1.5 阴影规范

```css
--sh-sm:  0 1px 4px rgba(0,0,0,.03)    /* 悬浮卡片 */
--sh-md:  0 4px 16px rgba(0,0,0,.05)   /* 标准卡片 */
--sh-lg:  0 8px 32px rgba(0,0,0,.08)   /* 弹窗浮层 */
```

---

## 二、组件规范

### 2.1 按钮

**主按钮（CTA）：**
```css
.btn-primary {
  width: 100%;
  background: var(--mint);
  color: #fff;
  border: none;
  border-radius: 14px;
  padding: 16px;
  font-size: 17px;
  font-weight: 600;
  min-height: 54px;
}
```

**次按钮：**
```css
.btn-secondary {
  background: var(--cream2);
  color: var(--ink);
  border: none;
  border-radius: 12px;
  padding: 12px 20px;
  font-size: 15px;
  min-height: 44px;
}
```

**文字按钮：**
```css
.btn-text {
  background: none;
  border: none;
  color: var(--mint);
  font-size: 15px;
  font-weight: 500;
  min-height: 44px;
}
```

### 2.2 卡片

**标准卡片：**
```css
.card {
  background: var(--card);
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,.03);
}
```

**Hero 卡片：**
```css
.hero-card {
  background: linear-gradient(135deg, var(--mint-l), var(--sky-l));
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(126,200,184,.15);
}
```

### 2.3 列表项

**标准列表项：**
```css
.row {
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 12px;
  min-height: 50px;
}
.row-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.row-title {
  font-size: 17px;
  color: var(--ink);
}
.row-sub {
  font-size: 13px;
  color: var(--ink2);
}
```

### 2.4 输入框

```css
.form-input {
  width: 100%;
  background: var(--card);
  border: 1px solid var(--sep);
  border-radius: 12px;
  padding: 14px 16px;
  font-size: 17px;
  color: var(--ink);
  min-height: 50px;
}
.form-input:focus {
  border-color: var(--mint);
}
```

### 2.5 Tab Bar

```css
.tabbar {
  position: absolute;
  bottom: 0;
  height: 83px;
  background: rgba(253,249,243,.85);
  backdrop-filter: blur(20px);
  border-top: .5px solid var(--sep);
  display: flex;
  justify-content: space-around;
  padding-top: 6px;
}
.tab {
  min-width: 64px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.tab svg { width: 26px; height: 26px; }
.tab span { font-size: 10px; }
```

---

## 三、页面设计规范

### 3.1 Welcome 引导页

**布局：**
- 顶部：Logo + 标题 + 副标题
- 中部：表单（姓名/生日/性别/喂养方式/关心问题）
- 底部：CTA 按钮

**交互：**
- 性别选择：Segmented Control
- 关心问题：可多选 Tag
- CTA 按钮：点击后进入首页

### 3.2 Home 首页

**布局：**
- 顶部：孩子信息 + 设置按钮
- Hero：今日重点卡片（呼吸光晕动画）
- 快捷入口：2×2 网格
- 记录列表：iOS 分组列表
- AI 建议：浮动条（漂浮动画）
- 底部：Tab Bar

**动效：**
- Hero 卡片：breathe 动画
- 快捷卡片：hover 上浮
- AI 浮动条：float 动画
- Tab 切换：indicator 滑动

### 3.3 Schedule 日程页

**布局：**
- 顶部：导航栏（返回 + 标题）
- 日期显示
- 时间轴：左侧时间 + 右侧卡片
- 当前时间：脉冲动画

**交互：**
- 时间轴竖线连接
- 当前时间高亮
- 卡片可点击展开

### 3.4 AI Chat 对话页

**布局：**
- 顶部：导航栏
- 消息区：气泡列表
- 快捷问题：标签列表
- 输入区：输入框 + 发送按钮

**交互：**
- 消息：用户右对齐（mint），AI 左对齐（white）
- 打字动画：三个跳动圆点
- 快捷问题：点击直接发送

### 3.5 Milestones 里程碑页

**布局：**
- 顶部：导航栏 + 月龄大数字
- 分类卡片：2×2 网格
- 里程碑列表：可打勾

**交互：**
- 打勾：bounceIn 动画 + 彩纸爆发
- 分类卡片：scaleIn 动画

### 3.6 Profile 个人中心页

**布局：**
- 头像（渐变旋转光环）
- 名字/信息
- 编辑按钮
- 设置列表

---

## 四、动效规范

### 4.1 动画时长

```css
即时反馈:  100ms   按钮点击、开关切换
标准过渡:  300ms   页面切换、列表展开
复杂动画:  400ms   弹窗出现、页面入场
延迟叠加:  50ms/项  列表项逐个入场
```

### 4.2 缓动函数

```css
--ease-spring: cubic-bezier(.34, 1.56, .64, 1)  /* 弹性效果 */
--ease-out:    cubic-bezier(.25, .46, .45, .94)  /* 出场动画 */
--ease-in:     cubic-bezier(.4, 0, 1, 1)         /* 入场动画 */
```

### 4.3 动画清单

| 动画 | 时长 | 缓动 | 用途 |
|------|------|------|------|
| slideUp | 400ms | spring | 卡片入场 |
| fadeIn | 300ms | ease | 页面淡入 |
| scaleIn | 350ms | spring | 弹窗/卡片缩放 |
| breathe | 4s | ease-in-out | Hero 卡片呼吸 |
| float | 4s | ease-in-out | AI 浮动条 |
| shimmer | 3s | ease-in-out | CTA 光扫 |
| pulse | 2s | ease-in-out | Tab 图标脉冲 |
| confettiFall | 1.2s | ease | 彩纸下落 |
| bounceIn | 400ms | spring | 打勾弹跳 |
| ringDraw | 1.2s | ease | 环形进度 |

---

## 五、设备适配

### 5.1 设计尺寸

```
基准宽度: 375px (iPhone SE)
适配范围: 320px ~ 428px
设计高度: 812px (iPhone X+)
```

### 5.2 安全区域

```css
body {
  padding-top: env(safe-area-inset-top, 20px);
  padding-bottom: calc(83px + env(safe-area-inset-bottom, 20px));
}
.tabbar {
  height: calc(60px + env(safe-area-inset-bottom));
  padding-bottom: env(safe-area-inset-bottom);
}
```

### 5.3 PWA 支持

```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#7EC8B8">
<link rel="manifest" href="manifest.json">
```

---

## 六、高保真原型

### 6.1 原型文件

| 页面 | 文件 | 说明 |
|------|------|------|
| Welcome | `babygrow-final.html` | 引导页 + 表单 |
| Home | `babygrow-final.html` | 首页仪表盘 |
| Schedule | `babygrow-final.html` | 日程时间轴 |
| AI Chat | `babygrow-final.html` | 对话界面 |
| Milestones | `babygrow-final.html` | 里程碑追踪 |
| Profile | `babygrow-final.html` | 个人中心 |

### 6.2 原型交互

- ✅ Tab 切换（带 indicator 滑动）
- ✅ 卡片点击（scale 缩放）
- ✅ 里程碑打勾（彩纸动画）
- ✅ AI 对话（打字动画）
- ✅ 页面入场（stagger 动画）
- ✅ 呼吸光晕（Hero 卡片）
- ✅ 漂浮动画（AI 浮动条）
- ✅ 环形进度（睡眠评分）

### 6.3 设计稿交付

```
交付格式: Figma（推荐）+ HTML 原型
设计稿: [待创建 Figma 链接]
HTML 原型: ~/babygrow/docs/ui-mockups/babygrow-final.html
```

---

> 本文档为 UI 设计规范，设计和开发参考。
