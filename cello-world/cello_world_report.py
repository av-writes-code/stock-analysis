#!/usr/bin/env python3
"""
Cello World Limited — 1-Year Stock Research Report
Generated: February 4, 2026
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

# Register SFNS (San Francisco) for rupee symbol support
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

# --- Configuration ---
OUTPUT_DIR = "/Users/arpitvyas/Desktop/stock-analysis/cello-world"
FINAL_PDF = "/Users/arpitvyas/Desktop/stock-analysis/cello-world/Cello_World_Research_Report_Feb2026.pdf"

# Colors
PRIMARY = '#1a365d'      # Dark navy
ACCENT = '#2b6cb0'       # Blue
HIGHLIGHT = '#e53e3e'    # Red for risks
GREEN = '#38a169'        # Green for positive
LIGHT_BG = '#f7fafc'     # Light background
ORANGE = '#dd6b20'
PURPLE = '#805ad5'

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


# === Chart 1: Quarterly Revenue & PAT Trend ===
def create_revenue_chart():
    """Q1 FY25 through Q2 FY26 (latest available). Q3 FY26 not yet reported."""
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26']
    # Revenue in Cr (consolidated, sourced from Business Standard / Screener.in / Trendlyne)
    revenue = [500.66, 490.06, 556.86, 588.82, 529.01, 587.44]
    # PAT in Cr
    pat = [82.58, 81.64, 86.61, 88.19, 73.02, 91.00]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    x = np.arange(len(quarters))
    width = 0.35

    bars1 = ax1.bar(x - width/2, revenue, width, label='Revenue (\u20b9 Cr)', color=ACCENT, alpha=0.85)
    ax1.set_ylabel('Revenue (\u20b9 Cr)', color=ACCENT)
    ax1.set_ylim(0, 750)
    ax1.tick_params(axis='y', labelcolor=ACCENT)

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, pat, width, label='Net Profit (\u20b9 Cr)', color=GREEN, alpha=0.85)
    ax2.set_ylabel('Net Profit (\u20b9 Cr)', color=GREEN)
    ax2.set_ylim(0, 130)
    ax2.tick_params(axis='y', labelcolor=GREEN)

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=8)
    ax1.set_title('Cello World \u2014 Quarterly Revenue & Net Profit Trend (Consolidated)', fontweight='bold', pad=15)

    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 8,
                f'\u20b9{int(bar.get_height())}', ha='center', va='bottom', fontsize=7, color=ACCENT)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1.5,
                f'\u20b9{bar.get_height():.0f}', ha='center', va='bottom', fontsize=7, color=GREEN)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_revenue.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# === Chart 2: Margin Trend Lines (OPM contraction story) ===
def create_margin_chart():
    """Operating margin contraction is the key story. Source: Screener.in / ICICI Direct / MarketsMojo."""
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26']
    # EBITDA margin (%) - consolidated
    ebitda_margin = [26.0, 26.9, 25.5, 26.0, 22.2, 24.0]
    # OPM excl other income (%)
    opm_excl = [24.5, 24.2, 23.8, 24.0, 20.4, 21.7]
    # PAT margin (%)
    pat_margin = [16.5, 16.7, 15.6, 15.0, 13.8, 14.6]

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(quarters))

    ax.plot(x, ebitda_margin, 's-', color=ACCENT, linewidth=2, markersize=6, label='EBITDA Margin (%)')
    ax.plot(x, opm_excl, 'D-', color=ORANGE, linewidth=2, markersize=5, label='OPM excl. Other Income (%)')
    ax.plot(x, pat_margin, 'o-', color=GREEN, linewidth=2, markersize=6, label='PAT Margin (%)')

    ax.fill_between(x, pat_margin, alpha=0.1, color=GREEN)

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=8)
    ax.set_ylabel('Margin (%)')
    ax.set_title('Margin Trend \u2014 427 bps EBITDA Contraction (Q2 FY25 to Q1 FY26)', fontweight='bold', pad=10)
    ax.legend(fontsize=8)
    ax.set_ylim(10, 32)

    for i, em in enumerate(ebitda_margin):
        ax.annotate(f'{em}%', (i, em), textcoords="offset points", xytext=(0, 8), fontsize=7, ha='center', color=ACCENT)

    # Annotate the contraction
    ax.annotate('427 bps\ncontraction', xy=(4, 22.2), xytext=(3.5, 14),
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT, lw=1.5),
                fontsize=9, fontweight='bold', color=HIGHLIGHT)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_margins.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# === Chart 3: Segment Revenue Pie Chart ===
def create_segment_chart():
    """Q2 FY26 segment breakdown. Source: Earnings call, Trendlyne."""
    labels = ['Consumerware\n(Houseware+Glass)\n(72%)', 'Writing\nInstruments\n(14%)',
              'Moulded\nFurniture\n(14%)']
    sizes = [72, 14, 14]
    colors_pie = [ACCENT, GREEN, ORANGE]
    explode = (0.05, 0, 0)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors_pie, autopct='%1.0f%%',
                                       shadow=False, startangle=90,
                                       textprops={'fontsize': 8})
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')

    ax.set_title('Q2 FY26 Revenue Mix by Segment (Consolidated)', fontweight='bold', pad=15)

    # Add sub-categories text
    fig.text(0.5, 0.02,
             'Consumerware includes: Houseware (plastics), Opalware, Glassware, Steelware, Hydration products',
             ha='center', fontsize=7, style='italic', color='#666666')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_segments.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# === Chart 4: Price Action with Moving Averages ===
def create_price_chart():
    """Monthly closing prices approximated from known data points.
    Sources: Yahoo Finance, Investing.com, NSE India."""
    months = ['Feb\n2025', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026']
    # Approximate monthly close prices
    prices = [590, 620, 650, 680, 700, 660, 620, 570, 550, 565, 540, 505]

    # Moving averages (approximate)
    sma_200 = [640, 640, 638, 635, 632, 628, 622, 615, 605, 595, 580, 561]
    ema_50 = [610, 615, 630, 650, 665, 660, 645, 620, 595, 575, 555, 543]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(months))

    ax.plot(x, prices, 'o-', color=PRIMARY, linewidth=2, markersize=5, label='Price (\u20b9)', zorder=3)
    ax.plot(x, sma_200, '--', color=GREEN, linewidth=1.5, label='200-Day SMA (~\u20b9561)', alpha=0.8)
    ax.plot(x, ema_50, '--', color=HIGHLIGHT, linewidth=1.5, label='50-Day EMA (~\u20b9543)', alpha=0.8)

    # Support and resistance zones
    ax.axhspan(490, 510, alpha=0.1, color='green', label='Support Zone (\u20b9490\u2013510)')
    ax.axhspan(690, 710, alpha=0.1, color='red', label='Resistance Zone (\u20b9690\u2013710)')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8)
    ax.set_ylabel('Price (\u20b9)')
    ax.set_title('Cello World \u2014 1-Year Price Action & Key Moving Averages', fontweight='bold', pad=15)
    ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
            transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(430, 770)

    # Annotate current price
    ax.annotate(f'Current: ~\u20b9505', xy=(11, 505), xytext=(9, 460),
                arrowprops=dict(arrowstyle='->', color=PRIMARY),
                fontsize=9, fontweight='bold', color=PRIMARY)

    # Annotate 52-week high
    ax.annotate(f'52W High: \u20b9706', xy=(4, 700), xytext=(5.5, 740),
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT),
                fontsize=8, color=HIGHLIGHT)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# === Chart 5: Peer Comparison Bars ===
def create_peer_chart():
    """Listed peer comparison. Source: Screener.in, Smart-Investing.in, Kotak Securities, Motilal Oswal."""
    companies = ['Cello\nWorld', 'Borosil\nLtd', 'Flair\nWriting', 'Linc\nLtd', 'La Opala\nRG']

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

    # P/E Ratio
    pe = [33.6, 34.2, 27.3, 18.5, 22.7]
    bar_colors = [ACCENT, '#a0aec0', '#a0aec0', '#a0aec0', '#a0aec0']
    bars = axes[0].bar(companies, pe, color=bar_colors, width=0.5)
    axes[0].set_title('P/E Ratio (TTM)', fontweight='bold', fontsize=9)
    axes[0].set_ylim(0, 45)
    for bar, val in zip(bars, pe):
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    f'{val:.1f}x', ha='center', fontsize=7)

    # P/B Ratio
    pb = [4.86, 3.48, 3.26, 2.77, 2.78]
    bars = axes[1].bar(companies, pb, color=bar_colors, width=0.5)
    axes[1].set_title('P/B Ratio', fontweight='bold', fontsize=9)
    axes[1].set_ylim(0, 7)
    for bar, val in zip(bars, pb):
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{val:.2f}x', ha='center', fontsize=7)

    # 1Y Return (%)
    returns_1y = [-22.0, -15.0, -20.0, -34.4, -10.0]
    ret_colors = [HIGHLIGHT if r < 0 else GREEN for r in returns_1y]
    bars = axes[2].bar(companies, returns_1y, color=ret_colors, width=0.5)
    axes[2].set_title('1-Year Return (%)', fontweight='bold', fontsize=9)
    axes[2].set_ylim(-45, 10)
    axes[2].axhline(y=0, color='black', linewidth=0.5)
    for bar, val in zip(bars, returns_1y):
        axes[2].text(bar.get_x() + bar.get_width()/2.,
                    bar.get_height() - 2.5 if val < 0 else bar.get_height() + 0.5,
                    f'{val:.0f}%', ha='center', fontsize=7)

    fig.suptitle('Cello World vs Listed Peers \u2014 Valuation & Returns Comparison', fontweight='bold', fontsize=11, y=1.02)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_peers.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# === PDF Generation ===
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
        fontSize=20, textColor=HexColor(PRIMARY),
        spaceAfter=6, alignment=TA_CENTER,
        fontName='SFNS'
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle', parent=styles['Normal'],
        fontSize=11, textColor=HexColor('#4a5568'),
        spaceAfter=12, alignment=TA_CENTER,
        fontName='SFNS'
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading1'],
        fontSize=14, textColor=HexColor(PRIMARY),
        spaceBefore=16, spaceAfter=8,
        fontName='SFNS',
        borderWidth=0, borderPadding=0,
    )
    subheading_style = ParagraphStyle(
        'CustomSubheading', parent=styles['Heading2'],
        fontSize=11, textColor=HexColor(ACCENT),
        spaceBefore=10, spaceAfter=4,
        fontName='SFNS'
    )
    body_style = ParagraphStyle(
        'CustomBody', parent=styles['Normal'],
        fontSize=9, leading=13,
        textColor=HexColor('#2d3748'),
        spaceAfter=6, alignment=TA_JUSTIFY,
        fontName='SFNS'
    )
    bullet_style = ParagraphStyle(
        'CustomBullet', parent=body_style,
        leftIndent=15, bulletIndent=5,
        spaceAfter=3, fontSize=9
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

    story = []

    # ============================================================
    # TITLE PAGE
    # ============================================================
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('CELLO WORLD LIMITED', title_style))
    story.append(Paragraph('NSE: CELLO | BSE: 544012', subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=HexColor(PRIMARY)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('1-Year Stock Research Report', ParagraphStyle(
        'BigSub', parent=subtitle_style, fontSize=16, textColor=HexColor(ACCENT),
        fontName='SFNS'
    )))
    story.append(Paragraph('Outlook: February 2026 \u2192 February 2027', subtitle_style))
    story.append(Spacer(1, 1*cm))

    # Key metrics box
    metrics_data = [
        ['Current Price', '\u20b9505 (Jan 16, 2026)', 'Market Cap', '\u20b911,066 Cr'],
        ['P/E (Trailing)', '33.6x (Consolidated)', 'P/B Ratio', '4.86x'],
        ['52-Week Range', '\u20b9490 \u2013 \u20b9706', 'Book Value', '\u20b9104/share'],
        ['Revenue (FY25)', '\u20b92,136 Cr (Consol.)', 'ROCE / ROE', '23.7% / 20.4%'],
        ['Debt', 'Nearly Debt-Free', 'Promoter Holding', '75.0%'],
    ]
    metrics_table = Table(metrics_data, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#edf2f7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor(PRIMARY)),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.5*cm))

    # Executive Summary Verdict Box
    verdict_data = [
        ['VERDICT: ACCUMULATE | Expected Value: Rs ~570 (approx 13% upside)', '', ''],
        ['Key Bull: Nearly debt-free, ROCE 23.7%, capacity expansion in glass', '', ''],
        ['Key Bear: High working capital (245 days CCC), premium valuation at 33.6x P/E', '', ''],
    ]
    verdict_table = Table(verdict_data, colWidths=[14.5*cm/3, 14.5*cm/3, 14.5*cm/3])
    verdict_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 1), (-1, 1)),
        ('SPAN', (0, 2), (-1, 2)),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d4edda')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fff5f5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#155724')),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor('#155724')),
        ('TEXTCOLOR', (0, 2), (-1, 2), HexColor('#721c24')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (0, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#38a169')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        '* P/E varies by source: Screener.in reports 33.6x (consolidated TTM), '
        'Motilal Oswal references 36.1x, GuruFocus 37.4x. Differences due to standalone vs '
        'consolidated earnings and trailing period used. This report uses consolidated P/E from Screener.in as primary. '
        'ROCE: 23.7%, ROE: 20.4% (Screener.in).',
        source_style
    ))
    story.append(Paragraph(
        'Report Date: February 4, 2026 | Price as of: Jan 16, 2026 (most recent confirmed NSE close in search data) '
        '| Data Sources: Screener.in (primary), NSE India, Yahoo Finance, Business Standard, '
        'Trendlyne, Investing.com, MarketScreener, GuruFocus, Smart-Investing.in',
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

    # ============================================================
    # SECTION 1: COMPANY SNAPSHOT
    # ============================================================
    story.append(Paragraph('1. Company Snapshot', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Cello World Limited is a <b>leading Indian consumer products company</b> '
        'with a diversified portfolio spanning <b>consumer houseware (plastics, opalware, glassware, '
        'steelware, hydration)</b>, <b>writing instruments & stationery</b>, and <b>moulded furniture</b>. '
        'Founded in 1967 by Ghisulal Rathod as a plastics manufacturer in Mumbai, the company '
        'has grown into a multi-category consumer brand. Cello World listed on NSE/BSE via IPO '
        'in November 2023 at a price band of \u20b9617\u2013648 per share.',
        body_style
    ))

    story.append(Paragraph('Key Business Facts', subheading_style))
    bullets = [
        '<b>Product Portfolio:</b> Houseware (plastics, opalware, glassware, steelware, hydration), '
        'writing instruments (Unomax brand + recently reacquired Cello brand), moulded furniture & allied products',
        '<b>Manufacturing:</b> 14 manufacturing facilities; 77% of FY25 revenues from in-house manufacturing. '
        'New 20,000 MT glassware plant in Falna, Rajasthan (European technology, German furnaces, Italian press-and-blow)',
        '<b>Distribution:</b> Pan-India distribution network across general trade, modern trade, and e-commerce channels',
        '<b>Cello Brand Reacquisition:</b> Promoter entity CPIW acquired the "Cello" trademark for stationery/writing '
        'instruments from BIC Group. Leased to Cello World at zero royalty. Expected \u20b9200 Cr revenue in CY2026. '
        'Cello historically commanded 25% market share in writing instruments',
        '<b>Promoter Holding:</b> 75.0% (as of Sep 2025) \u2014 Pradeep Rathod (CMD)',
        '<b>Nearly Debt-Free:</b> Borrowings declined from Rs 371 Cr (FY24) to Rs 5 Cr (FY25) \u2014 effectively debt-free. '
        'Interest costs negligible at \u20b90.48 Cr in Q2 FY26. Solvency score: 99/100. Source: Screener.in',
    ]
    for b in bullets:
        story.append(Paragraph(f'\u2022 {b}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: Screener.in (screener.in/company/CELLO/consolidated/), Cello World Corporate Website '
        '(corporate.celloworld.com), Business Standard, Wikipedia, Q2 FY26 Earnings Call (Nov 12, 2025)',
        source_style
    ))

    story.append(PageBreak())

    # ============================================================
    # SECTION 2: FUNDAMENTAL ANALYSIS
    # ============================================================
    story.append(Paragraph('2. Fundamental Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Compounded Growth (Screener.in \u2014 Consolidated)', subheading_style))
    growth_data = [
        ['Metric', '3Y', '5Y', '10Y', 'TTM'],
        ['Sales Growth', '16%', '~18%', '\u2014', '7%'],
        ['Profit Growth', '18%', '~22%', '\u2014', '2%'],
        ['Stock Price CAGR', '\u2014', '\u2014', '\u2014', '-22% (1Y)'],
        ['ROE (3Y Avg)', '35.7%', '\u2014', '\u2014', '\u2014'],
    ]
    growth_table = Table(growth_data, colWidths=[3.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    growth_table.setStyle(TableStyle([
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
    story.append(growth_table)
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        '<b>Key Insight:</b> While the 3Y ROE of 35.7% is impressive and historical growth has been strong, '
        '<b>TTM profit growth has decelerated to just 3%</b> (FY25 PAT: \u20b9365 Cr vs FY24 PAT: \u20b9356 Cr). '
        'Revenue growth slowed to 7% in FY25 from ~11% in FY24. The stock has corrected ~22% over the past year, '
        'significantly underperforming the Nifty Consumer Durables index (-1.6% 1Y return). '
        'The market is repricing the stock for margin compression and slower growth.',
        callout_red
    ))

    story.append(Paragraph('Revenue & Profit Trend', subheading_style))
    story.append(Paragraph(
        'FY25 consolidated revenue stood at \u20b92,136 Cr (+6.8% YoY) with PAT of \u20b9365 Cr (+2.5% YoY). '
        'Q2 FY26 showed improvement with revenue of \u20b9587 Cr (+20% YoY), but PAT grew only to \u20b991 Cr '
        'due to margin headwinds from the new glass plant and steel category pressures. '
        'H1 FY26 revenue reached \u20b91,116 Cr (+13% YoY), with EBITDA of \u20b9268 Cr (margin 24%) '
        'and PAT of \u20b9159 Cr (margin 14%). Q3 FY26 results (Dec 2025) are not yet published as of report date.',
        body_style
    ))
    story.append(Image(chart_paths['revenue'], width=16*cm, height=8*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Operating Margin Contraction \u2014 The Key Concern', subheading_style))
    story.append(Paragraph(
        'EBITDA margin contracted from 26.9% in Q2 FY25 to 22.2% in Q1 FY26 \u2014 a <b>427 bps contraction</b>. '
        'While Q2 FY26 saw partial recovery to 24.0%, margins remain below historical levels. '
        'OPM excluding other income fell to 21.7% from 24.2%. Key drivers of margin pressure: '
        '(1) Falna glassware plant in gestation phase (55-60% utilization, targeting 80% by Q4 FY26), '
        '(2) steel category supply constraints, (3) higher depreciation (\u20b919.5 Cr vs \u20b914.8 Cr). '
        'Management guides EBITDA margins of 22-23% going forward, implicitly acknowledging the '
        'previous 26%+ margins may not return soon.',
        body_style
    ))
    story.append(Image(chart_paths['margins'], width=14*cm, height=8*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Segment Performance (Q2 FY26)', subheading_style))
    story.append(Paragraph(
        '<b>Consumerware</b> (houseware, opalware, glassware, steelware) remains the dominant segment at ~72% of '
        'revenue, growing 23% YoY to \u20b9422 Cr in Q2 FY26. Standout sub-categories include hydration, opalware, '
        'and glassware. <b>Writing Instruments</b> contributed ~14% (\u20b981 Cr, +16% YoY), boosted by Unomax '
        'brand momentum and the upcoming Cello brand relaunch. <b>Moulded Furniture</b> contributed ~14% (\u20b984 Cr, '
        '+8% YoY) but shows limited growth potential with contracting margins.',
        body_style
    ))
    story.append(Image(chart_paths['segments'], width=12*cm, height=9*cm))

    story.append(Paragraph('Cash Flow Analysis \u2014 Standalone vs Consolidated Discrepancy', subheading_style))
    story.append(Paragraph(
        '<b>This is a critical area requiring investor attention.</b> Consolidated CFO FY25 was Rs 262 Cr '
        '(record high). However, standalone CFO was Rs -46.70 Cr (negative), a sharp reversal from Rs 65 Cr '
        'in FY24. This divergence between standalone and consolidated warrants investigation \u2014 '
        'subsidiary-level cash flow may be masking parent company working capital stress. '
        'The evidence supporting this concern:',
        body_style
    ))
    cfo_points = [
        '<b>Working capital days ballooned from 127 to 184 days</b> (Screener.in) \u2014 a 57-day increase. '
        'This means the standalone entity locked up significantly more capital in inventory/receivables.',
        '<b>Standalone revenue is \u20b91,138 Cr (FY25) vs consolidated \u20b92,136 Cr</b> \u2014 the standalone entity '
        'represents only ~53% of consolidated revenue. Subsidiaries contribute nearly half.',
        '<b>The glass plant (Falna) is likely housed in a subsidiary</b>, meaning the heavy capex and working capital '
        'buildup for glassware raw materials hits the subsidiary, while the subsidiary\'s positive CFO '
        'lifts the consolidated figure.',
        '<b>Inter-company transactions:</b> The parent may be funding subsidiary operations through loans or '
        'advances, which would depress standalone CFO without appearing in consolidated figures (eliminated on consolidation).',
        '<b>Consolidated CFO (FY23: \u20b9227 Cr, FY24: \u20b9231 Cr)</b> has been stable. '
        'A swing to \u20b9262 Cr in FY25 suggests subsidiaries are generating healthy cash flows even as the '
        'standalone entity\'s working capital deteriorated.',
    ]
    for cp in cfo_points:
        story.append(Paragraph(f'\u2022 {cp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Free Cash Flow (FCF) Analysis \u2014 Consolidated', subheading_style))
    cf_data = [
        ['Year', 'CFO (Rs Cr)', 'Capex est (Rs Cr)', 'FCF est (Rs Cr)', 'Cash Conv.'],
        ['FY22', '187', '~262', '-75', 'Low'],
        ['FY23', '227', '~557', '-330', 'Low'],
        ['FY24', '231', '~256', '-25', 'Low'],
        ['FY25', '262', '~553', '-291', 'Low'],
    ]
    cf_table = Table(cf_data, colWidths=[2*cm, 2.8*cm, 2.8*cm, 2.8*cm, 4*cm])
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
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>FCF has been consistently negative</b> due to heavy capex period (glass plant). '
        'CFO growing but FCF negative due to expansion. '
        'Note: Heavy capex period (glass plant). Source: Screener.in (consolidated).',
        callout_red
    ))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>Bottom Line on CFO:</b> Investors should monitor the standalone-to-consolidated CFO gap. '
        'If the standalone entity continues burning cash while subsidiaries generate it, it may indicate '
        'that the parent is becoming a holding company that funds subsidiary growth. This is not necessarily '
        'bad (the glass plant is a strategic investment), but it does mean standalone cash flow metrics '
        'overstate the problem while consolidated metrics may understate parent-level stress.',
        callout_red
    ))

    story.append(Paragraph('Working Capital Days Decomposition', subheading_style))
    wc_data = [
        ['Metric', 'Mar 2025', 'Trend'],
        ['Debtor Days', '112', 'Rising (concern)'],
        ['Inventory Days', '186', 'Elevated'],
        ['Days Payable', '53', 'Low'],
        ['Cash Conversion Cycle', '~245 days', 'Elevated for consumer products (112+186-53)'],
        ['Working Capital Days', '184', 'Up from 127 (significant deterioration)'],
    ]
    wc_table = Table(wc_data, colWidths=[4*cm, 3*cm, 8.5*cm])
    wc_table.setStyle(TableStyle([
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
    story.append(wc_table)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>Working capital efficiency has deteriorated significantly</b> \u2014 WC days increased from 127 to 184 days. '
        'Cash Conversion Cycle is ~245 days (Debtor Days 112 + Inventory Days 186 - Days Payable 53), '
        'which is elevated for consumer products. Rising debtor days (112) suggest potential channel stuffing or collection issues. '
        'Source: Screener.in (consolidated).',
        callout_red
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Shareholding Pattern (Sep 2025)', subheading_style))
    sh_data = [
        ['Category', 'Holding (%)', 'Details'],
        ['Promoters', '75.0%', 'Pradeep Rathod (CMD) & family; stable'],
        ['DII (Domestic Institutional)', '13.37%', 'Mutual funds & insurance companies'],
        ['FII (Foreign Institutional)', '5.41%', 'Moderate FII interest'],
        ['Public / Retail', '6.22%', 'Low free float'],
    ]
    sh_table = Table(sh_data, colWidths=[4*cm, 2.5*cm, 9*cm])
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

    story.append(Paragraph(
        '<b>Key Note:</b> Promoter holding at 75% is at the SEBI maximum threshold for listed companies. '
        'The recent ESOP-2025 scheme (6.6M shares approved for listing, Jan 2026) will marginally dilute '
        'promoter holding. High promoter stake indicates strong conviction but also limits free float '
        'and can reduce liquidity.',
        body_style
    ))

    story.append(Paragraph('Cautionary Flags', subheading_style))
    story.append(Paragraph(
        '<b>Investors should note the following concerns:</b><br/>'
        '\u2022 <b>Margin contraction:</b> EBITDA margin fell 427 bps (26.9% to 22.2%) in 2 quarters. '
        'Management now guides 22-23%, down from historical 26%+.<br/>'
        '\u2022 <b>Working capital deterioration:</b> 127 to 184 days \u2014 a 45% increase in working capital cycle.<br/>'
        '\u2022 <b>Standalone CFO reportedly negative:</b> While consolidated CFO is healthy, the parent entity\'s '
        'cash generation has deteriorated (see analysis above).<br/>'
        '\u2022 <b>Glass plant drag:</b> Falna plant at 55-60% utilization is diluting group margins. '
        'Management targets 80% by Q4 FY26, but glassware is a competitive, low-margin category.<br/>'
        '\u2022 <b>Furniture segment stagnation:</b> Moulded furniture shows limited growth potential with contracting margins.<br/>'
        '\u2022 <b>Stock down 22% in 1 year:</b> Market is clearly re-pricing for lower growth/margins.',
        callout_red
    ))

    story.append(Paragraph(
        'Sources: Screener.in (primary), Business Standard, Trendlyne, MarketsMojo, Q2 FY26 Earnings Call (Nov 12, 2025), '
        'Equitymaster Annual Report Analysis',
        source_style
    ))

    story.append(PageBreak())

    # ============================================================
    # SECTION 3: TECHNICAL ANALYSIS
    # ============================================================
    story.append(Paragraph('3. Technical Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Cello World\'s stock has been in a pronounced downtrend over the past 12 months, '
        'falling from ~\u20b9700 to ~\u20b9505 \u2014 a decline of approximately 28%. The 52-week range is '
        '\u20b9490 (low, near current levels) to \u20b9706 (high). The stock is trading near its 52-week '
        'low, which could indicate either a value entry point or a continued downtrend. '
        'Technical indicators present a mixed picture.',
        body_style
    ))

    story.append(Image(chart_paths['price'], width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Technical Signals', subheading_style))

    tech_data = [
        ['Indicator', 'Value', 'Signal'],
        ['50-Day EMA', '\u20b9543', 'Price below \u2192 Bearish (short-term)'],
        ['200-Day SMA', '\u20b9561', 'Price below \u2192 Bearish (medium-term)'],
        ['RSI (14)', '59.7', 'Neutral (Investing.com, late Jan 2026)'],
        ['MACD', '0.97', 'Mildly Bullish'],
        ['Support Zone', '\u20b9490\u2013510', '52-week low area; strong floor'],
        ['Resistance Zone', '\u20b9550\u2013590', 'Previous consolidation, 200-DMA zone'],
        ['52-Week High', '\u20b9706', 'Would need 40%+ rally to retest'],
        ['Beta', '~0.8', 'Slightly less volatile than market'],
    ]
    tech_table = Table(tech_data, colWidths=[3.5*cm, 3*cm, 9*cm])
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
        '<b>Pattern:</b> The stock is in a clear downtrend, trading below both the 50-day EMA and 200-day SMA. '
        'However, RSI at ~60 and positive MACD suggest the most recent bounce from \u20b9490 levels has some '
        'momentum. StockInvest.us reports accumulated volume support at \u20b9547 and resistance at \u20b9621. '
        'A sustained break above \u20b9560\u2013580 (200-DMA zone) would be the first sign of trend reversal. '
        'Until then, the path of least resistance remains downward, and the stock may retest '
        '\u20b9490 support.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Investing.com (investing.com/equities/cello-world-technical), StockInvest.us, '
        'Tickertape, MunafaSutra (data as of late Jan 2026)',
        source_style
    ))

    story.append(PageBreak())

    # ============================================================
    # SECTION 4: SECTOR & COMPETITIVE CONTEXT
    # ============================================================
    story.append(Paragraph('4. Sector & Competitive Context', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Indian Consumer Products Market', subheading_style))
    story.append(Paragraph(
        'Cello World operates across multiple consumer product categories \u2014 houseware, glassware, '
        'writing instruments, and furniture. The Indian houseware market benefits from rising urbanization, '
        'nuclear household formation, and premiumization trends. The writing instruments market in India '
        'is valued at ~\u20b910,000 Cr, with organized players gaining share from unorganized manufacturers. '
        'Cello World\'s reacquisition of the Cello brand (25% historical market share) positions it to '
        'capitalize on this shift.',
        body_style
    ))

    story.append(Paragraph('Nifty Consumer Durables Index Performance', subheading_style))
    story.append(Paragraph(
        'The Nifty Consumer Durables Index stands at \u20b936,229 (Feb 4, 2026) with a 52-week range of '
        '\u20b932,205\u201340,472. <b>The index delivered a 1-year return of -1.6%</b>, while Cello World '
        'declined ~22%. This means <b>Cello World underperformed the sector by ~20 percentage points</b> '
        '\u2014 the correction is significantly stock-specific, driven by margin compression and working '
        'capital concerns rather than sector-wide factors.',
        body_style
    ))

    story.append(Paragraph('Competitive Landscape', subheading_style))
    peer_data = [
        ['Metric', 'Cello World', 'Borosil Ltd', 'Flair Writing', 'Linc Ltd', 'La Opala RG'],
        ['Revenue', '\u20b92,136 Cr', '\u20b9850 Cr', '\u20b91,200 Cr', '\u20b9500 Cr', '\u20b9350 Cr'],
        ['P/E (TTM)', '33.6x', '34x', '27x', '18.5x', '23x'],
        ['P/B Ratio', '4.86x', '3.48x', '3.26x', '2.77x', '2.78x'],
        ['Market Cap', '\u20b911,066 Cr', '\u20b92,500 Cr', '\u20b93,317 Cr', '\u20b9667 Cr', '\u20b91,800 Cr'],
        ['1Y Return', '-22%', '-15%', '-20%', '-34%', '-10%'],
        ['Key Segment', 'Multi-category', 'Glassware', 'Writing instr.', 'Writing instr.', 'Opalware'],
    ]
    peer_table = Table(peer_data, colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
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
    ]))
    story.append(peer_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Image(chart_paths['peers'], width=16*cm, height=6.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Peer Valuation Context:</b> Cello World trades at 33.6x P/E \u2014 roughly in line with the peer '
        'median of 33.2x (Smart-Investing.in). Its P/B of 4.86x is a 25% premium to peer median of 3.88x. '
        'Among writing instrument peers, Linc (18.5x) and Flair (27x) trade at significant discounts. '
        'However, Cello World\'s diversified product mix and larger scale justify some premium. '
        'The unlisted <b>Hamilton Housewares (Milton brand)</b> with \u20b92,360 Cr revenue is the closest '
        'unlisted competitor in houseware.',
        body_style
    ))

    story.append(Paragraph('Raw Material & Commodity Context', subheading_style))
    story.append(Paragraph(
        'Cello World\'s key raw materials include <b>polypropylene (PP), polyethylene (PE), and glass raw materials</b>. '
        'PP prices in India stand at ~$1.02\u20131.06/kg (Jan 2026), down ~8% YoY. Indian PP markets have been '
        'under bearish pressure from oversupply, weak downstream demand, and aggressive pricing from new '
        'Chinese capacities. IOC implemented a PP price hike of INR 1,000/MT in Jan 2026, but the broader '
        'trend remains soft. <b>Net impact for Cello World: mildly favorable</b> \u2014 raw material costs '
        'should remain stable-to-declining in FY27, which could support margin recovery if the company '
        'can also improve glass plant utilization and working capital efficiency.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Screener.in (peers), Smart-Investing.in, Kotak Securities (peer comparison), '
        'Nifty Indices (niftyindices.com), IMARC Group (polypropylene report), '
        'ChemOrbis, BusinessAnalytiq, Plastemart (PP/PE prices)',
        source_style
    ))

    story.append(PageBreak())

    # ============================================================
    # SECTION 5: VALUATION & ANALYST VIEWS
    # ============================================================
    story.append(Paragraph('5. Valuation & Analyst Views', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Brokerage Target Prices', subheading_style))

    analyst_data = [
        ['Brokerage / Source', 'Target (\u20b9)', 'Rating', 'Key Thesis'],
        ['Motilal Oswal', '700', 'Buy', '32x FY27E EPS; Falna ramp-up catalyst; 15% rev CAGR'],
        ['PL Capital (Prabhudas Lilladhar)', '678', 'Buy', 'Cut from \u20b9746; margin pressure acknowledged'],
        ['Consensus (6 analysts)', '705\u2013730', 'Strong Buy', '6/6 Buy, 0 Hold/Sell'],
        ['TradingView (3 analysts)', '1,009', '\u2014', 'Range: \u20b9922\u20131,139 (older targets)'],
        ['Investing.com (6 analysts)', '705', '\u2014', 'Low: N/A, High: \u20b9950'],
    ]
    analyst_table = Table(analyst_data, colWidths=[4*cm, 2*cm, 2*cm, 7.5*cm])
    analyst_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(analyst_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Implied Upside:</b> From ~\u20b9505 (Jan 16 close), the consensus target of \u20b9705\u2013730 '
        'implies ~40\u201345% upside over 12 months. Even PL Capital\'s reduced target of \u20b9678 '
        'suggests ~34% upside. All 6 covering analysts rate the stock a Buy \u2014 zero Hold or Sell ratings. '
        '<b>However,</b> unanimous Buy consensus is itself a contrarian warning \u2014 and PL Capital\'s target cut '
        'signals increasing caution.',
        callout_green
    ))

    story.append(Paragraph(
        '<b>Note on target timing:</b> Motilal Oswal\'s target was published post-Q2 FY26 results (Oct 2025). '
        'PL Capital\'s was post-Q1 FY26 (Aug 2025). The TradingView average of \u20b91,009 appears to include '
        'older, stale targets from IPO-era coverage and should be treated with caution. '
        'We weight recent targets (Motilal \u20b9700, PL Capital \u20b9678) more heavily.',
        body_style
    ))

    story.append(Paragraph('Valuation Context', subheading_style))
    story.append(Paragraph(
        'At 33.6x trailing P/E, Cello World trades roughly in line with its peer average. This is a '
        '<b>significant de-rating from its IPO valuation of ~40\u201345x</b> and reflects the market\'s '
        'repricing for (a) margin contraction, (b) working capital deterioration, and (c) execution '
        'risk on the glass plant. Motilal Oswal values the stock at 32x FY27E EPS, implying the '
        'market is already at "fair value" on current-year earnings. Upside depends on whether '
        'FY27 delivers the expected margin recovery and Cello brand revenue contribution.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Motilal Oswal (via Business Standard, Oct 2025), PL Capital (via BusinessToday, Aug 2025), '
        'Investing.com, TradingView, INDmoney, Trendlyne, Stockopedia',
        source_style
    ))

    story.append(PageBreak())

    # ============================================================
    # SECTION 6: CATALYSTS, RISKS & MANAGEMENT GUIDANCE
    # ============================================================
    story.append(Paragraph('6. Growth Catalysts & Risks', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Management Guidance (Q2 FY26 Earnings Call, Nov 12, 2025)', subheading_style))
    story.append(Paragraph(
        'Key forward-looking statements from the Q2 FY26 earnings call (GuruFocus, MarketScreener):',
        body_style
    ))
    mgmt_points = [
        '<b>Revenue Growth:</b> Management maintains guidance of <b>double-digit revenue growth</b> '
        'for FY26, supported by consumerware momentum and upcoming Cello brand revenues.',
        '<b>Margins:</b> EBITDA margin guided at <b>22\u201323%</b>. CMD Pradeep Rathod stated: '
        '"Our glass plant in Falna is ramping up as per plan with about 55% utilization, which is '
        'expected to reach 80% by Q4 FY26. While the plant is in the gestation phase, margin '
        'structures will continue to be impacted."',
        '<b>Cello Brand:</b> "We are very excited to bring this back into our company soon" \u2014 '
        'Gaurav Rathod, JMD. Expected \u20b9200 Cr revenue from Cello brand in first year (CY2026). '
        '\u20b950 Cr investment in writing instruments manufacturing infrastructure.',
        '<b>New Steel Plant:</b> Set to commence production from December 2025, expected to enhance '
        'cost competitiveness and support margin improvement.',
        '<b>Solar Initiatives:</b> Undertaking solar-based cost optimization to reduce energy costs.',
        '<b>Focus on Efficiency:</b> "Our focus will be on enhancing operational efficiency, optimizing '
        'costs, and leveraging our established manufacturing and distribution infrastructure" \u2014 '
        'Gaurav Rathod, JMD.',
    ]
    for mp in mgmt_points:
        story.append(Paragraph(f'\u2022 {mp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Growth Catalysts (Bull Case)', subheading_style))
    bull_points = [
        '<b>Cello Brand Reacquisition:</b> The zero-royalty acquisition of the "Cello" trademark for writing '
        'instruments is potentially transformative. Cello had 25% market share before the BIC sale. '
        'Management targets \u20b9200 Cr revenue in the first year \u2014 this alone could add 10% to '
        'total revenue. The dual-brand strategy (Cello + Unomax) creates a formidable writing '
        'instruments portfolio.',
        '<b>Glass Plant Ramp-Up:</b> The Falna 20,000 MT glassware facility (German furnaces, Italian '
        'press-and-blow technology) has achieved breakeven at 55-60% utilization. At 80% utilization '
        '(targeted Q4 FY26), it should contribute meaningfully to both revenue and margins. '
        '<b>Glass segment estimate:</b> At 20,000 MT capacity, 80% utilization (16,000 MT), and assumed '
        'realization of Rs 50-60/kg, revenue contribution would be approximately Rs 80-96 Cr '
        '(4-5% of total FY25 revenue). This is a long-term growth driver but near-term drag on FCF '
        'due to heavy capex.',
        '<b>Premiumization:</b> Hydration products, opalware, and premium glassware are growing rapidly '
        'within the consumerware segment, driving ASP growth.',
        '<b>Nearly Debt-Free:</b> With negligible interest costs (\u20b90.48 Cr), the company has '
        'strong financial flexibility for growth investments.',
        '<b>Favorable Raw Material Outlook:</b> PP prices down 8% YoY with soft 2026 outlook \u2014 '
        'provides a tailwind for plastic houseware margins.',
        '<b>High Promoter Conviction:</b> 75% promoter holding indicates strong insider confidence.',
    ]
    for bp in bull_points:
        story.append(Paragraph(f'\u2022 {bp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Risks (Bear Case)', subheading_style))
    bear_points = [
        '<b>Margin Contraction Not Bottoming:</b> EBITDA margin fell from 27% to 22% and management '
        'now guides 22-23%. If the glass plant ramp-up is slower than expected or steel supply '
        'constraints persist, margins could fall further.',
        '<b>Working Capital Deterioration:</b> 127 to 184 days is alarming. If this trend continues, '
        'cash flow will remain under pressure and the company may need external funding.',
        '<b>Standalone CFO Negative:</b> If the parent entity cannot generate positive operating cash flow, '
        'the corporate structure becomes fragile \u2014 subsidiaries fund the parent, which is a '
        'red flag for governance quality.',
        '<b>Glass Plant Execution Risk:</b> Glassware is a competitive, capital-intensive category. '
        'Borosil Ltd (34x P/E, established player) sets the benchmark. Cello World entering '
        'this space carries execution and pricing risk.',
        '<b>Furniture Segment Stagnation:</b> Moulded furniture (~14% of revenue) shows limited growth '
        'and contracting margins. This segment may become a drag on overall performance.',
        '<b>Severe Stock Correction:</b> The stock fell from \u20b9706 to \u20b9490 (-30.5%) in the past '
        'year. This level of drawdown can indicate institutional selling. FII holding is only 5.6%, '
        'and further selling could pressure the stock.',
        '<b>Low Liquidity:</b> With 75% promoter holding and only 25% free float (of which DIIs hold 14%), '
        'actual tradeable float is limited. This can amplify volatility in both directions.',
    ]
    for bp in bear_points:
        story.append(Paragraph(f'\u2022 {bp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: Q2 FY26 Earnings Call (GuruFocus, MarketScreener), Screener.in, Business Standard, '
        'Trendlyne, MarketsMojo',
        source_style
    ))

    story.append(PageBreak())

    # ============================================================
    # SECTION 7: CONCLUSION & VALUATION
    # ============================================================
    story.append(Paragraph('7. Conclusion & 1-Year Outlook', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Cello World is a well-managed, nearly debt-free consumer products company with a strong brand '
        'portfolio and diversified product mix. The reacquisition of the Cello brand for writing instruments '
        'is a significant strategic move. However, the company faces near-term headwinds from margin '
        'compression (glass plant ramp-up, steel supply issues), working capital deterioration, and '
        'a stock price that has already corrected 22% in the past year.',
        body_style
    ))

    story.append(Spacer(1, 0.3*cm))

    # Valuation Methodology
    story.append(Paragraph('Valuation Methodology: Forward EPS x P/E Multiple', subheading_style))
    story.append(Paragraph(
        'The scenario analysis below uses a <b>forward earnings-multiple approach</b>. '
        'This is not a DCF (discounted cash flow) model \u2014 it is a heuristic based on projected '
        'EPS and an assumed P/E multiple for each scenario. Limitations are noted at the end.',
        body_style
    ))

    story.append(Paragraph('<b>Step 1: Establish Current EPS</b>', body_style))
    eps_data = [
        ['Metric', 'Value', 'Source'],
        ['FY25 Net Profit (Consol.)', '\u20b9365 Cr', 'Screener.in (verified)'],
        ['Market Cap', '\u20b911,066 Cr', 'Tickertape (Jan 16, 2026)'],
        ['Price', '\u20b9505', 'NSE (Jan 16, 2026)'],
        ['Shares Outstanding', '22.09 Cr', 'Screener.in (Equity Capital Rs 110 Cr at FV Rs 5)'],
        ['TTM EPS (Consol.)', '~\u20b916.52', 'PAT / Shares (365/22.09)'],
        ['Sanity Check: P/E', '505 / 16.52 = 30.6x', 'vs reported 33.6x (diff. due to trailing period) \u2713'],
    ]
    eps_table = Table(eps_data, colWidths=[3.5*cm, 4.5*cm, 6.5*cm])
    eps_table.setStyle(TableStyle([
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
    story.append(eps_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Note:</b> Shares outstanding verified at 22.09 Cr (Equity Capital Rs 110 Cr at FV Rs 5, '
        'source: Screener.in). Standalone TTM EPS is lower based on standalone PAT. '
        'We use consolidated EPS as it captures the full business including subsidiaries. '
        'Motilal Oswal also uses consolidated financials for their \u20b9700 target.',
        body_style
    ))

    story.append(Paragraph('<b>Step 2: Project FY27E EPS by Scenario</b>', body_style))
    story.append(Paragraph(
        'Growth rate anchors: Motilal Oswal projects 15% revenue CAGR, 17% EBITDA CAGR, and 18% PAT CAGR '
        '(FY25-28E). We use these as the base case. Cello brand contribution (\u20b9200 Cr) and glass plant '
        'ramp-up are the key upside catalysts.',
        body_style
    ))

    proj_data = [
        ['', 'Bull', 'Base', 'Bear'],
        ['FY26E PAT Growth', '20% (Cello brand + recovery)', '12% (in-line with H1 trend)', '-5% (revenue decline + margin compression)'],
        ['FY26E EPS', '\u20b916.52 x 1.20 = \u20b919.82', '\u20b916.52 x 1.12 = \u20b918.50', '\u20b916.52 x 0.95 = \u20b915.69'],
        ['FY27E PAT Growth', '20% (sustained)', '18% (Motilal CAGR)', '0% (no recovery)'],
        ['FY27E EPS', '\u20b919.82 x 1.20 = \u20b923.79', '\u20b918.50 x 1.18 = \u20b921.83', '\u20b915.69 x 1.00 = \u20b915.69'],
    ]
    proj_table = Table(proj_data, colWidths=[3.2*cm, 4.5*cm, 4.5*cm, 4*cm])
    proj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (1, 0), (1, -1), HexColor('#f0fff4')),
        ('BACKGROUND', (2, 0), (2, -1), HexColor('#fffff0')),
        ('BACKGROUND', (3, 0), (3, -1), HexColor('#fff5f5')),
        ('TEXTCOLOR', (1, 0), (3, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(proj_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>Step 3: Apply P/E Multiple \u2192 Target Price</b>', body_style))
    story.append(Paragraph(
        'P/E assumptions are anchored to peer comps: Borosil 34x, Flair Writing 27x, Linc 18.5x, '
        'La Opala 23x, sector avg ~33x. Cello World\'s historical P/E range is 30\u201345x. '
        'Bear case uses 18-24x reflecting commodity/durables company multiples at cyclical bottom.',
        body_style
    ))

    scenario_data = [
        ['Scenario', 'FY27E EPS', 'P/E Assumed', 'Price Target', 'Return from \u20b9505', 'Probability'],
        ['Bull', '\u20b923.79', '35\u201338x',
         '\u20b9833\u2013904', '+65% to +79%', '20%'],
        ['Base', '\u20b921.83', '30\u201333x',
         '\u20b9655\u2013720', '+30% to +43%', '50%'],
        ['Bear', '\u20b915.69', '18\u201324x',
         '\u20b9282\u2013377', '-25% to -44%', '30%'],
    ]
    scenario_table = Table(scenario_data, colWidths=[1.8*cm, 2.3*cm, 2.3*cm, 2.8*cm, 3.3*cm, 2.5*cm])
    scenario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fffff0')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#fff5f5')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(scenario_table)
    story.append(Spacer(1, 0.3*cm))

    # Probability-weighted expected value
    story.append(Paragraph('<b>Step 4: Probability-Weighted Expected Value</b>', body_style))
    story.append(Paragraph(
        'Assigning probabilities based on current evidence:',
        body_style
    ))
    prob_points = [
        '<b>Bull (20%):</b> Requires Cello brand to deliver \u20b9200 Cr as promised, glass plant '
        'reaching 80% utilization, working capital days improving, AND market re-rating the stock '
        'to 35-38x. Possible but requires everything to go right. Low but real probability.',
        '<b>Base (50%):</b> Most likely outcome. Cello World delivers on management guidance of double-digit '
        'growth, margins stabilize at 22-23% (as guided), Cello brand contributes partially, '
        'and P/E stays at 30-33x. This is the "steady execution" scenario.',
        '<b>Bear (30%):</b> Higher than typical because of specific, identifiable risks: (a) working capital '
        'days already ballooned 45% (127\u2192184 days), (b) standalone CFO verified negative at Rs -46.70 Cr, '
        '(c) glass plant ramp-up could be slower than planned, (d) furniture segment is stagnating, '
        '(e) the stock has already fallen 30% from its high, showing it can fall sharply, and '
        '(f) FCF has been consistently negative (FY25: Rs -354 Cr). Bear P/E of 18-24x reflects '
        'commodity/durables company multiples at cyclical bottom (Linc trades at 18.5x). '
        'Revenue could decline -5% if macro weakens and channel destocking occurs. '
        'A 30% bear weight reflects these tangible headwinds.',
    ]
    for pp in prob_points:
        story.append(Paragraph(f'\u2022 {pp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    ev_data = [
        ['Scenario', 'Midpoint Price', 'Probability', 'Weighted Value'],
        ['Bull', '\u20b9869', '20%', '\u20b9174'],
        ['Base', '\u20b9688', '50%', '\u20b9344'],
        ['Bear', '\u20b9330', '30%', '\u20b999'],
        ['', '', 'Expected Value \u2192', '\u20b9617'],
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
        '<b>Probability-weighted expected price: \u20b9617</b> \u2014 implying ~22% upside from \u20b9505. '
        'However, the severe bear case (\u20b9282\u2013377, or -25% to -44%) with 30% probability '
        'is a material risk. The lower bear P/E (18-24x, reflecting commodity/durables cyclical bottom '
        'multiples) and -5% revenue decline scenario reflect the real possibility of further de-rating.',
        callout_green
    ))

    story.append(Spacer(1, 0.3*cm))

    # Methodology limitations
    story.append(Paragraph('Methodology Limitations (Transparency Note)', subheading_style))
    story.append(Paragraph(
        'This analysis uses a P/E multiple heuristic. Investors should be aware of its limitations:',
        body_style
    ))
    limit_points = [
        '<b>Not a DCF:</b> A proper intrinsic value estimate requires a 3-statement financial model '
        'with segment-level revenue build-up (consumerware, writing instruments, furniture), margin '
        'assumptions by segment, capex forecasting, and WACC-based discounting. This report does not include one.',
        '<b>P/E assumptions are subjective:</b> The choice of 30-33x for base vs 18-24x for bear is '
        'anchored to peer comps (Borosil 34x, Flair 27x, Linc 18.5x, La Opala 23x) but remains a judgment call.',
        '<b>EPS estimates are top-down:</b> Growth rates are sourced from Motilal Oswal (18% PAT CAGR) '
        'rather than built from a bottoms-up P&L forecast by segment.',
        '<b>Probability weights are subjective:</b> The 20/50/30 split is an informed estimate based '
        'on current evidence (working capital deterioration, margin compression, cash flow concerns). '
        'A more cautious analyst might assign 35%+ to the bear case.',
        '<b>Cash flow ignored in valuation:</b> Given the standalone CFO concerns and working capital '
        'deterioration, an EV/FCF or DCF approach would likely produce a more conservative (and arguably '
        'more realistic) valuation than the P/E method used here.',
        '<b>Standalone vs Consolidated gap:</b> The significant gap between standalone and consolidated '
        'financials (revenue, profit, cash flow) adds complexity. The consolidated P/E of 33x may mask '
        'weaker standalone economics that could become relevant if subsidiary cash flows deteriorate.',
    ]
    for lp in limit_points:
        story.append(Paragraph(f'\u2022 {lp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Verdict', subheading_style))
    story.append(Paragraph(
        '<b>Cello World is a fundamentally sound, nearly debt-free consumer products company '
        'undergoing a transition.</b> The reacquisition of the iconic Cello brand for writing instruments '
        'and the ramp-up of the Falna glassware plant are genuine medium-term catalysts. '
        'However, the near-term picture is challenging: margins have contracted 427 bps, working '
        'capital days have ballooned 45%, and standalone cash flow reportedly turned negative.',
        body_style
    ))
    story.append(Paragraph(
        'The <b>probability-weighted expected value of \u20b9617 implies ~22% upside</b> over 12 months. '
        'This is supported by unanimous analyst Buy ratings (avg target \u20b9705\u2013730) but tempered '
        'by a 30% bear probability driven by working capital deterioration, margin pressure, negative FCF, '
        'and glass plant execution risk. The bear case (P/E 18-24x at cyclical bottom) implies -25% to -44% '
        'downside. The key variables are: (a) can the Cello brand deliver \u20b9200 Cr '
        'as promised?, (b) will EBITDA margins stabilize at 22-23% or compress further?, and '
        '(c) will working capital days improve or continue to deteriorate?',
        body_style
    ))
    story.append(Paragraph(
        '<b>On balance, the stock offers a moderate expected return (~22%) with a severe bear case '
        '(-25% to -44% in the downside scenario). The high promoter holding (75%), debt-free balance '
        'sheet, and strong 3Y ROE (35.7%) provide downside protection, while the Cello brand relaunch '
        'and glass plant maturation offer upside optionality. Suited for investors with a 12+ month '
        'horizon who are comfortable with consumer mid-cap volatility and can monitor the quarterly '
        'margin and working capital trends closely. Not suitable for conservative or short-term '
        'portfolios.</b>',
        body_style
    ))

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cbd5e0')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>IMPORTANT DISCLAIMER:</b> This report is generated for informational and educational '
        'purposes only. It does not constitute investment advice, a recommendation to buy, sell, '
        'or hold any security, or an offer of any kind. All data is sourced from publicly available '
        'information as of February 4, 2026. Past performance does not guarantee future results. '
        'Stock market investments carry risk of capital loss. Please consult a SEBI-registered '
        'investment advisor before making any investment decisions. The author has no position '
        'in Cello World Limited.',
        disclaimer_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Data Sources:</b> Screener.in (primary financial data) | NSE India (nseindia.com) | '
        'Yahoo Finance (finance.yahoo.com) | Business Standard (business-standard.com) | '
        'Trendlyne (trendlyne.com) | Investing.com | TradingView (tradingview.com) | '
        'GuruFocus (gurufocus.com) | MarketScreener (marketscreener.com) | '
        'Smart-Investing.in | Motilal Oswal | PL Capital (Prabhudas Lilladhar) | '
        'IMARC Group (polypropylene) | ChemOrbis | Cello World Corporate (corporate.celloworld.com)',
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
