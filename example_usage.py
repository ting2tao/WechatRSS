"""
RSS解析器使用示例
"""

from rss_parser import fetch_and_parse_rss, print_feed_summary, print_all_articles, print_article_content

def main():
    # RSS订阅地址
    RSS_URL = "https://wechat2rss.xlab.app/feed/33d986064f59be5263de2ca822fb3e0bdd59eb81.xml"
    
    # 获取并解析RSS
    feed = fetch_and_parse_rss(RSS_URL)
    
    # 1. 打印摘要（显示3篇文章）
    print("=" * 80)
    print("功能1：打印文章摘要")
    print("=" * 80)
    print_feed_summary(feed, max_items=3)
    
    # 2. 自定义输出：遍历所有文章标题
    print("\n" + "=" * 80)
    print("功能2：打印所有文章标题")
    print("=" * 80)
    print("\n所有文章标题:")
    for idx, item in enumerate(feed.items, 1):
        print(f"{idx}. {item.title} ({item.pub_date})")
    
    # 3. 打印单篇文章的完整内容
    print("\n" + "=" * 80)
    print("功能3：打印单篇文章的完整内容")
    print("=" * 80)
    if feed.items:
        # 打印第一篇文章的完整内容
        print_article_content(feed.items[0], remove_html=True, max_length=1000)
    
    # 4. 打印所有文章的完整内容
    print("\n" + "=" * 80)
    print("功能4：打印所有文章的完整内容")
    print("=" * 80)
    print("\n(此功能显示所有文章的完整内容)")
    # 为了示例简洁，只打印前2篇文章的完整内容
    for i, item in enumerate(feed.items[:2], 1):
        print(f"\n--- 文章 {i}/{len(feed.items)} ---")
        print_article_content(item, remove_html=True, max_length=500)

if __name__ == "__main__":
    main()
