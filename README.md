# WeChat RSS 解析器

简洁、优雅、高性能的RSS解析器，专为微信公众号RSS源设计。

## 特性

- ✅ **高性能**: 使用Python标准库`xml.etree.ElementTree`，纯C实现，解析速度快
- ✅ **零依赖**: 无需安装任何第三方库，开箱即用
- ✅ **类型安全**: 使用`dataclasses`定义数据结构，清晰明确
- ✅ **优雅简洁**: 代码结构清晰，易于理解和扩展
- ✅ **完整功能**: 支持RSS 2.0标准，包括content:encoded命名空间

## 快速开始

### 基本用法

```bash
# 直接运行主程序（默认显示文章摘要）
python main.py

# 打印完整文章内容
python main.py --full

# 限制显示文章数量
python main.py --limit 3
```

### 作为库使用

```python
from rss_parser import fetch_and_parse_rss, print_feed_summary, print_all_articles, print_article_content

# 获取并解析RSS
feed = fetch_and_parse_rss("https://wechat2rss.xlab.app/feed/33d986064f59be5263de2ca822fb3e0bdd59eb81.xml")

# 打印概览
print_feed_summary(feed, max_items=5)

# 打印所有文章的完整内容
print_all_articles(feed, remove_html=True)

# 打印单篇文章的完整内容
if feed.items:
    print_article_content(feed.items[0], remove_html=True, max_length=1000)

# 自定义处理
for item in feed.items:
    print(f"标题: {item.title}")
    print(f"链接: {item.link}")
    print(f"发布时间: {item.pub_date}")
```

## 项目结构

```
WeChat RSS/
├── main.py              # 主程序入口
├── rss_parser.py        # RSS解析器核心代码
├── example_usage.py     # 使用示例
├── USAGE.md             # 使用说明文档
├── requirements.txt     # 依赖文件（空，使用标准库）
├── pyproject.toml       # 项目配置
└── README.md            # 说明文档
```

## 数据模型

### RSSFeed（频道信息）
- `title`: 频道标题
- `link`: 频道链接
- `description`: 频道描述
- `managing_editor`: 管理编辑
- `pub_date`: 发布日期
- `last_build_date`: 最后构建日期
- `items`: 文章列表（List[RSSItem]）

### RSSItem（单篇文章）
- `title`: 文章标题
- `link`: 文章链接
- `description`: 文章描述
- `content`: 完整内容（从content:encoded提取）
- `pub_date`: 发布日期（datetime对象）

## 日志输出示例

### 摘要模式（默认）

```
2026-02-09 15:44:11 - INFO - 开始获取RSS: https://wechat2rss.xlab.app/feed/33d986064f59be5263de2ca822fb3e0bdd59eb81.xml
2026-02-09 15:44:13 - INFO - RSS获取成功，开始解析...
2026-02-09 15:44:13 - INFO - 解析完成：频道 '猫笔刀'，共 20 条文章
================================================================================
RSS频道: 猫笔刀
链接: https://wechat2rss.xlab.app/feed/33d986064f59be5263de2ca822fb3e0bdd59eb81.xml
描述: 记录与分享！
发布时间: Sun, 08 Feb 2026 22:21:53 +0800
文章总数: 20
================================================================================

最新 3 篇文章:

【文章 1】
标题: 4小时，不够
链接: https://mp.weixin.qq.com/s?__biz=MzE5ODk2NjUwOA==&mid=2247496791&idx=1&sn=1d969881e8f13dbeb9c167c5f1f3c4ea
发布时间: 2026-02-08 22:21:00
摘要: moomoocat 2026-02-08 22:21 中国香港...
...
```

### 完整内容模式

```bash
python main.py --full
```

输出将包含每篇文章的完整内容，自动清理HTML标签，格式化显示：

```
################################################################################
# RSS频道: 猫笔刀
# 共 20 篇文章
################################################################################

[1/20]
================================================================================
标题: 4小时，不够
链接: https://mp.weixin.qq.com/s?__biz=MzE5ODk2NjUwOA==&mid=2247496791&idx=1&sn=1d969881e8f13dbeb9c167c5f1f3c4ea
发布时间: 2026-02-08 22:21:00

--------------------------------------------------------------------------------
文章内容:
--------------------------------------------------------------------------------

这几天冬奥会悄么么开始了你们知道吗，要不是临海家里的客厅有电视机...
（完整文章内容）
================================================================================
```

## 命令行参数

- `--full` 或 `-f`: 打印完整文章内容（默认只显示摘要）
- `--limit N`: 限制显示的文章数量（仅摘要模式有效）

## 完整内容功能

新增 `print_article_content()` 和 `print_all_articles()` 函数，特点：

1. **自动清理HTML标签**: 使文章内容更易于阅读
2. **智能文本处理**: 移除多余空白字符，格式化输出
3. **灵活配置**: 可控制打印长度、是否清理HTML等
4. **清晰的格式化**: 使用分隔线和标题使内容易于区分

使用示例：

```python
from rss_parser import print_article_content, print_all_articles

# 打印单篇文章（清理HTML，不限制长度）
print_article_content(item, remove_html=True, max_length=None)

# 打印所有文章（清理HTML，每篇最多1000字）
print_all_articles(feed, remove_html=True, max_length=1000)
```

## 性能优势

1. **内存效率高**: 使用`xml.etree.ElementTree`的`fromstring`，直接解析字符串，无需迭代器复杂逻辑
2. **CPU效率高**: ElementTree使用C语言实现，解析速度快
3. **零拷贝设计**: 使用dataclasses避免不必要的数据转换
4. **标准库保证**: 无需担心第三方库的版本兼容和安全问题

## 技术栈

- Python 3.9+
- xml.etree.ElementTree (标准库)
- dataclasses (标准库)
- logging (标准库)

## License

MIT License
