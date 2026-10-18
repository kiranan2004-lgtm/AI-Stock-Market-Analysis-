import os
import re
import html
import json
import logging
import datetime
import email.utils
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from apps.market.models import Stock
from .models import NewsArticle

logger = logging.getLogger(__name__)
analyzer = SentimentIntensityAnalyzer()


class NewsSentimentService:
    """
    Robust Financial News Ingestion and Sentiment Analysis Service.
    
    Architecture:
    1. Primary Live Feed: Google News Financial RSS (zero configuration, high availability,
       supports both Indian NSE/BSE equities like TCS.NS and US stocks like AAPL).
    2. Optional Feed: NewsAPI.org (if NEWS_API_KEY is configured in settings/env).
    3. NLP Sentiment Engine: VADER (Valence Aware Dictionary and sEntiment Reasoner),
       specifically calibrated for sentiment polarity and compound scoring.
    4. Database Persistence: Upserts news items into SQLite NewsArticle table for audit
       trail and offline fallback caching.
    """

    @classmethod
    def get_stock_news(cls, symbol: Optional[str] = None, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fetches news for a specific stock symbol or the broad financial market,
        performs VADER sentiment analysis, and caches articles in the database.
        """
        clean_symbol = symbol.strip().upper() if symbol else None
        cache_key = f"news_feed_{clean_symbol or 'ALL_MARKET'}"
        
        if not force_refresh:
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result

        target_stock: Optional[Stock] = None
        if clean_symbol and clean_symbol != 'MARKET':
            target_stock = Stock.objects.filter(symbol=clean_symbol).first()

        provider_used = "Google News Financial RSS"
        error_message = None
        articles_data: List[Dict[str, Any]] = []

        # Tier 1: Try NewsAPI.org if API key is provided
        news_api_key = getattr(settings, 'NEWS_API_KEY', '') or os.getenv('NEWS_API_KEY', '')
        if news_api_key:
            try:
                articles_data = cls._fetch_from_newsapi(clean_symbol, target_stock, news_api_key)
                if articles_data:
                    provider_used = "NewsAPI.org Financial Stream"
            except Exception as e:
                logger.warning(f"NewsAPI query failed, falling back to Google News RSS: {e}")

        # Tier 2: Google News Financial RSS (Default & Free)
        if not articles_data:
            try:
                articles_data = cls._fetch_from_google_rss(clean_symbol, target_stock)
                provider_used = "Google News Financial RSS"
            except Exception as e:
                logger.error(f"Google News RSS fetch failed: {e}")
                error_message = f"Live news feed temporarily unavailable: {str(e)}"

        # Process and persist articles
        processed_articles: List[NewsArticle] = []
        if articles_data:
            for item in articles_data:
                try:
                    headline = item['headline'][:490]
                    link = item['url'][:990]
                    publisher = item.get('publisher', 'Financial Media')[:140]
                    published_at = item.get('published_at') or timezone.now()
                    summary = item.get('summary', '')

                    # Run VADER NLP Sentiment Analysis
                    text_to_score = f"{headline}. {summary}" if summary else headline
                    scores = analyzer.polarity_scores(text_to_score)
                    compound = round(scores['compound'], 3)

                    if compound >= 0.05:
                        sentiment_label = 'POSITIVE'
                    elif compound <= -0.05:
                        sentiment_label = 'NEGATIVE'
                    else:
                        sentiment_label = 'NEUTRAL'

                    # Upsert into SQLite database
                    article_obj, _ = NewsArticle.objects.update_or_create(
                        url=link,
                        defaults={
                            'stock': item.get('stock') or target_stock,
                            'headline': headline,
                            'publisher': publisher,
                            'published_at': published_at,
                            'sentiment_label': sentiment_label,
                            'sentiment_score': compound,
                            'summary': summary,
                        }
                    )
                    processed_articles.append(article_obj)
                except Exception as ex:
                    logger.error(f"Error persisting news article: {ex}")

        # Tier 3: Offline Database Cache Fallback if live fetch failed
        if not processed_articles:
            qs = NewsArticle.objects.all()
            if target_stock:
                qs = qs.filter(stock=target_stock)
            elif clean_symbol and clean_symbol != 'MARKET':
                qs = qs.filter(stock__symbol=clean_symbol)
            
            db_articles = list(qs.order_by('-published_at')[:25])
            if db_articles:
                processed_articles = db_articles
                provider_used = "Local Database Cache (Offline Mode)"
                error_message = None

        # Compute Sentiment Distribution Metrics
        pos_count = sum(1 for a in processed_articles if a.sentiment_label == 'POSITIVE')
        neu_count = sum(1 for a in processed_articles if a.sentiment_label == 'NEUTRAL')
        neg_count = sum(1 for a in processed_articles if a.sentiment_label == 'NEGATIVE')
        total = len(processed_articles)
        avg_score = round(sum(a.sentiment_score for a in processed_articles) / total, 3) if total > 0 else 0.0

        distribution = {
            'positive_pct': round((pos_count / total * 100), 1) if total > 0 else 0.0,
            'neutral_pct': round((neu_count / total * 100), 1) if total > 0 else 0.0,
            'negative_pct': round((neg_count / total * 100), 1) if total > 0 else 0.0,
            'positive_count': pos_count,
            'neutral_count': neu_count,
            'negative_count': neg_count,
            'average_score': avg_score,
            'total_articles': total,
        }

        result = {
            'symbol': clean_symbol if clean_symbol else 'MARKET',
            'articles': processed_articles,
            'distribution': distribution,
            'provider': provider_used,
            'error': error_message,
            'disclaimer': (
                'Sentiment polarity scores are generated by rule-based and lexical NLP models (VADER) '
                'evaluating headline and summary terminology. Sentiment metrics are informational and do '
                'not constitute investment recommendations.'
            ),
        }

        # Cache for 5 minutes (300 seconds)
        if processed_articles:
            cache.set(cache_key, result, 300)

        return result

    @classmethod
    def _fetch_from_google_rss(cls, symbol: Optional[str], stock: Optional[Stock]) -> List[Dict[str, Any]]:
        """
        Fetches live financial news from Google News RSS feed.
        """
        is_indian = True
        if stock:
            is_indian = stock.symbol.endswith('.NS') or stock.symbol.endswith('.BO') or stock.currency == 'INR'
            query = f'"{stock.name}" stock'
        elif symbol and symbol != 'MARKET':
            is_indian = symbol.endswith('.NS') or symbol.endswith('.BO')
            query = f'"{symbol}" stock'
        else:
            query = 'Nifty 50 Sensex Indian stock market economy earnings'
            is_indian = True

        if is_indian:
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
        else:
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-US&gl=US&ceid=US:en"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        # 10 second timeout for network requests
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read()

        tree = ET.fromstring(xml_data)
        items = tree.findall('.//item')
        
        results = []
        for item in items[:25]:
            raw_title = (item.find('title').text or '').strip()
            link = (item.find('link').text or '').strip()
            pub_date_raw = (item.find('pubDate').text or '').strip()
            source_elem = item.find('source')
            source_name = (source_elem.text or '').strip() if source_elem is not None else ''

            if not raw_title or not link:
                continue

            # Separate headline from publisher suffix (e.g. "Headline - NDTV Profit")
            if ' - ' in raw_title:
                parts = raw_title.rsplit(' - ', 1)
                headline = parts[0].strip()
                if not source_name:
                    source_name = parts[1].strip()
            else:
                headline = raw_title.strip()

            publisher = source_name or 'Financial Media'

            # Parse RFC 2822 published timestamp
            try:
                published_at = email.utils.parsedate_to_datetime(pub_date_raw)
                if not timezone.is_aware(published_at):
                    published_at = timezone.make_aware(published_at, datetime.timezone.utc)
            except Exception:
                published_at = timezone.now()

            # Clean description HTML to obtain a summary snippet
            raw_desc = item.find('description').text or ''
            clean_desc = html.unescape(re.sub(r'<[^>]+>', ' ', raw_desc))
            clean_desc = clean_desc.replace('\ufffd', '-').replace('&nbsp;', ' ')
            clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()

            # If description has meaningful content beyond just the headline
            if len(clean_desc) > len(headline) + 15:
                summary = clean_desc
            else:
                target_name = stock.name if stock else (symbol if symbol else 'market equities')
                summary = f"Live coverage and financial analysis regarding {target_name} published by {publisher}."

            # If symbol was generic, attempt to link article to an active stock in DB
            matched_stock = stock
            if not matched_stock:
                headline_upper = headline.upper()
                for s in Stock.objects.filter(is_active=True):
                    sym_clean = s.symbol.split('.')[0]
                    if (s.name and s.name.upper() in headline_upper) or (len(sym_clean) >= 3 and sym_clean in headline_upper):
                        matched_stock = s
                        break

            results.append({
                'headline': headline,
                'url': link,
                'publisher': publisher,
                'published_at': published_at,
                'summary': summary,
                'stock': matched_stock,
            })

        return results

    @classmethod
    def _fetch_from_newsapi(cls, symbol: Optional[str], stock: Optional[Stock], api_key: str) -> List[Dict[str, Any]]:
        """
        Fetches live articles from NewsAPI.org when a user configures NEWS_API_KEY.
        """
        if stock:
            query = f'"{stock.name}" OR "{stock.symbol.split(".")[0]}"'
        elif symbol and symbol != 'MARKET':
            query = f'"{symbol}"'
        else:
            query = 'Nifty OR Sensex OR "Stock Market" OR "Reserve Bank of India"'

        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={urllib.parse.quote(query)}&"
            f"sortBy=publishedAt&language=en&pageSize=20&"
            f"apiKey={api_key}"
        )

        headers = {'User-Agent': 'StockSenseAI/2.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        articles = data.get('articles', [])
        results = []
        for a in articles:
            title = (a.get('title') or '').strip()
            link = (a.get('url') or '').strip()
            if not title or not link or '[Removed]' in title:
                continue

            publisher = a.get('source', {}).get('name') or 'Financial Media'
            pub_str = a.get('publishedAt')
            try:
                published_at = datetime.datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
            except Exception:
                published_at = timezone.now()

            summary = (a.get('description') or a.get('content') or '').strip()
            summary = html.unescape(re.sub(r'<[^>]+>', ' ', summary))

            results.append({
                'headline': title,
                'url': link,
                'publisher': publisher,
                'published_at': published_at,
                'summary': summary or f"Report on {stock.name if stock else 'financial markets'} by {publisher}.",
                'stock': stock,
            })

        return results
