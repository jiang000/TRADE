# 交易随笔 · 投资与期权阅读笔记

一个基于 **GitHub Pages + Jekyll** 的个人博客，把本仓库里的 Markdown 文章自动渲染成网页。首页是「文章名称超链接」的**瀑布流**布局，点击任意卡片即可进入对应的文章正文。

- 站点地址：<https://jiang000.github.io/TRADE/>
- 首页布局：瀑布流（Pinterest 风格，按发布时间倒序）
- 每篇文章：标题 + 作者 + 发布日期 + 正文 + 图片

---

## 目录结构

```
TRADE/
├── index.html          # 首页（瀑布流，自动列出所有文章）
├── 404.html            # 404 页面
├── _config.yml         # 站点配置（标题 / baseurl / 构建设置）
├── _layouts/
│   └── default.html    # 站点统一布局与样式（含瀑布流 CSS）
├── tools/
│   └── update_frontmatter.py   # 给文章补齐 front matter 的脚本
├── assets/             # 各文章图片，按「文章名/」分文件夹存放
└── *.md                # 文章（每篇一个 Markdown 文件）
```

---

## 如何部署到 GitHub Pages

1. 把本仓库推送到 GitHub（已配置 `origin` 为 `jiang000/TRADE`）：

   ```bash
   git add .
   git commit -m "feat: 博客首页 + GitHub Pages 配置"
   git push origin master
   ```

2. 打开仓库页 → **Settings → Pages**（左侧「代码和自动化」分类下）。

3. 在 **Build and deployment** 的 Source 下拉框里选择 **Deploy from a branch**，分支选 `master`、目录选 `/ (root)`，点 **Save**。

4. 等 1~2 分钟，GitHub 会自动用 Jekyll 构建。构建完成后，站点就上线在：

   ```
   https://jiang000.github.io/TRADE/
   ```

> 构建状态可在仓库的 **Actions** 标签页查看；若构建失败，会在此处给出报错信息。

---

## 新增一篇文章

文章由你的「下载公众号文章」技能生成，通常已带有 `author` 和 `date`。要让它在博客首页的瀑布流里正常显示，front matter 需要包含以下字段：

```yaml
---
title: "文章标题"          # 显示用标题（不含 .md）
layout: default            # 套用博客布局
author: 某公众号
date: 2025.01.01           # 原始日期（可保留）
pubdate: "2025.01.01"      # 用于首页排序/展示（字符串，格式 YYYY.MM.DD）
---
```

**无需手写** —— 下载完新文章后，在仓库根目录跑一次脚本即可自动补齐缺失字段：

```bash
python tools/update_frontmatter.py
```

脚本是幂等的：已有字段不会被重复添加，原 `author` / `date` 等保持不变。

---

## 自定义

- **改站点标题 / 副标题**：编辑 `_config.yml` 里的 `title` 与 `description`。
- **改配色 / 样式**：编辑 `_layouts/default.html` 里 `<style>` 中的 CSS 变量（`:root`）。
- **换成用户主页或自定义域名**：把 `_config.yml` 里的 `baseurl` 改为 `""`（默认 `/TRADE` 是项目站点路径）。

---

## 技术说明

- 使用 GitHub Pages 原生的 **Jekyll** 渲染，无需本地安装 Ruby/Jekyll，推送到 `master` 分支即自动构建。
- 首页瀑布流通过 `index.html` 里的 Liquid 模板自动遍历 `site.pages`（按 `pubdate` 倒序），新增文章无需改动首页。
- 文章正文里的图片使用相对路径 `assets/文章名/xxx.png`，Jekyll 渲染后路径保持不变。
