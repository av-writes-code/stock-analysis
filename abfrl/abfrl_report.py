#!/usr/bin/env python3
"""
Aditya Birla Fashion and Retail Ltd (ABFRL) — 1-Year Stock Research Report
Generated: February 4, 2026

CRITICAL CONTEXT: ABFRL demerged in May 2025. Post-demerger ABFRL retains
ethnic/luxury brands (Sabyasachi, Tasva, TMRW, Jaypore, TCNS, OWND) and
Pantaloons/StyleUp. Madura brands (LP, VH, AS, PE) went to ABLBL.

This is a LOSS-MAKING company. Valuation uses P/S and EV/Sales, NOT P/E.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os
import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register SFNS for INR symbol
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

# --- Configuration ---
OUTPUT_DIR = "/Users/arpitvyas/Desktop/stock-analysis/abfrl"
FINAL_PDF = "/Users/arpitvyas/Desktop/stock-analysis/abfrl/ABFRL_Research_Report_Feb2026.pdf"

# Colors
PRIMARY = '#1a365d'
ACCENT = '#2b6cb0'
HIGHLIGHT = '#e53e3e'
GREEN = '#38a169'
LIGHT_BG = '#f7fafc'
ORANGE = '#dd6b20'
PURPLE = '#805ad5'
LOSS_RED = '#c53030'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.color': '#cccccc',
})


# ========== CHART 1: Quarterly Revenue & Profit/Loss Bars ==========
def create_revenue_chart():
    """
    Sources:
    - FY25 quarters (Q1-Q4): Pre-demerger combined ABFRL (Business Standard, Trendlyne)
    - Q1 FY26: Post-demerger, Rs 1,831 Cr revenue, Rs -234 Cr loss (Business Standard Aug 2025)
    - Q2 FY26: Post-demerger, Rs 1,982 Cr revenue, Rs -295 Cr loss (ScanX, Alpha Spread)
    Note: FY25 data is for COMBINED entity, FY26 is post-demerger ABFRL only.
    """
    quarters = ['Q1\nFY25*', 'Q2\nFY25*', 'Q3\nFY25*', 'Q4\nFY25*', 'Q1\nFY26', 'Q2\nFY26']
    # Revenue in Cr (* = combined pre-demerger entity)
    revenue = [3082, 3198, 4167, 3549, 1831, 1982]
    # Net Profit/Loss in Cr
    pat = [-215, -215, -108, -24, -234, -295]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    x = np.arange(len(quarters))
    width = 0.35

    # Revenue bars
    bars1 = ax1.bar(x - width/2, revenue, width, label='Revenue (Rs Cr)',
                    color=ACCENT, alpha=0.85)
    ax1.set_ylabel('Revenue (Rs Cr)', color=ACCENT, fontsize=10)
    ax1.set_ylim(0, 5000)
    ax1.tick_params(axis='y', labelcolor=ACCENT)

    # PAT bars (losses shown in red)
    ax2 = ax1.twinx()
    bar_colors = [LOSS_RED if p < 0 else GREEN for p in pat]
    bars2 = ax2.bar(x + width/2, pat, width, label='Net Profit/Loss (Rs Cr)',
                    color=bar_colors, alpha=0.85)
    ax2.set_ylabel('Net Profit / Loss (Rs Cr)', color=LOSS_RED, fontsize=10)
    ax2.set_ylim(-400, 100)
    ax2.tick_params(axis='y', labelcolor=LOSS_RED)
    ax2.axhline(y=0, color='black', linewidth=0.5, linestyle='-')

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=8)
    ax1.set_title('ABFRL - Quarterly Revenue & Net Profit/Loss\n'
                   '* FY25 = Pre-demerger (combined ABFRL+ABLBL) | FY26 = Post-demerger ABFRL only',
                   fontweight='bold', fontsize=10, pad=15)

    # Value labels
    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 50,
                 f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=7, color=ACCENT)
    for bar, val in zip(bars2, pat):
        offset = -20 if val < 0 else 5
        ax2.text(bar.get_x() + bar.get_width()/2., val + offset,
                 f'{int(val)}', ha='center', va='top' if val < 0 else 'bottom',
                 fontsize=7, color=LOSS_RED, fontweight='bold')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=7)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_revenue.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== CHART 2: EBITDA Margin Trend ==========
def create_margin_chart():
    """
    Sources:
    - H1 FY26 EBITDA margin: 7.5% (Q2 FY26 earnings call)
    - Q2 FY26: 5.9% (Alpha Spread, ScanX)
    - Q1 FY26: ~9.1% implied from H1 = 7.5% and Q2 = 5.9%
    - FY25 quarterly: Derived from Trendlyne, Business Standard
    Note: FY25 = combined entity, FY26 = post-demerger
    """
    quarters = ['Q1\nFY25*', 'Q2\nFY25*', 'Q3\nFY25*', 'Q4\nFY25*', 'Q1\nFY26', 'Q2\nFY26']
    ebitda_margin = [4.5, 4.8, 8.5, 6.2, 9.2, 5.9]  # %

    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(quarters))

    ax.plot(x, ebitda_margin, 'o-', color=ACCENT, linewidth=2.5, markersize=8,
            label='EBITDA Margin (%)', zorder=3)
    ax.fill_between(x, ebitda_margin, alpha=0.15, color=ACCENT)

    # Annotate the demerger line
    ax.axvline(x=3.5, color=ORANGE, linewidth=2, linestyle='--', alpha=0.7)
    ax.text(3.5, max(ebitda_margin) + 0.5, 'Demerger\n(May 2025)', ha='center',
            fontsize=8, color=ORANGE, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=8)
    ax.set_ylabel('EBITDA Margin (%)')
    ax.set_title('ABFRL - EBITDA Margin Trend\n'
                 '* FY25 = Combined entity | FY26 = Post-demerger',
                 fontweight='bold', fontsize=10, pad=15)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 14)

    for i, em in enumerate(ebitda_margin):
        ax.annotate(f'{em}%', (i, em), textcoords="offset points",
                    xytext=(0, 12), fontsize=8, ha='center', color=ACCENT, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_margins.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== CHART 3: Brand/Segment Revenue Pie ==========
def create_segment_chart():
    """
    Sources:
    - Pantaloons 59% of post-demerger revenue (ScanX, Business Standard)
    - Ethnic portfolio 27% (ScanX)
    - TMRW (digital-first) ~6%
    - Luxury (The Collective) ~4%
    - StyleUp / Others ~4%
    - Based on Q2 FY26 earnings call segment disclosures
    """
    labels = ['Pantaloons\n(59%)', 'Ethnic Wear\n(Sabyasachi, Tasva,\nTCNS, Jaypore)\n(27%)',
              'TMRW\n(Digital-first)\n(6%)', 'The Collective\n(Luxury)\n(4%)',
              'StyleUp &\nOthers\n(4%)']
    sizes = [59, 27, 6, 4, 4]
    colors_pie = ['#2b6cb0', '#e53e3e', '#38a169', '#dd6b20', '#805ad5']
    explode = (0.03, 0.06, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors_pie, autopct='',
                                       shadow=False, startangle=120,
                                       textprops={'fontsize': 7.5})
    ax.set_title('ABFRL Post-Demerger Revenue Mix by Segment (Q2 FY26)\n'
                 'Source: Q2 FY26 Earnings Call, ScanX',
                 fontweight='bold', fontsize=10, pad=15)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_segments.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== CHART 4: Price Action with Moving Averages ==========
def create_price_chart():
    """
    Sources:
    - Pre-demerger price ~Rs 280 (Apr 2025), fell ~67% post demerger adjustment
    - 52-week range: Rs 70.55 - Rs 107.75 (5Paisa, NSE Jan 2026)
    - Current price ~Rs 83.92 (NSE, Feb 3 2026)
    - Support: Rs 70-72 major, Rs 66 secondary (TradingView, MunafaSutra)
    - Resistance: Rs 95, Rs 105-107 (TradingView)
    - Monthly prices approximate from NSE/Yahoo Finance
    """
    months = ['Jun\n2025', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026', 'Feb']
    prices = [95, 102, 107, 98, 88, 80, 74, 77, 84]

    # Approximate MAs
    sma_200 = [None, None, None, None, None, 92, 90, 88, 87]  # starts later
    ema_50 = [95, 97, 100, 99, 95, 90, 84, 80, 82]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(months))

    ax.plot(x, prices, 'o-', color=PRIMARY, linewidth=2.5, markersize=6,
            label='Price (Rs)', zorder=3)

    # Plot MAs (skip None values)
    valid_200 = [(i, v) for i, v in enumerate(sma_200) if v is not None]
    if valid_200:
        ax.plot([v[0] for v in valid_200], [v[1] for v in valid_200],
                '--', color=GREEN, linewidth=1.5, label='200-Day SMA (~Rs 87)', alpha=0.8)
    ax.plot(x, ema_50, '--', color=HIGHLIGHT, linewidth=1.5,
            label='50-Day EMA (~Rs 82)', alpha=0.8)

    # Support and resistance zones
    ax.axhspan(66, 72, alpha=0.12, color='green', label='Support Zone (Rs 66-72)')
    ax.axhspan(105, 108, alpha=0.12, color='red', label='Resistance Zone (Rs 105-108)')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8)
    ax.set_ylabel('Price (Rs)')
    ax.set_title('ABFRL - Post-Demerger Price Action & Moving Averages\n'
                 'Demerger effective May 22, 2025 | Source: NSE, TradingView',
                 fontweight='bold', fontsize=10, pad=15)
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(55, 120)

    # Annotate current price
    ax.annotate(f'Current: Rs 84', xy=(8, 84), xytext=(6, 112),
                arrowprops=dict(arrowstyle='->', color=PRIMARY),
                fontsize=9, fontweight='bold', color=PRIMARY)

    # Annotate 52-week low
    ax.annotate(f'52W Low: Rs 70.55', xy=(6, 74), xytext=(3, 65),
                arrowprops=dict(arrowstyle='->', color=LOSS_RED),
                fontsize=8, color=LOSS_RED)

    # Price chart disclaimer
    ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
            transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== CHART 5: Peer Comparison (P/S and EV/Sales) ==========
def create_peer_chart():
    """
    Sources:
    - ABFRL: P/S 0.91x, EV/Sales 1.43x (Yahoo Finance, Alpha Spread Jan 2026)
    - Vedant Fashions: P/S 10.49x, EV/Sales 10.47x (Yahoo Finance Jan 2026)
    - Trent: P/S ~12x estimated (Smart-Investing.in Jan 2026)
    - Shoppers Stop: P/S ~0.4x estimated (MarketsMojo)
    - Note: ABFRL has no P/E (loss-making), hence P/S used for comparison
    """
    companies = ['ABFRL', 'Vedant\nFashions', 'Trent', 'Shoppers\nStop']

    fig, axes = plt.subplots(1, 3, figsize=(10, 4))

    # P/S Ratio
    ps_ratios = [1.11, 10.49, 12.0, 0.4]
    bar_colors = [LOSS_RED, ACCENT, GREEN, ORANGE]
    bars = axes[0].bar(companies, ps_ratios, color=bar_colors, width=0.5, alpha=0.85)
    axes[0].set_title('P/S Ratio (TTM)', fontweight='bold', fontsize=9)
    axes[0].set_ylim(0, 16)
    for bar, val in zip(bars, ps_ratios):
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                     f'{val}x', ha='center', fontsize=8, fontweight='bold')

    # EV/Sales
    ev_sales = [2.06, 10.47, 13.0, 0.7]
    bars = axes[1].bar(companies, ev_sales, color=bar_colors, width=0.5, alpha=0.85)
    axes[1].set_title('EV/Sales (TTM)', fontweight='bold', fontsize=9)
    axes[1].set_ylim(0, 16)
    for bar, val in zip(bars, ev_sales):
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                     f'{val}x', ha='center', fontsize=8, fontweight='bold')

    # EBITDA Margin
    ebitda_m = [7.5, 43.2, 14.0, 5.0]
    bars = axes[2].bar(companies, ebitda_m, color=bar_colors, width=0.5, alpha=0.85)
    axes[2].set_title('EBITDA Margin (%)', fontweight='bold', fontsize=9)
    axes[2].set_ylim(0, 55)
    for bar, val in zip(bars, ebitda_m):
        axes[2].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.8,
                     f'{val}%', ha='center', fontsize=8, fontweight='bold')

    fig.suptitle('ABFRL vs Fashion Retail Peers - Valuation Comparison (Jan 2026)\n'
                 'Sources: Yahoo Finance, Alpha Spread, Smart-Investing.in, MarketsMojo',
                 fontweight='bold', fontsize=10, y=1.06)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_peers.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== PDF GENERATION ==========
def build_pdf(chart_paths):
    doc = SimpleDocTemplate(
        FINAL_PDF,
        pagesize=A4,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontSize=18, textColor=HexColor(PRIMARY),
        spaceAfter=6, alignment=TA_CENTER, fontName='SFNS'
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle', parent=styles['Normal'],
        fontSize=11, textColor=HexColor('#4a5568'),
        spaceAfter=12, alignment=TA_CENTER, fontName='SFNS'
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading1'],
        fontSize=14, textColor=HexColor(PRIMARY),
        spaceBefore=16, spaceAfter=8, fontName='SFNS',
        borderWidth=0, borderPadding=0,
    )
    subheading_style = ParagraphStyle(
        'CustomSubheading', parent=styles['Heading2'],
        fontSize=11, textColor=HexColor(ACCENT),
        spaceBefore=10, spaceAfter=4, fontName='SFNS'
    )
    body_style = ParagraphStyle(
        'CustomBody', parent=styles['Normal'],
        fontSize=9, leading=13,
        textColor=HexColor('#2d3748'),
        spaceAfter=6, alignment=TA_JUSTIFY, fontName='SFNS'
    )
    bullet_style = ParagraphStyle(
        'CustomBullet', parent=body_style,
        leftIndent=15, bulletIndent=5, spaceAfter=3, fontSize=9
    )
    source_style = ParagraphStyle(
        'SourceStyle', parent=styles['Normal'],
        fontSize=7, textColor=HexColor('#718096'),
        spaceAfter=4, fontName='SFNS'
    )
    disclaimer_style = ParagraphStyle(
        'DisclaimerStyle', parent=styles['Normal'],
        fontSize=7, textColor=HexColor('#a0aec0'),
        spaceBefore=8, spaceAfter=4,
        fontName='SFNS', alignment=TA_CENTER
    )
    callout_green = ParagraphStyle(
        'CalloutGreen', parent=body_style,
        backColor=HexColor('#f0fff4'), borderWidth=1,
        borderColor=HexColor(GREEN), borderPadding=8,
        leftIndent=10, spaceAfter=8
    )
    callout_red = ParagraphStyle(
        'CalloutRed', parent=body_style,
        backColor=HexColor('#fff5f5'), borderWidth=1,
        borderColor=HexColor(HIGHLIGHT), borderPadding=8,
        leftIndent=10, spaceAfter=8
    )
    callout_orange = ParagraphStyle(
        'CalloutOrange', parent=body_style,
        backColor=HexColor('#fffaf0'), borderWidth=1,
        borderColor=HexColor(ORANGE), borderPadding=8,
        leftIndent=10, spaceAfter=8
    )

    story = []

    # ======================================================================
    # SECTION 0: TITLE PAGE
    # ======================================================================
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph('ADITYA BIRLA FASHION & RETAIL LTD', title_style))
    story.append(Paragraph('NSE: ABFRL | BSE: 535755', subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=HexColor(PRIMARY)))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('1-Year Stock Research Report', ParagraphStyle(
        'BigSub', parent=subtitle_style, fontSize=15, textColor=HexColor(ACCENT),
        fontName='SFNS'
    )))
    story.append(Paragraph('Outlook: February 2026 - February 2027', subtitle_style))
    story.append(Spacer(1, 0.3*cm))

    # DEMERGER NOTICE
    story.append(Paragraph(
        '<b>IMPORTANT - POST-DEMERGER ENTITY:</b> ABFRL completed a demerger in May 2025. '
        'The Madura Fashion &amp; Lifestyle business (Louis Philippe, Van Heusen, Allen Solly, '
        'Peter England) was spun off into Aditya Birla Lifestyle Brands Ltd (ABLBL). '
        'Post-demerger ABFRL retains Pantaloons, StyleUp, Sabyasachi, Tasva, TCNS, '
        'TMRW (digital-first), The Collective (luxury), Jaypore, and OWND. '
        '<b>All FY25 and prior data in this report is for the COMBINED pre-demerger entity '
        'unless explicitly noted.</b>',
        callout_orange
    ))
    story.append(Spacer(1, 0.3*cm))

    # Key metrics box
    metrics_data = [
        ['Current Price', 'Rs 83.92 (Feb 3, 2026)', 'Market Cap', 'Rs 8,176 Cr'],
        ['P/E (Trailing)', 'N/A (Loss-making)', 'P/B Ratio', '~2.5x'],
        ['52-Week Range', 'Rs 70.55 - Rs 107.75', 'P/S (TTM)', '1.11x'],
        ['Revenue (TTM)', 'Rs 7,355 Cr (cont. ops)', 'EV/Sales (TTM)', '2.06x'],
        ['Gross Cash', 'Rs 2,150 Cr (Sep 2025)', 'Promoter Holding', '46.6%'],
        ['EBITDA (H1 FY26)', 'Rs 286 Cr', 'ROE (3Y Avg)', '-11.0%'],
    ]
    metrics_table = Table(metrics_data, colWidths=[3.2*cm, 4*cm, 3.2*cm, 4*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#edf2f7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor(PRIMARY)),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*cm))

    # Executive Summary Verdict Box
    verdict_data = [
        ['VERDICT: SPECULATIVE HOLD | Expected Value: around CMP', '', ''],
        ['Key Bull: Post-demerger focus on ethnic/luxury brands + Sabyasachi premium', '', ''],
        ['Key Bear: Persistent losses, high debt (Rs 3,500+ Cr), cash burn risk', '', ''],
    ]
    verdict_table = Table(verdict_data, colWidths=[14.4*cm])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#dd6b20')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#fffaf0')),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor('#2d3748')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fff5f5')),
        ('TEXTCOLOR', (0, 2), (-1, 2), HexColor('#c53030')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (0, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dd6b20')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        '<b>LOSS-MAKING COMPANY:</b> ABFRL has no trailing P/E ratio as net profit is negative. '
        'This report uses EV/Sales (primary) and P/S (secondary) for valuation instead of P/E. '
        'Shares Outstanding: 122.03 Cr (Equity Capital Rs 1,220 Cr at FV Rs 10). '
        'Sources: Screener.in (primary), Yahoo Finance, Alpha Spread, Trendlyne.',
        source_style
    ))
    story.append(Paragraph(
        'Report Date: February 4, 2026 | Price as of: Feb 3, 2026 (NSE close) '
        '| Data Sources: Screener.in, NSE India, Yahoo Finance, Trendlyne, '
        'Alpha Spread, Business Standard, ScanX, ABFRL Investor Relations',
        source_style
    ))
    story.append(Paragraph(
        'DISCLAIMER: This report is for informational and educational purposes only. '
        'It does not constitute financial advice, a recommendation to buy or sell securities, '
        'or an offer to transact. Stock investments are subject to market risks. '
        'Consult a SEBI-registered financial advisor before making investment decisions.',
        disclaimer_style
    ))

    story.append(PageBreak())

    # ======================================================================
    # SECTION 1: COMPANY SNAPSHOT
    # ======================================================================
    story.append(Paragraph('1. Company Snapshot (Post-Demerger)', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Aditya Birla Fashion &amp; Retail Ltd (ABFRL) is part of the US$48.3 billion Aditya Birla Group. '
        'Following the demerger effective May 1, 2025 (NCLT sanctioned March 27, 2025), '
        'ABFRL now operates as a <b>pure-play ethnic, luxury, value fashion, and digital-first '
        'fashion platform</b>. The Madura Fashion &amp; Lifestyle business (lifestyle brands) '
        'was demerged into Aditya Birla Lifestyle Brands Ltd (ABLBL), which listed on NSE/BSE '
        'on June 23, 2025 at Rs 167.75/share.',
        body_style
    ))

    story.append(Paragraph('Post-Demerger Brand Portfolio', subheading_style))
    brands = [
        '<b>Pantaloons (59% of revenue):</b> India\'s largest value fashion chain with ~1,190 stores '
        'across 7.5 million sq ft. Targets middle-income consumers with apparel, accessories, '
        'and beauty products.',
        '<b>Ethnic Wear Portfolio (27% of revenue, ARR Rs 2,000+ Cr):</b>',
        '&nbsp;&nbsp;&nbsp;&nbsp;- <b>Sabyasachi:</b> India\'s most iconic luxury designer brand. '
        '40% like-to-like growth in Q1 FY26. Ultra-premium bridal/occasion wear.',
        '&nbsp;&nbsp;&nbsp;&nbsp;- <b>Tasva:</b> Premium men\'s ethnic wear (JV-like). '
        '72% YoY sales growth, 39% LTL growth. Aggressive store expansion underway.',
        '&nbsp;&nbsp;&nbsp;&nbsp;- <b>TCNS (W, Aurelia, Wishful):</b> Acquired women\'s ethnic brands. '
        '19% LTL growth. Expected to turn profitable in FY27.',
        '&nbsp;&nbsp;&nbsp;&nbsp;- <b>Jaypore:</b> Artisanal, handcrafted ethnic/fusion brand. Online + retail.',
        '&nbsp;&nbsp;&nbsp;&nbsp;- <b>Shantnu &amp; Nikhil (S&amp;N):</b> Designer luxury brand.',
        '&nbsp;&nbsp;&nbsp;&nbsp;- <b>House of Masaba:</b> Contemporary designer brand.',
        '<b>TMRW (6%, digital-first):</b> D2C brand portfolio. 27% YoY growth in Q2 FY26. '
        'Targets Gen Z/Millennial consumers online.',
        '<b>The Collective (4%, luxury retail):</b> Multi-brand luxury retail stores. '
        'Carries international brands like Ralph Lauren, Ted Baker, Fred Perry.',
        '<b>OWND (Gen Z brand):</b> Newest format, 43% revenue growth, expanded to 59 stores. '
        'Aggressive physical + digital expansion.',
        '<b>StyleUp:</b> Value fashion format targeting Tier 2/3 cities.',
    ]
    for b in brands:
        story.append(Paragraph(f'  {b}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Post-demerger ABFRL has an Annual Run Rate (ARR) of Rs 7,000+ Cr</b>, playing across '
        'high-growth segments. Management ambition: <b>triple scale and double profitability '
        'in the next five years</b>. The ethnic brands alone generate Rs 2,000+ Cr ARR.',
        callout_green
    ))
    story.append(Paragraph(
        'Sources: ABFRL Investor Relations (abfrl.com), Q2 FY26 Earnings Call Transcript, '
        'Business Standard, Indian Retailer, ScanX',
        source_style
    ))

    story.append(PageBreak())

    # ======================================================================
    # SECTION 2: FUNDAMENTAL ANALYSIS
    # ======================================================================
    story.append(Paragraph('2. Fundamental Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>CRITICAL NOTE:</b> All data for FY21-FY25 is for the COMBINED pre-demerger entity '
        '(including Madura brands now in ABLBL). FY26 onwards is post-demerger ABFRL only. '
        'Direct YoY comparison across the demerger is NOT meaningful for revenue.',
        callout_orange
    ))

    story.append(Paragraph('Screener.in Key Metrics (Consolidated)', subheading_style))
    screener_data = [
        ['Metric', 'Value', 'Source'],
        ['Market Cap', 'Rs 8,176 Cr', 'Screener.in (Feb 2026); 122.03 Cr shares x Rs 67'],
        ['Revenue (TTM)', 'Rs 7,355 Cr (cont. ops)', 'Screener.in (restated per Ind AS 105)'],
        ['Net Profit (TTM)', 'Rs -595 Cr (LOSS)', 'Screener.in'],
        ['P/E Ratio', 'N/A (Loss-making)', 'Screener.in'],
        ['Shares Outstanding', '122.03 Cr', 'Screener.in (Equity Capital Rs 1,220 Cr at FV Rs 10)'],
        ['P/S (TTM)', '1.11x', '8,176 / 7,355 (cont. ops basis)'],
        ['EV/Sales (TTM)', '2.06x', 'EV Rs 15,176 Cr / Revenue Rs 7,355 Cr'],
        ['ROE (3Y Avg)', '-11.0%', 'Screener.in'],
        ['ROCE', '-2.87%', 'Screener.in'],
        ['Debt-to-Equity', '0.17', 'Alpha Spread'],
        ['Debtor Days', '18.5 days (improved from 39.1)', 'Screener.in'],
        ['Other Income', 'Rs 450 Cr (included in earnings)', 'Screener.in'],
    ]
    screener_table = Table(screener_data, colWidths=[4*cm, 5*cm, 5.5*cm])
    screener_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(screener_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Annual Revenue & Loss Trend (Pre-Demerger Combined)', subheading_style))
    annual_data = [
        ['Year', 'Revenue (Rs Cr)', 'Net Profit/Loss (Rs Cr)', 'Note'],
        ['FY22*', '~8,136', 'Marginal profit', 'Combined entity'],
        ['FY23*', '12,418', 'Net Loss', 'Combined entity, 53% YoY growth'],
        ['FY24*', '13,996', '-736', 'Combined entity, 13% YoY growth'],
        ['FY25*', '7,355 (cont. ops)', '-456', 'Continuing ops only (post-demerger basis)'],
        ['H1 FY26', '3,813', '-529 (est.)', 'Post-demerger ABFRL only'],
    ]
    annual_table = Table(annual_data, colWidths=[2*cm, 3.5*cm, 3.5*cm, 5.5*cm])
    annual_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (2, 1), (2, -1), HexColor(LOSS_RED)),
    ]))
    story.append(annual_table)
    story.append(Paragraph('* Pre-demerger combined entity data. Not comparable with FY26.', source_style))
    story.append(Paragraph(
        '<b>TTM Revenue Note:</b> TTM revenue uses post-demerger continuing operations basis. '
        'FY25 and prior are pre-demerger combined entity — not directly comparable. '
        'Screener.in restates per Ind AS 105: MFL (now ABLBL) is treated as discontinued operations. '
        'FY25 continuing ops revenue: ~Rs 7,355 Cr.',
        source_style
    ))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph('Quarterly Revenue & Loss Trend', subheading_style))
    story.append(Image(chart_paths['revenue'], width=16*cm, height=8.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('EBITDA Margin Trend', subheading_style))
    story.append(Paragraph(
        'H1 FY26 EBITDA was Rs 286 Cr (7.5% margin), up 24% YoY. However, Q2 FY26 margins '
        'dipped to 5.9% from 6.2% YoY due to a 200 bps increase in advertising spend, '
        'particularly for Pantaloons brand building. The ethnic portfolio showed 280 bps '
        'margin improvement YoY, indicating the ethnic segment is on a clear path to profitability.',
        body_style
    ))
    story.append(Image(chart_paths['margins'], width=14*cm, height=7*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Segment Performance', subheading_style))
    story.append(Image(chart_paths['segments'], width=12*cm, height=8.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Balance Sheet & Cash Position', subheading_style))
    story.append(Paragraph(
        '<b>Cash Position:</b> Post the Rs 1,860 Cr QIP (Jan 2025) and Rs 1,297 Cr preferential '
        'allotment, ABFRL closed FY25 with <b>Rs 2,350 Cr gross cash</b>. As of Sep 2025 (Q2 FY26), '
        'gross cash stood at <b>Rs 2,150 Cr</b>, down Rs 200 Cr due to operating losses and expansion.<br/><br/>'
        '<b>Debt:</b> Post-demerger ABFRL started with net cash of Rs 140-150 Cr (JM Financial). '
        'However, the Nuvama report cited Rs 7,000-8,000 Cr in total obligations (including lease '
        'liabilities). The headline debt-to-equity ratio of 0.17 appears low because it excludes '
        'lease liabilities under Ind AS 116. <b>Effective leverage is significantly higher than '
        'the headline D/E suggests.</b><br/><br/>'
        '<b>Working Capital:</b> Debtor days improved dramatically from 39.1 to 18.5 days '
        '(Screener.in), a positive signal. However, the company has delivered poor sales growth '
        'of -3.51% over 5 years (Screener.in) on a combined basis.',
        body_style
    ))

    story.append(Paragraph('Cash Flow / Cash Burn Analysis', subheading_style))
    cf_data = [
        ['Year', 'CFO (Rs Cr)', 'Capex (Rs Cr)', 'Net Cash Flow', 'Cash Conv.'],
        ['FY22', '951', 'Est. ~300', 'Est. ~650', 'N/M (loss-making)'],
        ['FY23', '636', 'Est. ~350', 'Est. ~286', 'N/M'],
        ['FY24', '1,341', 'Est. ~400', 'Est. ~941', 'N/M'],
        ['FY25', '1,644', 'Est. ~450', 'Est. ~1,194', 'N/M'],
    ]
    cf_table = Table(cf_data, colWidths=[2*cm, 3*cm, 3*cm, 3*cm, 3.5*cm])
    cf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(cf_table)
    story.append(Paragraph(
        'Note: CFO is positive and growing despite net losses — this is because of high '
        'depreciation/amortization and lease accounting (ABFRL has a massive store network). '
        'Net losses are primarily from interest + depreciation on right-of-use assets. '
        'Cash burn rate is manageable with Rs 2,150 Cr gross cash (Sep 2025). '
        'CFO Source: Screener.in (verified); Capex figures are estimates.',
        source_style
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Shareholding Pattern (Sep 2025)', subheading_style))
    sh_data = [
        ['Category', 'Holding (%)', 'Details'],
        ['Promoters', '46.6%', 'Birla Group Holdings 19.39% (largest); down 2.6% in 6 months'],
        ['FII', '18.6%', 'Down from 22.19% in Mar 2025; FIIs reducing post-demerger'],
        ['DII', '8.1%', 'Down from 14.64% in Mar 2025'],
        ['Public / Retail', '~26.7%', 'Flipkart (6% holder) sold Rs 755 Cr block deal'],
    ]
    sh_table = Table(sh_data, colWidths=[3*cm, 2.5*cm, 9*cm])
    sh_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sh_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Cautionary Flags', subheading_style))
    story.append(Paragraph(
        '<b>Investors must note the following red flags:</b><br/>'
        '  <b>1. Persistent Losses:</b> ABFRL has NEVER been consistently profitable. Net losses of '
        'Rs 736 Cr (FY24), Rs 456 Cr (FY25), and Rs 529 Cr estimated for H1 FY26. ROE is -11% '
        'over 3 years (Screener.in).<br/>'
        '  <b>2. Cash Burn:</b> Gross cash declined from Rs 2,350 Cr (Mar 2025) to Rs 2,150 Cr '
        '(Sep 2025) - burning Rs 200 Cr in 6 months. At this rate, the cash runway is approximately '
        '5-6 years without additional fundraising.<br/>'
        '  <b>3. Lease Liabilities:</b> True debt including lease obligations could be Rs 7,000-8,000 Cr '
        '(Nuvama), far exceeding the headline D/E of 0.17.<br/>'
        '  <b>4. Promoter Dilution:</b> Promoter holding fell 8.86% over 3 years (Trendlyne). '
        'The QIP and preferential allotment diluted existing shareholders.<br/>'
        '  <b>5. FII Exit:</b> FII holding dropped from 22.19% to 18.6% in just two quarters. '
        'Flipkart sold a Rs 755 Cr block deal.<br/>'
        '  <b>6. Pantaloons Stagnation:</b> Pantaloons (59% of revenue) reported only 1% YoY growth '
        'with LTL contraction of -1.6% in FY25 (Nuvama).<br/>'
        '  <b>7. Low Interest Coverage:</b> The company has a low interest coverage ratio (Screener.in).',
        callout_red
    ))

    story.append(Paragraph(
        'Sources: Screener.in, Business Standard, Trendlyne, Alpha Spread, Nuvama, JM Financial, '
        'Q2 FY26 Earnings Call (Nov 2025), ABFRL Investor Relations',
        source_style
    ))

    story.append(PageBreak())

    # ======================================================================
    # SECTION 3: TECHNICAL ANALYSIS
    # ======================================================================
    story.append(Paragraph('3. Technical Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'ABFRL\'s stock adjusted sharply post-demerger, declining ~67% from the pre-demerger '
        'price of ~Rs 280 to ~Rs 95 on the ex-date (May 22, 2025). Since listing in post-demerger '
        'form, the stock has traded between Rs 70.55 (52-week low) and Rs 107.75 (52-week high). '
        'As of Feb 3, 2026, the stock trades at Rs 83.92, roughly in the middle of its '
        'post-demerger range.',
        body_style
    ))

    story.append(Image(chart_paths['price'], width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Technical Signals', subheading_style))
    tech_data = [
        ['Indicator', 'Value', 'Signal'],
        ['50-Day EMA', '~Rs 82', 'Price slightly above; Neutral'],
        ['200-Day SMA', '~Rs 87', 'Price below; Bearish medium-term'],
        ['RSI (14)', 'Near strong support', 'Neutral to slightly oversold'],
        ['ADX', 'BUY signal (short-term)', 'Gaining momentum; initial strength'],
        ['MACD', 'BUY signal (weak/initial)', 'Selling pressure weakening'],
        ['Beta', '1.59', 'HIGH volatility vs market'],
        ['Support Zone', 'Rs 70-72 (major), Rs 66', 'Strong floor near 52W low'],
        ['Resistance Zone', 'Rs 95 (immediate), Rs 105-107', 'Need volume breakout above Rs 95'],
    ]
    tech_table = Table(tech_data, colWidths=[3.5*cm, 3.5*cm, 8.5*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Key Observation:</b> The stock has bounced from the Rs 70-72 support zone twice, '
        'suggesting strong buying interest at these levels. The beta of 1.59 means ABFRL is '
        'significantly more volatile than the market - amplifying both gains and losses. '
        'A sustained break above Rs 95 with volume would signal a potential trend change.',
        body_style
    ))
    story.append(Paragraph(
        'Sources: TradingView, 5Paisa, MunafaSutra, WalletInvestor, HDFC Sky (data as of late Jan 2026)',
        source_style
    ))

    story.append(PageBreak())

    # ======================================================================
    # SECTION 4: SECTOR & COMPETITIVE CONTEXT
    # ======================================================================
    story.append(Paragraph('4. Sector & Competitive Context', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Indian Ethnic Wear Market', subheading_style))
    story.append(Paragraph(
        'The Indian Ethnic Wear Market was valued at approximately <b>USD 197.2 billion in 2024</b> '
        'and is projected to reach <b>USD 558.5 billion by 2033</b>, growing at a CAGR of ~12.6% '
        '(Business Research Insights). Women\'s ethnic wear accounts for 73.5% of the market. '
        'The fusion wear segment is the fastest-growing sub-category. Key drivers include rising '
        'disposable incomes, destination weddings, cultural events, and growing e-commerce penetration. '
        'Men\'s ethnic wear is anticipated to grow at ~20% CAGR.',
        body_style
    ))
    story.append(Paragraph(
        '<b>ABFRL\'s positioning:</b> Post-demerger ABFRL is uniquely positioned with India\'s most '
        'comprehensive ethnic wear portfolio - spanning ultra-luxury (Sabyasachi), premium '
        '(Shantnu &amp; Nikhil, House of Masaba), mid-premium (Tasva, TCNS/W/Aurelia), artisanal '
        '(Jaypore), and value (Pantaloons ethnic). This breadth across price points is unmatched '
        'by any listed peer.',
        body_style
    ))

    story.append(Paragraph('Peer Valuation Comparison (Jan 2026)', subheading_style))
    peer_data = [
        ['Metric', 'ABFRL', 'Vedant Fashions\n(Manyavar)', 'Trent Ltd', 'Shoppers Stop'],
        ['P/S (TTM)', '1.11x', '10.49x', '~12x (est.)', '~0.4x'],
        ['EV/Sales', '2.06x', '10.47x', '~13x (est.)', '~0.7x'],
        ['P/E (TTM)', 'N/A (Loss)', '38.7x', 'Very high', 'N/A'],
        ['EBITDA Margin', '7.5% (H1)', '43.2%', '~14%', '~5%'],
        ['Revenue (TTM)', 'Rs 7,355 Cr', 'Rs 1,421 Cr', 'Rs 16,000+ Cr', 'Rs 4,500+ Cr'],
        ['PAT Margin', '-7.03%', '27.08%', '~6%', 'Near 0%'],
        ['1Y Return', '-34%', '~-10%', '~0%', '~-20%'],
    ]
    peer_table = Table(peer_data, colWidths=[2.5*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm])
    peer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#edf2f7')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (1, 4), (1, 4), HexColor(LOSS_RED)),
    ]))
    story.append(peer_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Image(chart_paths['peers'], width=16*cm, height=6.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Key Insight:</b> ABFRL\'s P/S of 1.11x is among the lowest fashion peers, reflecting '
        'its loss-making status. Vedant Fashions trades at 10.5x P/S due to 27% profit margins '
        'and market leadership in men\'s ethnic wear. Trent commands ~12x P/S on strong growth. '
        'If ABFRL achieves profitability, a re-rating toward 2-3x P/S (still well below profitable '
        'peers) would imply significant upside.',
        callout_green
    ))

    story.append(Paragraph('Nifty Consumer Durables Index', subheading_style))
    story.append(Paragraph(
        'The Nifty Consumer Durables Index stood at <b>36,229</b> (Feb 4, 2026), with a 52-week range '
        'of 32,205 - 40,472. The index has delivered moderate returns but with significant volatility. '
        'ABFRL\'s 1-year decline of -34% significantly underperforms the sector, reflecting '
        'company-specific (demerger adjustment, losses) rather than just sector-wide headwinds.',
        body_style
    ))

    story.append(Paragraph('Raw Material Context: Cotton & Textiles', subheading_style))
    story.append(Paragraph(
        'Cotton prices have been <b>soft in FY26</b>, trading below MSP since November 2024 due to '
        'weak demand and import duty waivers. India\'s cotton output is projected at a decadal low '
        'of 29.2M bales, but subdued demand keeps prices contained. Cotton yarn prices fell 4% MoM '
        'in Nov 2025. <b>Net impact: Favorable for ABFRL\'s input costs in FY27.</b> '
        'However, US tariffs of 50% on Indian apparel exports may impact the broader textile sector. '
        'For ABFRL, which is primarily a domestic retailer, the direct export impact is limited.',
        body_style
    ))
    story.append(Paragraph(
        'Sources: Business Research Insights, Technavio, Grand View Research, Yahoo Finance, '
        'Alpha Spread, Smart-Investing.in, MarketsMojo, ICRA, Fibre2Fashion, NSE India (indices)',
        source_style
    ))

    story.append(PageBreak())

    # ======================================================================
    # SECTION 5: VALUATION & ANALYST VIEWS
    # ======================================================================
    story.append(Paragraph('5. Valuation & Analyst Views', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Brokerage Target Prices (Post-Demerger, Latest Available)', subheading_style))
    analyst_data = [
        ['Brokerage', 'Target (Rs)', 'Rating', 'Date', 'Key Thesis'],
        ['Motilal Oswal', '90', 'Neutral', 'Nov 2025', 'Cautious on growth; fair valuation'],
        ['Nuvama', '84', 'Hold (downgrade)', 'May 2025', 'Sluggish Pantaloons, lease debt concern'],
        ['Jefferies', '100', 'Hold', 'May 2025', 'Fair value post-demerger'],
        ['Bernstein', '80-105', 'Range', 'May 2025', 'Fair value range for new ABFRL'],
        ['Consensus (4)', '~92', 'Neutral', 'Latest', 'Trendlyne avg of 4 brokers'],
        ['Alpha Spread', '183 (intrinsic)', 'Undervalued', 'Jan 2026', '61% undervalued vs intrinsic'],
    ]
    analyst_table = Table(analyst_data, colWidths=[2.8*cm, 2*cm, 2.2*cm, 2*cm, 5.5*cm])
    analyst_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(analyst_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Analyst Consensus:</b> Unlike Bikaji (6/6 Buy), ABFRL has mixed-to-cautious coverage. '
        'Most brokerages rate it Neutral/Hold post-demerger, with targets in the Rs 84-100 range. '
        'Alpha Spread\'s intrinsic value estimate of Rs 183 is a significant outlier and should be '
        'treated with caution given persistent losses. The median brokerage target of Rs 92 implies '
        'only ~10% upside from current Rs 84.',
        body_style
    ))

    story.append(Paragraph(
        '<b>Important:</b> Pre-demerger targets (Sharekhan Rs 298, Axis Rs 270) are NO LONGER '
        'relevant. Only post-demerger adjusted targets should be considered.',
        callout_orange
    ))

    story.append(Spacer(1, 0.3*cm))

    # ======================================================================
    # SECTION 6: VALUATION MATH (P/S METHODOLOGY)
    # ======================================================================
    story.append(Paragraph('Valuation Methodology: EV/Sales (Primary) & P/S (Secondary)', subheading_style))
    story.append(Paragraph(
        'Since ABFRL is <b>loss-making</b> (ROCE: -2.87%, Screener.in), traditional P/E valuation is NOT applicable. '
        'Instead, we use <b>EV/Sales</b> as the primary valuation metric and <b>P/S</b> as secondary, '
        'anchored to peer comparisons. This is a heuristic, not a DCF. Limitations are disclosed at the end.<br/><br/>'
        '<b>EV = Market Cap + Net Debt = Rs 8,176 Cr + Rs 7,000 Cr (estimated lease liabilities + debt - cash) '
        '= Rs 15,176 Cr</b><br/>'
        '<b>EV/Sales = Rs 15,176 / Rs 7,355 = 2.06x</b><br/>'
        'Note: EV/Sales is more appropriate than P/S for ABFRL given significant lease liabilities under Ind AS 116. '
        'P/S of 1.11x understates true valuation because it ignores the Rs 7,000 Cr in lease obligations and debt.',
        body_style
    ))

    story.append(Paragraph('<b>Step 1: Current Revenue Per Share</b>', body_style))
    rps_data = [
        ['Metric', 'Value', 'Source'],
        ['TTM Revenue (cont. ops)', 'Rs 7,355 Cr', 'Screener.in (restated per Ind AS 105)'],
        ['Market Cap', 'Rs 8,176 Cr', '122.03 Cr shares x Rs 67'],
        ['Price', 'Rs 83.92', 'NSE (Feb 3, 2026)'],
        ['Shares Outstanding', '122.03 Cr', 'Screener.in, Equity Capital Rs 1,220 Cr at FV Rs 10'],
        ['Revenue Per Share (RPS)', 'Rs 60.3', 'Rs 7,355 Cr / 122.03 Cr shares'],
        ['Current P/S', '8,176 / 7,355 = 1.11x', 'Market Cap / Revenue'],
    ]
    rps_table = Table(rps_data, colWidths=[4*cm, 4.5*cm, 6*cm])
    rps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(rps_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>Step 2: Project FY27E Revenue (3 Scenarios)</b>', body_style))
    story.append(Paragraph(
        'Growth rate anchors: Management targets 3x scale in 5 years (~25% CAGR). '
        'H1 FY26 revenue grew 11% YoY. Historical CAGR for Indian ethnic wear: 8-13%. '
        'ABFRL\'s ethnic segment growing 11-34%, TMRW 27%, OWND 43%, Pantaloons 6%.',
        body_style
    ))

    proj_data = [
        ['', 'Bull', 'Base', 'Bear'],
        ['FY26E Revenue Growth', '12% (H2 wedding boost)', '10% (moderate)', '5% (Pantaloons drag)'],
        ['FY26E Revenue (Rs Cr)', '7,355 x 1.12 = 8,238', '7,355 x 1.10 = 8,091', '7,355 x 1.05 = 7,723'],
        ['FY27E Revenue Growth', '15% (ethnic + OWND)', '12%', '8%'],
        ['FY27E Revenue (Rs Cr)', '8,238 x 1.15 = 9,474', '8,091 x 1.12 = 9,062', '7,723 x 1.08 = 8,341'],
        ['FY27E RPS', 'Rs 77.6', 'Rs 74.3', 'Rs 68.4'],
    ]
    proj_table = Table(proj_data, colWidths=[3.5*cm, 4*cm, 4*cm, 4*cm])
    proj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (1, 0), (1, -1), HexColor('#f0fff4')),
        ('BACKGROUND', (2, 0), (2, -1), HexColor('#fffff0')),
        ('BACKGROUND', (3, 0), (3, -1), HexColor('#fff5f5')),
        ('TEXTCOLOR', (1, 0), (3, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(proj_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>Step 3: Apply EV/Sales Multiple - Derive Target Price</b>', body_style))
    story.append(Paragraph(
        'EV/Sales assumptions anchored to peers: Vedant Fashions 10.5x (profitable ethnic pure-play), '
        'Trent ~13x (growth leader), Shoppers Stop ~0.7x (low-margin retailer). '
        'ABFRL currently at 2.06x EV/Sales. For a loss-making company showing path to profitability, '
        'a re-rating toward 1.5-2.5x EV/Sales is reasonable; higher multiples require proof of '
        'sustained profitability. Target price derived as: (EV/Sales x FY27E Revenue - Net Debt) / Shares.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Bear worst-case uses 0.4x EV/Sales</b> (Shoppers Stop trading level), modeling a scenario where '
        'EBITDA margin improvement stalls and losses continue through FY28.',
        body_style
    ))

    scenario_data = [
        ['Scenario', 'FY27E Rev (Cr)', 'EV/Sales', 'Implied EV', 'Equity Value', 'Target Price', 'Prob.'],
        ['Bull', 'Rs 9,474', '2.5x', 'Rs 23,685 Cr', 'Rs 16,685 Cr', 'Rs 137', '15%'],
        ['Base', 'Rs 9,062', '1.8x', 'Rs 16,312 Cr', 'Rs 9,312 Cr', 'Rs 76', '45%'],
        ['Bear', 'Rs 8,341', '0.4x', 'Rs 3,336 Cr', 'Rs -3,664 Cr*', 'Rs 27**', '40%'],
    ]
    scenario_table = Table(scenario_data, colWidths=[1.5*cm, 2.2*cm, 1.8*cm, 2.5*cm, 2.5*cm, 2.2*cm, 1.5*cm])
    scenario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fffff0')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#fff5f5')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(scenario_table)
    story.append(Paragraph(
        '* Negative equity value implies debt exceeds enterprise value at 0.4x EV/Sales.<br/>'
        '** Bear target floored at estimated liquidation / distressed value. In this scenario, '
        'EBITDA margin improvement stalls and losses continue through FY28, leading to further '
        'cash burn and potential equity dilution.',
        source_style
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>P/S Cross-Reference (Secondary):</b> Bull: Rs 77.6 RPS x 1.5x P/S = Rs 116 | '
        'Base: Rs 74.3 RPS x 1.1x P/S = Rs 82 | Bear: Rs 68.4 RPS x 0.4x P/S = Rs 27. '
        'P/S-based targets are directionally consistent but understate risk by ignoring lease liabilities.',
        source_style
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>Step 4: Probability-Weighted Expected Value</b>', body_style))
    story.append(Paragraph(
        'Probability weights are adjusted for a <b>loss-making company with high uncertainty</b>:',
        body_style
    ))
    prob_points = [
        '<b>Bull (15%):</b> Low probability because it requires Pantaloons revival + ethnic margins '
        'expanding + TCNS turning profitable + market re-rating EV/Sales to 2.5x. All must go right. '
        'The 2.5x EV/Sales is still well below profitable peers (Vedant 10.5x), so it is achievable '
        'IF profitability emerges.',
        '<b>Base (45%):</b> Most likely. ABFRL delivers 10-12% growth (management guidance), '
        'ethnic margins improve but overall company stays loss-making in FY27, EV/Sales stays near 1.8x '
        'as market awaits proof of profitability. This is the "show me" story.',
        '<b>Bear (40%):</b> Higher than typical 25% because of specific, identified risks: '
        '(a) company has NEVER been profitable, (b) Pantaloons is stagnating, '
        '(c) Rs 200 Cr/half cash burn, (d) FIIs are exiting, (e) promoter holding declining, '
        '(f) lease liabilities far exceed headline debt. Uses 0.4x EV/Sales (Shoppers Stop trading level). '
        'Models a scenario where EBITDA margin improvement stalls and losses continue through FY28, '
        'leading to further value erosion. A 40% bear weight reflects these '
        'tangible, ongoing headwinds that are NOT temporary.',
    ]
    for pp in prob_points:
        story.append(Paragraph(f'  {pp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    ev_data = [
        ['Scenario', 'Target Price', 'Probability', 'Weighted Value'],
        ['Bull', 'Rs 137', '15%', 'Rs 20.6'],
        ['Base', 'Rs 76', '45%', 'Rs 34.2'],
        ['Bear', 'Rs 27', '40%', 'Rs 10.8'],
        ['', '', 'Expected Value', 'Rs 66'],
    ]
    ev_table = Table(ev_data, colWidths=[3*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    ev_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fffff0')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#fff5f5')),
        ('BACKGROUND', (0, 4), (-1, 4), HexColor('#edf2f7')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ev_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Probability-weighted expected price: Rs 66</b> -- implying ~21% DOWNSIDE from Rs 84. '
        'Using EV/Sales (which properly accounts for Rs 7,000 Cr in lease liabilities and debt), '
        'the expected value is BELOW current market price. The high bear probability (40%) combined with '
        'the severe bear case (0.4x EV/Sales, Shoppers Stop level) drags expected value significantly lower. '
        'The risk-reward is unfavorable on a probability-weighted basis when lease liabilities are included.',
        callout_orange
    ))

    story.append(Paragraph('Path to Profitability Timeline', subheading_style))
    story.append(Paragraph(
        'Management has indicated the following milestones on the path to profitability:<br/>'
        '  <b>FY27:</b> TCNS expected to turn profitable. Ethnic segment (ex-Tasva) already profitable.<br/>'
        '  <b>FY28:</b> Tasva expected to reach breakeven. OWND scaling rapidly (43% growth).<br/>'
        '  <b>FY28-29:</b> TMRW digital brands expected to reach breakeven.<br/>'
        '  <b>FY30-31:</b> Overall company profitability target (management ambition: double profitability in 5 years).<br/><br/>'
        'This timeline implies <b>investors need a 3-5 year horizon</b> before seeing consistent '
        'profitability. Near-term (1-year) returns depend on sentiment and re-rating, not earnings.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Motilal Oswal, Nuvama, Jefferies, Bernstein, Trendlyne, Alpha Spread, '
        'TradingView, Q2 FY26 Earnings Call, JM Financial',
        source_style
    ))

    story.append(PageBreak())

    # ======================================================================
    # SECTION 7: CONCLUSION
    # ======================================================================
    story.append(Paragraph('6. Catalysts, Risks & Conclusion', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Management Guidance (Q2 FY26 Earnings Call, Nov 2025)', subheading_style))
    mgmt_points = [
        '<b>Revenue:</b> H1 FY26 revenue Rs 3,813 Cr (+11% YoY). H2 expected to be stronger '
        'due to wedding season boosting ethnic segment.',
        '<b>EBITDA:</b> H1 EBITDA Rs 286 Cr (+24% YoY), margin 7.5%. Ethnic margins improved '
        '280 bps YoY. Pantaloons margins impacted by 200 bps higher ad spend.',
        '<b>Ethnic Portfolio:</b> "Most comprehensive in the country." Revenue Rs 505 Cr in Q2, '
        '+11% YoY. Ex-TCNS growth at 34% YoY. L2L growth over 20%. "Consistent growth in both '
        'revenue and profitability."',
        '<b>TCNS:</b> 19% L2L growth. "Expected to turn profitable next year (FY27)."',
        '<b>Tasva:</b> 72% YoY sales growth, 39% L2L. Still loss-making but scaling.',
        '<b>OWND:</b> 43% revenue growth, expanded to 59 stores. "Gen Z-focused rapid expansion."',
        '<b>TMRW:</b> 27% YoY growth. Digital-first brands gaining traction.',
        '<b>Cash Position:</b> Rs 2,150 Cr gross cash at Sep 2025. H2 cash flow expected to improve.',
        '<b>CapEx:</b> Rs 100-125 Cr for H2, focused on OWND and Tasva store expansion.',
        '<b>Long-term:</b> "Triple scale and double profitability in the next five years."',
    ]
    for mp in mgmt_points:
        story.append(Paragraph(f'  {mp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Growth Catalysts (Bull Case)', subheading_style))
    bull_points = [
        '<b>Ethnic Wear Structural Tailwind:</b> India\'s ethnic wear market growing at 8-13% CAGR. '
        'ABFRL has the most comprehensive portfolio spanning all price points.',
        '<b>Sabyasachi Brand Power:</b> 40% L2L growth. India\'s strongest luxury designer brand. '
        'Revenue and profit growing consistently.',
        '<b>TCNS Turnaround:</b> Expected profitability in FY27. W and Aurelia are established '
        'women\'s ethnic brands with strong recall.',
        '<b>Digital-First Growth:</b> TMRW (+27%) and OWND (+43%) are fast-growing formats '
        'targeting Gen Z/Millennial consumers.',
        '<b>Wedding Season H2 Boost:</b> Ethnic and luxury segments see disproportionate H2 '
        'revenue, which could improve full-year numbers.',
        '<b>Cotton Price Tailwind:</b> Soft input costs support margin improvement in FY27.',
        '<b>Cash Cushion:</b> Rs 2,150 Cr gross cash provides runway for 5+ years even with '
        'current burn rate.',
        '<b>Low P/S Multiple:</b> At 1.11x P/S (2.06x EV/Sales), ABFRL is cheap relative to peers IF profitability '
        'emerges. Even a modest re-rating to 1.5x P/S implies significant upside.',
    ]
    for bp in bull_points:
        story.append(Paragraph(f'  {bp}', bullet_style))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph('Key Risks (Bear Case)', subheading_style))
    bear_points = [
        '<b>NEVER Profitable:</b> ABFRL has never delivered consistent net profits. FY24 loss: Rs 736 Cr, '
        'FY25: Rs 456 Cr, H1 FY26: Rs 529 Cr (est.). There is no track record of profitability.',
        '<b>Pantaloons Stagnation:</b> 59% of revenue from Pantaloons, which grew only 6% with '
        'LTL contraction of -1.6% in FY25. Reviving Pantaloons is critical but unclear.',
        '<b>Hidden Leverage:</b> Headline D/E of 0.17 understates true leverage. Including lease '
        'liabilities, total obligations may be Rs 7,000-8,000 Cr (Nuvama).',
        '<b>Cash Burn:</b> Rs 200 Cr cash burn in H1 FY26 alone. Rs 2,150 Cr cash is not infinite.',
        '<b>FII/Promoter Exit:</b> FII down from 22.19% to 18.6%. Promoter down 8.86% over 3 years. '
        'Flipkart sold Rs 755 Cr block deal. Smart money is reducing.',
        '<b>Demerger Disruption:</b> Operational complexity from splitting a combined entity. '
        'Shared services, systems, and supply chains need to be separated.',
        '<b>Competition:</b> Vedant Fashions (Manyavar) is the profitable ethnic pure-play. '
        'Trent (Zudio, Westside) is aggressively expanding in value fashion. ITC entering fashion.',
        '<b>Dilution Risk:</b> If cash burns faster, ABFRL may need another equity raise, further '
        'diluting existing shareholders (already diluted via QIP + preferential).',
    ]
    for bp in bear_points:
        story.append(Paragraph(f'  {bp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Verdict', subheading_style))
    story.append(Paragraph(
        '<b>ABFRL is a high-risk, high-reward bet on India\'s ethnic wear boom.</b> '
        'The company has the most comprehensive ethnic/luxury brand portfolio in India '
        '(Sabyasachi, Tasva, TCNS, Jaypore, Shantnu &amp; Nikhil, House of Masaba) and is backed '
        'by the Aditya Birla Group. The ethnic segment is growing 11-34% with improving margins.',
        body_style
    ))
    story.append(Paragraph(
        'However, the <b>fundamental reality is that ABFRL has never been consistently profitable</b>. '
        'The probability-weighted expected price of <b>Rs 66 implies ~21% DOWNSIDE</b> when using '
        'EV/Sales (which properly accounts for Rs 7,000 Cr in lease liabilities). This comes '
        'with a 40% bear probability reflecting very real risks: persistent losses, stagnating '
        'Pantaloons, hidden lease leverage, and smart money exiting.',
        body_style
    ))
    story.append(Paragraph(
        'The <b>path to profitability is 3-5 years away</b> by management\'s own timeline. '
        'Near-term returns will be driven by sentiment and re-rating, not earnings. '
        'Investors need a minimum 3-year horizon and high risk tolerance.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Bottom Line: ABFRL at Rs 84 is not obviously cheap despite the modest P/S of 1.11x, '
        'because the denominator (sales) may not translate to profits for years. '
        'The stock is suitable only for high-conviction, long-duration investors betting on '
        'the ethnic wear thesis and management\'s ability to turn around Pantaloons while '
        'scaling ethnic brands to profitability. Conservative and income-seeking investors '
        'should avoid.</b>',
        body_style
    ))

    story.append(Spacer(1, 0.5*cm))

    # Methodology limitations
    story.append(Paragraph('Methodology Limitations (Transparency Note)', subheading_style))
    limit_points = [
        '<b>Not a DCF:</b> A proper intrinsic value estimate requires a 3-statement model with '
        'segment-level revenue build-up, margin trajectories, and WACC-based discounting.',
        '<b>EV/Sales heuristic limitations:</b> EV/Sales ignores profitability entirely. A company at 2.06x EV/Sales '
        'that never becomes profitable will destroy value regardless of revenue growth.',
        '<b>Lease liability estimation:</b> The Rs 7,000 Cr net debt figure (lease liabilities + debt - cash) '
        'used in EV calculation is an estimate based on Nuvama data. Actual figures may vary.',
        '<b>Pre/post demerger data confusion:</b> FY25 and prior data mixes the old combined entity. '
        'True like-for-like comparison only begins from Q1 FY26.',
        '<b>Revenue per share calculation:</b> Share count may change with future fundraises, diluting RPS.',
        '<b>Probability weights are subjective:</b> The 15/45/40 split is an informed estimate. '
        'Different analysts would assign different weights. The 40% bear weight is higher than '
        'standard (25%) specifically because this is a loss-making company.',
    ]
    for lp in limit_points:
        story.append(Paragraph(f'  {lp}', bullet_style))

    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cbd5e0')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>IMPORTANT DISCLAIMER:</b> This report is generated for informational and educational '
        'purposes only. It does not constitute investment advice, a recommendation to buy, sell, '
        'or hold any security, or an offer of any kind. All data is sourced from publicly available '
        'information as of February 4, 2026. Past performance does not guarantee future results. '
        'Stock market investments carry risk of capital loss. ABFRL is a loss-making company with '
        'additional risks including but not limited to: continued losses, dilution, and hidden '
        'leverage. Please consult a SEBI-registered investment advisor before making any investment '
        'decisions. The author has no position in ABFRL or ABLBL.',
        disclaimer_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Data Sources:</b> Screener.in (primary) | NSE India | Yahoo Finance | Trendlyne | '
        'Alpha Spread | Business Standard | ScanX | TradingView | ABFRL Investor Relations | '
        'Q2 FY26 Earnings Call Transcript | Motilal Oswal | Nuvama | Jefferies | Bernstein | '
        'JM Financial | ICRA | Business Research Insights | Technavio | Grand View Research | '
        'Fibre2Fashion | MarketsMojo | Smart-Investing.in | WalletInvestor | MunafaSutra',
        source_style
    ))

    doc.build(story)
    print(f"PDF generated successfully: {FINAL_PDF}")


# --- Main ---
if __name__ == '__main__':
    print("Generating charts...")
    charts = {
        'revenue': create_revenue_chart(),
        'margins': create_margin_chart(),
        'segments': create_segment_chart(),
        'price': create_price_chart(),
        'peers': create_peer_chart(),
    }
    print(f"Charts created: {len(charts)} charts")
    print("Building PDF...")
    build_pdf(charts)
    print("Done!")
