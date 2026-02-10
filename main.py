"""
WeChat RSS 主程序
"""

import sys
from rss_parser import fetch_and_parse_rss, print_feed_summary, print_all_articles


def main():
    """主入口函数"""
    RSS_URL = "https://wechat2rss.xlab.app/feed/33d986064f59be5263de2ca822fb3e0bdd59eb81.xml"
    
    # 检查命令行参数
    print_full = "--full" in sys.argv or "-f" in sys.argv
    max_items = 5
    
    if "--limit" in sys.argv:
        try:
            idx = sys.argv.index("--limit")
            max_items = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            print("警告: --limit 参数无效，使用默认值5")
    
    try:
        feed = fetch_and_parse_rss(RSS_URL)
        
        if print_full:
            # 打印所有文章的完整内容
            print_all_articles(feed, remove_html=True, max_length=None)
        else:
            # 仅打印文章摘要（默认）
            print_feed_summary(feed, max_items=max_items)
            print("\n提示: 使用 --full 参数打印完整文章内容")
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
