# Fix All Critical Issues Across 6 Stock Reports

**Date:** February 4, 2026
**Scope:** Fix critique findings, update SKILL.md, update ANALYSIS_SOP.md, push to GitHub
**Reports:** Bikaji, Sula Vineyards, ABFRL, ABLBL, Cello World, IDFC First Bank

---

## Phase 1: Systemic Fixes (Apply to ALL 6 reports)

These 5 issues appear in multiple/all reports. Fix them in every script.

### 1.1 Add Executive Summary Box on Page 1
**What:** Every report lacks a one-line verdict on the title page.
**Fix:** After the metrics table on page 1, add a colored callout box:
```
VERDICT: [BUY/HOLD/AVOID] | Expected Value: Rs [X] ([Y]% upside/downside)
Key Bull: [one line] | Key Bear: [one line]
```
**Logic:** A fund manager needs Buy/Hold/Sell + target in 30 seconds.
**Benchmark:** Motilal Oswal initiation reports always have a "CMP / TP / Rating" box on page 1.

### 1.2 Add "APPROXIMATED" Watermark on All Price Charts
**What:** Price charts use estimated monthly closes and simulated MAs. This is disclosed only in Python comments, not in the PDF.
**Fix:** Add a visible subtitle under each price chart title:
```python
ax.set_title('...Price Action...', fontweight='bold')
ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
        transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')
```
**Logic:** Transparency rule from SKILL.md: "Every number must have a named source and date."

### 1.3 Fix Shares Outstanding (Use Primary Source, Not Market Cap / Price)
**What:** All reports derive shares as `Market Cap / Price` (circular). This cascades into EPS and P/E errors.
**Fix:** For each stock, use WebSearch to verify actual shares outstanding from BSE filings or Screener.in's "No. of Equity Shares" field. Hard-code the verified number with source citation.
**Verification:** `Price / (Net Profit / Shares) = P/E` must match Screener.in within 5%.

### 1.6 Data Triangulation & Anti-Approximation Protocol
**What:** Reports rely too heavily on approximations (estimated monthly prices, estimated segment splits, unverified figures).
**Mandatory data hierarchy:**
1. **Screener.in (FREE tier)** — ABSOLUTE MUST for every stock. WebFetch both standalone and consolidated pages. Extract: Compounded Growth, Quarterly Results, Annual P&L/BS/CF, Ratios, Working Capital days, Shareholding.
2. **BSE/NSE filings** — For share count, shareholding pattern, board resolutions, CCPS conversion details.
3. **Company press releases / earnings call transcripts** — For management guidance, segment data, direct quotes.
4. **Named brokerage reports** (via TradingView, Business Standard) — For analyst targets with dates.
5. **Sector data** (IMARC, CRISIL, industry bodies) — For market size, growth rates.

**Triangulation rules:**
- Every KEY metric (revenue, PAT, EPS, P/E, shares outstanding) must be cross-checked across at least 2 sources.
- If two sources disagree, note both values and explain the discrepancy.
- If a data point cannot be verified from at least one authoritative source, label it "UNVERIFIED" or "ESTIMATED" in the report.
- Never present estimated/approximated data as fact. Always use qualifiers: "approximately", "estimated", "illustrative".
- Price charts: If actual daily/monthly closing prices are unavailable, use yfinance Python library to fetch real prices instead of approximating.

**For price data specifically:**
```python
import yfinance as yf
ticker = yf.Ticker("SYMBOL.NS")
hist = ticker.history(period="1y", interval="1mo")
# Use actual monthly closes instead of approximated values
```

### 1.4 Add Cash Flow Analysis Section (CFO, FCF, Cash Conversion)
**What:** SKILL.md quality checklist requires "CFO trend, FCF, cash conversion ratio." Only Bikaji partially delivers.
**Fix:** In each report's Fundamental Analysis section, add:
```
Cash Flow Analysis (Screener.in, Consolidated)
| Year    | CFO (Cr) | Capex (Cr) | FCF (Cr) | Cash Conv. (CFO/PAT) |
| FY22    | ...      | ...        | ...      | ...%                 |
| FY23    | ...      | ...        | ...      | ...%                 |
| FY24    | ...      | ...        | ...      | ...%                 |
| FY25    | ...      | ...        | ...      | ...%                 |
```
**Data source:** WebFetch Screener.in cash flow statement for each stock.
**For IDFC First Bank (bank):** Skip CFO/FCF, instead add Credit Cost Ratio, PCR, Slippage Ratio.

### 1.5 Stress-Test Bear Cases
**What:** Bear case P/E floors and probability weights are too mild across all reports.
**Fix:** For each report, check:
- Does the bear P/E go AT LEAST to sector-average or below? (Not just "slightly below")
- Is bear probability >= 30% for stocks with deteriorating fundamentals?
- Does the bear scenario model NEGATIVE growth, not just "growth halves"?
- Add a "worst case" footnote for extreme scenarios (e.g., 10% probability at 15x P/E)

---

## Phase 2: Per-Report Critical Fixes

### 2.1 Bikaji Foods (7.4 -> target 8.5)
**File:** `/private/tmp/.../scratchpad/bikaji_report.py`

| # | Issue | Fix | Tool |
|---|-------|-----|------|
| 1 | Q3 revenue mismatch: chart 776 vs text 731 | WebSearch "Bikaji Q3 FY26 revenue" to verify. Update whichever is wrong. | WebSearch + Edit |
| 2 | Cash conversion: 30% vs 39% | Calculate once (FCF/PAT), use consistently everywhere | Edit |
| 3 | EBITDA margin bps: 466 vs 430 | Fix: 12.5 - 8.2 = 4.3 ppts = 430 bps | Edit |
| 4 | 52-week high 818.70 vs resistance 864 | Clarify: 818.70 is closing high, 864 was intraday. Or correct resistance zone. | Edit |

### 2.2 Sula Vineyards (7.0 -> target 8.0)
**File:** `/Users/arpitvyas/Desktop/stock-analysis/sula-vineyards/sula_report.py`

| # | Issue | Fix | Tool |
|---|-------|-----|------|
| 1 | 5Y rev CAGR 3.6% vs market 14-16% = market share loss | Add explicit paragraph: "Sula's 5Y revenue CAGR of 3.6% significantly lags the Indian wine market CAGR of 14-16%, indicating market share erosion" | Edit |
| 2 | Cash flow analysis absent | Add CFO/FCF table from Screener.in (FY22-FY25) | WebFetch + Edit |
| 3 | Bear case too mild (0% FY27 growth, 20-25x P/E) | Change bear to -15% FY27 growth, 15-20x P/E. Raise bear probability to 40% | Edit |
| 4 | ROCE contradiction (25.3% vs 18.2%) | Pick one source, note the other as discrepancy | Edit |
| 5 | P/E sanity check exceeds 5% | Fix shares outstanding from primary source | WebSearch + Edit |

### 2.3 ABFRL (6.0 -> target 7.5)
**File:** `/Users/arpitvyas/Desktop/stock-analysis/abfrl/abfrl_report.py`

| # | Issue | Fix | Tool |
|---|-------|-----|------|
| 1 | P/S inconsistency (1.03x vs 0.91x) | Verify actual share count from BSE. Recalculate P/S with correct shares. | WebSearch + Edit |
| 2 | Zero cash flow analysis | Add cash burn waterfall: Operating outflow, Capex, Lease payments, Net burn, Runway | WebFetch + Edit |
| 3 | TTM revenue mixing pre/post-demerger | Add explicit note: "TTM revenue uses Screener.in restated continuing-operations basis" | Edit |
| 4 | Should use EV/Sales not P/S | Switch primary valuation to EV/Sales. Show EV derivation (MCap + Debt - Cash). Keep P/S as secondary. | Edit |
| 5 | Bear case not harsh enough | Add 0.4x P/S worst-case scenario (Shoppers Stop level). Raise bear to 40%. | Edit |

### 2.4 ABLBL (5.4 -> target 7.0)
**File:** `/Users/arpitvyas/Desktop/stock-analysis/ablbl/ablbl_report.py`

| # | Issue | Fix | Tool |
|---|-------|-----|------|
| 1 | EV Rs 101 contradicts ACCUMULATE verdict | Change verdict to HOLD/NEUTRAL. Or re-run valuation with adjusted bear probability to get EV > CMP. Be honest about the contradiction. | Edit |
| 2 | QIP dilution ignored in share count | WebSearch actual post-QIP share count. Recalculate all EPS figures. | WebSearch + Edit |
| 3 | LTL growth not quantified for Lifestyle | WebSearch "ABLBL same store sales growth Q3 FY26" or "LTL growth lifestyle brands" | WebSearch + Edit |
| 4 | Brand pie uses fabricated data | Add prominent "ILLUSTRATIVE ONLY - individual brand splits not disclosed" watermark. Or replace with segment-level bar (Lifestyle vs Emerging) using reported data only. | Edit |
| 5 | Trailing P/E 293x misleading | Change to "N/M (Newly Listed)" on title page. Show only forward P/E. | Edit |

### 2.5 Cello World (6.4 -> target 7.5)
**File:** `/Users/arpitvyas/Desktop/stock-analysis/cello-world/cello_world_report.py`

| # | Issue | Fix | Tool |
|---|-------|-----|------|
| 1 | CFO unverified (-47 Cr standalone) | WebSearch "Cello World FY25 cash flow from operations standalone" to verify. If unverifiable, add prominent caveat. | WebSearch + Edit |
| 2 | Working capital days not decomposed | WebFetch Screener.in for debtor days, inventory days, payable days separately | WebFetch + Edit |
| 3 | Glass plant contribution not quantified | Add: "At 80% utilization (16,000 MT), est. revenue contribution ~Rs X Cr (Y% of total)" | WebSearch + Edit |
| 4 | Missing FCF analysis | Add CFO-Capex=FCF table from Screener.in | WebFetch + Edit |
| 5 | Bear P/E floor too high (24-28x) | Extend to 18-24x for true bear (commodity company multiples) | Edit |

### 2.6 IDFC First Bank (5.6 -> target 7.5)
**File:** `/Users/arpitvyas/Desktop/stock-analysis/idfc-first-bank/idfc_first_bank_report.py`

| # | Issue | Fix | Tool |
|---|-------|-----|------|
| 1 | UBS rating MISREPRESENTED as Neutral | Fix to: UBS SELL, Rs 75 target (Nov 19, 2025). Do NOT soften. | Edit |
| 2 | BV/share temporal mismatch | Use current BV/share (~Rs 52.9 post-capital raise) as primary. P/B = 84/52.9 = 1.60x. | Edit |
| 3 | CCPS conversion price omitted | Add: "Warburg CCPS converted at Rs 60/share (VWAP trigger). This provides Rs 60 institutional floor." | Edit |
| 4 | No credit cost, PCR, slippage ratio | WebSearch these metrics. Add a Banking Quality Metrics table. | WebSearch + Edit |
| 5 | Dilution impact not quantified | Add EPS bridge: FY24 EPS Rs 4.85 (610 Cr shares) -> FY25 EPS Rs 1.77 (860 Cr shares). Show PAT needed to restore peak EPS. | Edit |
| 6 | 9% expected return vs risk-free rate | Add note: "Expected 9% return barely exceeds 1Y G-Sec yield of 7-7.5%, offering minimal risk premium for a turnaround bet." | Edit |

---

## Phase 3: Execution Plan

### Tools & Approach
1. **WebSearch** — Verify data points: UBS rating, actual share counts (6 stocks), CFO figures, CCPS price, credit metrics
2. **WebFetch** — Screener.in cash flow statements for all 6 stocks (add CFO/FCF tables)
3. **Edit** — Targeted edits to each Python script (fix numbers, add sections, fix text)
4. **Bash** — Re-run all 6 scripts to regenerate PDFs
5. **Read** — Verify PDFs render correctly

### Execution Order
1. **Data verification round** (parallel WebSearch agents for all 6 stocks — share counts, UBS, CFO)
2. **Systemic fixes** (executive summary, price chart disclaimer — edit all 6 scripts)
3. **Per-report fixes** (edit each script with verified data)
4. **Regenerate all 6 PDFs** (bash python3 for each)
5. **Update SKILL.md** with lessons learned (new rules from critique findings)
6. **Update ANALYSIS_SOP.md** on GitHub
7. **Git commit and push**

### Benchmark Reports (for quality reference)
- **Motilal Oswal initiation reports** — Gold standard for Indian equity research: CMP/TP/Rating box on page 1, SOTP valuation, segment-level analysis, credit cost trends for banks
- **HDFC Securities sector reports** — Peer comparison tables with actual multiples, margin bridge analysis
- **Kotak Institutional Equities** — Gordon Growth Model for bank valuation, justified P/B calculation
- **Nuvama (formerly Edelweiss)** — Detailed working capital analysis, inventory days decomposition

### Key Principles from Benchmarks
1. **Page 1 must have the verdict** — Every institutional report opens with Rating + TP + key thesis
2. **Show the margin bridge** — Not just "margin improved 430 bps" but WHY (RM cost -200 bps, mix +150 bps, opex leverage +80 bps)
3. **Cash flow > P&L** — Institutional reports spend more space on cash flow quality than revenue growth
4. **Peer multiples must be CURRENT** — Not "approximately" — exact figures with dates
5. **Bear case = real pain** — Institutional bear cases model 30-50% downside, not 10-15%
6. **Fabricated data must be labeled** — Any estimated chart gets "Illustrative" watermark

---

## Phase 4: SKILL.md Updates (Post-Fix)

Add these new rules based on critique findings:

### New Critical Rules (append to existing 7)
8. **Executive summary on page 1.** Every report must have a verdict box (Rating, Expected Value, Key Bull/Bear) on the title page.
9. **Shares outstanding from primary source.** Never derive shares as Market Cap / Price. Use BSE filings, Screener.in, or annual report. Cite the source.
10. **Price chart transparency.** All approximated price charts must have a visible "Approximated monthly data; MAs are illustrative" disclaimer IN THE PDF (not just in code comments).
11. **Cash flow is mandatory.** CFO trend (3-5 years), FCF (CFO - Capex), and Cash Conversion Ratio (CFO/PAT) must appear in every report. For banks: substitute Credit Cost Ratio, PCR, Slippage Ratio.
12. **Bear case stress test.** Bear P/E must go to sector average or below. Bear probability must be >= 30% for any stock with: (a) declining profits, (b) negative cash flow, (c) institutional selling, or (d) credit rating downgrades. Must model negative growth, not just slower growth.
13. **Verdict must match EV.** If probability-weighted Expected Value < CMP, verdict MUST be HOLD or AVOID, not BUY. No exceptions.
14. **No fabricated charts.** If individual data is not disclosed (e.g., brand-level revenue), use only reported segment data. Any estimated chart must have prominent "ILLUSTRATIVE ONLY" label.
15. **Analyst targets must be dated.** Flag any target older than 3 months. Flag any target that predates the latest quarterly results.

### New Quality Checklist Items (append to existing 17)
- [ ] Executive summary box on page 1 with Rating + EV
- [ ] Shares outstanding from primary source (not derived)
- [ ] Price chart has visible "approximated" disclaimer
- [ ] Cash flow table: CFO, Capex, FCF, Cash Conversion (3+ years)
- [ ] Bear case P/E at or below sector average
- [ ] Bear probability >= 30% if fundamentals deteriorating
- [ ] Verdict consistent with probability-weighted EV (EV < CMP = HOLD/AVOID)
- [ ] All estimated/approximated charts labeled as such
- [ ] Analyst targets flagged if > 3 months old

### Banking-Specific Additions (new section)
When analyzing a bank:
- Use P/B (not P/E) as primary valuation metric
- Include Gordon Growth Model: Justified P/B = (ROE - g) / (CoE - g)
- Required metrics: NIM, GNPA/NNPA, CASA, Cost-to-Income, ROA, ROE, CAR (CET1 breakdown)
- Credit quality section: Credit Cost Ratio trend, PCR, Slippage Ratio, Restructured Book
- Dilution analysis: Show EPS bridge if significant share issuance

### Loss-Making Company Additions (new section)
When analyzing a loss-making company:
- Use EV/Sales (not P/S) as primary if significant debt/leases
- Show EV derivation: Market Cap + Net Debt (including lease liabilities if material)
- Cash burn waterfall: Operating outflow, Capex, Lease payments, Net burn, Runway
- Path to profitability timeline with specific milestones
- Bear probability minimum 35%

### Subagent Usage (new section)
When spawning subagents via Task tool for report generation:
- Subagents CANNOT invoke the Skill tool
- Embed full methodology by instructing agents to READ this SKILL.md file as Step 1
- Also instruct agents to READ the Bikaji template script as structural reference
- Agents often get auto-denied on Bash — the parent thread should run Python scripts

---

## Phase 5: Verification

1. All 6 PDFs regenerate without errors
2. Each PDF has executive summary on page 1
3. Each price chart has visible "approximated" disclaimer
4. Cash flow table present in all 6 reports
5. UBS correctly shown as SELL in IDFC report
6. ABLBL verdict consistent with its expected value
7. Git push succeeds with updated SKILL.md + ANALYSIS_SOP.md + all report scripts
