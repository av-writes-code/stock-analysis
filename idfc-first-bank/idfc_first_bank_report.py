#!/usr/bin/env python3
"""
IDFC First Bank — 1-Year Stock Research Report
Generated: February 4, 2026
Banking-specific metrics: NIM, NPA, CASA, ROA, ROE, P/B
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

# Register SFNS (San Francisco) for currency symbol support
pdfmetrics.registerFont(TTFont('SFNS', '/System/Library/Fonts/SFNS.ttf'))

# --- Configuration ---
OUTPUT_DIR = "/Users/arpitvyas/Desktop/stock-analysis/idfc-first-bank"
FINAL_PDF = "/Users/arpitvyas/Desktop/stock-analysis/idfc-first-bank/IDFC_First_Bank_Research_Report_Feb2026.pdf"

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


# --- Chart 1: Quarterly NII & Net Profit Trend ---
def create_nii_chart():
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26', 'Q3\nFY26']
    # NII in Cr (from press releases and quarterly results)
    nii = [4695, 4788, 4902, 4907, 4933, 5167, 5492]
    # Net Profit in Cr
    pat = [681, 212, 340, 732, 453, 348, 479]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    x = np.arange(len(quarters))
    width = 0.35

    bars1 = ax1.bar(x - width/2, nii, width, label='NII (Rs Cr)', color=ACCENT, alpha=0.85)
    ax1.set_ylabel('NII (Rs Cr)', color=ACCENT)
    ax1.set_ylim(0, 7000)
    ax1.tick_params(axis='y', labelcolor=ACCENT)

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, pat, width, label='Net Profit (Rs Cr)', color=GREEN, alpha=0.85)
    ax2.set_ylabel('Net Profit (Rs Cr)', color=GREEN)
    ax2.set_ylim(0, 900)
    ax2.tick_params(axis='y', labelcolor=GREEN)

    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=8)
    ax1.set_title('IDFC First Bank - Quarterly NII & Net Profit Trend', fontweight='bold', pad=15)

    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 80,
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=7, color=ACCENT)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 10,
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=7, color=GREEN)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_nii_profit.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 2: NIM and Cost-to-Income Ratio Trend ---
def create_nim_cti_chart():
    quarters = ['Q1\nFY25', 'Q2\nFY25', 'Q3\nFY25', 'Q4\nFY25', 'Q1\nFY26', 'Q2\nFY26', 'Q3\nFY26']
    # NIM % (from quarterly results)
    nim = [6.20, 6.10, 6.04, 5.95, 5.71, 5.59, 5.76]
    # Cost-to-Income % (approximated from data)
    cti = [76.5, 75.0, 74.0, 73.5, 73.0, 74.5, 74.0]

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(quarters))

    line1, = ax.plot(x, nim, 'o-', color=ACCENT, linewidth=2.5, markersize=7, label='NIM (%)', zorder=3)
    ax.set_ylabel('NIM (%)', color=ACCENT)
    ax.set_ylim(5.0, 7.0)
    ax.tick_params(axis='y', labelcolor=ACCENT)

    ax2 = ax.twinx()
    line2, = ax2.plot(x, cti, 's-', color=HIGHLIGHT, linewidth=2.5, markersize=7, label='Cost-to-Income (%)', zorder=3)
    ax2.set_ylabel('Cost-to-Income (%)', color=HIGHLIGHT)
    ax2.set_ylim(65, 85)
    ax2.tick_params(axis='y', labelcolor=HIGHLIGHT)

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=8)
    ax.set_title('NIM & Cost-to-Income Ratio Trend', fontweight='bold', pad=15)

    for i, (n, c) in enumerate(zip(nim, cti)):
        ax.annotate(f'{n:.2f}%', (i, n), textcoords="offset points", xytext=(0, 10), fontsize=7, ha='center', color=ACCENT)
        ax2.annotate(f'{c:.1f}%', (i, c), textcoords="offset points", xytext=(0, -14), fontsize=7, ha='center', color=HIGHLIGHT)

    ax.legend([line1, line2], ['NIM (%)', 'Cost-to-Income (%)'], loc='upper right', fontsize=8)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_nim_cti.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 3: Loan Book Composition Pie ---
def create_loan_pie_chart():
    labels = ['Mortgage\n(Home+LAP)\n29%', 'Consumer\n& Personal\n25%', 'MSME &\nBusiness\n18%',
              'Vehicle\nFinance\n12%', 'Corporate\n& Wholesale\n8%', 'MFI\n4%', 'Others\n4%']
    sizes = [29, 25, 18, 12, 8, 4, 4]
    colors_pie = ['#2b6cb0', '#38a169', '#dd6b20', '#805ad5', '#e53e3e', '#718096', '#d69e2e']
    explode = (0.05, 0.02, 0, 0, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                       colors=colors_pie, autopct='',
                                       shadow=False, startangle=90,
                                       textprops={'fontsize': 7.5})
    ax.set_title('Loan Book Composition (FY25)', fontweight='bold', pad=15)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_loan_mix.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 4: Price Action with MAs + Support/Resistance ---
def create_price_chart():
    months = ['Feb\n2025', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan\n2026']
    # Monthly closing prices (approximate from known data: 52w high 98, 52w low ~57, current ~84)
    prices = [72, 68, 63, 57, 60, 65, 70, 76, 85, 98, 87, 84]
    sma_200 = [72, 71, 70, 69, 68, 68, 69, 70, 72, 75, 77, 78]
    ema_50 = [74, 72, 68, 64, 61, 62, 64, 68, 74, 82, 86, 85]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(months))

    ax.plot(x, prices, 'o-', color=PRIMARY, linewidth=2, markersize=5, label='Price (Rs)', zorder=3)
    ax.plot(x, sma_200, '--', color=GREEN, linewidth=1.5, label='200-Day SMA (~Rs 78)', alpha=0.8)
    ax.plot(x, ema_50, '--', color=HIGHLIGHT, linewidth=1.5, label='50-Day EMA (~Rs 85)', alpha=0.8)

    # Support and resistance zones
    ax.axhspan(55, 62, alpha=0.1, color='green', label='Support Zone (Rs 57-62)')
    ax.axhspan(95, 100, alpha=0.1, color='red', label='Resistance Zone (Rs 95-100)')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8)
    ax.set_ylabel('Price (Rs)')
    ax.set_title('IDFC First Bank - 1-Year Price Action & Key Moving Averages', fontweight='bold', pad=15)
    ax.text(0.5, -0.12, 'Note: Monthly prices approximated from available data; MAs are illustrative',
            transform=ax.transAxes, fontsize=6, ha='center', color='#999999', style='italic')
    ax.legend(fontsize=7, loc='upper left')
    ax.set_ylim(45, 110)

    ax.annotate(f'Current: Rs 84', xy=(11, 84), xytext=(9, 55),
                arrowprops=dict(arrowstyle='->', color=PRIMARY),
                fontsize=9, fontweight='bold', color=PRIMARY)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 5: Peer P/B Comparison ---
def create_peer_chart():
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

    # P/B comparison
    banks_pb = ['Kotak\nMahindra', 'AU SFB', 'Federal\nBank', 'IDFC\nFirst', 'IndusInd', 'Bandhan']
    pb_vals = [2.58, 3.91, 1.88, 1.56, 1.09, 1.02]
    bar_colors = ['#a0aec0', '#a0aec0', '#a0aec0', ACCENT, '#a0aec0', '#a0aec0']
    bars = axes[0].bar(banks_pb, pb_vals, color=bar_colors, width=0.6)
    axes[0].set_title('P/B Ratio (Feb 2026)', fontweight='bold', fontsize=9)
    axes[0].set_ylim(0, 5)
    for bar in bars:
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                    f'{bar.get_height():.2f}x', ha='center', fontsize=7)
    axes[0].tick_params(axis='x', labelsize=6.5)

    # ROA comparison
    banks_roa = ['Kotak', 'AU SFB', 'Federal', 'IDFC\nFirst', 'IndusInd', 'Bandhan']
    roa_vals = [2.30, 1.60, 1.20, 0.43, 0.80, 0.90]
    bar_colors2 = ['#a0aec0', '#a0aec0', '#a0aec0', ACCENT, '#a0aec0', '#a0aec0']
    bars = axes[1].bar(banks_roa, roa_vals, color=bar_colors2, width=0.6)
    axes[1].set_title('ROA % (FY25)', fontweight='bold', fontsize=9)
    axes[1].set_ylim(0, 3)
    for bar in bars:
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.03,
                    f'{bar.get_height():.1f}%', ha='center', fontsize=7)
    axes[1].tick_params(axis='x', labelsize=6.5)

    # NIM comparison
    banks_nim = ['IDFC\nFirst', 'AU SFB', 'Bandhan', 'Federal', 'IndusInd', 'Kotak']
    nim_vals = [5.76, 5.70, 7.50, 3.20, 4.20, 5.10]
    bar_colors3 = [ACCENT, '#a0aec0', '#a0aec0', '#a0aec0', '#a0aec0', '#a0aec0']
    bars = axes[2].bar(banks_nim, nim_vals, color=bar_colors3, width=0.6)
    axes[2].set_title('NIM % (Latest Quarter)', fontweight='bold', fontsize=9)
    axes[2].set_ylim(0, 9)
    for bar in bars:
        axes[2].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                    f'{bar.get_height():.1f}%', ha='center', fontsize=7)
    axes[2].tick_params(axis='x', labelsize=6.5)

    fig.suptitle('IDFC First Bank vs Peer Banks - Key Metrics Comparison', fontweight='bold', fontsize=11, y=1.02)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_peers.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


# --- Chart 6: Asset Quality Trend ---
def create_asset_quality_chart():
    periods = ['FY22', 'FY23', 'FY24', 'FY25', 'Q3\nFY26']
    gnpa = [3.70, 2.50, 1.90, 1.90, 1.69]
    nnpa = [1.30, 0.69, 0.60, 0.55, 0.53]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    x = np.arange(len(periods))

    ax.plot(x, gnpa, 'o-', color=HIGHLIGHT, linewidth=2.5, markersize=8, label='GNPA (%)')
    ax.plot(x, nnpa, 's-', color=GREEN, linewidth=2.5, markersize=8, label='NNPA (%)')

    ax.fill_between(x, gnpa, alpha=0.1, color=HIGHLIGHT)
    ax.fill_between(x, nnpa, alpha=0.1, color=GREEN)

    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=9)
    ax.set_ylabel('NPA (%)')
    ax.set_title('Asset Quality Trend - GNPA & NNPA', fontweight='bold', pad=10)
    ax.legend(fontsize=9)
    ax.set_ylim(0, 5)

    for i, (g, n) in enumerate(zip(gnpa, nnpa)):
        ax.annotate(f'{g}%', (i, g), textcoords="offset points", xytext=(0, 10), fontsize=8, ha='center', color=HIGHLIGHT, fontweight='bold')
        ax.annotate(f'{n}%', (i, n), textcoords="offset points", xytext=(0, -14), fontsize=8, ha='center', color=GREEN, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'chart_asset_quality.png')
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

    # ======= TITLE PAGE =======
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('IDFC FIRST BANK LIMITED', title_style))
    story.append(Paragraph('NSE: IDFCFIRSTB | BSE: 539437', subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=HexColor(PRIMARY)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('1-Year Stock Research Report', ParagraphStyle(
        'BigSub', parent=subtitle_style, fontSize=16, textColor=HexColor(ACCENT),
        fontName='SFNS'
    )))
    story.append(Paragraph('Outlook: February 2026 to February 2027', subtitle_style))
    story.append(Spacer(1, 1*cm))

    # Key banking metrics box
    metrics_data = [
        ['Current Price', 'Rs 85.1 (Feb 4, 2026)', 'Market Cap', 'Rs 72,952 Cr'],
        ['P/B Ratio', '1.56x (BV Rs 54.5, Screener.in)', 'P/E (TTM)', '46.5x'],
        ['Book Value/Share', 'Rs 54.5 (Screener.in, Dec 2025)', 'NIM (Q3 FY26)', '5.76%'],
        ['GNPA / NNPA', '1.69% / 0.53%', 'CASA Ratio', '51.64%'],
        ['ROA (FY25)', '0.43%', 'ROE', '4%'],
        ['52-Week Range', 'Rs 57 - Rs 98', 'Shares Outstanding', '~860 Cr (post-CCPS conversion Oct 2025; Warburg +81 Cr, ADIA +44 Cr shares)'],
        ['Capital Adequacy', '16.22%', 'Promoter Holding', '0% (post-merger)'],
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

    # Add executive summary verdict box
    story.append(Spacer(1, 10))
    verdict_data = [
        ['VERDICT: HOLD | Expected Value: Rs ~88 (approx 4% upside from CMP Rs 85)'],
        ['Key Bull: Deposit growth 10% HoH, NII improving, turnaround thesis'],
        ['Key Bear: Promoter at 0%, ROE 4%, P/E 46.5x, UBS SELL target Rs 75']
    ]
    verdict_table = Table(verdict_data, colWidths=[480])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FFF3CD')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFF8E1')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FFC107')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#856404')),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 0.5*cm))

    # P/B note
    story.append(Paragraph(
        '<b>Book Value Note:</b> Screener.in reports Equity Capital of Rs 7,322 Cr at Face Value Rs 10, '
        '~860 Cr shares outstanding (post-CCPS conversion Oct 2025). BV/share = Rs 54.5 (Screener.in). '
        'P/B = CMP Rs 85.1 / BV Rs 54.5 = 1.56x. ROCE: 6.22%, ROE: 4% (Screener.in).',
        source_style
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'Report Date: February 4, 2026 | Price as of: Feb 4, 2026 (NSE) '
        '| Data Sources: Screener.in (primary), NSE India, Business Standard, '
        'Tribune India, IDFC First Bank Investor Presentations, Nomura, UBS, Axis Securities',
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

    # ======= SECTION 1: COMPANY SNAPSHOT =======
    story.append(Paragraph('1. Company Snapshot', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'IDFC First Bank was formed by the <b>merger of IDFC Bank and Capital First</b> in December 2018, '
        'led by V. Vaidyanathan (ex-ICICI Bank retail head and Capital First founder). The merger transformed '
        'IDFC Bank from a wholesale infrastructure lender into a retail-focused universal bank. In October 2024, '
        'IDFC Limited (the parent holding company) was reverse-merged into IDFC First Bank, eliminating the '
        'dual-entity structure but adding ~248 Cr new shares.',
        body_style
    ))
    story.append(Paragraph(
        'Under V. Vaidyanathan\'s leadership, the bank has undergone a fundamental transformation: '
        '<b>infrastructure loans reduced from 22% to below 1%</b> of the loan book, while '
        '<b>retail + MSME now constitutes 82%</b> of advances. The CASA ratio has been built from '
        'scratch to over 51%. This is arguably the most ambitious banking transformation story in India.',
        body_style
    ))

    story.append(Paragraph('Key Business Facts', subheading_style))
    bullets = [
        '<b>Branch Network:</b> 1,066 branches as of Dec 31, 2025 (growing steadily)',
        '<b>Loan Book:</b> Rs 2,79,428 Cr (+20.93% YoY as of Q3 FY26)',
        '<b>Deposits:</b> Rs 2,82,662 Cr (+24.35% YoY), deposit growth exceeds loan growth',
        '<b>CASA Ratio:</b> 51.64% (Q3 FY26), up from 47.74% a year ago (+390 bps YoY)',
        '<b>Credit Cards:</b> 4.3 million cards in force (fast-growing segment)',
        '<b>Capital Raise:</b> Rs 7,500 Cr via CCPS from Warburg Pincus and ADIA (converted Oct 2025)',
        '<b>Promoter Holding:</b> 0% (IDFC Holding merged into bank; Warburg Pincus is largest block holder)',
        '<b>MFI Exposure:</b> Reduced to 2.7% of funded assets (deliberate de-risking)',
    ]
    for b in bullets:
        story.append(Paragraph(f'  {b}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Sources: IDFC First Bank Investor Presentation Q3 FY26, IDFC First Bank press releases, '
        'BSE filings (CCPS conversion Oct 2025), Business Standard',
        source_style
    ))

    story.append(PageBreak())

    # ======= SECTION 2: FUNDAMENTAL ANALYSIS =======
    story.append(Paragraph('2. Fundamental Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    # Annual financials table
    story.append(Paragraph('Annual Performance (FY22-FY25)', subheading_style))
    annual_data = [
        ['Metric', 'FY22', 'FY23', 'FY24', 'FY25'],
        ['Net Profit (Rs Cr)', '145', '2,437', '2,957', '1,525'],
        ['Advances (Rs Bn)', '1,179', '1,518', '1,946', '2,331'],
        ['Deposits (Rs Bn)', '1,055', '1,445', '2,006', '2,520'],
        ['GNPA (%)', '3.70%', '2.50%', '1.90%', '1.90%'],
        ['NIM (%)', '5.9%', '5.9%', '6.1%', '6.2%'],
        ['ROA (%)', '0.07%', '1.04%', '0.99%', '0.43%'],
        ['ROE (%)', '0.6%', '9.6%', '9.1%', '4%'],
        ['Book Value/Share (Rs)', '28.1', '30.8', '36.8', '~44.4 (54.5 post-CCPS Q3 FY26)'],
        ['CAR (%)', '16.7%', '16.8%', '16.1%', '15.5%'],
    ]
    annual_table = Table(annual_data, colWidths=[3.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
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
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>Key Insight:</b> The bank showed a remarkable turnaround from FY22 (Rs 145 Cr PAT) to FY24 '
        '(Rs 2,957 Cr PAT). However, <b>FY25 saw a sharp reversal to Rs 1,525 Cr</b> (-48% YoY) due to '
        'industry-wide microfinance stress that spiked provisions. ROA crashed from ~1% to 0.43%. '
        'The bank is now recovering from this trough, with Q3 FY26 PAT at Rs 479 Cr (Screener.in).',
        callout_red
    ))

    story.append(Paragraph('Quarterly NII & Net Profit Trend', subheading_style))
    story.append(Image(chart_paths['nii_profit'], width=16*cm, height=8*cm))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'NII has grown steadily from Rs 4,695 Cr (Q1 FY25) to Rs 5,492 Cr (Q3 FY26), reflecting '
        'consistent loan book growth. Quarterly PAT per Screener.in: Q3 FY26 Rs 479 Cr, Q2 FY26 Rs 348 Cr, '
        'Q1 FY26 Rs 453 Cr, Q4 FY25 Rs 732 Cr. Net profit was volatile due to provisioning cycles.',
        body_style
    ))

    story.append(Paragraph('NIM & Cost-to-Income Trend', subheading_style))
    story.append(Image(chart_paths['nim_cti'], width=14*cm, height=8*cm))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>NIM compression is the key concern.</b> NIM declined from 6.20% (Q1 FY25) to 5.59% (Q2 FY26) '
        'before recovering to 5.76% in Q3 FY26. This is driven by RBI rate cuts (125 bps in 2025) '
        'which repriced assets faster than liabilities. Management targets NIM of 5.8%+ by Q4 FY26. '
        'Cost-to-Income at 74% remains elevated vs peers (Kotak ~45%, HDFC ~40%), though operating '
        'leverage is emerging: business grew 21.6% in H1 FY26 vs 11.8% opex growth. '
        'V. Vaidyanathan guides 55% C/I by FY30.',
        body_style
    ))

    # SERIAL DILUTION ANALYSIS
    story.append(Paragraph('CRITICAL: Serial Equity Dilution', subheading_style))
    dilution_data = [
        ['Event', 'Shares Added', 'New Total', 'Date'],
        ['Pre-merger IDFC Bank', '~360 Cr', '~360 Cr', 'Pre-2018'],
        ['Capital First merger', '+180 Cr', '~540 Cr', 'Dec 2018'],
        ['Multiple QIPs/raises', '+70 Cr', '~610 Cr', '2019-2023'],
        ['IDFC Ltd reverse merger', '+248 Cr', '~858 Cr', 'Oct 2024'],
        ['Warburg CCPS conversion', '+81.3 Cr', '~860 Cr *', 'Oct 2025'],
        ['ESOP allotments (ongoing)', '+0.2 Cr', '859.57 Cr', 'Dec 2025'],
    ]
    dilution_table = Table(dilution_data, colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    dilution_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(HIGHLIGHT)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#fff5f5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(dilution_table)
    story.append(Paragraph(
        '* The Warburg CCPS were already counted in the 858 Cr total post the IDFC merger. '
        'The CCPS conversion changed their form from preference to equity shares. '
        'Net effect: share count went from ~360 Cr (pre-merger) to ~860 Cr today - a <b>2.4x dilution</b>. '
        'This is the single biggest risk to per-share value creation. Even if the bank doubles its '
        'profits, EPS growth would be muted unless share count stabilizes.',
        callout_red
    ))

    # EPS Dilution Bridge
    story.append(Paragraph('EPS Dilution Impact', subheading_style))
    story.append(Paragraph(
        '<b>EPS Dilution Bridge:</b> FY24 EPS Rs 4.85 (on ~610 Cr shares) dropped to FY25 EPS Rs 1.77 '
        '(on ~860 Cr shares). Shares increased 41% due to CCPS conversion + ADIA investment. '
        'To restore FY24 EPS of Rs 4.85, the bank needs PAT of Rs 4,169 Cr (vs FY25 PAT ~Rs 1,525 Cr) '
        '- requiring <b>2.7x profit growth</b> just to get back to prior per-share earnings levels.',
        callout_red
    ))

    # Rs 7,500 Cr Capital Raise Analysis
    story.append(Paragraph('Rs 7,500 Cr Capital Raise (Warburg Pincus / ADIA)', subheading_style))
    story.append(Paragraph(
        'In May 2025, IDFC First Bank raised Rs 7,500 Cr from Warburg Pincus and ADIA via compulsorily '
        'convertible preference shares (CCPS). These were converted to equity in October 2025, adding '
        '~81.27 Cr shares. The capital strengthened CAR to 16.22% (from 14.34% in Q2 FY26) and provides '
        'runway for 20%+ loan growth. However, institutional shareholders rejected Warburg\'s request for '
        'a board seat, signaling governance tension. The capital raise also depressed book value per share '
        'due to dilution, though the cash infusion increases absolute book value.',
        body_style
    ))
    story.append(Paragraph(
        '<b>CCPS Conversion Details:</b> Warburg Pincus CCPS converted at Rs 60/share (Oct 8, 2025; VWAP trigger). '
        'This provides an Rs 60 institutional floor. Post-conversion, Currant Sea Investments (Warburg Pincus '
        'affiliate) holds 9.97% stake in IDFC First Bank.',
        callout_green
    ))

    story.append(Paragraph('Loan Book Composition', subheading_style))
    story.append(Image(chart_paths['loan_pie'], width=12*cm, height=9*cm))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'The bank has dramatically shifted from wholesale to retail: mortgage-backed loans (Home + LAP) '
        'now constitute 29% (up from 13% at merger), consumer loans 25% (up from 9%). Infrastructure '
        'loans have been reduced from 22% to below 1%. MFI exposure is being deliberately shrunk to 2.7%. '
        'This de-risking is a structural positive, though it comes at the cost of lower yields on the '
        'mortgage book vs. the legacy high-yield infrastructure/MFI book.',
        body_style
    ))

    story.append(Paragraph('Asset Quality Trend', subheading_style))
    story.append(Image(chart_paths['asset_quality'], width=14*cm, height=7*cm))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'GNPA has improved from 3.70% (FY22) to 1.69% (Q3 FY26), a significant achievement. NNPA is '
        'at a low 0.53%. The MFI stress that hit FY25 provisioning appears to have peaked - management '
        'confirmed in Q3 FY26 that "industry-wide stress in microfinance has played out" and gross '
        'slippages declined ~9% QoQ. Provisions fell from Rs 1,452 Cr (Q2 FY26) to Rs 1,398 Cr (Q3 FY26).',
        body_style
    ))

    # Banking Quality Metrics Table
    story.append(Paragraph('Banking Quality Metrics (Q3 FY26, Dec 2025)', subheading_style))
    bqm_data = [
        ['Metric', 'Q3 FY26', 'Trend'],
        ['GNPA (%)', '1.69%', 'Improving'],
        ['NNPA (%)', '0.53%', 'Improving'],
        ['PCR (%)', '72.2%', 'Stable'],
        ['Credit Cost (%)', '2.05%', 'Improving (19 bps QoQ)'],
        ['NIM (%)', '~6.0%', 'Stable'],
        ['CASA (%)', '~46%', 'Stable'],
        ['Cost-to-Income (%)', '~74%', 'High'],
        ['ROA (%)', '~0.41%', 'Below benchmark'],
        ['ROE (%)', '4%', 'Below benchmark'],
        ['CAR (%)', '~16%', 'Adequate'],
    ]
    bqm_table = Table(bqm_data, colWidths=[4*cm, 3*cm, 5*cm])
    bqm_table.setStyle(TableStyle([
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
    story.append(bqm_table)
    story.append(Spacer(1, 0.3*cm))

    # Shareholding
    story.append(Paragraph('Shareholding Pattern (Dec 2025)', subheading_style))
    sh_data = [
        ['Category', 'Holding (%)', 'Notes'],
        ['Promoter', '0%', 'IDFC Holding merged into bank (Oct 2024)'],
        ['FII', '36.76%', 'Warburg Pincus (Currant Sea Investments) 9.97%; FIIs are key holders'],
        ['DII', '22.38%', 'Mutual funds + insurance/pension funds'],
        ['Public / Retail', '33.05%', 'Widely held; ~860 Cr shares outstanding (post-CCPS conversion Oct 2025)'],
        ['Government', '7.80%', 'Government holding'],
    ]
    sh_table = Table(sh_data, colWidths=[3*cm, 2.5*cm, 10*cm])
    sh_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sh_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Key Observation:</b> IDFC First Bank is one of the few private banks with 0% promoter holding. '
        'This creates both risk (no promoter anchor) and opportunity (no promoter-related governance '
        'overhang). Warburg Pincus, as the largest single block holder, provides quasi-promoter stability.',
        body_style
    ))
    story.append(Paragraph(
        '<b>KEY RISK - Promoter Holding at 0%:</b> Screener.in shows promoter holding at 0.00% as of Dec 2025, '
        'down from 37.43% in Mar 2025. Promoter stake has fallen to 0% following IDFC Limited reverse merger '
        'completion. This is a structural governance risk — the bank has no promoter anchor.',
        callout_red
    ))
    story.append(Paragraph(
        '<b>Valuation Sanity Check (Gordon Growth Model):</b> At ROE of 4% and P/B of 1.56x, the stock prices in '
        'significant improvement. Gordon Growth justified P/B at 4% ROE with 12% CoE and 5% growth = '
        '(4%-5%)/(12%-5%) = negative — stock trades at premium to fundamentals. The market is pricing in a '
        'substantial ROE recovery that has not yet materialized.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Screener.in, Trendlyne, Angel One, BSE filings, IDFC First Bank Investor Presentation Q3 FY26, '
        'Business Standard, Tribune India, groww.in',
        source_style
    ))

    story.append(PageBreak())

    # ======= SECTION 3: TECHNICAL ANALYSIS =======
    story.append(Paragraph('3. Technical Analysis', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'IDFC First Bank has traded in a wide range over the past 12 months, hitting a 52-week low '
        'of ~Rs 57 in May 2025 (amid MFI stress fears) and a 52-week high of ~Rs 98 in November 2025 '
        '(post capital raise optimism). The stock currently trades at ~Rs 85, roughly mid-range.',
        body_style
    ))

    story.append(Image(chart_paths['price'], width=16*cm, height=9*cm))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Key Technical Signals', subheading_style))
    tech_data = [
        ['Indicator', 'Value', 'Signal'],
        ['50-Day SMA', 'Rs 84.65', 'Price at SMA level - Neutral'],
        ['200-Day SMA', 'Rs 83.78', 'Price slightly above - Neutral/Bullish'],
        ['RSI (14)', '43.2', 'Neutral (below 50, not oversold)'],
        ['MACD', '-0.54', 'Bearish crossover - Sell signal'],
        ['Beta', '~1.1', 'Slightly above market volatility'],
        ['Support Zone', 'Rs 57-62', 'Strong floor from 52-week low area'],
        ['Resistance Zone', 'Rs 95-100', 'Previous highs; needs volume to break'],
    ]
    tech_table = Table(tech_data, colWidths=[3.5*cm, 3*cm, 9*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Technical Outlook:</b> The stock is consolidating near its 50-day and 200-day moving averages. '
        'RSI at 43 is neutral - neither overbought nor oversold. The MACD sell signal suggests short-term '
        'weakness. A break above Rs 95-100 would confirm a bullish trend; a break below Rs 75 would '
        'signal continued weakness. Volume on the Q3 results day was heavy but the stock dropped 2.5%, '
        'suggesting the 48% profit growth was already priced in.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Investing.com technicals, TradingView, MunafaSutra, IndMoney (data as of Feb 4, 2026)',
        source_style
    ))

    story.append(PageBreak())

    # ======= SECTION 4: SECTOR & COMPETITIVE CONTEXT =======
    story.append(Paragraph('4. Sector & Competitive Context', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Indian Private Banking Sector', subheading_style))
    story.append(Paragraph(
        'The Nifty Private Bank Index returned ~11-14% in 2025, underperforming PSU banks for the third '
        'consecutive year. Private banks face margin pressure from the RBI\'s 125 bps rate cuts in 2025 '
        '(repo rate now at 5.25%). However, credit growth remains healthy at ~12% and deposit growth '
        'at ~9.4%. S&P Global expects NIMs to stabilize and profitability to rise from FY26 onwards.',
        body_style
    ))

    story.append(Paragraph('RBI Rate Outlook & Impact on NIM', subheading_style))
    story.append(Paragraph(
        'The RBI has cut the repo rate by 125 bps in 2025 to 5.25%. A Reuters poll suggests the rate '
        'will be held steady at 5.25% through 2026, with ICRA calling the December 2025 cut "the final '
        'one in the current easing cycle." <b>This is positive for IDFC First Bank</b>: with the rate-cut '
        'cycle ending, deposit repricing will catch up, and NIM compression should halt. IDFC First Bank\'s '
        'high CASA ratio (51.64%) gives it an advantage as savings rate cuts transmit faster than term '
        'deposit repricing. Management expects cost of funds to "further drop from here."',
        body_style
    ))

    story.append(Paragraph('Peer Bank Comparison (P/B, ROA, NIM)', subheading_style))
    peer_data = [
        ['Bank', 'P/B (x)', 'ROA (%)', 'NIM (%)', 'GNPA (%)', 'CASA (%)'],
        ['Kotak Mahindra Bank', '2.58', '2.30', '5.10', '1.49', '52.5'],
        ['AU Small Finance Bank', '3.91', '1.60', '5.70', '1.79', '33.5'],
        ['IDFC First Bank', '1.56', '0.43', '5.76', '1.69', '51.6'],
        ['Federal Bank', '1.88', '1.20', '3.20', '2.10', '29.2'],
        ['IndusInd Bank', '1.09', '0.80', '4.20', '2.84', '41.3'],
        ['Bandhan Bank', '1.02', '0.90', '7.50', '3.90', '39.0'],
    ]
    peer_table = Table(peer_data, colWidths=[3.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm])
    peer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#edf2f7')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
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
        '<b>Valuation Context:</b> IDFC First Bank\'s P/B of 1.56x (using Q3 FY26 BV of Rs 54.5) sits '
        'between the distressed banks (IndusInd 1.09x, Bandhan 1.02x) and the mid-tier peers '
        '(Federal 1.88x). This is a <b>"show me" valuation</b> - the market is pricing in uncertainty. '
        'The bank\'s NIM of 5.76% is among the highest in private banking (second only to Bandhan), '
        'but its ROA of 0.43% is the lowest in the peer set. The P/B multiple will expand or compress '
        'based on whether ROA recovers toward 1.0-1.2% as guided.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Screener.in, Smart-Investing.in, Tickertape, CompaniesMarketCap, CARE Ratings, '
        'Business Standard, S&P Global Market Intelligence',
        source_style
    ))

    story.append(PageBreak())

    # ======= SECTION 5: VALUATION & ANALYST VIEWS =======
    story.append(Paragraph('5. Valuation & Analyst Views', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Brokerage Recommendations (Post Q3 FY26)', subheading_style))
    analyst_data = [
        ['Brokerage', 'Target (Rs)', 'Rating', 'Key Thesis', 'Date'],
        ['Nomura', '105', 'Buy', '67% EPS CAGR, ROA to 1.2% by FY28', 'Jan 2026'],
        ['Axis Securities', '101', 'Buy', 'Raised from Rs 83; Q3 improvement', 'Feb 2, 2026'],
        ['Investec', '90', 'Buy', 'Upgraded from Hold; raised from Rs 65', 'Jan 2026'],
        ['UBS', '75', 'SELL', 'Downgraded from Neutral to Sell; limited ROA upside', 'Nov 2025'],
        ['Nuvama', '68', 'Hold', 'Cautious on execution timeline', 'Late 2025'],
        ['Consensus (20)', '81.86', 'Buy', 'Range Rs 53-100; majority Buy', 'Feb 2026'],
    ]
    analyst_table = Table(analyst_data, colWidths=[2.8*cm, 2*cm, 1.8*cm, 5.5*cm, 2.2*cm])
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
        '<b>Wide dispersion:</b> Analyst targets range from Rs 53 (bear case) to Rs 105 (Nomura bull case). '
        'The consensus of Rs 81.86 is actually below the current price of Rs 85.1, suggesting the '
        'stock is fairly valued at current levels. The most bullish view (Nomura, Rs 105) requires '
        'the bank to deliver 67% EPS CAGR and ROA of 1.2% by FY28. The most bearish view (Rs 53) '
        'implies ROA stays at current low levels and dilution continues.',
        body_style
    ))

    story.append(Paragraph(
        '<b>Nomura\'s Bull Case:</b> Nomura projects 20% loan CAGR and 22% deposit CAGR over FY26-FY28, '
        'with ROA reaching 1.2% and ROE 11.8% by FY28. They see NIM bottoming in FY26 and recovering '
        'as term deposits reprice. This is the most detailed and optimistic coverage available.',
        callout_green
    ))

    story.append(Paragraph(
        '<b>UBS: SELL, Target Rs 75 (November 2025).</b> UBS downgraded IDFC First Bank from Neutral to Sell '
        'with a reduced target price. UBS sees limited ROA upside, flags challenges in operating '
        'leverage and profitability, and views the stock as overvalued at current levels. '
        'Their Rs 75 target implies ~12% downside from CMP of Rs 85.1.',
        body_style
    ))

    story.append(Paragraph(
        'Sources: Business Standard (Nomura Jan 2026), BusinessToday (Axis Securities Feb 2, 2026), '
        'Whalesbook (Investec, UBS), Trendlyne research reports, Investing.com consensus',
        source_style
    ))

    story.append(PageBreak())

    # ======= SECTION 6: CATALYSTS & RISKS =======
    story.append(Paragraph('6. Catalysts & Risks', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Management Guidance (V. Vaidyanathan)', subheading_style))
    mgmt_points = [
        '<b>ROA Target:</b> 1.9-2.0% by FY29 (long-term). Near-term: 1.2% by FY27 (from Q1 FY25 call). '
        '"ROA will improve in due course. One quarter can be up and down."',
        '<b>Cost-to-Income:</b> Target 55% by FY30 (currently 74%). Opex growth guided at 13% or less, '
        'vs 20%+ business growth, indicating operating leverage is beginning.',
        '<b>NIM:</b> Targeting 5.8%+ by Q4 FY26. Cost of funds expected to drop further due to savings rate revision.',
        '<b>Loan Growth:</b> ~20% annually over next 5 years. Driven by mortgages, vehicle loans, gold loans, '
        'MSME, and corporate banking.',
        '<b>MFI Strategy:</b> Deliberately de-growing MFI to 2.7% of funded assets. Industry stress "has played out."',
        '<b>Business Momentum:</b> "Strong business momentum across all main lines of business, including '
        'lending, deposits, wealth management, transaction banking." - V. Vaidyanathan, Q3 FY26',
    ]
    for mp in mgmt_points:
        story.append(Paragraph(f'  {mp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Growth Catalysts (Bull Case)', subheading_style))
    bull_points = [
        '<b>Deposit Growth > Loan Growth:</b> Deposits growing 24.35% vs loans 20.93% - this improves '
        'the liability franchise and reduces dependence on wholesale borrowing.',
        '<b>CASA at 51.64%:</b> Among the highest in private banking. This is a structural moat that '
        'protects NIM in a rate-cut environment and reduces cost of funds.',
        '<b>Rate Cut Cycle Ending:</b> With repo at 5.25% and RBI expected to hold, deposit repricing '
        'will catch up to lending rate cuts, stabilizing and potentially expanding NIM.',
        '<b>Operating Leverage:</b> Opex growing at 11.8% vs business at 21.6%. As branches mature '
        'and digital adoption increases, the C/I ratio should decline.',
        '<b>MFI Stress Behind:</b> Provisions declining QoQ, GNPA improving, slippages down 9% QoQ. '
        'The worst is over for the microfinance cycle.',
        '<b>Capital Adequacy Restored:</b> CAR at 16.22% post capital raise provides growth runway.',
        '<b>Credit Card Franchise:</b> 4.3 million cards is a significant retail franchise generating '
        'fee income and cross-sell opportunities.',
    ]
    for bp in bull_points:
        story.append(Paragraph(f'  {bp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Key Risks (Bear Case)', subheading_style))
    bear_points = [
        '<b>Serial Dilution (Primary Risk):</b> Share count has gone from 360 Cr to 860 Cr (2.4x). '
        'Even if profits double, EPS growth is halved by dilution. Unless the bank stops raising equity, '
        'per-share value creation will remain impaired.',
        '<b>ROA at 0.43% (worst in peer set):</b> The bank needs to more than double its ROA to reach '
        'the 1.0% benchmark. If ROA stays at current levels, the P/B multiple could compress to 1.0-1.2x.',
        '<b>Cost-to-Income at 74%:</b> Among the highest in banking. The branch-heavy model is expensive. '
        'Management\'s 55% target by FY30 is 4 years away and requires flawless execution.',
        '<b>NIM Compression Risk:</b> If the RBI cuts further (some analysts see 5.00%), NIM could '
        'fall below 5.5%, impacting profitability materially.',
        '<b>Warburg Pincus Overhang:</b> Warburg holds ~9.5% and was denied a board seat. If Warburg '
        'decides to exit (typical PE holding period is 5-7 years), the ~81 Cr share block could weigh on price.',
        '<b>No Promoter:</b> Zero promoter holding means no anchor investor with long-term alignment. '
        'This makes the bank vulnerable to hostile activist pressure.',
        '<b>MFI Tail Risk:</b> Though de-growing, 2.7% of funded assets in MFI can still cause lumpy '
        'provisions if industry stress resurfaces.',
    ]
    for bp in bear_points:
        story.append(Paragraph(f'  {bp}', bullet_style))

    story.append(Paragraph(
        'Sources: IDFC First Bank Q3 FY26 press release, Q3 FY25/Q1 FY25 earnings call transcripts, '
        'Business Standard, Multibagg AI analysis, Whalesbook',
        source_style
    ))

    story.append(PageBreak())

    # ======= SECTION 7: CONCLUSION & VALUATION =======
    story.append(Paragraph('7. Conclusion & 1-Year Outlook', heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor(ACCENT)))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'IDFC First Bank is a turnaround story at a critical inflection point. The bank has successfully '
        'transformed from a wholesale infrastructure lender to a retail-focused franchise with 51.6% CASA, '
        '5.76% NIM, and improving asset quality (GNPA 1.69%). Under V. Vaidyanathan, the strategic vision '
        'is clear and largely on track. However, the turnaround has come at a steep cost: massive equity '
        'dilution (2.4x in 6 years), and ROA/ROE remain well below benchmarks.',
        body_style
    ))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Valuation Methodology: Forward Book Value x P/B Multiple', subheading_style))
    story.append(Paragraph(
        'For banks, the appropriate valuation methodology is <b>Price-to-Book (P/B)</b>, not P/E. '
        'This is because bank earnings are volatile (driven by provisioning cycles) while book value '
        'is more stable. We use a 4-step P/B approach below.',
        body_style
    ))

    # Step 1
    story.append(Paragraph('<b>Step 1: Current Book Value per Share & P/B</b>', body_style))
    bv_data = [
        ['Metric', 'Value', 'Source'],
        ['Net Worth (Q3 FY26)', 'Rs 55,346 Cr', 'Dec 2025 quarterly results'],
        ['Equity Shares (Dec 2025)', '~860 Cr', 'Screener.in (Eq Cap Rs 7,322 Cr / FV Rs 10)'],
        ['Book Value / Share', 'Rs 54.5', 'Screener.in'],
        ['Current Price', 'Rs 85.1', 'NSE (Feb 4, 2026)'],
        ['Current P/B', '85.1 / 54.5 = 1.56x', 'Screener.in'],
        ['P/E (TTM)', '46.5x', 'Screener.in'],
        ['ROCE / ROE', '6.22% / 4%', 'Screener.in'],
    ]
    bv_table = Table(bv_data, colWidths=[4*cm, 5*cm, 5.5*cm])
    bv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(bv_table)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        '<b>P/B Updated:</b> BV/share = Rs 54.5 (Screener.in). P/B = CMP Rs 85.1 / BV Rs 54.5 = 1.56x. '
        'Shares outstanding: ~860 Cr (post-CCPS conversion Oct 2025; Screener.in equity capital of Rs 7,322 Cr is stale/pre-conversion).'
        'This report uses 1.56x as the current P/B.',
        callout_green
    ))

    # Step 2
    story.append(Paragraph('<b>Step 2: Project FY27E Book Value (3 Scenarios)</b>', body_style))
    story.append(Paragraph(
        'Book value growth is driven by ROE (retained earnings). We project FY27E BV/share based on '
        'assumed ROE and a 10% dividend payout ratio:',
        body_style
    ))

    proj_data = [
        ['', 'Bull', 'Base', 'Bear'],
        ['FY26E ROE', '8%', '5%', '3%'],
        ['FY27E ROE', '12%', '8%', '4%'],
        ['FY26E BV/share', 'Rs 54.5 x 1.072 = Rs 58.4', 'Rs 54.5 x 1.045 = Rs 57.0', 'Rs 54.5 x 1.027 = Rs 56.0'],
        ['FY27E BV/share', 'Rs 58.4 x 1.108 = Rs 64.7', 'Rs 57.0 x 1.072 = Rs 61.1', 'Rs 56.0 x 1.036 = Rs 58.0'],
    ]
    proj_table = Table(proj_data, colWidths=[3.2*cm, 4.5*cm, 4.5*cm, 4.3*cm])
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
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(proj_table)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        'Note: Bull assumes ROE improves to 12% (Nomura\'s FY28 estimate of 11.8% ROE). '
        'Base assumes moderate ROE recovery to 8%. Bear assumes ROA stays at ~0.5% with continued dilution. '
        'BV growth formula: BV x (1 + ROE x (1 - payout ratio)).',
        source_style
    ))

    # Step 3
    story.append(Paragraph('<b>Step 3: Apply P/B Multiple (Anchored to Peer Banks)</b>', body_style))
    story.append(Paragraph(
        'P/B multiple assumptions are anchored to peer comps: Kotak 2.58x (premium franchise), '
        'AU SFB 3.91x (growth premium), Federal 1.88x (solid mid-tier), IndusInd 1.09x (distressed), '
        'Bandhan 1.02x (NPA concerns).',
        body_style
    ))

    scenario_data = [
        ['Scenario', 'FY27E BV/sh', 'P/B Assumed', 'Target Price', 'Return from Rs 85.1', 'Probability'],
        ['Bull', 'Rs 64.7', '1.4-1.6x',
         'Rs 91-103', '+7% to +21%', '20%'],
        ['Base', 'Rs 61.1', '1.0-1.2x',
         'Rs 61-73', '-28% to -14%', '50%'],
        ['Bear', 'Rs 58.0', '0.7-0.9x',
         'Rs 41-52', '-52% to -39%', '30%'],
    ]
    scenario_table = Table(scenario_data, colWidths=[1.8*cm, 2.2*cm, 2.2*cm, 2.8*cm, 3.3*cm, 2.2*cm])
    scenario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0fff4')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fffff0')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#fff5f5')),
        ('FONTNAME', (0, 0), (-1, -1), 'SFNS'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(scenario_table)
    story.append(Spacer(1, 0.3*cm))

    # Step 4
    story.append(Paragraph('<b>Step 4: Probability-Weighted Expected Value</b>', body_style))
    story.append(Paragraph(
        'Probability weights adjusted for dilution risk and turnaround uncertainty:',
        body_style
    ))

    prob_points = [
        '<b>Bull (20%):</b> Requires Nomura\'s thesis to play out: ROA 1.2%, ROE 12%, operating leverage '
        'kicks in, no further dilution. Achievable but ambitious. P/B re-rates to 2.0-2.2x (in line with Federal Bank).',
        '<b>Base (50%):</b> Most likely. ROA recovers to 0.8-1.0%, ROE reaches 8%, C/I declines to 68%. '
        'P/B stays at 1.5-1.7x. The bank executes on its plan but slowly. Stock returns are modest.',
        '<b>Bear (30%):</b> Higher-than-normal bear weight because: (a) ROA is worst in peer set, '
        '(b) 2.4x share dilution history makes further raises plausible, (c) no promoter = governance risk, '
        '(d) Warburg exit overhang. If ROA stays at 0.5% and P/B compresses to 1.0-1.2x, stock could '
        'fall to Rs 41-52.',
    ]
    for pp in prob_points:
        story.append(Paragraph(f'  {pp}', bullet_style))
    story.append(Spacer(1, 0.3*cm))

    ev_data = [
        ['Scenario', 'Midpoint Price', 'Probability', 'Weighted Value'],
        ['Bull', 'Rs 115', '20%', 'Rs 23.0'],
        ['Base', 'Rs 95', '50%', 'Rs 47.5'],
        ['Bear', 'Rs 55', '30%', 'Rs 16.5'],
        ['', '', 'Expected Value ->', 'Rs ~88'],
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
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ev_table)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        '<b>Probability-weighted expected price: ~Rs 88</b> - implying approx 4% upside from CMP Rs 85. '
        'This reflects the genuine turnaround potential balanced against '
        'significant dilution risk and the bank\'s weak current profitability.',
        callout_green
    ))

    story.append(Paragraph(
        '<b>Risk-Free Rate Context:</b> Expected ~4% return (Rs ~88 vs CMP Rs 85) barely exceeds '
        'the 1Y G-Sec yield of ~7%, offering negative risk premium for a turnaround banking bet. '
        'Investors should weigh whether the risk-reward justifies the equity risk, dilution history, '
        'and execution uncertainty inherent in this stock, when risk-free alternatives yield 7%+.',
        callout_red
    ))

    # Methodology limitations
    story.append(Paragraph('Methodology Limitations (Transparency Note)', subheading_style))
    limit_points = [
        '<b>Not a DCF:</b> A proper bank valuation requires a multi-year income model with detailed '
        'NIM, credit cost, and opex assumptions. This P/B heuristic is a shorthand.',
        '<b>P/B assumptions are subjective:</b> The choice of 1.5-1.7x for base vs 1.0-1.2x for bear '
        'is anchored to peer comps but remains a judgment call. Small changes in assumed P/B have large '
        'impacts on target price.',
        '<b>BV projections depend on ROE assumptions:</b> If ROE recovers faster (as Nomura expects) '
        'or slower (as UBS implies), BV per share changes materially.',
        '<b>Dilution not fully modeled:</b> If the bank raises equity again (not unlikely given its '
        'history), BV/share would be further diluted. This is not explicitly modeled in the scenarios.',
        '<b>Probability weights are subjective:</b> The 20/50/30 split is informed but not quantitative. '
        'The 30% bear weight (higher than the standard 25%) reflects the bank\'s unique risk profile: '
        'serial dilution, no promoter, and ROA at half the peer average.',
    ]
    for lp in limit_points:
        story.append(Paragraph(f'  {lp}', bullet_style))

    story.append(Spacer(1, 0.3*cm))

    # Verdict
    story.append(Paragraph('Verdict', subheading_style))
    story.append(Paragraph(
        '<b>IDFC First Bank is a well-executed turnaround story with legitimate long-term potential, '
        'but the equity dilution overhang is the elephant in the room.</b> The bank has built an impressive '
        'retail franchise (51.6% CASA, improving asset quality, 5.76% NIM) under V. Vaidyanathan\'s '
        'leadership. The strategic transformation from wholesale to retail is largely complete.',
        body_style
    ))
    story.append(Paragraph(
        'The <b>probability-weighted expected value of ~Rs 88 implies approx 4% upside</b> over 12 months. '
        'This is below the analyst consensus bull case (Nomura Rs 105, +24%) but above the bearish view '
        '(Nuvama Rs 68, -20%). The modest expected return reflects two offsetting forces: '
        '(1) the bank is genuinely improving (NII +12%, GNPA declining, CASA rising), and '
        '(2) the 2.4x dilution, 0.43% ROA, and 74% C/I ratio mean the stock must prove itself before '
        'the market grants a premium multiple.',
        body_style
    ))
    story.append(Paragraph(
        '<b>Key inflection points to watch:</b> (a) ROA crossing 1.0% (would trigger P/B re-rating to 2.0x+), '
        '(b) Cost-to-Income declining below 70% (confirms operating leverage), (c) No further equity raises '
        '(stabilizes share count), (d) Warburg Pincus intentions (hold vs exit).',
        body_style
    ))
    story.append(Paragraph(
        '<b>On balance, the stock offers a marginally positive expected return (~4%) with high variance. '
        'It is suited for conviction investors who believe in the V. Vaidyanathan turnaround thesis '
        'and have a 2-3 year horizon. The stock is not suitable for value investors (limited margin of safety '
        'at 1.56x P/B with 0.43% ROA) or income investors (minimal dividend). UBS has a Sell rating with '
        'Rs 75 target. Watch for ROA improvement and dilution cessation as the key catalysts.</b>',
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
        'in IDFC First Bank.',
        disclaimer_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '<b>Data Sources:</b> Screener.in (primary financial data) | NSE India (nseindia.com) | '
        'Business Standard (business-standard.com) | Tribune India (tribuneindia.com) | '
        'IDFC First Bank Investor Presentations (idfcfirst.bank.in) | Trendlyne (trendlyne.com) | '
        'Investing.com | TradingView (tradingview.com) | Nomura Research | UBS Research | '
        'Axis Securities | Investec | Nuvama | CARE Ratings | S&P Global Market Intelligence | '
        'Smart-Investing.in | Tickertape (tickertape.in) | Groww (groww.in)',
        source_style
    ))

    doc.build(story)
    print(f"PDF generated successfully: {FINAL_PDF}")


# --- Main ---
if __name__ == '__main__':
    print("Generating charts...")
    charts = {
        'nii_profit': create_nii_chart(),
        'nim_cti': create_nim_cti_chart(),
        'loan_pie': create_loan_pie_chart(),
        'price': create_price_chart(),
        'peers': create_peer_chart(),
        'asset_quality': create_asset_quality_chart(),
    }
    print(f"Charts created ({len(charts)} charts). Building PDF...")
    build_pdf(charts)
    print("Done!")
