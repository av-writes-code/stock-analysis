---
name: stock-critique
description: "Critique a completed stock research report (PDF or Python script) for financial accuracy, data fidelity, investment savviness, comprehensiveness, and structural quality. Use when the user asks to review, poke holes, critique, or quality-check a stock report."
allowed-tools:
  - Read
  - WebSearch
  - WebFetch
  - Grep
  - Glob
  - Task
metadata:
  version: "1.0"
  author: "av-writes-code"
  created: "February 4, 2026"
---

# Stock Report Critique — Quality Assessment Skill

## When to Use
- User asks to "critique", "review", "poke holes", "quality check" a stock report
- User wants to verify data accuracy in a completed report
- User asks to benchmark a report against institutional quality standards

## Output
- Scores across 5 dimensions (1-10 scale)
- Specific line-by-line issues categorized as Critical / Major / Minor
- Actionable fix list with sources

## Critique Framework (5 Dimensions)

### 1. Financial Accuracy (Weight: 30%)
Check every number against its claimed source:
- P/E, P/B, EPS — cross-check with Screener.in
- Revenue, PAT, margins — match to quarterly results
- Share count — verify from BSE/Screener.in equity capital / face value, NOT Market Cap / Price
- Analyst targets — verify brokerage name, rating, target price, and DATE
- Look for: internal contradictions (same metric with different values in different sections)

### 2. Data Fidelity & Sourcing (Weight: 25%)
- Is Screener.in used as primary source? (mandatory for Indian stocks)
- Are sources named and dated for every key number?
- Are approximations labeled as such? (price charts, segment splits)
- Triangulation: Are key metrics cross-checked across 2+ sources?
- Red flags: "approximately", "estimated" without qualification; round numbers without source

### 3. Investment Savviness (Weight: 20%)
- Does the bear case model REAL pain (negative growth, P/E de-rating to sector average)?
- Is the verdict consistent with the probability-weighted EV? (EV < CMP must be HOLD/AVOID)
- Are risks given equal weight to opportunities? (not just "risks exist but we're bullish anyway")
- Cash flow analysis present? (CFO trend, FCF, cash conversion — not just P&L focus)
- For banks: P/B valuation, Gordon Growth Model, credit metrics (NPA, CASA, NIM)
- For loss-makers: EV/Sales not P/S, cash burn runway, path to profitability

### 4. Comprehensiveness (Weight: 15%)
- Minimum 5 charts (revenue, margins, segments, price action, peers)
- Shareholding with FII/DII/MF breakdown and trend
- Working capital analysis (debtor days, inventory days, payable days)
- Management guidance with direct quotes
- Sector/competitive context (not just company in isolation)
- Regulatory/macro risks (e.g., EU FTA for wine, RBI norms for banks)

### 5. Structure & Presentation (Weight: 10%)
- Executive summary / verdict box on page 1
- Price chart has "approximated" disclaimer if not using real data
- Consistent formatting, no orphaned sections
- Methodology limitations disclosed
- Disclaimer present

## Scoring Guide
- **9-10**: Institutional quality (Motilal Oswal / HDFC Securities level)
- **7-8**: Publishable with minor fixes
- **5-6**: Significant gaps but usable framework
- **3-4**: Major data or analytical errors
- **1-2**: Fundamentally unreliable

## Issue Classification
- **Critical**: Factual errors that change the investment thesis (wrong EPS, misrepresented analyst rating, verdict contradicts EV)
- **Major**: Missing analysis that a serious investor would need (no cash flow, no bear stress test, stale analyst targets)
- **Minor**: Presentation/formatting issues, minor rounding differences

## Benchmark Reports
Compare against:
- Motilal Oswal initiation reports (CMP/TP/Rating box on page 1, SOTP valuation)
- HDFC Securities sector reports (peer comparison with actual multiples)
- Kotak Institutional Equities (Gordon Growth for banks)
- Nuvama (working capital decomposition)

## Process
1. Read the report script/PDF
2. For each key metric, WebSearch or WebFetch to verify against Screener.in / BSE
3. Score across 5 dimensions
4. List all issues as Critical / Major / Minor with specific line references
5. Provide actionable fix list
