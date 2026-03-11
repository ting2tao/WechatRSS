"""
简洁高性能的RSS解析器
使用标准库实现，无需额外依赖
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from xml.etree import ElementTree as ET
from logging import getLogger, INFO, basicConfig
import re

# 配置日志
basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = getLogger(__name__)


@dataclass
class RSSItem:
    """RSS条目数据模型"""
    title: str
    link: str
    description: str
    content: Optional[str] = None
    pub_date: Optional[datetime] = None
    summary: Optional[str] = None  # 200字左右的文章总结
    
    def __post_init__(self):
        # 自动解析日期字符串
        if isinstance(self.pub_date, str):
            try:
                self.pub_date = datetime.strptime(
                    self.pub_date.strip(), 
                    '%a, %d %b %Y %H:%M:%S %z'
                )
            except ValueError:
                self.pub_date = None


@dataclass
class RSSFeed:
    """RSS频道数据模型"""
    title: str
    link: str
    description: str
    managing_editor: Optional[str] = None
    pub_date: Optional[datetime] = None
    last_build_date: Optional[datetime] = None
    items: List[RSSItem] = field(default_factory=list)


class RSSParser:
    """高性能RSS解析器"""
    
    def __init__(self, xml_content: str):
        self.xml_content = xml_content
        self.namespaces = {
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }
    
    def parse(self) -> RSSFeed:
        """
        解析RSS XML并返回结构化数据
        
        使用iter解析提高内存效率，特别适合大文件
        """
        # 直接解析字符串内容（性能已足够好，代码更简洁）
        rss_root = ET.fromstring(self.xml_content)
        channel = rss_root.find('channel')
        
        if channel is None:
            raise ValueError("无效的RSS格式：缺少channel元素")
        
        # 解析频道信息
        feed = RSSFeed(
            title=self._get_text(channel, 'title', default=''),
            link=self._get_text(channel, 'link', default=''),
            description=self._get_text(channel, 'description', default=''),
            managing_editor=self._get_text(channel, 'managingEditor'),
            pub_date=self._get_text(channel, 'pubDate'),
            last_build_date=self._get_text(channel, 'lastBuildDate')
        )
        
        # 解析条目
        for item_elem in channel.findall('item'):
            item = RSSItem(
                title=self._get_text(item_elem, 'title', default=''),
                link=self._get_text(item_elem, 'link', default=''),
                description=self._get_text(item_elem, 'description', default=''),
                content=self._get_text(item_elem, 'encoded', namespace='content'),
                pub_date=self._get_text(item_elem, 'pubDate')
            )
            feed.items.append(item)
        
        return feed
    
    def _get_text(self, element, tag: str, default: Optional[str] = None, 
                  namespace: Optional[str] = None) -> Optional[str]:
        """安全获取XML元素文本"""
        if namespace:
            tag = f'{{{self.namespaces[namespace]}}}{tag}'
        
        elem = element.find(tag)
        return elem.text if elem is not None else default


def fetch_and_parse_rss(url: str) -> RSSFeed:
    """
    获取并解析RSS
    
    Args:
        url: RSS订阅地址
        
    Returns:
        RSSFeed对象
    """
    import urllib.request
    import ssl
    
    logger.info(f"开始获取RSS: {url}")
    
    # 处理SSL证书验证（针对macOS等环境）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # 添加User-Agent避免403错误
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    
    with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
        xml_content = response.read().decode('utf-8')
    
    logger.info("RSS获取成功，开始解析...")
    
    parser = RSSParser(xml_content)
    feed = parser.parse()
    
    logger.info(f"解析完成：频道 '{feed.title}'，共 {len(feed.items)} 条文章")
    
    return feed


def print_feed_summary(feed: RSSFeed, max_items: int = 5) -> None:
    """
    打印RSS概览日志
    
    Args:
        feed: RSSFeed对象
        max_items: 最多显示的文章数量
    """
    logger.info("=" * 80)
    logger.info(f"RSS频道: {feed.title}")
    logger.info(f"链接: {feed.link}")
    logger.info(f"描述: {feed.description}")
    logger.info(f"发布时间: {feed.pub_date}")
    logger.info(f"文章总数: {len(feed.items)}")
    logger.info("=" * 80)
    
    logger.info(f"\n最新 {min(max_items, len(feed.items))} 篇文章:\n")
    
    for idx, item in enumerate(feed.items[:max_items], 1):
        logger.info(f"【文章 {idx}】")
        logger.info(f"标题: {item.title}")
        logger.info(f"链接: {item.link}")
        
        if item.pub_date:
            logger.info(f"发布时间: {item.pub_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 显示文章摘要（前200个字符）
        content_preview = (item.content or item.description or "")[:200]
        if content_preview:
            # 移除HTML标签
            import re
            content_preview = re.sub(r'<[^>]+>', '', content_preview)
            logger.info(f"摘要: {content_preview}...")
        
        logger.info("-" * 80)


def print_article_content(item: RSSItem, remove_html: bool = True, max_length: Optional[int] = None) -> None:
    """
    打印单篇文章的完整内容
    
    Args:
        item: RSSItem对象
        remove_html: 是否移除HTML标签
        max_length: 最大打印长度（None表示不限制）
    """
    import re
    
    print("\n" + "=" * 80)
    print(f"标题: {item.title}")
    print(f"链接: {item.link}")
    
    if item.pub_date:
        print(f"发布时间: {item.pub_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "-" * 80)
    print("文章内容:")
    print("-" * 80 + "\n")
    
    # 优先使用content，其次使用description
    content = item.content or item.description or "暂无内容"
    
    if remove_html:
        # 移除HTML标签
        content = re.sub(r'<[^>]+>', '', content)
        # 移除多余的空白字符
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
    
    if max_length and len(content) > max_length:
        content = content[:max_length] + "...\n\n[内容已截断]"
    
    print(content)
    print("\n" + "=" * 80)


def print_all_articles(feed: RSSFeed, remove_html: bool = True, max_length: Optional[int] = None) -> None:
    """
    打印RSS源中所有文章的完整内容
    
    Args:
        feed: RSSFeed对象
        remove_html: 是否移除HTML标签
        max_length: 每篇文章的最大打印长度（None表示不限制）
    """
    print("\n" + "#" * 80)
    print(f"# RSS频道: {feed.title}")
    print(f"# 共 {len(feed.items)} 篇文章")
    print("#" * 80 + "\n")
    
    for idx, item in enumerate(feed.items, 1):
        print(f"\n[{idx}/{len(feed.items)}]", end=" ")
        print_article_content(item, remove_html, max_length)


if __name__ == "__main__":
    RSS_URL = "https://wechat2rss.xlab.app/feed/33d986064f59be5263de2ca822fb3e0bdd59eb81.xml"
    
    try:
        feed = fetch_and_parse_rss(RSS_URL)
        print_feed_summary(feed, max_items=3)
    except Exception as e:
        logger.error(f"处理RSS时出错: {e}", exc_info=True)
