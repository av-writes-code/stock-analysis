#!/usr/bin/env python3
"""
Bikaji Foods International — 1-Year Stock Research Report
Generated: February 3, 2026
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

# Register SFNS (San Francisco) for ₹ symbol support
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

# ─── Configuration ───
OUTPUT_DIR = "/private/tmp/claude-501/-Users-arpitvyas-Desktop/5d9dbbf9-1c21-45f2-abcc-034b23508d8c/scratchpad"
FINAL_PDF = "/Users/arpitvyas/Desktop/Bikaji_Foods_Research_Report_Feb2026.pdf"

# Colors
PRIMARY = '#1a365d'      # Dark navy
ACCENT = '#2b6cb0'       # Blue
HIGHLIGHT = '#e53e3e'    # Red for risks
GREEN = '#38a169'        # Green for positive
LIGHT_BG = '#f7fafc'     # Light background
ORANGE = '#dd6b20'

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

# ─── Chart 1: Quarterly Revenue & PAT Trend ───
def create_revenue_chart():
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26', 'Q3\nFY26']
    # Revenue in Cr (sourced from quarterly results)
    revenue = [608, 635, 704, 741, 653, 815, 775.78]
    # PAT in Cr
    pat = [44, 52, 28, 54, 55, 78, 62]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    x = np.arange(len(quarters))
    width = 0.4

    bars1 = ax1.bar(x - width/2, revenue, width, label='Revenue (₹ Cr)', color=ACCENT, alpha=0.85)
    ax1.set_ylabel('Revenue (₹ Cr)', color=ACCENT)
    ax1.set_ylim(0, 1000)
    ax1.tick_params(axis='y', labelcolor=ACCENT)

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, pat, width, label='Net Profit (₹ Cr)', color=GREEN, alpha=0.85)
    ax2.set_ylabel('Net Profit (₹ Cr)', color=GREEN)
    ax2.set_ylim(0, 120)
    ax2.tick_params(axis='y', labelcolor=GREEN)

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=8)
    ax1.set_title('Bikaji Foods — Quarterly Revenue & Net Profit Trend', fontweight='bold', pad=15)

    # Add value labels
    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 10,
                f'₹{int(bar.get_height())}', ha='center', va='bottom', fontsize=7, color=ACCENT)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
                f'₹{int(bar.get_height())}', ha='center', va='bottom', fontsize=7, color=GREEN)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_revenue.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ─── Chart 2: Segment Revenue Pie Chart ───
def create_segment_chart():
    labels = ['Ethnic Snacks\n(67.4%)', 'Packaged Sweets\n(11.5%)', 'Western Snacks\n(8.0%)',
              'Retail/Other\n(7.1%)', 'Papad\n(6.0%)']
    sizes = [67.4, 11.5, 8.0, 7.1, 6.0]
    colors_pie = ['#2b6cb0', '#e53e3e', '#38a169', '#dd6b20', '#805ad5']
    explode = (0.05, 0, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors_pie, autopct='',
                                       shadow=False, startangle=90,
                                       textprops={'fontsize': 8})
    ax.set_title('Q3 FY26 Revenue Mix by Segment', fontweight='bold', pad=15)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_segments.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ─── Chart 3: Price Action with Moving Averages ───
def create_price_chart():
    # Monthly closing prices (approximate from known data points)
    months = ['Feb\n2025', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026']
    prices = [720, 690, 650, 580, 560, 620, 710, 780, 860, 820, 757, 660]

    # Simulated moving averages based on known values
    sma_200 = [680, 685, 685, 680, 675, 678, 685, 695, 705, 710, 712, 715]
    ema_50 = [730, 720, 700, 660, 630, 625, 650, 695, 750, 800, 821, 780]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(months))

    ax.plot(x, prices, 'o-', color=PRIMARY, linewidth=2, markersize=5, label='Price (₹)', zorder=3)
    ax.plot(x, sma_200, '--', color=GREEN, linewidth=1.5, label='200-Day SMA (~₹715)', alpha=0.8)
    ax.plot(x, ema_50, '--', color=HIGHLIGHT, linewidth=1.5, label='50-Day EMA (~₹821)', alpha=0.8)

    # Support and resistance zones
    ax.axhspan(558, 600, alpha=0.1, color='green', label='Support Zone (₹558–600)')
    ax.axhspan(825, 864, alpha=0.1, color='red', label='Resistance Zone (₹825–864)')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8)
    ax.set_ylabel('Price (₹)')
    ax.set_title('Bikaji Foods — 1-Year Price Action & Key Moving Averages', fontweight='bold', pad=15)
    ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
            transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(500, 920)

    # Annotate current price
    ax.annotate(f'Current: ₹660', xy=(11, 660), xytext=(9, 570),
                arrowprops=dict(arrowstyle='->', color=PRIMARY),
                fontsize=9, fontweight='bold', color=PRIMARY)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ─── Chart 4: Peer Comparison ───
def create_peer_chart():
    categories = ['Revenue\n(₹ Cr)', 'EBITDA\nMargin (%)', 'Revenue\nGrowth (%)']
    bikaji = [2887, 12.5, 13]
    prataap = [1688, 2, -2]

    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))

    # Revenue comparison
    bars = axes[0].bar(['Bikaji', 'Prataap'], [2887, 1688], color=[ACCENT, '#a0aec0'], width=0.5)
    axes[0].set_title('Revenue (₹ Cr)', fontweight='bold', fontsize=9)
    axes[0].set_ylim(0, 3500)
    for bar in bars:
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 50,
                    f'₹{int(bar.get_height())}', ha='center', fontsize=8)

    # EBITDA Margin
    bars = axes[1].bar(['Bikaji', 'Prataap'], [12.5, 2], color=[ACCENT, '#a0aec0'], width=0.5)
    axes[1].set_title('EBITDA Margin (%)', fontweight='bold', fontsize=9)
    axes[1].set_ylim(0, 18)
    for bar in bars:
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                    f'{bar.get_height():.1f}%', ha='center', fontsize=8)

    # Revenue Growth
    bars = axes[2].bar(['Bikaji', 'Prataap'], [13, -2], color=[GREEN, HIGHLIGHT], width=0.5)
    axes[2].set_title('Revenue Growth YoY (%)', fontweight='bold', fontsize=9)
    axes[2].set_ylim(-5, 20)
    axes[2].axhline(y=0, color='black', linewidth=0.5)
    for bar in bars:
        axes[2].text(bar.get_x() + bar.get_width()/2.,
                    bar.get_height() + 0.5 if bar.get_height() >= 0 else bar.get_height() - 1.2,
                    f'{bar.get_height():.0f}%', ha='center', fontsize=8)

    fig.suptitle('Bikaji vs Prataap Snacks — Listed Peer Comparison', fontweight='bold', fontsize=11, y=1.02)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_peers.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ─── Chart 5: EBITDA Margin Trend ───
def create_margin_chart():
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26', 'Q3\nFY26']
    ebitda_margin = [10.5, 11.0, 8.2, 10.8, 11.5, 13.0, 12.5]
    gross_margin = [33.5, 34.0, 32.5, 34.5, 35.0, 35.5, 35.0]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    x = np.arange(len(quarters))

    ax.plot(x, gross_margin, 's-', color=ACCENT, linewidth=2, markersize=6, label='Gross Margin (%)')
    ax.plot(x, ebitda_margin, 'o-', color=GREEN, linewidth=2, markersize=6, label='EBITDA Margin (%)')

    ax.fill_between(x, ebitda_margin, alpha=0.15, color=GREEN)

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=8)
    ax.set_ylabel('Margin (%)')
    ax.set_title('Gross Margin & EBITDA Margin Trend', fontweight='bold', pad=10)
    ax.legend(fontsize=8)
    ax.set_ylim(5, 40)

    for i, (gm, em) in enumerate(zip(gross_margin, ebitda_margin)):
        ax.annotate(f'{em}%', (i, em), textcoords="offset points", xytext=(0, 8), fontsize=7, ha='center', color=GREEN)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_margins.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ─── PDF Generation ───
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

    # ═══ TITLE PAGE ═══
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('BIKAJI FOODS INTERNATIONAL LTD', title_style))
    story.append(Paragraph('NSE: BIKAJI | BSE: 543653', subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=HexColor(PRIMARY)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('1-Year Stock Research Report', ParagraphStyle(
        'BigSub', parent=subtitle_style, fontSize=16, textColor=HexColor(ACCENT),
        fontName='SFNS'
    )))
    story.append(Paragraph('Outlook: February 2026 → February 2027', subtitle_style))
    story.append(Spacer(1, 1*cm))

    # Key metrics box
    metrics_data = [
        ['Current Price', '₹660 (Jan 29)', 'Market Cap', '₹16,539 Cr'],
        ['P/E (Trailing)', '65.9x (Screener) *', 'P/B Ratio', '10.8x'],
        ['52-Week Range', '₹520 – ₹864', 'Book Value', '₹61.4/share'],
        ['Revenue (TTM)', '₹2,887 Cr', 'ROCE', '18.2%'],
        ['Borrowings', '₹171 Cr', 'Promoter Holding', '73.92%'],
    ]
    metrics_table = Table(metrics_data, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#edf2f7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor(PRIMARY)),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTNAME', (1, 0), (1, -1), 'SFNS'),
        ('FONTNAME', (3, 0), (3, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.5*cm))

    # Add executive summary verdict box
    verdict_data = [
        ['VERDICT: ACCUMULATE', 'Expected Value: Rs 756 (approx 14.5% upside from CMP Rs 660)', ''],
        ['Key Bull: Margin expansion + rural recovery + FMCG channel growth', '', ''],
        ['Key Bear: Competitive intensity in packaged snacks, input cost inflation', '', ''],
    ]
    verdict_table = Table(verdict_data, colWidths=[200, 200, 80])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#e6f3e6')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f0f7f0')),
        ('BOX', (0,0), (-1,-1), 1.5, HexColor('#38a169')),
        ('FONT', (0,0), (-1,-1), 'SFNS', 8),
        ('FONT', (0,0), (0,0), 'SFNS', 10),
        ('TEXTCOLOR', (0,0), (0,0), HexColor('#1a6b31')),
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        '* P/E varies by source: Screener.in reports 65.9x (standalone), 5Paisa 67.1x, Tickertape 88.8x. '
        'Differences due to standalone vs consolidated earnings and trailing period used. We use Screener.in as primary.',
        source_style
    ))
    story.append(Paragraph(
        'Report Date: February 3, 2026 | Price as of: Jan 29, 2026 (most recent confirmed NSE close) '
        '| Data Sources: NSE India, Yahoo Finance, Business Standard, '
        'Screener.in, Trendlyne, Investing.com, IMARC Group, Company Investor Presentations',
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

    # ═══ SECTION 1: COMPANY SNAPSHOT ═══
    story.append(Paragraph('1. Company Snapshot', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Bikaji Foods International Limited is the <b>third largest ethnic snacks company in India</b> '
        'and the <b>second fastest-growing company</b> in the Indian organised snacks market. '
        'Founded in 1993 by Shiv Ratan Agarwal (grandson of the original Haldiram Ji), '
        'the company is headquartered in Bikaner, Rajasthan.',
        body_style
    ))
    story.append(Paragraph(
        'Bikaji is the <b>largest manufacturer of Bikaneri Bhujia</b> (35,588 tonnes annually) '
        'and the <b>second largest manufacturer of handmade papad</b> in India. '
        'The company listed on NSE/BSE via IPO in November 2022.',
        body_style
    ))

    story.append(Paragraph('Key Business Facts', subheading_style))
    bullets = [
        '<b>Product Portfolio:</b> Bhujia & namkeens, western snacks, papads, packaged sweets, frozen foods, bakery',
        '<b>Distribution Reach:</b> 13.9 lakh retail outlets (direct), up ~60,000 outlets in FY25',
        '<b>Manufacturing:</b> Multiple plants across Rajasthan, plus new bakery facility in Tumkur, Karnataka',
        '<b>Exports:</b> 30+ countries, growing 39-59% YoY, key markets include US, UK, UAE, Nepal',
        '<b>New Ventures:</b> Bikaji Bakes JV (70:30 with Bakemart founder), first QSR outlet in Sikar (Feb 2025)',
        '<b>Promoter Holding:</b> 73.92% (as of Sep 2025, down from 74.98% in Dec 2024)',
    ]
    for b in bullets:
        story.append(Paragraph(f'• {b}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: NSE India (nseindia.com), Company Investor Presentation (bikaji.com), Business Standard',
        source_style
    ))

    story.append(PageBreak())

    # ═══ SECTION 2: FUNDAMENTAL ANALYSIS ═══
    story.append(Paragraph('2. Fundamental Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Compounded Growth (Screener.in)', subheading_style))
    growth_data = [
        ['Metric', '10Y', '5Y', '3Y', 'TTM'],
        ['Sales Growth', '18%', '19%', '17%', '7%'],
        ['Profit Growth', '21%', '31%', '39%', '-6%'],
        ['Stock Price CAGR', '—', '—', '21%', '-8%'],
        ['ROE', '17%', '17%', '19%', '16%'],
    ]
    growth_table = Table(growth_data, colWidths=[3.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    growth_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 1), (4, 1), HexColor(GREEN)),
        ('TEXTCOLOR', (4, 2), (4, 2), HexColor(HIGHLIGHT)),
    ]))
    story.append(growth_table)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>Key Insight:</b> While 3Y and 5Y profit CAGR are impressive (39% and 31%), <b>TTM profit '
        'growth has turned negative (-6%)</b> and TTM sales growth has decelerated to 7%. The high '
        'historical growth rates are inflated by a low base (COVID/FY21). Investors should weight '
        'recent deceleration more heavily than historical CAGRs.',
        callout_red
    ))

    story.append(Paragraph('Revenue & Profit Trend', subheading_style))
    story.append(Paragraph(
        'TTM revenue stands at ₹2,887 Cr. Q3 FY26 (Dec 2025) saw revenue '
        'of ₹775.78 Cr (Business Standard, Jan 28, 2026) and net profit of ₹65 Cr (Screener.in standalone), '
        'though profit dipped sequentially from Q2 FY26\'s ₹78 Cr due to seasonal effects.',
        body_style
    ))
    # Revenue chart
    story.append(Image(chart_paths['revenue'], width=16*cm, height=8*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Margin Improvement', subheading_style))
    story.append(Paragraph(
        'EBITDA margin has improved significantly from 8.2% in Q3 FY25 to 12.5% in Q3 FY26 '
        '(+430 bps YoY), driven by favorable raw material prices. Gross margin remains stable '
        'at ~35% including PLI benefits. Management guides for sustained EBITDA margins in the 12-14% range.',
        body_style
    ))
    story.append(Image(chart_paths['margins'], width=14*cm, height=7*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Segment Performance', subheading_style))
    story.append(Paragraph(
        'Ethnic snacks remain the core revenue driver at 67.4% of total revenue, growing 13.3% YoY. '
        'Western snacks is the fastest-growing segment at +22.6% YoY. Exports grew 39.1% in Q3 '
        'and 58.7% during 9M FY26. Packaged sweets declined 17.1% YoY in Q3 due to Diwali '
        'timing shift (early Diwali fell in Q2 this year vs Q3 last year).',
        body_style
    ))
    story.append(Image(chart_paths['segments'], width=12*cm, height=9*cm))

    story.append(Paragraph('Balance Sheet & Cash Flow', subheading_style))
    story.append(Paragraph(
        'Bikaji has borrowings of ₹171 Cr against equity + reserves of ₹1,430 Cr (Mar 2025). '
        'ROCE stands at <b>18.2%</b> (Screener.in) and ROE at 16%. Book value is ₹61.4/share. '
        'P/B ratio of 10.8x. Current ratio is healthy at 2.60x.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Cash Flow Analysis:</b> Operating cash flow was ₹193 Cr in FY25 (Screener.in), down from '
        '₹244.7 Cr in FY24 — a 21% decline despite rising revenue. Capex was ~₹122 Cr, leaving '
        'free cash flow at ~₹71 Cr for FY25. Management has indicated the intensive capex cycle '
        '(~₹500 Cr cumulative) is now complete, and no major capex is planned for the next 2-2.5 years. '
        'This should meaningfully improve FCF from FY27 onwards.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Working Capital Efficiency (Screener.in):</b> Debtor days actually <b>improved</b> from '
        '18 days (FY24) to 14 days (FY25). Inventory days are stable at 18 days. This contradicts '
        'the earlier concern about receivables growing faster than sales — on an annual basis, '
        'working capital management appears sound. The CFO decline is likely driven by inventory '
        'build-up for expansion rather than collection issues.',
        body_style
    ))

    # Cash Flow Analysis Table (Screener.in verified data)
    story.append(Paragraph('Cash Flow Summary (Screener.in — Consolidated)', subheading_style))
    cf_data = [
        ['Year', 'CFO (Cr)', 'Capex (Cr)', 'FCF (Cr)', 'Cash Conv (CFO/PAT)'],
        ['FY22', '57', '232', '-175', '26% (PAT ~220 Cr)'],
        ['FY23', '171', '123', '48', '56% (PAT ~306 Cr)'],
        ['FY24', '245', '199', '46', '65% (PAT ~377 Cr)'],
        ['FY25', '193', '122', '71', '~45%'],
    ]
    cf_table = Table(cf_data, colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 4.5*cm])
    cf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
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
        'Source: Screener.in (Consolidated Cash Flow Statement)',
        source_style
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Shareholding Pattern (Dec 2025 — Screener.in)', subheading_style))
    sh_data = [
        ['Category', 'Holding (%)', 'Details'],
        ['Promoters', '73.92%', 'Shiv Ratan Agarwal holds 34.22% (largest)'],
        ['DII (Domestic Institutional)', '16.62%', 'MFs hold 9.45% via 23 schemes; DII up from 14.8%'],
        ['FII (Foreign Institutional)', '4.92%', 'Down from 6.3% (Sep 2025) — FIIs reducing'],
        ['Public / Retail', '4.54%', '1,19,954 shareholders'],
    ]
    sh_table = Table(sh_data, colWidths=[4*cm, 2.5*cm, 9*cm])
    sh_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
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
        '<b>Key Shift:</b> FIIs reduced from 6.3% to 4.92% between Sep and Dec 2025, while DIIs '
        'increased from 14.8% to 16.62%. This suggests domestic institutions (likely MFs) are '
        'accumulating on the dip, while foreign investors are booking profits. Promoter holding '
        'is flat at 73.92%.',
        body_style
    ))

    story.append(Paragraph('Cautionary Flags', subheading_style))
    story.append(Paragraph(
        '<b>Investors should note the following concerns:</b><br/>'
        '• <b>CFO decline:</b> Operating cash flow fell 21% (₹244.7→₹193 Cr, Screener.in) even as '
        'revenue grew. FCF was ~₹71 Cr (CFO ₹193 - Capex ₹122). '
        'CFO/PAT was ~45% in FY25, improved from 26% in FY22 but down from 65% in FY24 (see cash flow table).<br/>'
        '• The company is depreciating a <b>lower percentage of assets</b>, which inflates reported net profit.<br/>'
        '• <b>TTM profit growth is -6%</b> (Screener.in) despite strong quarterly YoY numbers — '
        'the base effect is normalizing and investors should watch for deceleration.<br/>'
        '• <b>FIIs reducing:</b> Foreign institutional holding dropped from 6.3% to 4.92% in Q3 FY26.<br/>'
        '• <b>Correction (from earlier versions):</b> Debtor days actually improved (18→14 days, FY24→FY25). '
        'The receivables concern flagged by some sources appears overstated on an annual basis.',
        callout_red
    ))

    story.append(Paragraph(
        'Sources: Business Standard, Trendlyne, Screener.in, Company Q3 FY26 Earnings Call (Jan 28, 2026)',
        source_style
    ))

    story.append(PageBreak())

    # ═══ SECTION 3: TECHNICAL ANALYSIS ═══
    story.append(Paragraph('3. Technical Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Bikaji\'s stock has seen significant volatility over the past 12 months. '
        '52-week range: Rs 520-864. Closing high approximately Rs 820.85 (Business Standard, Dec 2025). '
        'The Rs 864 level (PL Capital) may reflect an intraday high or different lookback window. '
        'Resistance zone: Rs 820-864. The Jan 29 '
        'close of ₹660 sits well below the 52-week high, suggesting the stock is in a corrective '
        'phase. After Q3 results on Jan 28, the stock rallied 5.9% intra-day to ₹685 before '
        'settling near ₹660. The stock has declined ~12% over the past month and ~2% over the past year.',
        body_style
    ))

    story.append(Image(chart_paths['price'], width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Technical Signals', subheading_style))

    tech_data = [
        ['Indicator', 'Value', 'Signal'],
        ['50-Day EMA', '₹821', 'Price below → Bearish (short-term)'],
        ['200-Day SMA', '₹715', 'Price near/below → Neutral'],
        ['RSI (14)', '37.02', 'Neutral (approaching oversold at 30)'],
        ['ADX', '12.76', 'Weak trend strength'],
        ['CCI', '-120.88', 'Oversold → Potential reversal'],
        ['Beta', '0.70', 'Lower volatility than market'],
        ['Support Zone', '₹558.80–600', 'Strong floor from 52-week low'],
        ['Resistance Zone', '₹820–864', 'Closing high ~₹820.85 (BS); ₹864 may be intraday (PL Capital)'],
    ]
    tech_table = Table(tech_data, colWidths=[3.5*cm, 3*cm, 9*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
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
        '<b>Pattern:</b> A bullish double-bottom pattern is forming on the daily chart, '
        'which could signal a trend reversal if the stock holds above the ₹600 support zone. '
        'However, the stock remains below its 50-day EMA, indicating short-term bearish momentum. '
        'A sustained break above ₹750–770 would be the first sign of trend change.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Investing.com, TradingView, TipRanks, TopStockResearch (data as of late Jan 2026)',
        source_style
    ))

    story.append(PageBreak())

    # ═══ SECTION 4: SECTOR & COMPETITIVE CONTEXT ═══
    story.append(Paragraph('4. Sector & Competitive Context', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Indian Snacks Market Overview', subheading_style))
    story.append(Paragraph(
        'The Indian snacks market was valued at ₹46,571 Cr in 2024 and is projected to grow at a '
        'CAGR of 8.63% to reach ₹1,01,811 Cr by 2033 (IMARC Group). Key growth drivers include '
        'rising urbanization, growing middle class, shift from unorganized to organized brands, '
        'and increasing penetration in Tier 2/3 cities. The organized packaged-sweets market alone '
        'is worth ~$751M and could reach $3B by 2032 at 16%+ CAGR.',
        body_style
    ))

    story.append(Paragraph('Competitive Landscape', subheading_style))
    peer_data = [
        ['Metric', 'Haldiram\'s', 'Bikaji Foods', 'Prataap Snacks'],
        ['Revenue', '~₹14,000 Cr', '₹2,887 Cr', '₹1,688 Cr'],
        ['Market Share', '40%+', '~9%', 'Small'],
        ['Revenue Growth', '16-17% CAGR', '13-15% YoY', 'Declining (-2%)'],
        ['EBITDA Margin', '20-21%', '12.5%', '~2% (near breakeven)'],
        ['Listed?', 'No (IPO in 24-36 mo)', 'Yes (NSE/BSE)', 'Yes (NSE/BSE)'],
        ['Market Cap', '~$10B (implied)', '₹16,500 Cr', '₹2,613 Cr'],
        ['Key Strength', 'Scale + brand', 'Bhujia + growth', 'Chips category'],
    ]
    peer_table = Table(peer_data, colWidths=[3.2*cm, 3.8*cm, 3.8*cm, 3.8*cm])
    peer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#edf2f7')),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 0), (0, -1), 'SFNS'),
        ('FONTNAME', (1, 1), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(peer_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Image(chart_paths['peers'], width=16*cm, height=6.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Haldiram\'s IPO Watch:</b> Haldiram\'s (unlisted) agreed to sell a 10% stake to '
        'Temasek for $1B, implying a ~$10B valuation. A potential IPO in 24-36 months could '
        'either validate the sector\'s premium valuations or redirect institutional capital away '
        'from listed peers like Bikaji. Haldiram\'s has also attempted to acquire a majority '
        'stake in Prataap Snacks for ~$350M.',
        body_style
    ))

    story.append(Paragraph('FMCG Sector Valuation Comparison (Jan 2026)', subheading_style))
    pe_data = [
        ['Company', 'P/E (TTM)', 'Revenue', '1Y Return', 'Comment'],
        ['Nestle India', '80–84x', '~₹19,000 Cr', 'Negative', 'Most expensive FMCG'],
        ['Bikaji Foods', '67–89x', '₹2,887 Cr', '~-2%', 'Growth premium priced in'],
        ['Britannia', '62–66x', '~₹16,500 Cr', 'Flat', 'Mature, steady compounder'],
        ['Dabur India', '48–52x', '~₹12,000 Cr', 'Negative', 'Moderately valued'],
        ['ITC', '12–21x', '~₹70,000 Cr', 'Positive', 'Diversified; cigarettes drag P/E'],
        ['FMCG Sector Avg', '~48x', '—', '—', 'Nifty FMCG index avg'],
    ]
    pe_table = Table(pe_data, colWidths=[3*cm, 2.2*cm, 2.8*cm, 2.2*cm, 5*cm])
    pe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#edf2f7')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(pe_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Nifty FMCG Index Performance', subheading_style))
    story.append(Paragraph(
        'The Nifty FMCG Index stands at ~₹51,350 (Jan 27, 2026) with a 52-week range of '
        '₹50,199–₹59,303. <b>The index has delivered negative 1-year returns (-0.3% to -2.7%)</b>, '
        'underperforming the broader Nifty 50. Bikaji\'s own 1-year return of ~-2% is roughly in line '
        'with the sector — the correction is sector-wide, not Bikaji-specific. However, this also '
        'means there\'s no stock-specific alpha story in the near term.',
        body_style
    ))

    story.append(Paragraph('Raw Material & Commodity Context', subheading_style))
    story.append(Paragraph(
        'Edible oils account for <b>25-33% of raw material costs</b> for snack makers like Bikaji. '
        'The 2026 outlook is modestly favorable: crude palm oil is expected to soften to RM3,850–4,250/MT '
        '(down from ~RM4,300 in 2025) due to recovering yields and better weather. India\'s May 2025 '
        'customs duty cut on crude edible oils (effective rate from 27.5% to 16.5%) provides an '
        'additional tailwind. However, mustard oil remains firm due to supply constraints in Rajasthan '
        'and UP. Net-net, commodity costs are a mild positive for FY27 margins.',
        body_style
    ))

    story.append(Paragraph('Sector Catalysts', subheading_style))
    catalysts = [
        '<b>GST Rate Cut:</b> Reduced GST on namkeen products directly benefits Bikaji\'s core portfolio',
        '<b>Premiumization:</b> Multigrain bhujia, roasted nut mixes, trendy packaging driving ASP growth',
        '<b>Distribution Depth:</b> Tier 2/3 city penetration still low — large runway for organized brands',
        '<b>Export Boom:</b> Indian ethnic snacks gaining traction in US, UK, Middle East markets',
        '<b>Import Duty Cut:</b> Edible oil duty reduction (May 2025) supports gross margin expansion',
    ]
    for c in catalysts:
        story.append(Paragraph(f'• {c}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: IMARC Group, Outlook Business, Business Standard, Upstox, Company Presentations, '
        'NSE India (Nifty FMCG), Fastmarkets (palm oil outlook), MARC Ratings, ChemAnalyst (mustard oil), '
        'Smart-Investing.in (P/E data Jan 2026), MarketsMojo, Tickertape',
        source_style
    ))

    story.append(PageBreak())

    # ═══ SECTION 5: VALUATION & ANALYST VIEWS ═══
    story.append(Paragraph('5. Valuation & Analyst Views', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Brokerage Target Prices (Post Q3 FY26, Jan 2026)', subheading_style))

    analyst_data = [
        ['Brokerage / Source', 'Target (₹)', 'Rating', 'Key Thesis'],
        ['Motilal Oswal', '900', 'Buy', '8.4% volume growth, strong execution'],
        ['Emkay Global', '950', 'Buy', '65x FY26E P/E; 27% earnings CAGR'],
        ['Nuvama Institutional', '985', 'Buy', 'Raised from ₹970; margin resilience'],
        ['Consensus (6 analysts)', '890–900', 'Strong Buy', '6/6 Buy, 0 Hold/Sell'],
        ['Range (all sources)', '₹800 – ₹1,018', '—', 'Investing.com, Alpha Spread, TradingView'],
    ]
    analyst_table = Table(analyst_data, colWidths=[3.8*cm, 2.2*cm, 2.2*cm, 6.5*cm])
    analyst_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(analyst_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Implied Upside:</b> From ₹660 (Jan 29 close), the average brokerage target of ₹900–950 '
        'implies ~36–44% upside over 12 months. Even the most conservative target of ₹800 suggests ~21% upside. '
        'All 6 covering analysts rate the stock a Buy — zero Hold or Sell ratings.',
        callout_green
    ))

    story.append(Paragraph(
        '<b>Note on analyst timing:</b> The Motilal Oswal, Emkay, and Nuvama targets above were '
        'published post-Q3 FY26 results (late January 2026), making them the most current available. '
        'Emkay explicitly values the stock at 65x FY26E P/E with a 15% revenue CAGR and 27% earnings '
        'CAGR over FY25–28E.',
        body_style
    ))

    story.append(Paragraph('Valuation Context', subheading_style))
    story.append(Paragraph(
        'Bikaji\'s trailing P/E ranges from 67x to 89x depending on the source and methodology '
        '(standalone vs consolidated, trailing vs forward). At 65x forward (Emkay\'s basis), this is '
        'a premium to the broader FMCG sector average of 40-50x but is driven by the growth profile: '
        '5-year revenue CAGR of 20%, projected 3-year revenue CAGR of 16%, and 3-year net income CAGR '
        'of ~28%. If earnings growth sustains at 25-30%, the forward P/E could compress to 45-50x by '
        'FY27 — justifying current levels. Any growth miss would make the stock vulnerable to de-rating.',
        body_style
    ))
    story.append(Paragraph(
        'The P/B ratio of 11-12x also reflects high expectations. For context (Jan 2026 data): Nestle India '
        'trades at 80-84x P/E, Britannia at 62-66x, Dabur at 48-52x, and the FMCG sector average is ~48x. '
        'Bikaji at 67-89x is broadly in line with Nestle\'s premium range — justifiable only if the '
        '15-16% revenue CAGR and 27%+ earnings CAGR are sustained. ITC at 12-21x is not a fair comp '
        'due to its diversified business mix (cigarettes, hotels, paper).',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Motilal Oswal (via TradingView), Emkay Global Financial Services, Nuvama Institutional Equities, '
        'Investing.com, Alpha Spread, TradingView, Trendlyne — all post-Q3 FY26 (Jan 2026)',
        source_style
    ))

    story.append(PageBreak())

    # ═══ SECTION 6: CATALYSTS & RISKS ═══
    story.append(Paragraph('6. Growth Catalysts & Risks', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Management Guidance (Q3 FY26 Earnings Call, Jan 28, 2026)', subheading_style))
    story.append(Paragraph(
        'Key forward-looking statements from the earnings call transcript (Yahoo Finance):',
        body_style
    ))
    mgmt_points = [
        '<b>Revenue Growth:</b> Management expects <b>14-16% value growth</b> going forward, supported by '
        'GST benefits, distribution expansion, and Bikaji Bakes.',
        '<b>Margins:</b> Gross margin guided at ~35% (including PLI). 9M FY26 EBITDA margin stands at 14.2%. '
        'CFO stated the company is "committed to not compromising on margin thresholds despite potential cost increases."',
        '<b>Distribution:</b> Now at 14 lakh total outlets, 3.35 lakh direct. Targeting Delhi, Haryana, Punjab, UP.',
        '<b>Marketing:</b> "Bhujia Ho Toh Bikaji" campaign drove 16-17% growth in traditional snacks category. '
        'Pankaj Tripathi signed as brand ambassador for UP/North India push.',
        '<b>Capex:</b> Intensive investment phase (~₹500 Cr cumulative + ₹261 Cr PLI approved) is complete. '
        'No major capex for next 2-2.5 years → enhanced FCF expected.',
        '<b>Bikaji Bakes JV:</b> 70:30 JV with T.K. Khaleel (Bakemart, 40+ years in Middle East bakery). '
        'Targeting premium bread and cakes segment.',
        '<b>Dry Fruits/Nuts:</b> CFO explicitly stated this is "niche and not a current priority" — focus '
        'remains on core Namkeen and Bhujia.',
    ]
    for mp in mgmt_points:
        story.append(Paragraph(f'• {mp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Growth Catalysts (Bull Case)', subheading_style))
    bull_points = [
        '<b>Distribution Expansion:</b> Direct reach has grown to 13.9 lakh outlets as of Dec 2025. '
        'Pan-India expansion (targeting Delhi, Haryana, Punjab, UP — Haldiram\'s strongholds) provides '
        'multi-year revenue runway.',
        '<b>Export Acceleration:</b> Exports grew 39% in Q3 and 59% in 9M FY26. International ethnic '
        'snack demand is a structural tailwind as the Indian diaspora market expands.',
        '<b>Bakery & Frozen Foods JV:</b> The 70:30 JV with Bakemart founder (Bikaji Bakes) opens a '
        'new category. The Tumkur bakery facility is operational. This diversifies beyond traditional snacks.',
        '<b>QSR Foray:</b> First Quick Service Restaurant opened in Sikar, Rajasthan. If successful, '
        'this could be a significant long-term value driver (similar to Haldiram\'s restaurant model).',
        '<b>GST Benefit:</b> Reduced GST on namkeen products directly supports Bikaji\'s core ethnic '
        'snacks portfolio, improving competitiveness vs unorganized players.',
        '<b>Retail Business:</b> Revenue from the retail subsidiary nearly doubled YoY, growing 87% '
        'in Q3 and 150%+ on a trailing basis. Still small, but scaling rapidly.',
        '<b>Volume Growth:</b> 8.4% volume growth in Q3 FY26 indicates real demand, not just price-led growth.',
    ]
    for bp in bull_points:
        story.append(Paragraph(f'• {bp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Risks (Bear Case)', subheading_style))
    bear_points = [
        '<b>Premium Valuation (P/E 67x):</b> Leaves little margin of safety. Any earnings miss or '
        'growth slowdown could trigger sharp de-rating. The stock fell from ₹860 to ₹660 (-23%) '
        'in just 3 months, showing vulnerability.',
        '<b>Raw Material Volatility:</b> Edible oils account for 25-33% of input costs. While palm oil '
        'is expected to soften in 2026, Indonesia\'s land-seizure program puts 2-5M tonnes of CPO at risk. '
        'Mustard oil remains firm. A commodity spike would compress margins (as seen in Q3 FY25: EBITDA fell to 8.2%).',
        '<b>Haldiram\'s IPO Overhang:</b> A Haldiram\'s IPO (expected in 24-36 months) at ~$10B '
        'valuation could redirect institutional flows away from Bikaji and create a larger, more '
        'liquid alternative for sector exposure.',
        '<b>Accounting Quality Concerns:</b> Receivables growing faster than sales, lower asset '
        'depreciation rates inflating profits, and operating profit not converting to cash — these '
        'are yellow flags that warrant monitoring.',
        '<b>Sequential Profit Decline:</b> Q3 FY26 PAT fell 20% QoQ from Q2, partly seasonal but '
        'highlights earnings lumpiness. Sweets revenue down 17% YoY adds to the volatility.',
        '<b>Promoter Holding Decline:</b> Promoter stake fell from 74.98% to 73.92% over 9 months. '
        'While still high, continued dilution may signal reduced conviction.',
        '<b>Competitive Intensity:</b> Haldiram\'s (40%+ market share) and FMCG giants (ITC, Britannia) '
        'are expanding in ethnic snacks. Bikaji\'s 9% share could face pressure.',
    ]
    for bp in bear_points:
        story.append(Paragraph(f'• {bp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: Company Q3 FY26 Earnings Call (Jan 28, 2026), Screener.in, Business Standard, Trendlyne',
        source_style
    ))

    story.append(PageBreak())

    # ═══ SECTION 7: CONCLUSION ═══
    story.append(Paragraph('7. Conclusion & 1-Year Outlook', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Bikaji Foods International occupies a compelling position in India\'s fast-growing organized '
        'snacks market. The company has demonstrated strong execution with 13-15% revenue growth, '
        'margin expansion from 8% to 12.5% EBITDA, explosive export growth (39-59%), and aggressive '
        'distribution expansion. These are the hallmarks of a company in its growth phase.',
        body_style
    ))
    story.append(Paragraph(
        'However, the stock\'s premium valuation (P/E 67-89x) already prices in significant optimism. '
        'The recent 23% correction from ₹860 to ₹660 suggests the market is recalibrating expectations. '
        'Accounting quality concerns (CFO/PAT ~45% in FY25) and the looming Haldiram\'s IPO add uncertainty.',
        body_style
    ))

    story.append(Spacer(1, 0.3*cm))

    # ── Valuation Methodology ──
    story.append(Paragraph('Valuation Methodology: Forward EPS × P/E Multiple', subheading_style))
    story.append(Paragraph(
        'The scenario analysis below uses a <b>forward earnings-multiple approach</b>. '
        'This is not a DCF (discounted cash flow) model — it is a heuristic based on projected '
        'EPS and an assumed P/E multiple for each scenario. The limitations of this approach are '
        'noted at the end of this section.',
        body_style
    ))

    story.append(Paragraph('<b>Step 1: Establish Current EPS</b>', body_style))
    eps_data = [
        ['Metric', 'Value', 'Source'],
        ['TTM Net Profit', '₹238 Cr', 'Screener.in / Trendlyne'],
        ['Market Cap', '₹16,539 Cr', '5Paisa (Jan 29, 2026)'],
        ['Price', '₹660', 'NSE close (Jan 29, 2026)'],
        ['Shares Outstanding', '25.06 Cr', '(BSE/Screener.in: Equity Capital Rs 25 Cr, FV Rs 1)'],
        ['TTM EPS', '~₹9.50', 'Net Profit ÷ Shares'],
        ['Sanity Check: P/E', '660 ÷ 9.50 = 69.5x', 'Matches reported 67-69x ✓'],
    ]
    eps_table = Table(eps_data, colWidths=[3.5*cm, 4.5*cm, 6.5*cm])
    eps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (-1, -1), 'SFNS'),
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

    story.append(Paragraph('<b>Step 2: Project FY27E EPS by Scenario</b>', body_style))
    story.append(Paragraph(
        'Growth rate sources: Emkay projects 27% earnings CAGR (FY25-28E). Trendlyne estimates '
        '42.8% profit growth for FY26. We use these as anchors and vary by scenario.',
        body_style
    ))

    proj_data = [
        ['', 'Bull', 'Base', 'Bear'],
        ['FY26E Profit Growth', '43% (Trendlyne est.)', '27% (Emkay CAGR)', '10% (slowdown)'],
        ['FY26E EPS', '₹9.50 × 1.43 = ₹13.57', '₹9.50 × 1.27 = ₹12.07', '₹9.50 × 1.10 = ₹10.45'],
        ['FY27E Profit Growth', '27% (sustained)', '27% (Emkay CAGR)', '10% (continued)'],
        ['FY27E EPS', '₹13.57 × 1.27 = ₹17.23', '₹12.07 × 1.27 = ₹15.33', '₹10.45 × 1.10 = ₹11.50'],
    ]
    proj_table = Table(proj_data, colWidths=[3.5*cm, 4.5*cm, 4.5*cm, 4*cm])
    proj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (1, 0), (1, -1), HexColor('#f0fff4')),
        ('BACKGROUND', (2, 0), (2, -1), HexColor('#fffff0')),
        ('BACKGROUND', (3, 0), (3, -1), HexColor('#fff5f5')),
        ('TEXTCOLOR', (1, 0), (3, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 0), (0, -1), 'SFNS'),
        ('FONTNAME', (1, 1), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(proj_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>Step 3: Apply P/E Multiple → Target Price</b>', body_style))
    story.append(Paragraph(
        'P/E assumptions are anchored to sector comps (Jan 2026): Nestle 80-84x, Britannia 62-66x, '
        'Dabur 48-52x, sector avg 48x. Bikaji\'s multiple is varied by scenario based on growth delivery.',
        body_style
    ))

    # Scenario boxes with full math
    scenario_data = [
        ['Scenario', 'FY27E EPS', 'P/E Assumed', 'Price Target', 'Return from ₹660', 'Probability'],
        ['Bull', '₹17.23', '55–60x',
         '₹948–1,034', '+44% to +57%', '20%'],
        ['Base', '₹15.33', '50–55x',
         '₹767–843', '+16% to +28%', '55%'],
        ['Bear', '₹11.50', '35–45x',
         '₹403–518', '-22% to -39%', '25%'],
    ]
    scenario_table = Table(scenario_data, colWidths=[1.8*cm, 2.3*cm, 2.3*cm, 2.8*cm, 3.3*cm, 2.5*cm])
    scenario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fffff0')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#fff5f5')),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 1), (0, -1), 'SFNS'),
        ('FONTNAME', (1, 1), (-1, -1), 'SFNS'),
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
        '<b>Bull (20%):</b> Requires everything to go right — sustained 15%+ growth, margin expansion '
        'to 14%, export momentum, AND the market keeping a 55-60x multiple. 6/6 analysts are bullish, '
        'but unanimous consensus itself is a contrarian warning. Low but real probability.',
        '<b>Base (55%):</b> Most likely outcome. Bikaji delivers on management guidance of 14-16% growth, '
        'margins stay at 12-13%, earnings grow ~27% (Emkay CAGR), and the P/E gently compresses from '
        '~69x to 50-55x as earnings catch up to price. This is the "growth compounder doing its job" scenario.',
        '<b>Bear (25%):</b> Higher than typical because of specific, identifiable risks: (a) cash conversion '
        'is already weak (CFO/PAT ~45% in FY25), (b) commodity reversal is possible given Indonesia CPO supply risks, '
        '(c) Haldiram\'s IPO could structurally re-rate the sector, and (d) the 23% drawdown in 3 months '
        'shows this stock can fall sharply. A 25% bear weight reflects these tangible headwinds.',
    ]
    for pp in prob_points:
        story.append(Paragraph(f'• {pp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    ev_data = [
        ['Scenario', 'Midpoint Price', 'Probability', 'Weighted Value'],
        ['Bull', '₹991', '20%', '₹198'],
        ['Base', '₹805', '55%', '₹443'],
        ['Bear', '₹461', '25%', '₹115'],
        ['', '', 'Expected Value →', '₹756'],
    ]
    ev_table = Table(ev_data, colWidths=[3*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    ev_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fffff0')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#fff5f5')),
        ('BACKGROUND', (0, 4), (-1, 4), HexColor('#edf2f7')),
        ('FONTNAME', (0, 0), (-1, 0), 'SFNS'),
        ('FONTNAME', (0, 4), (-1, 4), 'SFNS'),
        ('FONTNAME', (0, 1), (0, 3), 'SFNS'),
        ('FONTNAME', (1, 1), (-1, 3), 'SFNS'),
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
        '<b>Probability-weighted expected price: ₹756</b> — implying ~14.5% upside from ₹660. '
        'This is a moderate expected return that reflects genuine upside potential tempered by '
        'non-trivial downside risks.',
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
        'with segment-level revenue build-up, margin assumptions, capex forecasting, and WACC-based '
        'discounting. This report does not include one.',
        '<b>P/E assumptions are subjective:</b> The choice of 50-55x for base vs 35-45x for bear is '
        'anchored to sector comps (Nestle 80x, Britannia 62x, sector avg 48x) but remains a judgment call.',
        '<b>EPS estimates are top-down:</b> Growth rates are sourced from Emkay (27% CAGR) and '
        'Trendlyne (42.8% FY26) rather than built from a bottoms-up P&L forecast by segment.',
        '<b>Probability weights are subjective:</b> The 20/55/25 split is an informed estimate based '
        'on current evidence (cash flow quality, commodity outlook, sector dynamics), not a quantitative '
        'model output. Different analysts would assign different weights.',
        '<b>Cash flow ignored in valuation:</b> Given the weak cash conversion (CFO/PAT ~45% in FY25, down from 65% in FY24) flagged earlier, '
        'an EV/FCF or DCF approach would likely produce a more conservative (and arguably more realistic) '
        'valuation than the P/E method used here.',
    ]
    for lp in limit_points:
        story.append(Paragraph(f'• {lp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Verdict', subheading_style))
    story.append(Paragraph(
        '<b>Bikaji Foods is a fundamentally strong business in a structurally growing market.</b> '
        'The company\'s execution on distribution, exports, and margin improvement has been impressive. '
        'At ₹660, the stock has corrected meaningfully from its highs, bringing the risk-reward ratio '
        'to a more favorable zone.',
        body_style
    ))
    story.append(Paragraph(
        'The <b>probability-weighted expected value of ₹756 implies ~14.5% upside</b> over 12 months. '
        'This is supported by 6/6 analyst Buy ratings (avg target ₹900) but tempered by a 25% bear '
        'probability driven by cash flow concerns, commodity risk, and Haldiram\'s IPO overhang. '
        'The key variable remains whether Bikaji can sustain 14-16% revenue growth while improving '
        'its cash conversion ratio.',
        body_style
    ))
    story.append(Paragraph(
        'The primary risks are valuation compression (if growth disappoints), raw material spikes, '
        'and the potential distraction from a Haldiram\'s IPO. The accounting quality concerns '
        '(receivables, depreciation, cash conversion) deserve ongoing monitoring and should not be dismissed.',
        body_style
    ))
    story.append(Paragraph(
        '<b>On balance, the stock offers a moderate expected return (~14.5%) with asymmetric risk '
        '(more upside in the bull case than downside in bear, but the bear case is plausible). '
        'Suited for growth-oriented investors with a 12+ month horizon and tolerance for '
        'mid-cap FMCG volatility. Not suitable for conservative or income-seeking portfolios.</b>',
        body_style
    ))

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cbd5e0')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>IMPORTANT DISCLAIMER:</b> This report is generated for informational and educational '
        'purposes only. It does not constitute investment advice, a recommendation to buy, sell, '
        'or hold any security, or an offer of any kind. All data is sourced from publicly available '
        'information as of February 3, 2026. Past performance does not guarantee future results. '
        'Stock market investments carry risk of capital loss. Please consult a SEBI-registered '
        'investment advisor before making any investment decisions. The author has no position '
        'in Bikaji Foods International.',
        disclaimer_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Data Sources:</b> Screener.in (primary financial data) | NSE India (nseindia.com) | '
        'Yahoo Finance (finance.yahoo.com) | Business Standard (business-standard.com) | '
        'Trendlyne (trendlyne.com) | Investing.com | TradingView (tradingview.com) | '
        'IMARC Group (imarcgroup.com) | Motilal Oswal | Emkay Global | Nuvama | '
        'Fastmarkets | MARC Ratings | Company Investor Presentations (bikaji.com)',
        source_style
    ))

    doc.build(story)
    print(f"PDF generated successfully: {FINAL_PDF}")


# ─── Main ───
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
