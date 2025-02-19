import validators

from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel

from urllib.parse import urlparse
import validators


def get_filtered_results(results, filter_list=None):
    allowed_extensions = [".html", ".shtml"]

    filtered_results = []
    for result in results:
        url = result.get("url") or result.get("link", "")

        # 检查URL的有效性
        if not validators.url(url):
            continue

        # 提取域名
        domain = urlparse(url).netloc

        # 如果提供了filter_list，校验域名是否在过滤列表内
        if filter_list:
            if not any(domain.endswith(filtered_domain) for filtered_domain in filter_list):
                continue
        filtered_results.append(result)

    return filtered_results


class SearchResult(BaseModel):
    link: str
    title: Optional[str]
    snippet: Optional[str]
