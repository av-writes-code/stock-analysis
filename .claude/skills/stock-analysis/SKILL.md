---
name: stock-analysis
description: "Generate a comprehensive 1-year equity research report (PDF) for any Indian stock. Covers fundamentals, technicals, sector context, peer comparison, valuation with probability-weighted scenarios, and a balanced conclusion. Use when the user asks to analyze a stock, create a stock report, or research an equity."
allowed-tools:
  - WebSearch
  - WebFetch
  - Bash
  - Write
  - Edit
  - Read
  - Task
metadata:
  version: "1.0"
  author: "av-writes-code"
  first-applied: "Bikaji Foods International, Feb 3 2026"
---

# Stock Analysis — 1-Year Equity Research Report Generator

## When to Use
- User asks to "analyze [stock name]", "research [stock]", "create a report on [stock]"
- User wants a 1-year forward outlook on any Indian listed equity
- User asks for fundamentals, technicals, valuation of an Indian stock

## Output
- A single PDF report saved to `~/Desktop/[Company]_Research_Report_[Date].pdf`
- Python script (matplotlib + reportlab) used to generate it
- All data sourced from free, publicly available platforms

## Critical Rules
1. **NEVER fabricate data.** Every number must have a named source and date.
2. **Screener.in is the primary data source** for Indian stocks (free tier). Always fetch it.
3. **Standalone vs Consolidated:** Screener.in defaults to standalone. Always check and note which basis is used. If consolidated is available, prefer it.
4. **P/E discrepancies:** Always note when P/E varies across sources and explain why (standalone vs consolidated, trailing vs forward).
5. **Show your math.** Valuation section must show EPS derivation, P/E assumptions (anchored to peer comps), and probability weights with rationale.
6. **Font for PDF:** Use SFNS (`/System/Library/Fonts/SFNS.ttf`) for proper INR symbol rendering on macOS.
7. **Correction culture:** If later data contradicts an earlier claim in the report, explicitly note the correction rather than silently changing it.

---

## Phase 1: Data Collection

### 1.1 Screener.in (PRIMARY — Always Fetch First)
```
URL: https://www.screener.in/company/{SYMBOL}/
     https://www.screener.in/company/{SYMBOL}/consolidated/  (prefer this)
```
**Extract:**
- Compounded Growth table (Sales, Profit, Stock Price CAGR — 3Y, 5Y, 10Y, TTM)
- Quarterly Results table (last 7-8 quarters: Sales, Net Profit, EPS)
- Annual P&L, Balance Sheet, Cash Flow (last 5 years)
- Key Ratios: P/E, P/B, Book Value, ROCE, ROE, Dividend Yield
- Working Capital: Debtor Days, Inventory Days, Payable Days (critical for quality assessment)
- Cash Flow from Operations (annual trend)
- Shareholding Pattern (Promoter, FII, DII, Public — latest quarter)

**Quality Checks from Screener.in:**
- Is CFO declining while profits grow? → Cash conversion concern
- Are debtor days increasing? → Aggressive revenue recognition risk
- Is promoter holding declining? → Insider confidence signal
- TTM growth vs 3Y/5Y CAGR — is growth decelerating?

### 1.2 Price & Market Data
- **Sources:** NSE India, Yahoo Finance, Investing.com, 5Paisa
- **Extract:** Current price (with exact date), 52-week range, market cap, beta
- **Note:** Always state the date of the price. If live price unavailable, state the most recent confirmed close.

### 1.3 Technical Indicators
- **Sources:** Investing.com technicals, TradingView, TipRanks
- **Extract:** 50-day EMA, 200-day SMA, RSI, ADX, CCI, support/resistance zones
- **Chart:** Monthly price approximation with MA overlays (disclose it's approximated)

### 1.4 Management Guidance
- **Source:** Earnings call transcript (Yahoo Finance, Trendlyne)
- **Extract:** Revenue/margin guidance, capex plans, new ventures, direct quotes
- **Tip:** Look for what management says is "not a priority" — that's as informative as what they're pursuing.

---

## Phase 2: Context & Comparisons

### 2.1 Analyst Targets (Named Brokerages Only)
- **Sources:** TradingView news, Investing.com consensus, Alpha Spread, Trendlyne
- **Require:** Brokerage name, target price, rating, date, key thesis
- **Minimum:** 3 named brokerages. Flag if targets are pre-latest quarterly results.
- **Red flag:** Unanimous Buy (6/6) is itself a contrarian warning — note this.

### 2.2 Sector Performance
- **Source:** NSE India sectoral indices (e.g., Nifty FMCG, Nifty IT, Nifty Pharma)
- **Extract:** Index level, 1Y return, 52-week range
- **Purpose:** Distinguish stock-specific underperformance from sector-wide correction

### 2.3 Peer Valuation Table
- **Source:** Smart-Investing.in, MarketsMojo, Tickertape, Screener.in peers section
- **Extract:** P/E for 4-5 listed peers + sector average
- **Purpose:** Anchor the P/E multiple assumptions in the valuation

### 2.4 Raw Material / Commodity Context
- **Source:** Varies by sector (edible oils for FMCG, crude for chemicals, etc.)
- **Extract:** Current price, 1-year outlook, duty/tariff changes, % of input cost
- **Purpose:** Assess margin risk/tailwind

---

## Phase 3: Valuation (Forward EPS x P/E)

### Step 1: Establish Current EPS
```
TTM Net Profit (from Screener.in) / Shares Outstanding (Market Cap / Price)
Sanity check: Price / EPS should match reported P/E within 5%
```

### Step 2: Project FY+2 EPS (3 Scenarios)
- **Bull:** Highest credible growth rate (analyst estimate or recent quarterly run-rate)
- **Base:** Consensus CAGR (from brokerage reports)
- **Bear:** Growth halves or turns negative (commodity shock, execution miss)

### Step 3: Apply P/E Multiple
Anchor to peer comps from Phase 2.3:
- **Bull:** P/E holds at growth premium (justified by sustained execution)
- **Base:** P/E compresses mildly (earnings catch up to price)
- **Bear:** P/E de-rates to sector average or below

### Step 4: Probability Weighting
```
Default starting weights (adjust based on evidence):
- Bull:  20% (unless specific catalysts make it higher)
- Base:  55% (the "most likely" outcome)
- Bear:  25% (raise if cash flow concerns, commodity risk, or competition exist)

Expected Value = Sum of (Scenario Midpoint x Probability)
```

### Step 5: Disclose Limitations
Always include:
- This is a P/E heuristic, not a DCF
- P/E assumptions are subjective, anchored to peer comps
- EPS estimates are top-down, not bottoms-up by segment
- Probability weights are judgment calls
- Cash flow quality should ideally be in the valuation (EV/FCF, DCF)

---

## Phase 4: Report Structure (7 Sections)

1. **Title Page** — Key metrics table (from Screener.in), disclaimers, data sources
2. **Company Snapshot** — Business overview, key facts, distribution, exports
3. **Fundamental Analysis** — Compounded growth table, quarterly trends, margins, cash flow, working capital, shareholding, cautionary flags
4. **Technical Analysis** — Price chart with MAs, support/resistance, indicator table
5. **Sector & Competitive Context** — Market size, peer comparison, sectoral index, commodity outlook, FMCG P/E table
6. **Valuation & Analyst Views** — Named brokerage targets, P/E context with peer anchoring
7. **Catalysts, Risks & Conclusion** — Management guidance, bull/bear factors, full valuation math, probability-weighted EV, methodology limitations, verdict

### Charts (Minimum 5)
1. Quarterly Revenue & Profit bars
2. Margin trend lines (Gross + EBITDA)
3. Segment revenue pie
4. Price action with MAs + support/resistance
5. Peer comparison bars

### Technical Implementation
- **Charts:** matplotlib, 150 DPI PNG
- **PDF:** reportlab with SFNS font (`/System/Library/Fonts/SFNS.ttf`)
- **Output:** `~/Desktop/{Company}_Research_Report_{Date}.pdf`

---

## Phase 5: Quality Checklist (Before Declaring Done)

- [ ] Screener.in data fetched and used as primary source
- [ ] Standalone vs Consolidated basis noted throughout
- [ ] Every number has a named source and date
- [ ] P/E discrepancies explained
- [ ] Cash flow analysis included (CFO trend, FCF, cash conversion ratio)
- [ ] Working capital days (debtor, inventory) with trend
- [ ] Shareholding with FII/DII/MF breakdown (latest quarter)
- [ ] At least 3 named brokerages with dated targets
- [ ] Peer P/E table with actual current multiples
- [ ] Sector index performance for context
- [ ] Commodity/raw material outlook relevant to the business
- [ ] Management guidance with direct quotes
- [ ] Valuation math fully shown (EPS, P/E, probability weights)
- [ ] Methodology limitations disclosed
- [ ] TTM growth vs historical CAGR compared (deceleration check)
- [ ] Disclaimer included
- [ ] Currency symbols render correctly (₹ via SFNS font)
- [ ] PDF opens cleanly, all charts render

---

## Known Gaps (Future Improvements)

1. **DCF Model** — Bottoms-up 3-statement model
2. **Consolidated vs Standalone reconciliation** — Automated check
3. **Market data API** — Live price instead of search-based approximation
4. **Insider Transactions** — Bulk/block deals, promoter pledging
5. **Options Chain** — Put-call ratio, max pain, OI patterns
6. **Historical Drawdown** — Max drawdown, recovery time, Sharpe ratio
7. **Sentiment Analysis** — News flow, Google Trends for brand
