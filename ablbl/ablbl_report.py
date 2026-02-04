#!/usr/bin/env python3
"""
Aditya Birla Lifestyle Brands Limited (ABLBL) -- 1-Year Stock Research Report
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

# Register SFNS (San Francisco) for proper INR symbol support
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

# --- Configuration ---
OUTPUT_DIR = "/Users/arpitvyas/Desktop/stock-analysis/ablbl"
FINAL_PDF = "/Users/arpitvyas/Desktop/stock-analysis/ablbl/ABLBL_Research_Report_Feb2026.pdf"

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


# ========== Chart 1: Quarterly Revenue & Net Profit ==========
def create_revenue_chart():
    """Q1-Q3 FY26 quarterly revenue and net profit (consolidated)."""
    quarters = ['Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26', 'Q3\nFY26']
    # Revenue in Cr (sourced from quarterly results / Business Standard / Screener.in)
    revenue = [1942, 1841, 2037, 2341]
    # Net Profit in Cr (reported consolidated PAT)
    pat = [52, 24, 23, 66]

    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(quarters))
    width = 0.35

    bars1 = ax1.bar(x - width/2, revenue, width, label='Revenue (\u20b9 Cr)', color=ACCENT, alpha=0.85)
    ax1.set_ylabel('Revenue (\u20b9 Cr)', color=ACCENT)
    ax1.set_ylim(0, 3000)
    ax1.tick_params(axis='y', labelcolor=ACCENT)

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, pat, width, label='Net Profit (\u20b9 Cr)', color=GREEN, alpha=0.85)
    ax2.set_ylabel('Net Profit (\u20b9 Cr)', color=GREEN)
    ax2.set_ylim(0, 120)
    ax2.tick_params(axis='y', labelcolor=GREEN)

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=9)
    ax1.set_title('ABLBL \u2014 Quarterly Revenue & Net Profit (Consolidated)', fontweight='bold', pad=15)

    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 30,
                f'\u20b9{int(bar.get_height())}', ha='center', va='bottom', fontsize=8, color=ACCENT)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1.5,
                f'\u20b9{int(bar.get_height())}', ha='center', va='bottom', fontsize=8, color=GREEN)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_revenue.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== Chart 2: EBITDA Margin Trend ==========
def create_margin_chart():
    """EBITDA margin trend showing the 20.6% Q3 FY26 achievement."""
    quarters = ['Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26', 'Q3\nFY26']
    # EBITDA margin % (consolidated, from company press releases)
    # Q4 FY25: ~17% (200bps higher YoY per Aditya Birla Group press release)
    # Q1/Q2 FY26: H1 FY26 margin was ~16% per management guidance
    # Q3 FY26: 18.4% overall, 20.6% for Lifestyle segment
    ebitda_margin_overall = [17.0, 15.5, 16.5, 18.4]
    ebitda_margin_lifestyle = [18.5, 17.0, 18.0, 20.6]

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(quarters))

    ax.plot(x, ebitda_margin_lifestyle, 's-', color=ACCENT, linewidth=2.5, markersize=8,
            label='Lifestyle Brands EBITDA Margin (%)')
    ax.plot(x, ebitda_margin_overall, 'o-', color=GREEN, linewidth=2.5, markersize=8,
            label='Overall EBITDA Margin (%)')

    ax.fill_between(x, ebitda_margin_overall, alpha=0.12, color=GREEN)

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=9)
    ax.set_ylabel('Margin (%)')
    ax.set_title('ABLBL \u2014 EBITDA Margin Trend (Lifestyle vs Overall)', fontweight='bold', pad=10)
    ax.legend(fontsize=8)
    ax.set_ylim(12, 24)

    for i, (om, lm) in enumerate(zip(ebitda_margin_overall, ebitda_margin_lifestyle)):
        ax.annotate(f'{om}%', (i, om), textcoords="offset points", xytext=(0, -14),
                    fontsize=8, ha='center', color=GREEN, fontweight='bold')
        ax.annotate(f'{lm}%', (i, lm), textcoords="offset points", xytext=(0, 10),
                    fontsize=8, ha='center', color=ACCENT, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_margins.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== Chart 3: Brand Revenue Pie ==========
def create_brand_chart():
    """Approximate brand revenue mix based on segment reporting."""
    # Lifestyle Brands segment: Rs 2,002 Cr in Q3 (85.4% of total Q3 revenue)
    # Emerging Businesses: Rs 355 Cr in Q3 (15.2% of total)
    # Note: Individual brand breakdowns not disclosed; pie shows segment + illustrative sub-split
    labels = ['Louis Philippe\n(Est. ~24%)', 'Van Heusen\n(Est. ~22%)',
              'Allen Solly\n(Est. ~20%)', 'Peter England\n(Est. ~18%)',
              'Reebok India\n(~7%)', 'American Eagle\n(~5%)',
              'VH Innerwear\n& Other (~4%)']
    sizes = [24, 22, 20, 18, 7, 5, 4]
    colors_pie = ['#2b6cb0', '#38a169', '#dd6b20', '#805ad5', '#e53e3e', '#319795', '#a0aec0']
    explode = (0.04, 0.04, 0.04, 0.04, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors_pie, autopct='',
                                       shadow=False, startangle=120,
                                       textprops={'fontsize': 8})
    ax.set_title('ABLBL \u2014 Estimated Brand Revenue Mix (Q3 FY26)\n'
                 'Note: Individual brand splits are estimated; segment data is reported',
                 fontweight='bold', pad=15, fontsize=10)

    # FIX 4: Add prominent watermark — individual brand splits are not publicly disclosed
    ax.text(0.5, 0.5, 'ILLUSTRATIVE ONLY\nIndividual brand-level revenue splits\nare not publicly disclosed\nby the company.',
            transform=ax.transAxes, fontsize=11, ha='center', va='center',
            color='red', alpha=0.35, fontweight='bold', rotation=30)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_brands.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== Chart 4: Price Action with MAs ==========
def create_price_chart():
    """Price action since listing (June 2025) with support/resistance zones."""
    # Monthly closing prices (approximate from known data points)
    # Listed June 23, 2025 at Rs 167.75; 52W high 175 (Jun 23); 52W low 100.86 (Jan 27, 2026)
    months = ['Jun\n2025', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026']
    prices = [168, 155, 148, 140, 130, 128, 120, 105]

    # Approximate MAs (limited history)
    sma_50 = [168, 162, 157, 152, 147, 143, 138, 132]
    sma_100 = [168, 165, 160, 155, 152, 148, 144, 140]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(months))

    ax.plot(x, prices, 'o-', color=PRIMARY, linewidth=2.5, markersize=6,
            label='Price (\u20b9)', zorder=3)
    ax.plot(x, sma_50, '--', color=HIGHLIGHT, linewidth=1.5,
            label='50-Day SMA (approx)', alpha=0.8)
    ax.plot(x, sma_100, '--', color=GREEN, linewidth=1.5,
            label='100-Day SMA (approx)', alpha=0.8)

    # Support and resistance zones
    ax.axhspan(100, 110, alpha=0.12, color='green', label='Support Zone (\u20b9100\u2013110)')
    ax.axhspan(160, 175, alpha=0.12, color='red', label='Resistance Zone (\u20b9160\u2013175)')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=9)
    ax.set_ylabel('Price (\u20b9)')
    ax.set_title('ABLBL \u2014 Price Action Since Listing (Jun 2025 \u2013 Jan 2026)',
                 fontweight='bold', pad=15)
    # FIX 7: Price chart disclaimer
    ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
            transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')
    ax.legend(fontsize=7, loc='upper right')
    ax.set_ylim(85, 190)

    # Annotate listing price and current price
    ax.annotate(f'Listed: \u20b9168', xy=(0, 168), xytext=(1.5, 180),
                arrowprops=dict(arrowstyle='->', color=PRIMARY),
                fontsize=9, fontweight='bold', color=PRIMARY)
    ax.annotate(f'Current: \u20b9105', xy=(7, 105), xytext=(5.5, 95),
                arrowprops=dict(arrowstyle='->', color=HIGHLIGHT),
                fontsize=9, fontweight='bold', color=HIGHLIGHT)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== Chart 5: Peer Comparison ==========
def create_peer_chart():
    """Peer comparison: P/E, revenue, margins vs branded apparel peers."""
    companies = ['ABLBL', 'Trent', 'Page Ind.', 'Raymond', 'Vedant\nFashions']

    # P/E ratios (TTM, Jan 2026 sources)
    # ABLBL Screener P/E 80.4x (newly listed, low reported PAT); forward PE ~61x
    # Trent ~97x; Page Industries ~51x; Raymond ~25x; Vedant Fashions ~31x
    pe_ratios = [61, 97, 51, 25, 31]  # Using forward PE for ABLBL for fair comparison

    # Revenue (TTM in Rs Cr, approximate)
    revenues = [8164, 16500, 4800, 9500, 1450]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # P/E Comparison
    bar_colors = [ACCENT, '#a0aec0', '#a0aec0', '#a0aec0', '#a0aec0']
    bars = axes[0].bar(companies, pe_ratios, color=bar_colors, width=0.55)
    axes[0].set_title('Forward P/E Ratio (x)', fontweight='bold', fontsize=10)
    axes[0].set_ylim(0, 120)
    for bar, pe in zip(bars, pe_ratios):
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
                    f'{pe}x', ha='center', fontsize=8, fontweight='bold')

    # Revenue Comparison
    bars2 = axes[1].bar(companies, [r/1000 for r in revenues], color=bar_colors, width=0.55)
    axes[1].set_title('Revenue TTM (\u20b9 \'000 Cr)', fontweight='bold', fontsize=10)
    axes[1].set_ylim(0, 20)
    for bar, rev in zip(bars2, revenues):
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                    f'\u20b9{rev:,}', ha='center', fontsize=7)

    fig.suptitle('ABLBL vs Branded Apparel Peers \u2014 Valuation & Scale',
                 fontweight='bold', fontsize=11, y=1.02)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_peers.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== Chart 6 (Bonus): Store Expansion Trajectory ==========
def create_store_chart():
    """Store count trajectory and FY30 target."""
    periods = ['Jun\n2025', 'Sep\n2025', 'Dec\n2025', 'FY27E', 'FY28E', 'FY30E']
    stores = [3095, 3225, 3315, 3565, 3815, 4500]
    area = [4.3, 4.5, 4.8, 5.3, 5.8, 7.3]  # Million sq ft

    fig, ax1 = plt.subplots(figsize=(7, 4))
    x = np.arange(len(periods))

    bars = ax1.bar(x, stores, width=0.5, color=ACCENT, alpha=0.8, label='Store Count')
    ax1.set_ylabel('Number of Stores', color=ACCENT)
    ax1.set_ylim(0, 5500)
    ax1.tick_params(axis='y', labelcolor=ACCENT)

    ax2 = ax1.twinx()
    ax2.plot(x, area, 's-', color=ORANGE, linewidth=2, markersize=7,
             label='Retail Area (Mn sq ft)')
    ax2.set_ylabel('Retail Area (Mn sq ft)', color=ORANGE)
    ax2.set_ylim(0, 9)
    ax2.tick_params(axis='y', labelcolor=ORANGE)

    ax1.set_xticks(x)
    ax1.set_xticklabels(periods, fontsize=8)
    ax1.set_title('ABLBL \u2014 Store Expansion: Actual & Management Targets',
                  fontweight='bold', pad=12)

    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 50,
                f'{int(bar.get_height())}', ha='center', fontsize=7, color=ACCENT)
    for i, a in enumerate(area):
        ax2.text(i, a + 0.2, f'{a}', ha='center', fontsize=7, color=ORANGE, fontweight='bold')

    # Dashed line to separate actuals from estimates
    ax1.axvline(x=2.5, color='grey', linestyle='--', alpha=0.5)
    ax1.text(2.7, 5200, 'Estimates \u2192', fontsize=7, color='grey', fontstyle='italic')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=7)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_stores.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# ========== PDF Generation ==========
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
    callout_orange = ParagraphStyle(
        'CalloutOrange', parent=body_style,
        backColor=HexColor('#fffff0'), borderWidth=1,
        borderColor=HexColor(ORANGE), borderPadding=8,
        leftIndent=10, spaceAfter=8
    )

    story = []

    # =====================================================
    # SECTION 1: TITLE PAGE
    # =====================================================
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('ADITYA BIRLA LIFESTYLE BRANDS LTD', title_style))
    story.append(Paragraph('NSE: ABLBL | BSE: ABLBL', subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=HexColor(PRIMARY)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('1-Year Stock Research Report', ParagraphStyle(
        'BigSub', parent=subtitle_style, fontSize=16, textColor=HexColor(ACCENT),
        fontName='SFNS'
    )))
    story.append(Paragraph('Outlook: February 2026 \u2192 February 2027', subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>NEWLY LISTED (June 23, 2025)</b> \u2014 Demerged from ABFRL. Heritage lifestyle brands entity.',
        ParagraphStyle('NewlyListed', parent=body_style, alignment=TA_CENTER,
                       textColor=HexColor(ORANGE), fontSize=10, fontName='SFNS')
    ))
    story.append(Spacer(1, 0.8*cm))

    # Key metrics box
    metrics_data = [
        ['Current Price', '\u20b9105 (Jan 30, 2026)', 'Market Cap', '\u20b914,103 Cr'],
        ['P/E (Trailing)', 'N/M (Newly Listed) *', 'P/E (Forward)', '~61x (FY27E)'],
        ['P/E (Screener.in)', '80.4x', 'ROE', '10.7%'],
        ['P/B Ratio', '10.8x', 'Book Value', '~\u20b910.7/share'],
        ['52-Week Range', '\u20b9100.86 \u2013 \u20b9175.00', 'Revenue (TTM)', '\u20b98,164 Cr'],
        ['Net Debt', '~\u20b9781 Cr (Q4 FY25)', 'Promoter Holding', '46.6%'],
        ['Shares Outstanding', '122.03 Cr', 'Listing Date', 'June 23, 2025'],
    ]
    metrics_table = Table(metrics_data, colWidths=[3.3*cm, 3.8*cm, 3.3*cm, 3.8*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#edf2f7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor(PRIMARY)),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.4*cm))

    # FIX 6: Executive Summary / Verdict Box on Page 1
    verdict_data = [
        ['VERDICT: HOLD | Expected Value: Rs ~105 (in line with CMP)', '', ''],
        ['Key Bull: Premium brand portfolio (LP, VH, AS, PE) + 3,300 stores', '', ''],
        ['Key Bear: P/B 10.8x demanding, margins under pressure, newly listed', '', ''],
    ]
    verdict_table = Table(verdict_data, colWidths=[7*cm, 3.6*cm, 3.6*cm])
    verdict_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 1), (-1, 1)),
        ('SPAN', (0, 2), (-1, 2)),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#fffff0')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fff5f5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(ORANGE)),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor(GREEN)),
        ('TEXTCOLOR', (0, 2), (-1, 2), HexColor(HIGHLIGHT)),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (0, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor(ORANGE)),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        '* Trailing P/E marked N/M (Not Meaningful) due to limited reported PAT history post-demerger. '
        'Screener.in reports P/E of 80.4x, P/B of 10.8x, ROE of 10.7%. Shares: ~122 Cr (Equity Capital Rs 1,220 Cr at Sep 2025, FV Rs 10). '
        'Forward P/E of ~61x (based on FY27E earnings) is the most meaningful valuation metric. '
        'Market cap ~\u20b914,103 Cr (varies by date). '
        'Standalone vs consolidated basis further complicates comparison.',
        source_style
    ))
    story.append(Paragraph(
        'Report Date: February 4, 2026 | Price as of: Jan 30, 2026 (NSE close) '
        '| Data Sources: Screener.in, Business Standard, Aditya Birla Group Press Releases, '
        'Morgan Stanley, Motilal Oswal, HDFC Securities, Bernstein, TradingView, Yahoo Finance, '
        'StockAnalysis.com, Trendlyne, MarketScreener',
        source_style
    ))
    story.append(Paragraph(
        'DISCLAIMER: This report is for informational and educational purposes only. '
        'It does not constitute financial advice, a recommendation to buy or sell securities, '
        'or an offer to transact. Stock investments are subject to market risks. '
        'ABLBL has less than 1 year of listed history \u2014 data is limited. '
        'Consult a SEBI-registered financial advisor before making investment decisions.',
        disclaimer_style
    ))

    story.append(PageBreak())

    # =====================================================
    # SECTION 2: COMPANY SNAPSHOT
    # =====================================================
    story.append(Paragraph('1. Company Snapshot', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Aditya Birla Lifestyle Brands Limited (ABLBL) is <b>India\'s largest branded menswear company</b>, '
        'housing heritage lifestyle brands that have defined western formalwear and smart-casual fashion '
        'in India for over 25 years. The company was demerged from Aditya Birla Fashion & Retail Ltd '
        '(ABFRL) and listed on NSE/BSE on June 23, 2025.',
        body_style
    ))
    story.append(Paragraph(
        'The demerger was structured to separate the <b>profitable, established lifestyle brands</b> '
        '(ABLBL) from ABFRL\'s newer, loss-making businesses (Pantaloons, ethnic wear). '
        'ABLBL received \u20b91,000 Cr of debt from ABFRL\'s total \u20b93,000 Cr outstanding as of March 2024, '
        'and aims to become <b>debt-free in 2\u20133 years</b>.',
        body_style
    ))

    story.append(Paragraph('Brand Portfolio', subheading_style))
    brands = [
        '<b>Louis Philippe:</b> India\'s leading premium menswear brand. Top-of-pyramid positioning.',
        '<b>Van Heusen:</b> India\'s #1 premium lifestyle brand for men, women, and youth. Also runs innerwear vertical.',
        '<b>Allen Solly:</b> Pioneer of semi-formal/smart-casual revolution in India. Among fastest-growing brands.',
        '<b>Peter England:</b> Mass-premium segment. Largest brand by reach, covering Tier 2/3 cities.',
        '<b>Simon Carter:</b> Niche premium brand (limited scale).',
        '<b>Reebok India:</b> Licensed sportswear brand. Part of the "Emerging Businesses" segment.',
        '<b>American Eagle:</b> Youth-focused casualwear. Growing at 13\u201319% in Emerging Businesses segment.',
    ]
    for b in brands:
        story.append(Paragraph(f'\u2022 {b}', bullet_style))

    story.append(Paragraph('Key Business Facts', subheading_style))
    facts = [
        '<b>Store Count:</b> 3,315 stores (Dec 2025), 4.8 Mn sq ft retail area. Target: 4,500 stores, 7.3 Mn sq ft by FY30.',
        '<b>Distribution:</b> 37,000+ multi-brand outlets (MBOs), 7,000+ shop-in-shops across departmental stores.',
        '<b>Channel Mix:</b> EBO (Exclusive Brand Outlets), MBOs, Online (growing), Dept. Store SIS.',
        '<b>Store Additions:</b> 220+ gross stores in 9M FY26; targeting 250 stores/year going forward.',
        '<b>Revenue (TTM):</b> \u20b98,164 Cr (Screener.in consolidated). Net Profit: \u20b9145 Cr.',
        '<b>Promoter Holding:</b> 46.6% (Aditya Birla Group).',
    ]
    for f in facts:
        story.append(Paragraph(f'\u2022 {f}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: Screener.in (screener.in/company/ABLBL/consolidated/), Aditya Birla Group press releases, '
        'Business Standard (Feb 3, 2026), Company website (ablbl.in)',
        source_style
    ))

    story.append(PageBreak())

    # =====================================================
    # SECTION 3: FUNDAMENTAL ANALYSIS
    # =====================================================
    story.append(Paragraph('2. Fundamental Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Important Note:</b> ABLBL has limited financial history as a standalone listed entity. '
        'It listed on June 23, 2025 after demerger from ABFRL. Historical data is based on the '
        'demerged Madura Fashion & Lifestyle (MFL) business, which operated as a division of ABFRL. '
        'Screener.in shows limited compounded growth data given the short listing history.',
        callout_orange
    ))

    story.append(Paragraph('Quarterly Results (Consolidated)', subheading_style))
    qr_data = [
        ['Metric', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26'],
        ['Revenue (\u20b9 Cr)', '1,942', '1,841', '2,037', '2,341'],
        ['Revenue YoY Growth', '+4%', '+3.1%', '+4%', '+9.6%'],
        ['EBITDA (\u20b9 Cr)', '~330', '~285', '~336', '431'],
        ['EBITDA Margin', '~17%', '~15.5%', '~16.5%', '18.4%'],
        ['Net Profit (\u20b9 Cr)', '52', '24', '23', '66'],
        ['Lifestyle EBITDA Margin', '~18.5%', '~17%', '~18%', '20.6%'],
        ['Stores (cumulative)', '~3,095', '~3,130', '~3,225', '3,315'],
    ]
    qr_table = Table(qr_data, colWidths=[3.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    qr_table.setStyle(TableStyle([
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
    story.append(qr_table)
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        '<b>Key Insight:</b> Revenue growth is <b>accelerating</b> \u2014 from 3% in Q1 FY26 to ~10% in Q3 FY26. '
        'EBITDA margin expanded by 90 bps YoY to 20.6% for Lifestyle Brands in Q3. '
        'Net profit surged in Q3 (\u20b966 Cr, EPS \u20b90.54) after weak Q1-Q2 (\u20b924 Cr and \u20b923 Cr / EPS \u20b90.19 respectively), '
        'partly due to seasonality (festive quarter) and partly due to genuine operational improvement. '
        'Q3 FY26 EPS: \u20b90.54/share on 122.03 Cr shares outstanding.',
        callout_green
    ))

    story.append(Paragraph('Revenue & Profit Trend', subheading_style))
    story.append(Image(chart_paths['revenue'], width=16*cm, height=8.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('EBITDA Margin Improvement', subheading_style))
    story.append(Paragraph(
        'The Lifestyle Brands segment achieved 20.6% EBITDA margin in Q3 FY26, up 90 bps YoY. '
        'This is a strong result and approaches the management target of 18\u201320%+ EBITDA margin by FY30. '
        'Margin expansion is driven by better product mix, premiumization, and operating leverage from '
        'scale. Management has guided for overall EBITDA margins exceeding 18% by FY30.',
        body_style
    ))
    story.append(Image(chart_paths['margins'], width=14*cm, height=7.5*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Segment Performance (Q3 FY26)', subheading_style))
    seg_data = [
        ['Segment', 'Revenue (\u20b9 Cr)', 'YoY Growth', 'EBITDA Margin', 'Key Brands'],
        ['Lifestyle Brands', '2,002', '+9%', '20.6%', 'LP, VH, Allen Solly, PE'],
        ['Emerging Businesses', '355', '+13.4% (19% ex-F21)', '790 bps expansion', 'Reebok, AE, VH Innerwear'],
    ]
    seg_table = Table(seg_data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 4*cm])
    seg_table.setStyle(TableStyle([
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
    story.append(seg_table)
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        'Emerging Businesses achieved retail LTL (Like-to-Like) growth of 16% in Q3, with EBITDA margin '
        'expanding 790 bps YoY. This segment was previously loss-making; profitable growth here is a '
        'significant positive. Forever 21 has been exited from the base.',
        body_style
    ))

    story.append(Image(chart_paths['brands'], width=13*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Balance Sheet & Cash Flow', subheading_style))
    story.append(Paragraph(
        '<b>Debt Position:</b> ABLBL had net debt of ~\u20b9781 Cr as of Q4 FY25. The demerger transferred '
        '\u20b91,000 Cr of debt from ABFRL. Management targets becoming <b>debt-free in 2\u20133 years</b>. '
        'Note: The \u20b91,000 Cr QIP was raised by ABFRL pre-demerger, not by ABLBL separately. '
        'ABLBL shares were allocated 1:1 to ABFRL shareholders (122.03 Cr shares outstanding). '
        'On Feb 2, 2026, the board approved private placement of NCDs up to \u20b9500 Cr for refinancing.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Key Ratios (Screener.in):</b> P/E 80.4x, P/B 10.8x, ROE 10.7%. Revenue \u20b98,164 Cr. Profit \u20b9145 Cr. '
        'The company has a <b>low interest coverage ratio</b> \u2014 this is a flag. '
        'Book value per share is approximately \u20b910.7, implying significant goodwill/brand value in equity.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Free Cash Flow Outlook:</b> Motilal Oswal projects cumulative FCF of \u20b91,100 Cr over FY25\u201328E, '
        'which should help ABLBL become a net-cash company. This is a crucial variable \u2014 if FCF generation '
        'disappoints, the debt-free timeline will slip.',
        body_style
    ))

    # FIX 8: Cash Flow Table
    story.append(Paragraph('Cash Flow & Working Capital', subheading_style))
    cf_data = [
        ['Metric', 'FY25 (Mar 2025)'],
        ['CFO (\u20b9 Cr)', '1,144'],
        ['Net Debt', '781'],
        ['Debtor Days', '62'],
        ['Inventory Days', '235'],
        ['Payable Days', '237'],
        ['Working Capital Days', '-16 (negative = efficient)'],
        ['Source', 'Screener.in (only FY25 available \u2014 company incorporated 2025)'],
    ]
    cf_table = Table(cf_data, colWidths=[4.5*cm, 6*cm])
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
        'Note: Only FY25 data available \u2014 company incorporated/listed in 2025. No prior year cash flow history. '
        'Negative working capital days (-16) indicate ABLBL collects/manages inventory '
        'efficiently relative to payables, a positive sign for cash generation. CFO of \u20b91,144 Cr in FY25 '
        'is strong and supports the debt-free target in 2\u20133 years.',
        source_style
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Shareholding Pattern', subheading_style))
    sh_data = [
        ['Category', 'Holding (%)', 'Details'],
        ['Promoters', '46.60%', 'Aditya Birla Group; Kumar Mangalam Birla'],
        ['FII (Foreign Institutional)', '16.25%', 'Morgan Stanley, Bernstein coverage initiated'],
        ['DII (Domestic Institutional)', '17.05%', 'Mutual funds, insurance companies'],
        ['Public / Retail', '19.58%', '122.03 Cr shares outstanding (1:1 from ABFRL demerger)'],
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
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        '<b>Note:</b> Promoter holding at 46.6% is lower than typical Aditya Birla group companies. '
        'This is because the demerger allocated shares 1:1 to all ABFRL shareholders, '
        'reflecting ABFRL\'s promoter holding. Detailed FII/DII quarterly breakdown for ABLBL '
        'is limited given the short listing history.',
        body_style
    ))

    story.append(Paragraph('Cautionary Flags', subheading_style))
    story.append(Paragraph(
        '<b>Investors should note the following concerns:</b><br/>'
        '\u2022 <b>Newly Listed (< 1 year):</b> Listed June 23, 2025. Very limited standalone track record. '
        'No multi-year financial history to assess consistency.<br/>'
        '\u2022 <b>P/B of 10.8x:</b> Trading at over 10x book value implies the market is paying a large '
        'premium for brand intangibles. If growth disappoints, this multiple is vulnerable.<br/>'
        '\u2022 <b>Debt of ~\u20b9781 Cr:</b> Transferred from ABFRL demerger. Low interest coverage ratio noted '
        'by Screener.in. The NCD issuance of \u20b9500 Cr (Feb 2026) suggests ongoing funding needs.<br/>'
        '\u2022 <b>Demerger Supply Overhang:</b> ABFRL shareholders received ABLBL shares 1:1. Some investors '
        'who wanted exposure to Pantaloons/ethnic may sell ABLBL shares, creating supply pressure. '
        'The stock has fallen 37% from listing price of \u20b9168 to \u20b9105.<br/>'
        '\u2022 <b>Weak Q1/Q2 FY26:</b> Net profit was only \u20b924 Cr and \u20b923 Cr respectively, '
        'raising questions about earnings consistency outside the festive quarter.<br/>'
        '\u2022 <b>Low Promoter Holding (46.6%):</b> While stable, this is lower than many peer companies.',
        callout_red
    ))

    story.append(Paragraph('6 Consecutive Quarters of Positive LTL Growth', subheading_style))
    story.append(Paragraph(
        '<b>Q3 FY26 LTL growth: 6% overall across 3,000+ stores (6th consecutive quarter of positive '
        'retail LTL).</b> Lifestyle brands: 9% revenue growth, EBITDA margin 20.6% (+90 bps YoY). '
        'Emerging brands (American Eagle, Reebok): 16% LTL growth, EBITDA margin expanded 790 bps YoY. '
        'Six consecutive quarters of positive LTL is a strong signal of sustained operational momentum '
        'and brand health across the portfolio.',
        callout_green
    ))

    story.append(Paragraph(
        'Sources: Screener.in, Business Standard, Aditya Birla Group press releases, Motilal Oswal Research',
        source_style
    ))

    story.append(PageBreak())

    # =====================================================
    # SECTION 4: TECHNICAL ANALYSIS
    # =====================================================
    story.append(Paragraph('3. Technical Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Caveat:</b> ABLBL has been listed for only ~7 months (June 2025 \u2013 Jan 2026). '
        'Technical analysis with such limited history is inherently unreliable. '
        'Moving averages are based on approximated data. Treat all technical signals with caution.',
        callout_orange
    ))

    story.append(Paragraph(
        'ABLBL listed at \u20b9167.75 on June 23, 2025, hitting a 52-week high of \u20b9175 on the same day. '
        'Since then, the stock has been in a <b>persistent downtrend</b>, falling 37% to a 52-week low '
        'of \u20b9100.86 on January 27, 2026. The Jan 30 close of ~\u20b9105 is near the bottom of the range. '
        'The stock rallied ~7.5% intra-day to \u20b9112 after Q3 results (Feb 3, 2026) before settling.',
        body_style
    ))

    story.append(Image(chart_paths['price'], width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Technical Signals', subheading_style))
    tech_data = [
        ['Indicator', 'Value', 'Signal'],
        ['Price (Jan 30)', '\u20b9105.03', 'Near 52-week low'],
        ['52-Week High', '\u20b9175.00 (Jun 23)', 'Listing day; 40% above current'],
        ['52-Week Low', '\u20b9100.86 (Jan 27)', 'Very recent; testing support'],
        ['RSI (14)', '~37\u201338', 'Near oversold territory (30)'],
        ['Beta', '2.22', 'High volatility vs market'],
        ['Pattern', 'Falling wedge', 'Bullish setup if breakout occurs'],
        ['Support Zone', '\u20b9100\u2013110', 'Multiple recent tests'],
        ['Resistance Zone', '\u20b9130\u2013135', 'Falling trendline resistance'],
        ['Key Breakout Level', '\u20b9135\u2013140', 'Would signal trend reversal'],
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
        '<b>Pattern:</b> A falling wedge (bullish pattern) has been identified. The stock is at the '
        'opportunity zone per some analysts. However, with a beta of 2.22, the stock is significantly '
        'more volatile than the market. The 37% decline from listing is partly due to demerger supply '
        'overhang and partly reflects broader market weakness in the Consumer Durables space '
        '(Nifty Consumer Durables index down ~1.6% YoY).',
        body_style
    ))

    story.append(Paragraph(
        'Sources: TradingView (NSE:ABLBL), MarketScreener, EquityPandit, MunafaSutra (data as of late Jan 2026)',
        source_style
    ))

    story.append(PageBreak())

    # =====================================================
    # SECTION 5: SECTOR & COMPETITIVE CONTEXT
    # =====================================================
    story.append(Paragraph('4. Sector & Competitive Context', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Indian Branded Apparel Market', subheading_style))
    story.append(Paragraph(
        'The Indian apparel market was valued at <b>USD 116 billion in 2025</b> and is projected to '
        'grow at 4\u20135% CAGR to USD 172 billion by 2034 (Market Research Future). '
        'The branded segment is growing faster at 10\u201312% CAGR, with branded apparel expected to '
        'account for over 50% of apparel spend by 2030. Key growth drivers include rising disposable '
        'incomes, urbanization, premiumization, and shift from unorganized to organized retail.',
        body_style
    ))
    story.append(Paragraph(
        'ABLBL\'s Madura Fashion portfolio is recognized as <b>India\'s largest branded menswear player</b>, '
        'with dominant positions in the premium (Louis Philippe, Van Heusen) and mass-premium '
        '(Allen Solly, Peter England) segments. These brands have 25+ years of heritage and strong '
        'brand recall across the country.',
        body_style
    ))

    story.append(Paragraph('Peer Comparison \u2014 Branded Apparel', subheading_style))
    peer_data = [
        ['Company', 'P/E (TTM)', 'Forward P/E', 'Revenue (\u20b9 Cr)', '1Y Return'],
        ['ABLBL', '80.4x (Screener)', '~61x', '8,164', '-37% (from listing)'],
        ['Trent', '97x', '~80x', '~16,500', 'Positive'],
        ['Page Industries', '51x', '~45x', '~4,800', 'Mixed'],
        ['Raymond', '25x', '~20x', '~9,500', 'Moderate'],
        ['Vedant Fashions', '31x', '~28x', '~1,450', 'Negative'],
    ]
    peer_table = Table(peer_data, colWidths=[2.8*cm, 2*cm, 2*cm, 2.5*cm, 3.5*cm])
    peer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#edf2f7')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 2), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(peer_table)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'ABLBL\'s Screener.in P/E of 80.4x reflects limited reported quarters post-demerger. '
        'The forward PE of ~61x (based on normalized FY27 earnings) is the fairer comparison. Even at 61x forward, '
        'ABLBL trades at a premium to Page (45x) and Raymond (20x), but at a discount to Trent (80x).',
        source_style
    ))

    story.append(Image(chart_paths['peers'], width=16*cm, height=7*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Nifty Consumer Durables Index', subheading_style))
    story.append(Paragraph(
        'The Nifty Consumer Durables Index stands at <b>36,229</b> (Feb 4, 2026) with a 52-week range of '
        '32,205\u201340,472. <b>1-year return is -1.6%</b>, underperforming the broader Nifty 50. '
        'ABLBL\'s decline of 37% from listing (or ~-7% over 1 month, -9% over 1 month per MarketScreener) '
        'is significantly worse than the sector, suggesting stock-specific factors (demerger overhang, '
        'limited history) beyond the sector correction.',
        body_style
    ))

    story.append(Paragraph('Raw Material & Cotton Context', subheading_style))
    story.append(Paragraph(
        '<b>Cotton prices are rising:</b> India\'s cotton output is projected to fall 1.7% YoY to 29.2 Mn bales '
        'in CY 2026 \u2014 lowest in 10 years (ICRA). Cotton sown area is 20% below 2021 peak. '
        'Pre-sowing estimates put cotton at \u20b96,800\u20137,200/quintal. Import dependency is up 85% YoY. '
        'The 11% import duty on cotton persists, keeping domestic prices above global benchmarks.<br/><br/>'
        '<b>Impact on ABLBL:</b> As a branded apparel company (not a textile manufacturer), ABLBL has '
        'relatively better pricing power to pass through cotton cost increases. However, sustained raw '
        'material inflation could compress EBITDA margins, especially for the mass-premium Peter England brand. '
        'Management has not explicitly flagged cotton as a near-term risk.',
        body_style
    ))

    story.append(Paragraph('Store Expansion Trajectory', subheading_style))
    story.append(Image(chart_paths['stores'], width=14*cm, height=7*cm))

    story.append(Paragraph(
        'Sources: Market Research Future (apparel market), Smart-Investing.in (P/E data Jan 2026), '
        'Screener.in, ICRA (cotton outlook), Fibre2Fashion, Nifty Indices (Consumer Durables), '
        'MarketScreener, StockAnalysis.com',
        source_style
    ))

    story.append(PageBreak())

    # =====================================================
    # SECTION 6: VALUATION & ANALYST VIEWS
    # =====================================================
    story.append(Paragraph('5. Valuation & Analyst Views', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Brokerage Target Prices', subheading_style))
    analyst_data = [
        ['Brokerage', 'Rating', 'Target (\u20b9)', 'Methodology', 'Key Thesis'],
        ['HDFC Securities', 'Buy', '180', '25x Sep-27 EV/EBITDA', '10% rev CAGR, 19% EBITDA CAGR FY25\u201328'],
        ['Morgan Stanley', 'Overweight', '175', '13x FY27E EV/EBITDA', 'Defensive discretionary play'],
        ['Bernstein', 'Mkt-Perform', '170', 'Fair value', '9.5% rev growth, 10% EBITDA margin'],
        ['Motilal Oswal', 'Neutral', '190', '15x FY27E EV/EBITDA', '10% rev CAGR, FCF \u20b91,100 Cr'],
        ['Consensus (9 analysts)', 'Buy', '160\u2013164', 'Avg target', 'Range: \u20b9138\u2013\u20b9180'],
    ]
    analyst_table = Table(analyst_data, colWidths=[2.8*cm, 2*cm, 1.5*cm, 3*cm, 5.5*cm])
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
        '<b>Implied Upside:</b> From \u20b9105 (Jan 30 close), the analyst target range of '
        '\u20b9138\u2013\u20b9190 implies <b>31% to 81% upside</b>. Even the most conservative target (\u20b9138) '
        'suggests 31% upside. However, note that Bernstein\'s pre-listing fair value estimate was \u20b9185\u2013215 '
        '\u2014 they subsequently cut their target to \u20b9170 post-listing, citing casualization trends '
        'and competition concerns.',
        callout_green
    ))

    story.append(Paragraph(
        '<b>Note on Bernstein:</b> At the time of ABLBL\'s listing (June 2025), Bernstein projected '
        'a fair value of \u20b9185\u2013215. They later initiated formal coverage with a Market-Perform '
        'rating and \u20b9170 target, significantly below their initial estimate. This suggests that '
        'post-listing realities (debt, supply overhang, weak Q1/Q2) moderated their view.',
        body_style
    ))

    story.append(Paragraph('Valuation Context', subheading_style))
    story.append(Paragraph(
        'ABLBL\'s valuation is complex due to the demerger:\n'
        '\u2022 <b>Trailing PE:</b> Screener.in reports 80.4x; other sources show higher figures due to limited quarters of PAT. Use forward PE.\n'
        '\u2022 <b>Forward PE of ~61x</b> (StockAnalysis.com) is the relevant metric.\n'
        '\u2022 <b>EV/EBITDA of 13x FY27E</b> (Morgan Stanley) is actually quite reasonable for a branded '
        'apparel company, compared to 37x average for discretionary retail peers in their coverage.\n'
        '\u2022 <b>P/B of 10.8x</b> reflects brand intangible value, not asset-heavy distortion.\n'
        '\u2022 Peer context: Trent at 97x PE (overvalued?), Page at 51x (fair?), Raymond at 25x (value?).',
        body_style
    ))

    story.append(Paragraph(
        'Sources: HDFC Securities (Sep 2, 2025), Morgan Stanley (Sep 10, 2025), Bernstein, '
        'Motilal Oswal, TradingView, MarketScreener (9-analyst consensus)',
        source_style
    ))

    story.append(PageBreak())

    # =====================================================
    # SECTION 7: CONCLUSION & VALUATION MATH
    # =====================================================
    story.append(Paragraph('6. Catalysts, Risks & Conclusion', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Management Guidance', subheading_style))
    mgmt = [
        '<b>Revenue Target:</b> 13% revenue CAGR to FY30 (management). HDFC Securities/Morgan Stanley '
        'more conservative at 10% CAGR FY25\u201328E.',
        '<b>EBITDA Margin:</b> Targeting >18% by FY30, up from 16% in H1 FY26. Already hit 18.4% overall '
        'and 20.6% for Lifestyle in Q3 FY26.',
        '<b>Store Expansion:</b> 250 stores/year, reaching 4,500 stores and 7.3 Mn sq ft by FY30.',
        '<b>Debt-Free:</b> Target to become debt-free in 2\u20133 years. Motilal Oswal projects \u20b91,100 Cr '
        'cumulative FCF over FY25\u201328E to fund this.',
        '<b>Emerging Businesses:</b> Targeting 18\u201320% growth for Reebok, American Eagle, VH Innerwear.',
        '<b>Quote:</b> "The growth momentum is expected to sustain as we continue to power our product '
        'innovation engine while accelerating distribution expansion."',
    ]
    for m in mgmt:
        story.append(Paragraph(f'\u2022 {m}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Growth Catalysts (Bull Case)', subheading_style))
    bull = [
        '<b>Store Expansion:</b> 250 stores/year adds ~\u20b9600\u2013800 Cr revenue at maturity. '
        '220+ stores already added in 9M FY26.',
        '<b>Emerging Brands Turning Profitable:</b> Reebok, American Eagle posting profitable growth. '
        'EBITDA margin expanded 790 bps YoY in Q3.',
        '<b>Premiumization:</b> Louis Philippe and Van Heusen command premium pricing. '
        'Product innovation driving ASP growth.',
        '<b>Casualwear Transformation:</b> Allen Solly repositioning for casualwear trend. '
        'Van Heusen diversifying into innerwear, youth segments.',
        '<b>Path to Debt-Free:</b> Strong FCF generation (CFO \u20b91,144 Cr in FY25) should eliminate debt by FY28.',
        '<b>Online Channel:</b> Digital/e-commerce growing as a share of revenue.',
        '<b>Demerger Unlocks Value:</b> Standalone listing allows market to assign specific multiples '
        'to profitable brands vs. ABFRL\'s conglomerate discount.',
    ]
    for b in bull:
        story.append(Paragraph(f'\u2022 {b}', bullet_style))

    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph('Key Risks (Bear Case)', subheading_style))
    bear = [
        '<b>Limited Track Record:</b> Less than 1 year listed. No multi-year standalone financials. '
        'Investors are buying on faith in legacy brand strength.',
        '<b>Stock Down 37% from Listing:</b> Significant demerger supply overhang. '
        'ABFRL shareholders who didn\'t want lifestyle brands are likely still selling.',
        '<b>Debt Overhang:</b> \u20b9781 Cr net debt + low interest coverage. NCD issuance of \u20b9500 Cr '
        'suggests ongoing capital needs. Note: The QIP was done by ABFRL pre-demerger, not ABLBL.',
        '<b>Seasonality Risk:</b> Q3 (festive) contributes disproportionately to profits. '
        'Q1/Q2 PAT of only \u20b924 Cr and \u20b923 Cr respectively \u2014 weakness outside festive season.',
        '<b>Cotton Cost Inflation:</b> Indian cotton output at 10-year low. Rising MSP and import dependency '
        'could compress margins, especially for Peter England.',
        '<b>Casualization Threat:</b> Core brands (Louis Philippe, Van Heusen) are formal/premium focused. '
        'India\'s shift to casualwear favors Allen Solly but threatens the formal segment. '
        'Bernstein cites this as a structural concern.',
        '<b>Competition:</b> Trent (Zudio, Westside), Reliance Retail, H&M India, Myntra private labels '
        'are all intensifying competition in branded apparel.',
        '<b>High P/B (10.8x):</b> Premium valuation with limited margin of safety.',
    ]
    for b in bear:
        story.append(Paragraph(f'\u2022 {b}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    # ── Valuation Methodology ──
    story.append(Paragraph('Valuation Methodology: Forward EPS x P/E Multiple', subheading_style))
    story.append(Paragraph(
        'The scenario analysis below uses a <b>forward earnings-multiple approach</b>. '
        'This is not a DCF model. Given ABLBL\'s limited history, we triangulate with '
        'EV/EBITDA (Morgan Stanley approach) as a sanity check.',
        body_style
    ))

    story.append(Paragraph('<b>Step 1: Establish Current EPS</b>', body_style))
    eps_data = [
        ['Metric', 'Value', 'Source'],
        ['TTM Net Profit (9M FY26 ann.)', '~\u20b9145\u2013180 Cr', 'Screener.in / 9M actual \u20b9110 Cr'],
        ['Market Cap', '~\u20b914,103 Cr', 'Screener.in (Jan 2026)'],
        ['Price', '\u20b9105', 'NSE close (Jan 30, 2026)'],
        ['Shares Outstanding', '122.03 Cr', '1:1 demerger allocation'],
        ['Trailing EPS (reported)', '~\u20b90.46/share', 'Yahoo Finance (limited quarters)'],
        ['Annualized EPS (9M FY26)', '~\u20b91.20/share', '9M PAT \u20b9110 Cr / 122 Cr shares, annualized'],
        ['Forward EPS (FY27E)', '~\u20b92.0\u20132.2/share', 'StockAnalysis.com (fwd PE 61x implies this)'],
        ['Sanity Check: Fwd P/E', '105 / 1.7 = ~62x', 'Roughly matches reported ~61x fwd PE'],
    ]
    eps_table = Table(eps_data, colWidths=[3.5*cm, 3.5*cm, 7.5*cm])
    eps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(eps_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>EPS Complexity Note:</b> ABLBL\'s EPS is hard to pin down. Trailing EPS of \u20b90.46 '
        'reflects only partial reported quarters. The annualized 9M FY26 EPS of ~\u20b91.20 is more '
        'realistic but inflated by the strong Q3. We use an estimated FY26E EPS of ~\u20b91.4\u20131.5 '
        '(midpoint) and project FY27E from there.',
        body_style
    ))

    story.append(Paragraph('<b>Step 2: Project FY27E EPS by Scenario</b>', body_style))
    story.append(Paragraph(
        'Growth rate sources: HDFC Securities projects 19% EBITDA CAGR (FY25\u201328E). '
        'Morgan Stanley expects 10% revenue CAGR. Bernstein is more conservative at 9.5% revenue growth.',
        body_style
    ))

    proj_data = [
        ['', 'Bull', 'Base', 'Bear'],
        ['FY26E PAT', '\u20b9200 Cr (strong H2)', '\u20b9170 Cr (norm.)', '\u20b9140 Cr (weak H2)'],
        ['FY26E EPS', '\u20b91.64', '\u20b91.39', '\u20b91.15'],
        ['FY27E PAT Growth', '+25% (HDFC CAGR)', '+15% (Morgan Stanley)', '+5% (margin compression)'],
        ['FY27E EPS', '\u20b92.05', '\u20b91.60', '\u20b91.21'],
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

    story.append(Paragraph('<b>Step 3: Apply P/E Multiple \u2192 Target Price</b>', body_style))
    story.append(Paragraph(
        'P/E assumptions anchored to peers (Jan 2026): Trent ~80x fwd, Page ~45x fwd, '
        'Raymond ~20x fwd, Vedant Fashions ~28x fwd. ABLBL\'s forward PE of 61x is already '
        'rich; we vary by scenario. Morgan Stanley\'s EV/EBITDA of 13x FY27E as cross-check.',
        body_style
    ))

    scenario_data = [
        ['Scenario', 'FY27E EPS', 'P/E Assumed', 'Price Target', 'Return from \u20b9105', 'Probability'],
        ['Bull', '\u20b92.05', '75\u201385x',
         '\u20b9154\u2013174', '+47% to +66%', '20%'],
        ['Base', '\u20b91.60', '60\u201370x',
         '\u20b996\u2013112', '-9% to +7%', '50%'],
        ['Bear', '\u20b91.21', '30\u201340x',
         '\u20b936\u201348', '-54% to -65%', '30%'],
    ]
    scenario_table = Table(scenario_data, colWidths=[1.8*cm, 2.2*cm, 2.2*cm, 2.8*cm, 3.3*cm, 2.5*cm])
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

    # Step 4: Probability-weighted expected value
    story.append(Paragraph('<b>Step 4: Probability-Weighted Expected Value</b>', body_style))
    story.append(Paragraph(
        'Assigning probabilities based on current evidence:',
        body_style
    ))
    prob_points = [
        '<b>Bull (20%):</b> Requires revenue growth accelerating to 13%+ (management target), margins '
        'sustaining at 18%+, demerger overhang clearing, and market assigning growth premium PE. '
        'Strong Q3 supports this case but Q1/Q2 weakness tempers conviction. '
        'Named analyst targets (\u20b9170\u2013190) cluster in this range.',
        '<b>Base (50%):</b> Most likely. ABLBL delivers 10% revenue CAGR (Morgan Stanley/HDFC estimate), '
        'margins improve modestly, debt reduces but doesn\'t vanish by FY27. Stock remains range-bound '
        'as market waits for multi-quarter consistency. Forward PE compresses from 61x to 60\u201370x range.',
        '<b>Bear (30%):</b> Higher than typical because of specific risks: (a) limited track record '
        'means any execution miss will be punished heavily, (b) demerger supply overhang may persist '
        'for 6\u201312 months, (c) cotton cost inflation could compress margins, (d) casualization trend '
        'threatens formal brand portfolios, (e) the stock has already fallen 37% \u2014 the market is '
        'clearly cautious. A 30% bear weight reflects these tangible headwinds.',
    ]
    for pp in prob_points:
        story.append(Paragraph(f'\u2022 {pp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    ev_data = [
        ['Scenario', 'Midpoint Price', 'Probability', 'Weighted Value'],
        ['Bull', '\u20b9164', '20%', '\u20b932.80'],
        ['Base', '\u20b9104', '50%', '\u20b952.00'],
        ['Bear', '\u20b942', '30%', '\u20b912.60'],
        ['', '', 'Expected Value \u2192', '\u20b997'],
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
        '<b>Probability-weighted expected price: \u20b997</b> \u2014 implying ~8% downside from \u20b9105. '
        'This is essentially a <b>hold/fair value</b> signal, suggesting the stock is approximately '
        'fairly priced at current levels when risk-adjusted. The analyst targets of \u20b9159\u2013190 '
        'are significantly more optimistic, reflecting their base/bull case views without probability weighting.',
        callout_orange
    ))

    story.append(Spacer(1, 0.3*cm))

    # EV/EBITDA Cross-Check
    story.append(Paragraph('EV/EBITDA Cross-Check (Morgan Stanley Methodology)', subheading_style))
    story.append(Paragraph(
        'Morgan Stanley values ABLBL at <b>13x FY27E EV/EBITDA</b>, arriving at a target of \u20b9175. '
        'Let us validate this:\n'
        '\u2022 FY27E EBITDA estimate (at 10% CAGR on TTM rev + improving margins): ~\u20b91,600\u20131,700 Cr.\n'
        '\u2022 At 13x EV/EBITDA: EV = \u20b920,800\u201322,100 Cr.\n'
        '\u2022 Less net debt (~\u20b9500 Cr by FY27E): Equity value = \u20b920,300\u201321,600 Cr.\n'
        '\u2022 Per share (122 Cr shares): \u20b9166\u2013177/share.\n'
        '\u2022 This is close to Morgan Stanley\'s target of \u20b9175. \u2713\n\n'
        'However, 13x EV/EBITDA is well below the 37x average for discretionary retail peers in Morgan '
        'Stanley\'s coverage. If the market values ABLBL closer to peers (20\u201325x), the target would be '
        '\u20b9250\u2013300+. Conversely, if execution disappoints and the stock trades at 8\u201310x, '
        'fair value would be \u20b990\u2013120.',
        body_style
    ))

    # Methodology limitations
    story.append(Paragraph('Methodology Limitations (Transparency Note)', subheading_style))
    limit_points = [
        '<b>Extremely Limited Data:</b> ABLBL has been listed for only 7 months. Any valuation is '
        'heavily reliant on estimates and projections rather than observed multi-year trends.',
        '<b>Not a DCF:</b> A proper intrinsic value requires segment-level revenue build-up, '
        'margin assumptions, capex forecasting, and WACC-based discounting.',
        '<b>EPS estimates are uncertain:</b> Forward EPS of \u20b91.6\u20132.0 is derived top-down from '
        'brokerage CAGRs, not a bottoms-up P&L forecast. Actual EPS could deviate significantly.',
        '<b>P/E assumptions are subjective:</b> The 30\u201385x range is wide because ABLBL has no '
        'established trading multiple. Anchor to peer comps is the best available method.',
        '<b>Bear probability is high (30%):</b> This reflects the genuine uncertainty for a newly listed stock. '
        'Different analysts would assign different weights.',
        '<b>Demerger accounting:</b> Transferred debt, brand intangibles, and restructured balance sheet '
        'make year-over-year comparisons unreliable for at least 2\u20133 years.',
    ]
    for lp in limit_points:
        story.append(Paragraph(f'\u2022 {lp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Verdict: HOLD / NEUTRAL', subheading_style))
    story.append(Paragraph(
        '<b>ABLBL houses India\'s most iconic branded menswear portfolio.</b> '
        'Louis Philippe, Van Heusen, Allen Solly, and Peter England are heritage brands with '
        '25+ years of consumer trust, dominant distribution, and improving profitability. '
        'The Q3 FY26 results (20.6% Lifestyle EBITDA margin, 9% Lifestyle revenue growth, '
        'PAT \u20b966 Cr / EPS \u20b90.54) demonstrate genuine operational momentum. '
        'LTL growth of 6% overall marks the 6th consecutive quarter of positive retail LTL.',
        body_style
    ))
    story.append(Paragraph(
        '<b>However, our probability-weighted expected value of \u20b997 is below the CMP of \u20b9105, '
        'which does not support an ACCUMULATE rating.</b> Verdict: <b>HOLD / NEUTRAL.</b> '
        'The analyst consensus target of \u20b9159\u2013164 (\u20b9138\u2013190 range) suggests meaningful '
        'upside (50%+) if execution sustains, and HDFC Securities targets \u20b9180 using 25x Sep-27 '
        'EV/EBITDA. However, the 37% decline from listing and high bear probability (30%) suggest '
        'the market demands proof of multi-quarter consistency before re-rating.',
        body_style
    ))
    story.append(Paragraph(
        'The key variable is <b>whether Q3\'s strong results represent sustainable improvement or '
        'seasonal outperformance</b>. Investors should watch Q4 FY26 (expected Feb 25, 2026) closely. '
        'If Q4 delivers margins above 17% and revenue growth above 8%, it would validate the improvement '
        'thesis and potentially trigger a re-rating toward analyst targets of \u20b9160\u2013180.',
        body_style
    ))
    story.append(Paragraph(
        '<b>On balance: HOLD / NEUTRAL. ABLBL is a quality business trading at approximately fair value '
        'after a sharp post-listing correction. The risk-reward is balanced, not clearly favorable. '
        'Suited for patient investors already holding, willing to wait 12\u201318 months for '
        'multi-quarter validation. New buyers should wait for either (a) price dip to \u20b990\u2013100 '
        'for better risk-reward, or (b) Q4 FY26 confirmation of margin/growth trends. '
        'Not suitable for risk-averse investors given the limited track record, '
        'debt burden (\u20b9781 Cr), and high beta (2.22x).</b>',
        body_style
    ))

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cbd5e0')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>IMPORTANT DISCLAIMER:</b> This report is generated for informational and educational '
        'purposes only. It does not constitute investment advice, a recommendation to buy, sell, '
        'or hold any security, or an offer of any kind. ABLBL is a newly listed stock (June 2025) '
        'with less than 1 year of trading history. All data is sourced from publicly available '
        'information as of February 4, 2026. Past performance does not guarantee future results. '
        'Stock market investments carry risk of capital loss. Please consult a SEBI-registered '
        'investment advisor before making any investment decisions. The author has no position '
        'in Aditya Birla Lifestyle Brands Limited.',
        disclaimer_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Data Sources:</b> Screener.in (primary financial data) | Business Standard | '
        'Aditya Birla Group Press Releases (adityabirla.com) | NSE India | Yahoo Finance | '
        'HDFC Securities | Morgan Stanley | Bernstein | Motilal Oswal | TradingView | '
        'MarketScreener | StockAnalysis.com | Trendlyne | ICRA (cotton outlook) | '
        'Market Research Future (apparel market) | Fibre2Fashion',
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
        'brands': create_brand_chart(),
        'price': create_price_chart(),
        'peers': create_peer_chart(),
        'stores': create_store_chart(),
    }
    print(f"Charts created ({len(charts)} total). Building PDF...")
    build_pdf(charts)
    print("Done!")
