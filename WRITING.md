# 写作与发布

网站入口： https://doczbs.github.io/writing/

## 新建文章

```sh
python3 -m pip install -r scripts/requirements-writing.txt
python3 scripts/build_writing.py --new my-first-essay
```

编辑 `content/posts/my-first-essay.md`。文件名就是永久网址的一部分，使用英文小写和短横线。

```yaml
---
title: "文章标题"
date: 2026-10-13
kind: Essay
summary: "一句话介绍"
draft: true
---
```

下面直接写 Markdown。支持中英文、标题、图片、代码块、表格、引用、脚注。
`kind` 可以是 `Essay`、`Research note`、`Field note`。
图片放 `assets/writing/`，引用如 `![说明](/assets/writing/photo.jpg)`。

## 预览和发布

将要发布的文章设为 `draft: false`，然后：

```sh
python3 scripts/build_writing.py
python3 -m http.server 8000 --directory _site
```

打开 http://localhost:8000/writing/ 。文章、目录、阅读时间和 RSS 自动生成。
确认后提交 Markdown 和图片并推送，GitHub Actions 自动构建和发布：

```sh
git add content/posts/my-first-essay.md assets/writing/
git commit -m "Publish my first essay"
git push
```

未用图片时省略 `assets/writing/`。GitHub 网页编辑 Markdown 并提交同样会自动发布。

`draft: true` 不进入网站、目录或 RSS。**仓库是公开的，已提交的草稿源码仍可在 GitHub 被查看**；私密草稿请保存在仓库外，准备发布时再移入。

`content/posts/first-entry.md` 是草稿模板，不会发布。没有实际文章时，网站显示真实的空目录，不显示示例文章。
