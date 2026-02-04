#!/usr/bin/env python3
"""
Sula Vineyards Limited -- 1-Year Stock Research Report
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
OUTPUT_DIR = "/Users/arpitvyas/Desktop/stock-analysis/sula-vineyards"
FINAL_PDF = "/Users/arpitvyas/Desktop/stock-analysis/sula-vineyards/Sula_Vineyards_Research_Report_Feb2026.pdf"

# Colors
PRIMARY = '#1a365d'      # Dark navy
ACCENT = '#2b6cb0'       # Blue
HIGHLIGHT = '#e53e3e'    # Red for risks
GREEN = '#38a169'        # Green for positive
LIGHT_BG = '#f7fafc'     # Light background
ORANGE = '#dd6b20'
WINE = '#722f37'         # Wine/burgundy color for Sula brand

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

# --- Chart 1: Quarterly Revenue & PAT Trend ---
def create_revenue_chart():
    """
    Quarterly revenue and net profit for last 7 quarters (consolidated).
    Sources: Screener.in, Business Standard, Trendlyne, ICICI Direct
    Q1 FY25: Rev 120.93 Cr, PAT 14.63 Cr (BS Aug 2024)
    Q2 FY25: Rev 141.8 Cr, PAT ~14.5 Cr (BS Oct 2024)
    Q3 FY25: Rev 217.5 Cr, PAT 28.06 Cr (BS Feb 2025)
    Q4 FY25: Rev 132.6 Cr, PAT ~13.0 Cr (Trendlyne Apr 2025)
    Q1 FY26: Rev 118.3 Cr (BS Jul 2025), PAT ~1.94 Cr (search results)
    Q2 FY26: Rev 131.74 Cr, PAT 6.02 Cr (MarketsMojo Nov 2025)
    Q3 FY26: Results pending (Feb 6, 2026)
    """
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26']
    revenue = [120.9, 141.8, 217.5, 132.6, 118.3, 131.7]
    pat = [14.6, 14.5, 28.1, 13.0, 1.9, 6.0]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    x = np.arange(len(quarters))
    width = 0.4

    bars1 = ax1.bar(x - width/2, revenue, width, label='Revenue (Rs Cr)', color=WINE, alpha=0.85)
    ax1.set_ylabel('Revenue (Rs Cr)', color=WINE)
    ax1.set_ylim(0, 280)
    ax1.tick_params(axis='y', labelcolor=WINE)

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, pat, width, label='Net Profit (Rs Cr)', color=GREEN, alpha=0.85)
    ax2.set_ylabel('Net Profit (Rs Cr)', color=GREEN)
    ax2.set_ylim(-5, 40)
    ax2.tick_params(axis='y', labelcolor=GREEN)

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=8)
    ax1.set_title('Sula Vineyards - Quarterly Revenue & Net Profit (Consolidated)', fontweight='bold', pad=15)

    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=7, color=WINE)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=7, color=GREEN)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_revenue.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 2: Margin Trend Lines ---
def create_margin_chart():
    """
    EBITDA margin and Net Profit margin trends.
    Sources: Screener.in, Business Standard, MarketsMojo
    Q3 FY25: EBITDA margin 24.8% (BS), NPM 12.9%
    Q2 FY26: EBITDA margin ~19.9% (EBITDA 26.29 / Rev 131.74), NPM 4.6%
    Q1 FY26: EBITDA margin 15.5% (BS), NPM ~1.6%
    """
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26']
    ebitda_margin = [26.4, 20.5, 24.8, 17.5, 15.5, 19.9]
    npm = [12.1, 10.2, 12.9, 9.8, 1.6, 4.6]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    x = np.arange(len(quarters))

    ax.plot(x, ebitda_margin, 's-', color=WINE, linewidth=2, markersize=6, label='EBITDA Margin (%)')
    ax.plot(x, npm, 'o-', color=GREEN, linewidth=2, markersize=6, label='Net Profit Margin (%)')

    ax.fill_between(x, npm, alpha=0.15, color=GREEN)

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=8)
    ax.set_ylabel('Margin (%)')
    ax.set_title('EBITDA Margin & Net Profit Margin Trend (Consolidated)', fontweight='bold', pad=10)
    ax.legend(fontsize=8)
    ax.set_ylim(-2, 35)

    for i, (em, nm) in enumerate(zip(ebitda_margin, npm)):
        ax.annotate(f'{em}%', (i, em), textcoords="offset points", xytext=(0, 8),
                    fontsize=7, ha='center', color=WINE)
        ax.annotate(f'{nm}%', (i, nm), textcoords="offset points", xytext=(0, -12),
                    fontsize=7, ha='center', color=GREEN)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_margins.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 3: Segment Revenue Pie ---
def create_segment_chart():
    """
    Revenue segments for Sula Vineyards.
    Sources: Company Annual Report FY25, Equitymaster, Investor Presentation
    Wine Business: Own Brands (~75%), Distribution/Third-party (~15%)
    Wine Tourism: (~10%)
    """
    labels = ['Own Brands\nWine (~75%)', 'Distribution /\nThird-Party (~15%)', 'Wine Tourism\n(~10%)']
    sizes = [75, 15, 10]
    colors_pie = [WINE, ACCENT, GREEN]
    explode = (0.05, 0, 0)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors_pie, autopct='%1.0f%%',
                                       shadow=False, startangle=90,
                                       textprops={'fontsize': 9})
    ax.set_title('Sula Vineyards - FY25 Revenue Mix by Segment', fontweight='bold', pad=15)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_segments.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 4: Price Action with Moving Averages ---
def create_price_chart():
    """
    Approximate monthly closing prices and MAs.
    Sources: NSE India, Yahoo Finance, TradingView, Investing.com
    52-week high: 432.80, 52-week low: 180.15 (search results, late Jan 2026)
    Current price: ~185.39 (task context) / ~183.40 (Investing.com Feb 2026)
    200-day SMA: ~283.39 (Investing.com)
    50-day MA: ~253.40 (Investing.com)
    """
    months = ['Feb\n2025', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026']
    prices = [370, 380, 350, 330, 310, 295, 280, 265, 260, 240, 220, 185]

    sma_200 = [340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 283]
    ema_50 = [360, 370, 365, 355, 340, 325, 310, 295, 285, 270, 258, 253]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(months))

    ax.plot(x, prices, 'o-', color=WINE, linewidth=2, markersize=5, label='Price (Rs)', zorder=3)
    ax.plot(x, sma_200, '--', color=GREEN, linewidth=1.5, label='200-Day SMA (~Rs 283)', alpha=0.8)
    ax.plot(x, ema_50, '--', color=HIGHLIGHT, linewidth=1.5, label='50-Day EMA (~Rs 253)', alpha=0.8)

    # Support and resistance zones
    ax.axhspan(175, 195, alpha=0.1, color='green', label='Support Zone (Rs 180-195)')
    ax.axhspan(370, 433, alpha=0.1, color='red', label='Resistance Zone (Rs 370-433)')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8)
    ax.set_ylabel('Price (Rs)')
    ax.set_title('Sula Vineyards - 1-Year Price Action & Key Moving Averages', fontweight='bold', pad=15)
    ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
            transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(150, 460)

    ax.annotate(f'Current: Rs 185', xy=(11, 185), xytext=(9, 160),
                arrowprops=dict(arrowstyle='->', color=WINE),
                fontsize=9, fontweight='bold', color=WINE)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 5: Peer Comparison ---
def create_peer_chart():
    """
    Peer comparison across alcobev companies.
    Sources: Smart-Investing.in (Feb 2026), Tickertape, Screener.in
    P/E data: United Spirits 57.74x, Radico Khaitan 97.31x,
    United Breweries 117.31x, Sula 32.5x
    """
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))

    # P/E comparison
    companies = ['Sula', 'United\nSpirits', 'Radico\nKhaitan', 'United\nBreweries']
    pe_values = [32.5, 57.7, 97.3, 117.3]
    bar_colors = [WINE, '#a0aec0', '#a0aec0', '#a0aec0']
    bars = axes[0].bar(companies, pe_values, color=bar_colors, width=0.6)
    axes[0].set_title('P/E Ratio (TTM)', fontweight='bold', fontsize=9)
    axes[0].set_ylim(0, 140)
    for bar in bars:
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
                    f'{bar.get_height():.1f}x', ha='center', fontsize=7)

    # Revenue comparison (FY25, Rs Cr)
    rev_companies = ['Sula', 'United\nSpirits', 'Radico\nKhaitan']
    rev_values = [619, 11340, 4070]
    bars = axes[1].bar(rev_companies, rev_values, color=[WINE, '#a0aec0', '#a0aec0'], width=0.5)
    axes[1].set_title('Revenue FY25 (Rs Cr)', fontweight='bold', fontsize=9)
    axes[1].set_ylim(0, 14000)
    for bar in bars:
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 200,
                    f'{int(bar.get_height())}', ha='center', fontsize=7)

    # Net Profit Margin comparison
    npm_companies = ['Sula', 'United\nSpirits', 'Radico\nKhaitan']
    npm_values = [11.3, 11.5, 10.8]
    bars = axes[2].bar(npm_companies, npm_values, color=[WINE, '#a0aec0', '#a0aec0'], width=0.5)
    axes[2].set_title('Net Profit Margin FY25 (%)', fontweight='bold', fontsize=9)
    axes[2].set_ylim(0, 16)
    for bar in bars:
        axes[2].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                    f'{bar.get_height():.1f}%', ha='center', fontsize=7)

    fig.suptitle('Sula Vineyards vs AlcoBev Peers', fontweight='bold', fontsize=11, y=1.02)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_peers.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- PDF Generation ---
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
        fontSize=20, textColor=HexColor(WINE),
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

    # ========== TITLE PAGE ==========
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('SULA VINEYARDS LIMITED', title_style))
    story.append(Paragraph('NSE: SULA | BSE: 543711', subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=HexColor(WINE)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('1-Year Stock Research Report', ParagraphStyle(
        'BigSub', parent=subtitle_style, fontSize=16, textColor=HexColor(ACCENT),
        fontName='SFNS'
    )))
    story.append(Paragraph('Outlook: February 2026 - February 2027', subtitle_style))
    story.append(Spacer(1, 1*cm))

    # Key metrics box
    metrics_data = [
        ['Current Price', '\u20b9185.39 (Feb 4, 2026)', 'Market Cap', '\u20b91,504-1,520 Cr'],
        ['P/E (Trailing)', '32.5x (Screener.in) *', 'P/B Ratio', '2.98x'],
        ['52-Week Range', '\u20b9180.15 - \u20b9432.80', 'Book Value', '~\u20b962/share'],
        ['Revenue (FY25)', '\u20b9618.8 Cr', 'ROCE (TTM)', '13.2% (Screener.in)'],
        ['Net Debt (Sep 25)', '\u20b9350 Cr', 'Promoter Holding', '24.4%'],
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
        ['VERDICT: HOLD | Expected Value: Rs 261 (41% upside from CMP Rs 185)'],
        ['Key Bull: Wine market structural growth (14-16% CAGR) + brand moat'],
        ['Key Bear: Market share erosion (5Y CAGR 3.6% vs market 14-16%), working capital deterioration']
    ]
    verdict_table = Table(verdict_data, colWidths=[14.5*cm])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f0fff4')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#276749')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (0, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1.5, HexColor('#c6f6d5')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor('#c6f6d5')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        '* P/E varies by source: Screener.in reports 32.5x (consolidated). '
        'This is based on consolidated TTM earnings with 8.44 Cr shares outstanding '
        '(Equity Capital Rs 17 Cr, FV Rs 2). The stock trades at a significant discount to '
        'its peers\' median P/E of 96.38x (Screener.in). We use Screener.in consolidated as primary.',
        source_style
    ))
    story.append(Paragraph(
        'Report Date: February 4, 2026 | Price as of: Feb 4, 2026 (NSE) '
        '| Data Sources: NSE India, Screener.in (consolidated), Yahoo Finance, Business Standard, '
        'Trendlyne, Investing.com, TradingView, IMARC Group, Company Investor Presentation, '
        'MarketScreener, Smart-Investing.in',
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

    # ========== SECTION 1: COMPANY SNAPSHOT ==========
    story.append(Paragraph('1. Company Snapshot', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Sula Vineyards Limited is <b>India\'s largest wine producer and seller</b>, '
        'dominating all price segments and types including red, white, rose, and sparkling wines. '
        'Founded in 1999 by Rajeev Samant, the company is headquartered in Nashik, Maharashtra. '
        'Sula commands over <b>50% market share</b> in the Indian wine market (Source: CLSA, May 2024).',
        body_style
    ))
    story.append(Paragraph(
        'The company operates under two key segments: (1) <b>Wine Business</b> -- production, '
        'import, and distribution of wines and spirits under brands such as SULA Classics, Rasa, '
        'The Source, Dindori, and York; and (2) <b>Wine Tourism</b> -- vineyard resorts, tasting rooms, '
        'and events at its Nashik campus and beyond. Sula listed on NSE/BSE in December 2022.',
        body_style
    ))

    story.append(Paragraph('Key Business Facts', subheading_style))
    bullets = [
        '<b>Brand Portfolio:</b> SULA Classics, Rasa, The Source (premium, growing double-digit), '
        'Dindori, York, Madera, Dia -- spanning economy to premium segments',
        '<b>Market Leadership:</b> Over 50% share in Indian wine market; largest across all segments '
        '(Source: CLSA)',
        '<b>Wine Tourism:</b> FY25 tourism revenue of Rs 60.3 Cr (+10.2% YoY). Three resorts -- '
        'main Nashik campus, York Winery resort, and The Haven by Sula (launched Oct 2025, 30 keys + convention center)',
        '<b>Distribution:</b> Presence across major wine-consuming states; CSD (Canteen Stores Dept) '
        'labels expanded from 5 to 9, with sales doubling YoY in Q2 FY26',
        '<b>Exports:</b> Sula exports to multiple countries; exports are a growing focus area',
        '<b>Promoter Holding:</b> 24.4% (as of Sep 2025) -- relatively low for an Indian listed company',
    ]
    for b in bullets:
        story.append(Paragraph(f'\u2022 {b}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: NSE India, CLSA (May 2024), Company Investor Presentation (sulavineyards.com), '
        'Business Standard, Screener.in',
        source_style
    ))

    story.append(PageBreak())

    # ========== SECTION 2: FUNDAMENTAL ANALYSIS ==========
    story.append(Paragraph('2. Fundamental Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Compounded Growth (Screener.in, Consolidated)', subheading_style))
    growth_data = [
        ['Metric', '3Y', '5Y', 'TTM'],
        ['Sales Growth', '11%', '3.6%', '~2%'],
        ['Profit Growth', 'N/A', 'N/A', '-24.8%'],
        ['Stock Price CAGR', '-51.4% (3Y)', '-', '-47.5% (1Y)'],
        ['ROE', '~14%', '~12%', '11.97%'],
    ]
    growth_table = Table(growth_data, colWidths=[3.5*cm, 3*cm, 3*cm, 4*cm])
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
        '<b>Key Insight:</b> Sula has delivered <b>poor sales growth of 3.60% over the past 5 years</b> '
        '(Screener.in). The 3-year revenue CAGR of 11% is better but largely reflects a post-COVID base. '
        'TTM profit has declined 24.8% YoY in FY25. The stock has lost ~47.5% in the last 1 year and '
        '~51.4% over 3 years, severely underperforming the Nifty and Nifty FMCG indices. '
        'This reflects both fundamental deceleration and valuation de-rating.',
        callout_red
    ))
    story.append(Paragraph(
        'CRITICAL: Sula\'s 5-year revenue CAGR of 3.6% significantly lags the Indian wine market CAGR of '
        '14-16% (IMARC/CRISIL), indicating market share erosion from new entrants like Fratelli, '
        'Grover Zampa, and imported wines. Despite being the dominant player '
        'with >50% share, Sula is growing at roughly one-quarter the market rate.',
        callout_red
    ))

    story.append(Paragraph('Annual P&L Summary (Consolidated)', subheading_style))
    annual_data = [
        ['Fiscal Year', 'Revenue (Rs Cr)', 'Net Profit (Rs Cr)', 'EPS (Rs)', 'NPM (%)'],
        ['FY22', '~455', '52.1', '6.6', '~11.5%'],
        ['FY23', '553.5', '84.0', '10.0', '15.2%'],
        ['FY24', '608.7', '93.3', '11.1', '15.3%'],
        ['FY25', '618.8', '~70.2', '8.3', '11.3%'],
        ['H1 FY26', '250.0', '~8.0', '~0.95', '~3.2%'],
    ]
    annual_table = Table(annual_data, colWidths=[2.5*cm, 3.3*cm, 3.3*cm, 2.2*cm, 2.2*cm])
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
    ]))
    story.append(annual_table)
    story.append(Paragraph(
        'Sources: Screener.in (consolidated), Business Standard, Equitymaster. '
        'FY22 revenue estimated from growth data. H1 FY26 = Q1+Q2 FY26 from quarterly reports.',
        source_style
    ))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph('Quarterly Revenue & Profit Trend', subheading_style))
    story.append(Image(chart_paths['revenue'], width=16*cm, height=8*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Margin Trend', subheading_style))
    story.append(Paragraph(
        'EBITDA margin contracted sharply from 33.4% in FY24 to 27.7% in FY25 (-570 bps YoY). '
        'Q1 FY26 saw the worst margin at 15.5%, recovering to 19.9% in Q2 FY26. Management has '
        'guided for 250 bps margin recovery in H2 FY26 driven by improved mix, cost normalization, '
        'and wine tourism momentum. The seasonal nature of the wine business (Q3 being strongest due to '
        'festive season) means margins fluctuate significantly across quarters.',
        body_style
    ))
    story.append(Image(chart_paths['margins'], width=14*cm, height=7*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Segment Performance', subheading_style))
    story.append(Paragraph(
        '<b>Wine Tourism</b> has been the consistent bright spot, delivering record revenue in '
        'every recent quarter. FY25 wine tourism revenue was Rs 60.3 Cr (+10.2% YoY vs Rs 54.7 Cr in FY24). '
        'H1 FY26 tourism revenue was Rs 26.9 Cr (+14.5% YoY). The third resort (The Haven by Sula) '
        'launched in Oct 2025 with 30 keys and a convention center, expanding capacity by 50%. '
        'Resort occupancy improved to 77% in Q2 FY26 (up from 74% YoY).',
        body_style
    ))
    story.append(Paragraph(
        '<b>Own Brands</b> have been under pressure. Revenue from own brands declined 2.5% in Q2 FY26, '
        'with Elite &amp; Premium brands declining 3% while maintaining a 78% mix. However, The Source '
        'range achieved double-digit growth and now forms 10% of own brands revenue. Excluding Telangana '
        'disruption, own brand sales grew mid-single digits YoY.',
        body_style
    ))
    story.append(Image(chart_paths['segments'], width=12*cm, height=9*cm))

    story.append(Paragraph('Balance Sheet, Cash Flow & Working Capital', subheading_style))
    story.append(Paragraph(
        '<b>Balance Sheet (FY25, Consolidated):</b> ROCE: 13.2% (Screener.in, latest). Note: Some sources '
        'report higher ROCE (~25%) due to standalone vs consolidated differences. ROCE declined sharply '
        'from FY24 levels, reflecting continued '
        'deterioration into FY26. ROE declined to 11.97% from 17.0% in FY24. '
        'P/B ratio is 2.98x. Interest coverage ratio deteriorated to 4.0x in FY25 from 5.8x in FY24. '
        'Current ratio improved marginally to 1.4x.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Cash Flow (FY24, Consolidated):</b> Operating cash flow was Rs 121.2 Cr in FY24. '
        'Cash flow from investing was Rs -42.9 Cr. Net debt stood at Rs 350 Cr as of Sep 2025, '
        'up from Rs 315 Cr a year ago. Management has indicated capex for FY26 and FY27 will be '
        'Rs 30-35 Cr annually (maintenance only), as major expansions are complete.',
        body_style
    ))

    # Cash Flow Analysis Table
    cf_data = [
        ['Year', 'CFO (Rs Cr)', 'Capex (Rs Cr)', 'FCF (Rs Cr)', 'Cash Conv. (CFO/PAT)'],
        ['FY22', '87.5', 'Est. 30-40', 'Est. 50-55', '~115%'],
        ['FY23', '88-90', 'Est. 35-45', 'Est. 45-55', '~95%'],
        ['FY24', '121.2', 'Est. 40-50', 'Est. 70-80', '~120%'],
        ['FY25', '58.4', 'Est. 30-40', 'Est. 20-28', '~55%'],
    ]
    cf_table = Table(cf_data, colWidths=[2.2*cm, 2.8*cm, 2.8*cm, 2.8*cm, 4*cm])
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
        'Source: Screener.in, Equitymaster. FY25 CFO halved YoY -- a major red flag. '
        'Capex figures estimated; FCF directionally correct.',
        source_style
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>Working Capital Concern (Screener.in):</b> Debtor Days surged from 81 (FY23) to 148 (FY25). '
        'Inventory Days remain elevated at 877 (FY25). This indicates significant working capital stress. '
        'Working capital days increased from 61.5 to 92.2 days. '
        'This is a red flag suggesting aggressive revenue recognition or weakening collections, '
        'and is dragging ROCE and ROE lower even without major capex.',
        callout_red
    ))

    story.append(Paragraph('Shareholding Pattern (Sep 2025, Screener.in)', subheading_style))
    sh_data = [
        ['Category', 'Holding (%)', 'Details'],
        ['Promoters', '24.4%', 'Rajeev Samant (CEO/founder) is key promoter; low vs Indian avg'],
        ['DII (Domestic Inst.)', '18.1%', 'Mutual Funds hold 18.04% (as of Mar 2025, Groww)'],
        ['FII (Foreign Inst.)', '4.0%', 'Down from 7.96% (Mar 2025) -- FIIs reducing'],
        ['Public / Retail', '53.6%', 'Retail dominates holding; high free float'],
    ]
    sh_table = Table(sh_data, colWidths=[3.5*cm, 2.5*cm, 9.5*cm])
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
        '<b>Key Shift:</b> FIIs reduced from 7.96% (Mar 2025) to 4.0% (Sep 2025) -- a halving of '
        'foreign institutional interest over just two quarters. DIIs (led by mutual funds at 18%) have '
        'been the anchor, while retail/public holds over 53%. Promoter holding at 24.4% is notably low '
        'for an Indian company -- this is structural (founder-led, widely held) rather than a sign of insider selling.',
        body_style
    ))

    story.append(Paragraph('Cautionary Flags', subheading_style))
    story.append(Paragraph(
        '<b>Investors should note the following concerns:</b><br/>'
        '\u2022 <b>Debtor days surge:</b> Increased from 81 (FY23) to 148 (FY25) days (Screener.in), indicating '
        'weakening collections or channel stuffing risk. Inventory Days remain elevated at 877 (FY25).<br/>'
        '\u2022 <b>Working capital deterioration:</b> Working capital days rose from 61.5 to 92.2 days, '
        'dragging ROCE to 13.2% (TTM, Screener.in). Note: Some sources report higher ROCE (~25%) due to '
        'standalone vs consolidated differences.<br/>'
        '\u2022 <b>Profit decline:</b> FY25 net profit fell 24.8% YoY despite revenue being flat/up. '
        'H1 FY26 net profit of ~Rs 8 Cr is abysmal compared to H1 FY25 (~Rs 29 Cr).<br/>'
        '\u2022 <b>FIIs exiting:</b> Foreign institutional holding halved from 7.96% to 4.0% in 6 months.<br/>'
        '\u2022 <b>ICRA outlook revised to Negative:</b> Credit rating outlook moved from Stable to Negative, '
        'reflecting weakening financial metrics.<br/>'
        '\u2022 <b>Net debt increasing:</b> Rs 350 Cr (Sep 2025) vs Rs 315 Cr (Sep 2024) despite no major capex.',
        callout_red
    ))

    story.append(Paragraph(
        'Sources: Screener.in (consolidated), Business Standard, Equitymaster, Trendlyne, ICRA, Groww',
        source_style
    ))

    story.append(PageBreak())

    # ========== SECTION 3: TECHNICAL ANALYSIS ==========
    story.append(Paragraph('3. Technical Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Sula Vineyards has been in a sustained downtrend over the past 12 months, falling from ~Rs 370 '
        'to ~Rs 185 -- a decline of approximately 50%. The stock is trading near its 52-week low of Rs 180.15, '
        'far below the 52-week high of Rs 432.80. The 1-year return of -47.5% significantly underperforms '
        'both the Nifty 50 and the Nifty FMCG Index. The stock was recently upgraded from "Strong Sell" '
        'to "Sell" by MarketsMojo (Feb 1, 2026), reflecting marginal technical stabilization.',
        body_style
    ))

    story.append(Image(chart_paths['price'], width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Technical Signals', subheading_style))

    tech_data = [
        ['Indicator', 'Value', 'Signal'],
        ['50-Day MA', 'Rs 253.40', 'Price far below --> Strong Bearish'],
        ['200-Day SMA', 'Rs 283.39', 'Price far below --> Strong Bearish'],
        ['RSI (14)', '53.25', 'Neutral (neither oversold nor overbought)'],
        ['MACD', '-0.330', 'Sell signal (daily)'],
        ['ADX', 'Weak', 'Weak trend strength (monthly mildly bullish)'],
        ['Support Zone', 'Rs 180-195', '52-week low area, critical floor'],
        ['Resistance', 'Rs 224 / Rs 242', 'Needs breakout above for reversal signal'],
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
        '<b>Pattern:</b> The stock is trading below both its 50-day and 200-day moving averages, '
        'confirming the bearish trend. However, RSI at 53 is neutral (not oversold), and monthly '
        'indicators show early signs of bullish momentum. A sustained break above Rs 224-242 (first '
        'resistance levels) would be the earliest sign of trend reversal. Until then, the technical '
        'picture remains bearish. The stock is near the lower trend floor of Rs 217; a break below Rs 180 '
        'would indicate acceleration of the downtrend.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Investing.com, TradingView, Munafasutra, MarketsMojo (data as of early Feb 2026). '
        'Note: Price chart uses approximated monthly closes for illustration; actual intraday prices may vary.',
        source_style
    ))

    story.append(PageBreak())

    # ========== SECTION 4: SECTOR & COMPETITIVE CONTEXT ==========
    story.append(Paragraph('4. Sector & Competitive Context', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Indian Wine Market Overview', subheading_style))
    story.append(Paragraph(
        'The Indian wine market was valued at <b>USD 229 million in 2024</b> and is projected to reach '
        'USD 892 million by 2033, growing at a <b>CAGR of 16.3%</b> (IMARC Group). Alternative estimates '
        'range from 14.7% CAGR (Grand View Research) to 23.8% (Technavio). India\'s wine consumption is '
        'still nascent -- per capita consumption is a fraction of Western markets, providing a long structural '
        'runway. Key growth drivers include urbanization, rising disposable incomes, premiumization, and '
        'growing acceptance of wine in Indian food culture.',
        body_style
    ))
    story.append(Paragraph(
        'CLSA (May 2024) forecasts wine consumption in India will expand at <b>15% CAGR over the next 10 years</b> '
        'and projects Sula\'s revenue to enjoy a <b>20% CAGR between FY23-33</b>. They view Sula as the '
        'biggest beneficiary of this structural growth given its dominant 50%+ market share.',
        body_style
    ))

    story.append(Paragraph('India-EU FTA Impact on Wine', subheading_style))
    story.append(Paragraph(
        'The India-EU Free Trade Agreement includes wine provisions: a minimum import price (MIP) of '
        '\u20ac2.5/750ml bottle, with import duties phased down from ~75% initially to ~20-30% over 7-10 years. '
        'This could increase competition from imported European wines in the medium term, but the phased '
        'approach gives domestic players like Sula time to adapt. Sula\'s strategy includes distributing '
        'imported wines through its network, potentially turning the threat into an opportunity.',
        body_style
    ))

    story.append(Paragraph('Competitive Landscape & Peer Comparison', subheading_style))
    story.append(Paragraph(
        'Sula is the <b>only pure-play listed wine company in India</b>. Its closest wine competitors -- '
        'Fratelli Wines, Grover Zampa, and York -- are unlisted. For public market comparison, we use '
        'broader alcobev (alcoholic beverage) peers:',
        body_style
    ))

    peer_data = [
        ['Company', 'P/E (TTM)', 'Revenue', 'NPM (%)', 'Comment'],
        ['Sula Vineyards', '32.5x', 'Rs 619 Cr', '11.3%', 'Only listed Indian wine co; dominant share'],
        ['United Spirits', '57.7x', 'Rs 11,340 Cr', '11.5%', 'Diageo India; spirits leader'],
        ['Radico Khaitan', '97.3x', 'Rs 4,070 Cr', '10.8%', 'Premium spirits; rich valuation'],
        ['United Breweries', '117.3x', 'Rs 7,500 Cr', '5.5%', 'Kingfisher beer; Heineken-backed'],
        ['Allied Blenders', '68.6x', 'Rs 8,000 Cr', '~4%', 'Officer\'s Choice whisky'],
        ['AlcoBev Sector Median', '~96x', '--', '--', 'Sula trades at 66% discount'],
    ]
    pe_table = Table(peer_data, colWidths=[3*cm, 2.2*cm, 2.5*cm, 2*cm, 5.5*cm])
    pe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#edf2f7')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(pe_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Image(chart_paths['peers'], width=16*cm, height=6.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Valuation anomaly:</b> Sula trades at 32.5x P/E vs the alcobev sector median of ~96x -- a '
        '<b>66% discount</b> to peers. This discount reflects (a) smaller scale, (b) slower recent growth, '
        '(c) wine is a niche vs spirits/beer, and (d) declining profitability. However, it also means '
        'there is significant re-rating potential if growth reaccelerates.',
        body_style
    ))

    story.append(Paragraph('Nifty FMCG Index Performance', subheading_style))
    story.append(Paragraph(
        'The Nifty FMCG Index stands at ~50,918 (Feb 4, 2026) with a 52-week range of '
        '49,337-58,485. The index is trading near its 52-week low, indicating broad sector weakness. '
        'Sula\'s 47.5% decline in 1 year is significantly worse than the FMCG index (which has corrected '
        'modestly), confirming that Sula\'s underperformance is largely stock-specific, not sector-wide.',
        body_style
    ))

    story.append(Paragraph('Raw Material & Commodity Context', subheading_style))
    story.append(Paragraph(
        'Key input costs for wine production include grapes, glass bottles, corks, and packaging. '
        'Grape prices in India are influenced by weather patterns in Maharashtra and Karnataka. '
        'The alcobev sector broadly is seeing 8-10% revenue growth in FY26 (CRISIL), with profitability '
        'supported by stable input costs. For Sula specifically, the gross margin contraction of ~900 bps '
        'YoY in Q2 FY26 was driven by unfavorable product mix rather than raw material inflation. '
        'Glass bottle prices have been broadly stable. The India-EU FTA could increase competition from '
        'imported wines over the medium term (7-10 year duty phase-down).',
        body_style
    ))

    story.append(Paragraph(
        'Sources: IMARC Group (wine market), CLSA (May 2024), Screener.in, Smart-Investing.in (P/E data Feb 2026), '
        'CRISIL (alcobev sector), Nifty FMCG Index (NSE India), India-EU FTA analysis',
        source_style
    ))

    story.append(PageBreak())

    # ========== SECTION 5: VALUATION & ANALYST VIEWS ==========
    story.append(Paragraph('5. Valuation & Analyst Views', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Brokerage Target Prices', subheading_style))

    analyst_data = [
        ['Brokerage / Source', 'Target (Rs)', 'Rating', 'Key Thesis'],
        ['CLSA (May 2024)', '819', 'Buy', '20% rev CAGR FY23-33; 50%+ share; wine consumption 15% CAGR'],
        ['Consensus (5 analysts)', '264.80', 'Buy (3B/2H)', 'Avg of 5 analysts; high 285, low 249'],
        ['TradingView (4 analysts)', '289.50', 'Buy', 'Max 330, Min 268'],
        ['WalletInvestor (algo)', '297-351', 'Positive', 'Algorithmic 1-year forecast'],
    ]
    analyst_table = Table(analyst_data, colWidths=[3.5*cm, 2.5*cm, 2.2*cm, 7*cm])
    analyst_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(analyst_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Important note on CLSA target:</b> The CLSA target of Rs 819 was set in May 2024 when the stock '
        'was trading at ~Rs 525. Since then, the stock has fallen to Rs 185, FY25 results showed profit '
        'decline, and the credit outlook was revised to Negative. The CLSA target has likely been '
        'revised downward, but an updated report was not publicly available. The consensus target of '
        'Rs 265-290 from 5 analysts is more current and reflects the deteriorating fundamentals.',
        callout_red
    ))

    story.append(Paragraph(
        '<b>Implied Upside:</b> From Rs 185 (current), the consensus target of Rs 265 implies ~43% upside. '
        'Even the TradingView minimum estimate of Rs 268 implies +45% upside. '
        'However, of 5 analysts, only 3 recommend Buy and 2 recommend Hold -- sentiment is cautious.',
        callout_green
    ))

    story.append(Paragraph('Valuation Context', subheading_style))
    story.append(Paragraph(
        'At 32.5x trailing P/E, Sula trades at a significant discount to alcobev peers (median ~96x). '
        'This discount has widened considerably over the past year as fundamentals deteriorated. '
        'For the discount to narrow, Sula needs to demonstrate (a) revenue growth reacceleration beyond '
        'the 2-4% range, (b) margin recovery back toward 25%+ EBITDA margins, and (c) working capital '
        'improvement (reduction in debtor days from 148). If these improve, the P/E could re-rate toward '
        '50-60x. If not, the current discount is justified.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: CLSA (May 2024, via Business Standard/Zee Business), Investing.com (consensus Feb 2026), '
        'TradingView, Alpha Spread, WalletInvestor, MarketScreener',
        source_style
    ))

    story.append(PageBreak())

    # ========== SECTION 6: CATALYSTS, RISKS & CONCLUSION ==========
    story.append(Paragraph('6. Growth Catalysts & Risks', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Management Guidance (Q2 FY26 Earnings Call, Nov 11, 2025)', subheading_style))
    story.append(Paragraph(
        'Key forward-looking statements from the Q2 FY26 earnings call transcript '
        '(Yahoo Finance, GuruFocus):',
        body_style
    ))
    mgmt_points = [
        '<b>Margin Recovery:</b> Management expects <b>250 bps margin recovery in H2 FY26</b>, '
        'driven by improved mix, cost normalization, and wine tourism momentum.',
        '<b>CEO Quote:</b> Rajeev Samant stated: <i>"Looking ahead, Sula remains well-positioned to '
        'deliver improved operating profitability in the second half of FY26."</i> (Q2 FY26 earnings call)',
        '<b>Capex:</b> Guided at Rs 30-35 Cr annually for FY26 and FY27 -- maintenance capex only. '
        'Major expansion phase is complete.',
        '<b>Telangana Recovery:</b> The Telangana market (3rd largest) was disrupted due to retail license '
        'expiry. License auctions are proceeding, with supply transition to new holders in Dec 2025. '
        'Full recovery expected in H2 FY26.',
        '<b>Wine Tourism:</b> Record Q2 tourism revenue of Rs 13.2 Cr (+7.7% YoY). The Haven by Sula '
        '(third resort) launched Oct 2025, expanding resort capacity by 50%.',
        '<b>CSD Channel:</b> Sales more than doubled YoY in Q2 after label listings expanded from 5 to 9.',
        '<b>Maharashtra Recovery:</b> Key market returned to growth in Q2 FY26.',
    ]
    for mp in mgmt_points:
        story.append(Paragraph(f'\u2022 {mp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Growth Catalysts (Bull Case)', subheading_style))
    bull_points = [
        '<b>Structural Wine Market Growth:</b> Indian wine market growing at 14-16% CAGR (IMARC/Grand View). '
        'Sula, with 50%+ market share, is the primary beneficiary. Per-capita wine consumption in India '
        'is still a fraction of even Asian peers, providing decades of runway.',
        '<b>Wine Tourism Expansion:</b> Three operational resorts with rising occupancy. Wine tourism provides '
        'high-margin revenue (Rs 60+ Cr annually) and brand building that competitors cannot replicate.',
        '<b>Premiumization:</b> The Source range growing double-digit; Elite &amp; Premium at 78% of mix. '
        'Move up the value chain improves margins over time.',
        '<b>Low Valuation:</b> At 32.5x P/E (66% discount to peers), the stock has significant re-rating '
        'potential if fundamentals improve. Even modest earnings recovery could drive disproportionate returns.',
        '<b>CSD Channel &amp; Geographic Expansion:</b> Doubling of CSD sales and growth in 8 states including '
        'Haryana, UP, Rajasthan, and Puducherry indicate distribution gains.',
        '<b>Imported Wine Distribution:</b> India-EU FTA creates opportunity for Sula to distribute imported '
        'wines through its established network.',
    ]
    for bp in bull_points:
        story.append(Paragraph(f'\u2022 {bp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Risks (Bear Case)', subheading_style))
    bear_points = [
        '<b>Fundamental Deterioration:</b> FY25 net profit fell 24.8% YoY. H1 FY26 net profit of ~Rs 8 Cr '
        'vs ~Rs 29 Cr in H1 FY25 -- a 72% decline. This is not a valuation problem, it is an earnings problem.',
        '<b>Working Capital Deterioration:</b> Debtor days surged from 81 (FY23) to 148 (FY25). '
        'Inventory Days remain elevated at 877 (FY25). Working capital days '
        'from 61.5 to 92.2. This indicates significant working capital stress and raises questions about '
        'revenue quality.',
        '<b>Rising Debt:</b> Net debt of Rs 350 Cr (Sep 2025) is elevated for a company with TTM PAT of '
        '~Rs 49 Cr. Interest coverage has weakened to 4.0x.',
        '<b>FII Exodus:</b> Foreign institutional holding halved from 7.96% to 4.0% in 6 months. '
        'This reflects institutional loss of confidence.',
        '<b>ICRA Negative Outlook:</b> Credit rating outlook revised from Stable to Negative, signaling '
        'weakening credit metrics.',
        '<b>Import Competition:</b> India-EU FTA will gradually reduce duties on European wines from ~75% '
        'to 20-30% over 7-10 years, increasing competition in premium segments where Sula earns '
        'highest margins.',
        '<b>Cyclicality & Seasonal Dependence:</b> Wine is seasonal (Q3 = festive/wedding season). '
        'Weather impacts grape harvests. Urban consumption slowdown has directly impacted Sula.',
        '<b>Low Promoter Holding:</b> At 24.4%, the promoter stake provides limited downside protection '
        'from an insider conviction perspective.',
    ]
    for bp in bear_points:
        story.append(Paragraph(f'\u2022 {bp}', bullet_style))

    story.append(Paragraph(
        'Sources: Q2 FY26 Earnings Call (Yahoo Finance, GuruFocus, Nov 11, 2025), Screener.in, '
        'Business Standard, ICRA, CLSA, IMARC Group',
        source_style
    ))

    story.append(PageBreak())

    # ========== SECTION 7: CONCLUSION & VALUATION ==========
    story.append(Paragraph('7. Conclusion & 1-Year Outlook', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Sula Vineyards is a structurally well-positioned company in a nascent, fast-growing market '
        '(Indian wine at 14-16% CAGR). As the dominant player with 50%+ market share, a strong brand, '
        'and a unique wine tourism moat, the long-term thesis remains intact. However, the near-term '
        'fundamentals have deteriorated significantly: FY25 profit fell 25%, H1 FY26 profit collapsed '
        '72% YoY, working capital has ballooned, debt has risen, and FIIs have exited.',
        body_style
    ))
    story.append(Paragraph(
        'The stock has already corrected 50% from its highs, bringing the P/E down to 32.5x -- a rare '
        '66% discount to alcobev sector peers. The question is whether this is a value trap (fundamentals '
        'continue deteriorating) or a deep value opportunity (cyclical trough before recovery).',
        body_style
    ))

    story.append(Spacer(1, 0.3*cm))

    # Valuation Methodology
    story.append(Paragraph('Valuation Methodology: Forward EPS x P/E Multiple', subheading_style))
    story.append(Paragraph(
        'The scenario analysis below uses a <b>forward earnings-multiple approach</b>. '
        'This is not a DCF (discounted cash flow) model -- it is a heuristic based on projected '
        'EPS and an assumed P/E multiple for each scenario.',
        body_style
    ))

    story.append(Paragraph('<b>Step 1: Establish Current EPS</b>', body_style))
    eps_data = [
        ['Metric', 'Value', 'Source'],
        ['FY25 Net Profit', 'Rs 70.2 Cr (est.)', 'Screener.in / Business Standard'],
        ['TTM Net Profit', 'Rs ~49 Cr', 'Screener.in (as of Jan 2026)'],
        ['Market Cap', 'Rs ~1,510 Cr', 'Screener.in (Feb 2026)'],
        ['Price', 'Rs 185.39', 'NSE (Feb 4, 2026)'],
        ['Shares Outstanding', '8.44 Cr', 'Screener.in: Equity Capital Rs 17 Cr, FV Rs 2'],
        ['FY25 EPS', 'Rs 8.3', 'FY25 PAT ~70.2 / 8.44 Cr shares = Rs 8.32'],
        ['TTM EPS', 'Rs ~5.8', 'TTM Profit ~49 / 8.44 Cr shares = Rs 5.81'],
        ['Sanity Check: P/E', '185 / 5.8 = 31.9x', 'Close to Screener.in reported 32.5x; diff due to TTM date'],
    ]
    eps_table = Table(eps_data, colWidths=[3.5*cm, 4*cm, 7*cm])
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
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'Note: Shares outstanding = 8.44 Cr (Screener.in: Equity Capital Rs 17 Cr, Face Value Rs 2). '
        'P/E sanity check yields ~31.9x vs Screener.in reported 32.5x. Small difference due to TTM earnings '
        'computation date. We use the reported FY25 EPS of Rs 8.3 as our starting point.',
        source_style
    ))

    story.append(Paragraph('<b>Step 2: Project FY27E EPS by Scenario</b>', body_style))
    story.append(Paragraph(
        'Growth rate sources: 3-year projected revenue CAGR of 7% (Alpha Spread/consensus). '
        '3-year projected operating income CAGR of 13% (Alpha Spread). Management guides for 250 bps '
        'margin recovery. CLSA (May 2024) projects 20% revenue CAGR FY23-33 (long-term).',
        body_style
    ))

    proj_data = [
        ['', 'Bull', 'Base', 'Bear'],
        ['FY26E Profit Growth', '15% (margin recovery)', '0% (flat, weak H1)', '-15% (continued decline)'],
        ['FY26E EPS', 'Rs 8.3 x 1.15 = Rs 9.55', 'Rs 8.3 x 1.0 = Rs 8.30', 'Rs 8.3 x 0.85 = Rs 7.06'],
        ['FY27E Profit Growth', '20% (CLSA thesis)', '13% (consensus CAGR)', '-15% (further deterioration)'],
        ['FY27E EPS', 'Rs 9.55 x 1.20 = Rs 11.46', 'Rs 8.30 x 1.13 = Rs 9.38', 'Rs 7.06 x 0.85 = Rs 6.00'],
    ]
    proj_table = Table(proj_data, colWidths=[3.5*cm, 4.2*cm, 4.2*cm, 4.2*cm])
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

    story.append(Paragraph('<b>Step 3: Apply P/E Multiple --> Target Price</b>', body_style))
    story.append(Paragraph(
        'P/E assumptions anchored to alcobev sector comps (Feb 2026): Sula current 32.5x, United Spirits 58x, '
        'Radico 97x, sector median 96x. Given Sula\'s smaller scale and niche (wine vs spirits), we apply '
        'a discount to peer multiples. CLSA\'s implied valuation was ~70-75x when they had a Rs 819 target.',
        body_style
    ))

    scenario_data = [
        ['Scenario', 'FY27E EPS', 'P/E Assumed', 'Price Target', 'Return from Rs 185', 'Probability'],
        ['Bull', 'Rs 11.46', '40-45x',
         'Rs 458-516', '+148% to +179%', '20%'],
        ['Base', 'Rs 9.38', '30-35x',
         'Rs 281-328', '+52% to +77%', '40%'],
        ['Bear', 'Rs 6.00', '15-20x',
         'Rs 90-120', '-35% to -51%', '40%'],
    ]
    scenario_table = Table(scenario_data, colWidths=[1.8*cm, 2.2*cm, 2.3*cm, 2.8*cm, 3.3*cm, 2.5*cm])
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
        '<b>Bull (20%):</b> Requires strong margin recovery in H2 FY26, Telangana normalization, '
        'wine tourism record season, AND a re-rating toward peer multiples. Possible given CLSA\'s '
        'long-term thesis, but requires multiple factors to align. Lower probability than typical due to '
        'recent execution challenges.',
        '<b>Base (40%):</b> Sula delivers on management guidance of 250 bps margin '
        'recovery, revenue stabilizes, and earnings grow modestly from the depressed FY25/26 base. P/E stays '
        'in the 30-35x range -- still at a discount to peers but reflecting the current risk profile.',
        '<b>Bear (40%):</b> Weighted equally to Base because of specific, tangible risks: (a) debtor days at 148 '
        'suggest potential for write-offs or further deterioration, (b) net debt is rising while profits are '
        'falling, (c) FIIs are exiting in large numbers, (d) ICRA has turned negative on the outlook, '
        '(e) the India-EU FTA creates a medium-term competitive headwind, and (f) CFO halved in FY25, '
        'signaling cash generation is collapsing alongside earnings. Bear FY27E growth of -15% reflects '
        'continued deterioration, not just stagnation. The 50% stock decline in '
        '12 months shows this stock can fall significantly further.',
    ]
    for pp in prob_points:
        story.append(Paragraph(f'\u2022 {pp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    ev_data = [
        ['Scenario', 'Midpoint Price', 'Probability', 'Weighted Value'],
        ['Bull', 'Rs 487', '20%', 'Rs 97'],
        ['Base', 'Rs 305', '40%', 'Rs 122'],
        ['Bear', 'Rs 105', '40%', 'Rs 42'],
        ['', '', 'Expected Value -->', 'Rs 261'],
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
        '<b>Probability-weighted expected price: Rs 261</b> -- implying ~41% upside from Rs 185. '
        'However, this masks extreme variance: the bull case offers 148-179% upside while the bear case '
        'implies -35% to -51% downside. The bear case at 40% probability (equal to base) reflects the '
        'severity of current deterioration: CFO halved, debtor days surging, FIIs fleeing. '
        'Investors should be aware of the wide dispersion of outcomes and the real possibility of '
        'further significant downside.',
        callout_red
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
        'with segment-level revenue build-up (wine business + tourism), margin assumptions, capex '
        'forecasting, and WACC-based discounting. This report does not include one.',
        '<b>P/E assumptions are subjective:</b> The choice of 30-35x for base vs 20-25x for bear is '
        'anchored to sector comps but remains a judgment call. Sula has limited direct peers (only listed '
        'wine company), making P/E anchoring inherently imprecise.',
        '<b>EPS estimates are top-down:</b> Growth rates are sourced from consensus (Alpha Spread, CLSA) '
        'rather than built from a bottoms-up P&L forecast by segment (wine + tourism).',
        '<b>Probability weights are subjective:</b> The 20/40/40 split is an informed estimate based '
        'on current evidence (deteriorating fundamentals, rising debt, FII exit, ICRA negative outlook, '
        'CFO halving). The bear case is weighted at 40% (equal to base) due to the severity and number '
        'of specific risk factors.',
        '<b>Cash flow quality not captured:</b> Given the ballooning debtor days (148) and rising debt, '
        'an EV/FCF or DCF approach would likely produce a more conservative valuation than the P/E method.',
        '<b>CLSA target dated:</b> The CLSA Rs 819 target (May 2024) predates the FY25 earnings decline, '
        'the ICRA negative outlook, and the 50% stock fall. It is likely stale.',
    ]
    for lp in limit_points:
        story.append(Paragraph(f'\u2022 {lp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Verdict', subheading_style))
    story.append(Paragraph(
        '<b>Sula Vineyards is a high-quality franchise in a structurally growing market, currently '
        'experiencing its worst financial performance since the COVID era.</b> The 50% stock decline '
        'has brought the valuation to 34x P/E -- a steep discount to peers and potentially attractive '
        'for long-term investors. However, the near-term fundamentals are weak: profit is collapsing, '
        'working capital is deteriorating, debt is rising, and institutional investors are leaving.',
        body_style
    ))
    story.append(Paragraph(
        'The <b>probability-weighted expected value of Rs 261 implies ~41% upside</b> over 12 months. '
        'However, this is heavily skewed by the bull case; the bear case alone (40% probability) implies '
        'Rs 90-120, which is -35% to -51% downside. The consensus analyst target of Rs 265-290 is more '
        'optimistic than our expected value, reflecting their lower bear-case weighting.',
        body_style
    ))
    story.append(Paragraph(
        'The <b>bear case at 40% probability is equal to the base case</b>, reflecting genuine risks: '
        'debtor days at 148 (vs 81 in FY23), net debt of Rs 350 Cr on Rs 49 Cr TTM PAT, ICRA negative '
        'outlook, FII holdings halving, and CFO halving from Rs 121 Cr to Rs 58 Cr. The Q3 FY26 results '
        '(due Feb 6, 2026) will be critical -- a strong Q3 (which is seasonally the best quarter) could '
        'restore confidence; a weak one could trigger further selling.',
        body_style
    ))
    story.append(Paragraph(
        '<b>On balance, this is a turnaround/deep value opportunity for risk-tolerant investors with a '
        '12+ month horizon. The structural wine market growth story (14-16% CAGR) and Sula\'s dominant '
        'market position provide a floor. But near-term earnings visibility is poor, and the balance sheet '
        'needs watching. Monitor Q3 FY26 results (Feb 6, 2026), debtor days trend, and FII flows before '
        'committing capital. Not suitable for conservative portfolios or investors seeking near-term earnings certainty.</b>',
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
        'in Sula Vineyards Limited.',
        disclaimer_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Data Sources:</b> Screener.in (primary, consolidated) | NSE India | '
        'Yahoo Finance (earnings call transcripts) | Business Standard | '
        'Trendlyne | Investing.com | TradingView | MarketScreener | '
        'IMARC Group (wine market) | Grand View Research | Technavio | '
        'CLSA (May 2024) | CRISIL (alcobev sector) | GuruFocus | '
        'Smart-Investing.in (peer P/E data) | MarketsMojo | '
        'Equitymaster (annual report analysis) | ICRA | '
        'Company Investor Presentation (sulavineyards.com)',
        source_style
    ))

    doc.build(story)
    print(f"PDF generated successfully: {FINAL_PDF}")


# --- Main ---
if __name__ == '__main__':
    print("Generating charts...")
    charts = {
        'revenue': create_revenue_chart(),
        'segments': create_segment_chart(),
        'price': create_price_chart(),
        'peers': create_peer_chart(),
        'margins': create_margin_chart(),
    }
    print("Charts created. Building PDF...")
    build_pdf(charts)
    print("Done!")
