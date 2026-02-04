---
name: stock-data-verify
description: "Verify and triangulate financial data for an Indian stock using Screener.in, BSE/NSE filings, and brokerage reports. Use when the user asks to verify data, fact-check numbers, cross-check financial metrics, or triangulate stock data."
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Grep
  - Glob
metadata:
  version: "1.0"
  author: "av-writes-code"
  created: "February 4, 2026"
---

# Stock Data Verification & Triangulation Skill

## When to Use
- User asks to "verify", "fact-check", "triangulate", "cross-check" financial data
- Before or after generating a stock report, to validate key metrics
- When two sources disagree on a metric (e.g., different P/E values)
- When Screener.in data may be stale (e.g., post-corporate action like CCPS conversion, QIP, demerger)

## Output
- Verified data table with source citations
- Discrepancy notes where sources disagree
- Staleness flags for data that may be outdated due to corporate actions

## Data Source Hierarchy (Priority Order)

### Tier 1: Primary (Must Always Check)
1. **Screener.in** — `https://www.screener.in/company/{SYMBOL}/consolidated/`
   - Extract: Equity Capital, Face Value, CFO (3-5 years), ROCE, ROE, P/E, P/B, quarterly results, working capital days, shareholding
   - Shares = Equity Capital / Face Value
   - **Staleness risk**: Screener.in updates balance sheet data quarterly. Post-corporate actions (CCPS conversion, QIP, rights issue, demerger) the equity capital may be stale until the next quarterly filing.

### Tier 2: Regulatory Filings (For Share Count, Corporate Actions)
2. **BSE India** — `https://www.bseindia.com/stock-share-price/{name}/{bse-code}/`
   - Shareholding pattern (quarterly), paid-up capital, corporate actions
3. **NSE India** — `https://www.nseindia.com/get-quotes/equity?symbol={SYMBOL}`
   - Corporate announcements, board meeting outcomes

### Tier 3: Cross-Check Sources
4. **Business Standard** — Quarterly results, analyst coverage
5. **Trendlyne** — Consensus targets, peer comparison
6. **TradingView** — Analyst targets, technical data
7. **Yahoo Finance** — `yfinance` Python library for actual price data

### Tier 4: Sector/Macro Context
8. **IMARC, CRISIL, Euromonitor** — Market size, industry growth rates
9. **RBI** (for banks) — NPA norms, capital adequacy requirements

## Verification Checklist

### Share Count (Most Common Error)
- [ ] Screener.in Equity Capital / Face Value = shares
- [ ] Cross-check: Market Cap / CMP should roughly match
- [ ] If they don't match: check for CCPS conversion, QIP, ESOP allotment, rights issue
- [ ] For recent corporate actions: WebSearch BSE announcements

### P/E Ratio
- [ ] Screener.in P/E (may be standalone or consolidated)
- [ ] Calculate: CMP / (TTM Net Profit / Shares) — should match within 5%
- [ ] Note: standalone vs consolidated basis can cause 10-30% P/E difference

### Revenue & Profit (Quarterly)
- [ ] Screener.in quarterly results vs Business Standard/Trendlyne
- [ ] Pre-demerger vs post-demerger comparability (e.g., ABFRL/ABLBL)

### Cash Flow
- [ ] Screener.in annual cash flow statement (CFO, investing, financing)
- [ ] Note: Screener.in capex is embedded in "investing activities" — may include acquisitions

### Analyst Targets
- [ ] Brokerage name, rating, target price, DATE
- [ ] Flag if target predates latest quarterly results
- [ ] Flag if target is > 3 months old
- [ ] WebSearch for the specific brokerage + stock to verify

### Banking-Specific
- [ ] NIM from quarterly results (not approximated)
- [ ] GNPA/NNPA from asset quality disclosures
- [ ] CASA from quarterly investor presentation
- [ ] Capital adequacy from Basel III disclosures
- [ ] Post-CCPS/QIP share count (often stale on Screener.in)

## Common Pitfalls
1. **Market Cap / Price for shares** — Circular. Always use Equity Capital / Face Value.
2. **Screener.in equity capital stale after corporate action** — Cross-check with BSE shareholding pattern.
3. **Standalone vs Consolidated mismatch** — Screener.in defaults to standalone. Always check `/consolidated/` URL.
4. **Analyst targets without dates** — A 12-month-old target at Rs 800 is meaningless if the stock has fallen to Rs 500.
5. **CFO vs FCF confusion** — CFO is operating cash flow. FCF = CFO - Capex. Don't conflate them.
6. **Pre/post demerger revenue** — Not comparable. Flag explicitly.

## Process
1. Identify the stock and key metrics to verify
2. WebFetch Screener.in consolidated page
3. Extract all key data points
4. For each metric, cross-check against at least one other source
5. Flag discrepancies with both values and explanation
6. Check for recent corporate actions that may make data stale
7. Output a verified data table
