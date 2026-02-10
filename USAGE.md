# WeChat RSS 使用说明

## 功能介绍

本工具可以获取并解析微信公众号的RSS源，支持两种显示模式：

### 1. 摘要模式（默认）
只显示文章的标题、链接、发布时间和前200字的摘要。

```bash
python main.py
```

### 2. 完整内容模式
打印所有文章的完整内容，自动清理HTML标签以便阅读。

```bash
python main.py --full
# 或
python main.py -f
```

## 命令行参数

- `--full` 或 `-f`: 打印完整文章内容
- `--limit N`: 限制显示的文章数量（仅在摘要模式下有效）

### 示例

```bash
# 显示前3篇文章的摘要
python main.py --limit 3

# 打印所有文章的完整内容
python main.py --full

# 打印所有文章（完整内容），但每篇限制在1000字以内
# （这个功能需要在代码中调用 print_all_articles 时设置 max_length 参数）
```

## 在代码中使用

你也可以在自己的代码中使用这些功能：

```python
from rss_parser import fetch_and_parse_rss, print_feed_summary, print_all_articles, print_article_content

# 获取RSS源
feed = fetch_and_parse_rss("https://wechat2rss.xlab.app/feed/xxx.xml")

# 打印摘要（前5篇）
print_feed_summary(feed, max_items=5)

# 打印所有文章的完整内容
print_all_articles(feed, remove_html=True, max_length=None)

# 打印单篇文章的完整内容
if feed.items:
    print_article_content(feed.items[0], remove_html=True, max_length=1000)
```

## 功能特点

1. **自动清理HTML标签**: 使文章内容更易于阅读
2. **智能文本处理**: 移除多余空白字符，格式化输出
3. **灵活配置**: 可控制打印长度、是否清理HTML等
4. **清晰的格式化**: 使用分隔线和标题使内容易于区分

## RSS源配置

默认使用的RSS源地址在代码中配置，你可以在 `main.py` 中修改：

```python
RSS_URL = "https://wechat2rss.xlab.app/feed/你的RSS地址.xml"
```
