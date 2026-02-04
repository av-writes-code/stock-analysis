---
name: whatsapp-stock-summary
description: "Generate a WhatsApp-ready stock summary with green/red flags, analyst targets, and verdict from a completed stock research report. Use when the user asks for a WhatsApp summary, quick summary, or shareable stock note."
allowed-tools:
  - Read
  - Grep
  - WebSearch
metadata:
  version: "1.0"
  author: "av-writes-code"
  created: "February 4, 2026"
---

# WhatsApp Stock Summary Generator

## When to Use
- User asks for a "WhatsApp summary", "quick summary", "shareable note" for a stock
- User wants a concise version of a completed PDF report
- User asks to summarize stock analysis for sharing

## Output Format
```
### [STOCK NAME] (Rs [CMP]) — [VERDICT]

GREEN FLAGS:
+ [4-6 bullish points with data, sourced]

RED FLAGS:
- [4-6 bearish points with data, sourced]

[REGULATORY/MACRO UPDATE if relevant]:
- [Key recent development with date and source]

ANALYST TARGETS:
- [3-5 named brokerages with rating, target, date]
- Consensus ([N] analysts): Rs [X], [Buy/Hold/Sell] breakdown

VERDICT: [VERDICT]. Expected value Rs [X] ([Y]% upside/downside).
_Assumption: [Key assumption in 1-2 lines]_
```

## Rules

### Content Rules
1. **Every bullet must have data** — not just "strong brand" but "ROCE 23.7% (Screener.in)"
2. **Source in parentheses** — (Screener.in), (BSE), (Business Standard Jan 2026)
3. **Analyst targets must be named and dated** — not "analysts say Buy"
4. **Flag stale targets** — any target > 3 months old gets a "STALE" note
5. **Assumptions in italics** — explain key valuation assumptions in verdict line
6. **If our EV differs from consensus, explain why** — e.g., "Our EV is conservative vs consensus because we assign 40% bear probability"

### What to Include from the PDF Report
- Green/red flags: Pick the 4-6 most impactful from fundamentals section
- Analyst targets: All named brokerages from the valuation section
- Regulatory/macro: Any recent development (FTA, RBI policy, commodity price)
- Verdict: Must match the PDF report's verdict exactly
- Working capital red flags if material (debtor days, inventory days)
- Shareholding red flags if material (promoter decline, FII exit)
- Cash flow red flags if material (CFO decline, negative FCF)

### What NOT to Include
- Technical analysis details (RSI, MACD, support/resistance)
- Full valuation math (bull/base/bear scenarios)
- Detailed segment breakdowns
- Chart descriptions
- These belong in the full PDF report

### Ranking (If Multiple Stocks)
When summarizing multiple stocks, add a ranking at the end:
```
RANKING (1-Year Risk-Adjusted):
1. [STOCK] — [VERDICT], [X]% upside, [key reason]
...
```
Rank by: (1) EV upside %, (2) analyst consensus strength, (3) fundamental quality (ROCE, cash flow)

### Disclaimer
Always end with:
```
_DISCLAIMER: Not financial advice. For educational purposes only. Consult a SEBI-registered advisor._
```

## Process
1. Read the completed report script or PDF
2. Extract green flags (strongest 4-6 fundamental positives)
3. Extract red flags (strongest 4-6 risks/concerns)
4. Extract analyst targets with names, ratings, dates
5. Check for any recent regulatory/macro development via WebSearch
6. Format as WhatsApp message
7. Add assumptions note under verdict
