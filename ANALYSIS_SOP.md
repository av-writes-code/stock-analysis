# Stock Analysis SOP (Standard Operating Procedure)

**Author:** av-writes-code
**First Applied To:** Bikaji Foods International (NSE: BIKAJI), February 3, 2026
**Purpose:** Codified, repeatable process for producing a 1-year equity research report

---

## Phase 1: Data Collection (Sources & What to Extract)

### 1.1 Price & Market Data
- **Source:** NSE India, Yahoo Finance, Investing.com
- **Extract:** Current price (with exact date), 52-week range, market cap, P/E (trailing + forward), P/B, dividend yield, beta
- **Gotcha:** P/E varies by source (standalone vs consolidated, trailing vs forward). Always note methodology.

### 1.2 Financial Statements (Last 7-8 Quarters)
- **Source:** Screener.in, Trendlyne, Business Standard quarterly results
- **Extract:** Revenue, EBITDA, EBITDA margin, PAT, gross margin per quarter
- **Also Extract:** Cash flow from operations, capex, free cash flow (CFO - capex)
- **Gotcha:** Q3 sweets revenue can shift based on Diwali timing (Q2 vs Q3). Always note seasonal effects.

### 1.3 Segment Breakdown
- **Source:** Company investor presentations (bikaji.com), earnings call transcripts
- **Extract:** Revenue % by segment, YoY growth by segment, export growth separately

### 1.4 Balance Sheet & Working Capital
- **Source:** Screener.in, Stock Analysis
- **Extract:** Debt/equity, current ratio, ROCE, ROE, inventory days, receivable days, payable days
- **Critical Check:** Is operating profit converting to cash? Compare CFO to PAT. If cash conversion ratio < 70%, flag it.

### 1.5 Shareholding Pattern
- **Source:** Trendlyne, Angel One, BSE/NSE filings
- **Extract:** Promoter %, FII %, DII %, MF % (with number of schemes), largest non-promoter holder
- **Watch:** Promoter holding decline over quarters, retail buying spikes

### 1.6 Management Guidance
- **Source:** Earnings call transcripts (Yahoo Finance, Trendlyne)
- **Extract:** Revenue growth guidance, margin guidance, capex plans, new ventures, explicit "not a priority" statements
- **Tip:** Direct quotes are more credible than paraphrased guidance

---

## Phase 2: Analyst & Market Context

### 2.1 Brokerage Target Prices
- **Source:** TradingView (for Motilal Oswal etc.), Investing.com, Alpha Spread, Trendlyne
- **Require:** Named brokerage, specific target price, rating, date of report, key thesis
- **Quality Check:** Are targets post-latest quarterly results? Stale targets (pre-results) should be flagged.

### 2.2 Sector Index Performance
- **Source:** NSE India (Nifty FMCG), INDmoney, ICICI Direct
- **Extract:** Index level, 52-week range, 1M/3M/6M/1Y returns
- **Purpose:** Is the stock underperforming the sector, or is the whole sector down?

### 2.3 Peer Valuation Comparison
- **Source:** Smart-Investing.in, MarketsMojo, Tickertape
- **Extract:** P/E ratios for 4-5 listed peers (same sector)
- **For FMCG Snacks:** Nestle India, Britannia, Dabur, ITC, Prataap Snacks
- **Purpose:** Contextualise the stock's multiple vs sector average

### 2.4 Commodity / Raw Material Context
- **Source:** MARC Ratings, Fastmarkets (palm oil), ChemAnalyst (mustard oil), IMARC Group
- **Extract:** Current prices, 2026 outlook, duty changes, % of input cost
- **For Snacks:** Edible oils = 25-33% of raw material costs. Track palm oil and mustard oil specifically.

---

## Phase 3: Technical Analysis

### 3.1 Key Indicators
- **Source:** Investing.com technicals, TradingView, TipRanks
- **Extract:** 50-day EMA, 200-day SMA, RSI, ADX, CCI, beta
- **Identify:** Support zones, resistance zones, chart patterns (double bottom, head & shoulders etc.)

### 3.2 Price Chart
- **Use monthly closing prices** from known data points (52-week high/low, quarterly close dates)
- **Disclose:** Monthly approximation, not tick-level data (unless market API is used)

---

## Phase 4: Valuation (Forward EPS x P/E Multiple)

### 4.1 Establish Current EPS
```
TTM EPS = TTM Net Profit / Shares Outstanding
Shares Outstanding = Market Cap / Current Price
Sanity Check: Price / TTM EPS should match reported P/E (within 5%)
```

### 4.2 Project FY27E EPS (3 scenarios)
- **Bull:** Use highest credible growth rate (e.g., Trendlyne FY26 estimate + Emkay CAGR)
- **Base:** Use consensus CAGR (e.g., Emkay 27% earnings CAGR)
- **Bear:** Assume growth slows to <10% (commodity shock, execution miss)

### 4.3 Apply P/E Multiple
- Anchor to peer multiples (not arbitrary numbers)
- Bull: P/E holds at growth premium level (55-60x for high-growth FMCG)
- Base: P/E compresses mildly (50-55x as earnings catch up)
- Bear: P/E de-rates to sector average or below (40-45x)

### 4.4 Probability Weighting
```
Bull (20%): Everything goes right. Unanimous analyst Buy is itself a contrarian signal.
Base (55%): Most likely. Company delivers on guidance, P/E gently compresses.
Bear (25%): Higher than typical if specific tangible risks exist (cash flow, commodity, competition).

Expected Value = Sum of (Midpoint Price x Probability)
```

### 4.5 Methodology Transparency
Always disclose:
- This is a P/E heuristic, not a DCF
- P/E assumptions are subjective, anchored to peer comps
- EPS estimates are top-down (from analyst growth rates), not bottoms-up
- Probability weights are judgment calls
- Cash flow quality should ideally be reflected in valuation (EV/FCF, DCF)

---

## Phase 5: Report Assembly

### 5.1 Sections (in order)
1. **Title Page** — Key metrics table, disclaimers, sources
2. **Company Snapshot** — Business overview, key facts
3. **Fundamental Analysis** — Revenue/profit trends, margins, cash flow, shareholding, cautionary flags
4. **Technical Analysis** — Price chart, MA signals, support/resistance
5. **Sector & Competitive Context** — Market size, peer comparison, FMCG index, commodity outlook
6. **Valuation & Analyst Views** — Named brokerage targets, P/E context
7. **Growth Catalysts & Risks** — Management guidance, bull/bear factors
8. **Conclusion** — Full valuation math shown, probability-weighted EV, methodology limitations, verdict

### 5.2 Charts (minimum 5)
1. Quarterly revenue & profit bar chart
2. Margin trend line chart (gross + EBITDA)
3. Segment revenue pie chart
4. Price action with moving averages + support/resistance zones
5. Peer comparison bars

### 5.3 Technical Implementation
- **Charts:** matplotlib (saved as PNG at 150 DPI)
- **PDF:** reportlab (with ArialUnicode font for currency symbol support)
- **Currency:** Use ₹ symbol with Unicode-capable font, not "Rs."

---

## Phase 6: Quality Checklist (Before Publishing)

- [ ] Every number has a named source and date
- [ ] P/E discrepancies across sources are explained (trailing vs forward, standalone vs consolidated)
- [ ] Cash flow analysis included (not just P&L)
- [ ] Shareholding pattern with FII/DII/MF breakdown
- [ ] At least 3 named brokerages with dated target prices
- [ ] Peer P/E comparison table with actual current multiples
- [ ] Nifty FMCG sector performance for context
- [ ] Raw material/commodity outlook specific to the business
- [ ] Management guidance with direct quotes from earnings call
- [ ] Valuation math fully shown (EPS derivation, P/E assumptions, probability weights)
- [ ] Methodology limitations explicitly disclosed
- [ ] Disclaimer included
- [ ] Currency symbols render correctly in PDF
- [ ] All charts render cleanly

---

## Gaps This SOP Does NOT Cover (Future Improvements)

1. **DCF Model** — Build a proper 3-statement model with segment-level revenue, capex, WACC
2. **Insider Transaction Tracking** — Bulk/block deals, promoter pledging
3. **Corporate Governance Audit** — Auditor qualifications, related-party transactions
4. **Liquidity Analysis** — Average daily volume, delivery %, impact cost
5. **Options Chain Analysis** — Put-call ratio, max pain, open interest patterns
6. **Sentiment Analysis** — Social media, news flow, Google Trends for brand
7. **Historical Drawdown Analysis** — Max drawdown, recovery time, Sharpe ratio
