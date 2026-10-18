import re
import os
from typing import Dict, Any, List
from django.conf import settings
from apps.market.models import Stock
from apps.market.services import MarketDataService, DEFAULT_STOCK_UNIVERSE
from apps.analytics.services import TechnicalIndicatorService
from apps.portfolio.services import PortfolioAnalyticsService
from .models import ChatConversation, ChatMessage

class ResearchAssistantService:
    """
    Retrieval-grounded financial research assistant that pulls actual platform data
    before generating research responses.
    """

    @staticmethod
    def process_query(user, message_text: str, conversation_id: int = None) -> Dict[str, Any]:
        """
        Executes query parsing, facts retrieval, and grounded response synthesis.
        """
        message_text = message_text.strip()
        if not message_text:
            return {'success': False, 'error': 'Empty query.'}

        # 1. Manage Conversation History
        if conversation_id:
            conversation = ChatConversation.objects.filter(id=conversation_id, user=user).first()
        else:
            conversation = None

        if not conversation:
            # Create new conversation with title extracted from query
            title = message_text[:40] + ('...' if len(message_text) > 40 else '')
            conversation = ChatConversation.objects.create(user=user, title=title)

        # Record user turn
        ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=message_text
        )

        # 2. Tool / Data Retrieval Layer
        grounded_facts = []
        context_data = {}

        # Check for Portfolio intent
        portfolio_keywords = ['portfolio', 'holding', 'holdings', 'my stocks', 'my profit', 'my loss', 'invested', 'my return']
        if any(kw in message_text.lower() for kw in portfolio_keywords):
            p_summary = PortfolioAnalyticsService.get_user_portfolio_summary(user)
            context_data['portfolio'] = {
                'total_invested': float(p_summary['total_invested']),
                'current_value': float(p_summary['current_value']),
                'unrealized_pl': float(p_summary['unrealized_pl']),
                'unrealized_pl_pct': float(p_summary['unrealized_pl_pct']),
                'holdings_count': p_summary['total_holdings_count'],
            }
            grounded_facts.append(
                f"Authenticated User Portfolio: Total Invested = {p_summary['currency_symbol']}{p_summary['total_invested']}, "
                f"Current Value = {p_summary['currency_symbol']}{p_summary['current_value']}, "
                f"Unrealized P&L = {p_summary['currency_symbol']}{p_summary['unrealized_pl']} ({p_summary['unrealized_pl_pct']}%), "
                f"Total Active Holdings = {p_summary['total_holdings_count']} positions."
            )
            if p_summary['holdings']:
                h_str = ", ".join([f"{h['stock'].symbol} ({h['shares']} shares @ avg {h['avg_cost']})" for h in p_summary['holdings'][:5]])
                grounded_facts.append(f"Top Holdings: {h_str}")

        # Check for specific Tickers
        detected_symbols = []
        for symbol in DEFAULT_STOCK_UNIVERSE.keys():
            base_sym = symbol.replace('.NS', '')
            # Match exact ticker or symbol name in message
            pattern = r'\b(' + re.escape(symbol) + r'|' + re.escape(base_sym) + r')\b'
            if re.search(pattern, message_text, re.IGNORECASE):
                detected_symbols.append(symbol)

        # Also search in DB stocks
        if not detected_symbols:
            for s in Stock.objects.filter(is_active=True):
                base_s = s.symbol.replace('.NS', '')
                if base_s.lower() in message_text.lower() or s.name.lower() in message_text.lower():
                    detected_symbols.append(s.symbol)
                    if len(detected_symbols) >= 2:
                        break

        # Fetch quotes and indicators for detected symbols
        for sym in detected_symbols[:2]:
            quote = MarketDataService.get_stock_quote(sym)
            if quote.get('success'):
                context_data[sym] = {
                    'price': quote['current_price'],
                    'change_pct': quote['change_pct'],
                    'currency': quote['currency'],
                    'exchange': quote['exchange']
                }
                grounded_facts.append(
                    f"Market Quote for {quote['name']} ({sym}): Current Price = {quote['currency_symbol']}{quote['current_price']} {quote['currency']}, "
                    f"Daily Change = {quote['change']} ({quote['change_pct']}%), Day Range = {quote['day_low']} - {quote['day_high']}, "
                    f"52-Week Range = {quote.get('fifty_two_week_low', 'N/A')} - {quote.get('fifty_two_week_high', 'N/A')}, "
                    f"Volume = {quote['volume']:,} (Source: {quote['data_source']})."
                )

                # If indicators requested
                if any(ind in message_text.lower() for ind in ['rsi', 'macd', 'sma', 'indicator', 'average', 'volatility', 'technical']):
                    df, _ = MarketDataService.get_historical_ohlcv(sym, period='6mo')
                    if df is not None and not df.empty:
                        ind_res = TechnicalIndicatorService.calculate_indicators(df)
                        if ind_res.get('success'):
                            s = ind_res['summary']
                            grounded_facts.append(
                                f"Technical Indicators for {sym}: RSI(14) = {s['rsi_14']}, "
                                f"SMA(20) = {s['sma_20']}, SMA(50) = {s['sma_50']}, "
                                f"MACD = {s['macd_line']} (Signal: {s['signal_line']}), "
                                f"Annualized Volatility = {s['annualized_volatility']}%."
                            )

        # 3. Response Generation (Gemini LLM API or Grounded Research Engine)
        response_text = ""
        api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')

        if api_key and api_key != 'your_google_gemini_api_key_here':
            try:
                from google import genai
                client = genai.Client(api_key=api_key)

                system_prompt = (
                    "You are StockSense AI Research Assistant, an institutional-grade financial analytics assistant. "
                    "Answer user questions accurately, objectively, and concisely. "
                    "CRITICAL RULES: "
                    "1. Strictly ground all figures, prices, and percentages on the PROVIDED FACTS below. "
                    "2. NEVER invent numbers, prices, or fake corporate actions. "
                    "3. If requested data is not provided in facts, state clearly that it is not in the active dataset. "
                    "4. Include appropriate dates and data sources. "
                    "5. Remind the user that technical indicators and forecasts are analytical research tools, not financial advice.\n\n"
                    "GROUNDED FACTS:\n" + "\n".join(grounded_facts) if grounded_facts else "No specific stock or portfolio data retrieved for this prompt."
                )

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\n\nUser Question: {message_text}"
                )
                response_text = response.text

            except Exception as e:
                response_text = ResearchAssistantService._generate_deterministic_response(message_text, grounded_facts, str(e))
        else:
            response_text = ResearchAssistantService._generate_deterministic_response(message_text, grounded_facts, None)

        # Record assistant turn
        assistant_msg = ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_text,
            context_data=context_data
        )

        return {
            'success': True,
            'conversation_id': conversation.id,
            'message_id': assistant_msg.id,
            'content': response_text,
            'grounded_data': context_data
        }

    @staticmethod
    def _generate_deterministic_response(query: str, facts: List[str], api_error: str = None) -> str:
        """
        Reliable deterministic research synthesis when Gemini API key is not configured.
        Never hallucinates; formats verified ground-truth data cleanly.
        """
        response_parts = []

        if facts:
            response_parts.append("### StockSense Market Intelligence Summary")
            response_parts.append("Based on verified data retrieved from the platform backend:\n")
            for f in facts:
                response_parts.append(f"• **{f}**")
            
            response_parts.append("\n*Note: Market data is provided via Yahoo Finance (delayed ~15 mins). Historical performance and indicators are for research and educational purposes only.*")
        else:
            response_parts.append(
                "I am your StockSense Research Assistant. You can ask me about:\n"
                "• **Stock Quotes & Metrics**: e.g., *'What is the current price and day range of TCS?'* or *'Show metrics for Apple (AAPL)'*\n"
                "• **Technical Indicators**: e.g., *'Calculate RSI and MACD for Reliance Industries'* or *'Is Infosys overbought?'*\n"
                "• **Portfolio Analytics**: e.g., *'What is my total portfolio value and unrealized profit?'*\n"
                "• **Comparative Research**: e.g., *'Compare TCS and Infosys performance'*."
            )

        if api_error:
            response_parts.append(f"\n> **LLM API Notice**: External AI model returned an error ({api_error}). Local financial analytics engine generated the report above.")
        elif not getattr(settings, 'GEMINI_API_KEY', None):
            response_parts.append("\n> **System Note**: Generative conversational mode can be enabled by configuring `GEMINI_API_KEY` in your `.env` file. Grounded data retrieval is active.")

        return "\n\n".join(response_parts)
