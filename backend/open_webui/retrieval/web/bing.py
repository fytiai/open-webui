import logging
from typing import Optional

import requests

from open_webui.env import SRC_LOG_LEVELS
from open_webui.retrieval.web.main import SearchResult, get_filtered_results

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])
"""
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
"""


def search_bing(
        subscription_key: str,
        endpoint: str,
        locale: str,
        query: str,
        count: int,
        filter_list: Optional[list[str]] = None,
) -> list[SearchResult]:
    mkt = locale
    params = {"q": query, "mkt": mkt, "count": count, "responseFilter": ["Webpages", "News"], "freshness": "Month"}
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        json_response = response.json()
        results = json_response.get("webPages", {}).get("value", [])

        results = get_filtered_results(results, filter_list)
        return [
            SearchResult(
                link=result["url"],
                title=result.get("name"),
                snippet=result.get("snippet"),
            )
            for result in results
        ]
    except Exception as ex:
        log.error(f"Error: {ex}")
        raise ex




# if __name__ == "__main__":
    # main("https://fosun-lcp-clickpaas.oss-cn-shanghai.aliyuncs.com/fosun-dify-files-images/1221489743.pdf",
    #      "1221489743.pdf")

    # parser = argparse.ArgumentParser(description="Search Bing from the command line.")
    # parser.add_argument(
    #     "query",
    #     type=str,
    #     default="Top 5 international news today",
    #     help="The search query.",
    # )
    # parser.add_argument(
    #     "--count", type=int, default=5, help="Number of search results to return."
    # )
    # parser.add_argument(
    #     "--filter", nargs="*", help="List of filters to apply to the search results."
    # )
    # parser.add_argument(
    #     "--locale",
    #     type=str,
    #     default="en-US",
    #     help="The locale to use for the search, maps to market in api",
    # )
    #
    # # args = parser.parse_args()
    #
    # # results = search_bing(args.locale, args.query, args.count, args.filter)
    #
    # results = search_bing("","https://api.bing.microsoft.com/v7.0/search","zh-CN", "", 5, None)
    #
    # pprint(results)
