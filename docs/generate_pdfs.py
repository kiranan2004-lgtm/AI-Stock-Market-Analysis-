"""
StockSense AI - Professional PDF Documentation Generator
Builds publication-quality PDFs with ReportLab:
1. AI_Stock_Market_Project_Complete_Notes.pdf
2. AI_Stock_Market_Project_Interview_QA.pdf
3. AI_Stock_Market_Quick_Revision.pdf
4. AI_Stock_Market_Architecture_Diagrams.pdf
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), 'diagrams')

# Palette
PRIMARY = colors.HexColor('#1E3A8A')     # Deep Navy
SECONDARY = colors.HexColor('#2563EB')   # Vibrant Indigo
ACCENT = colors.HexColor('#059669')      # Emerald Green
DARK_TEXT = colors.HexColor('#0F172A')   # Slate 900
BODY_TEXT = colors.HexColor('#334155')   # Slate 700
LIGHT_BG = colors.HexColor('#F8FAFC')    # Slate 50
BORDER_COLOR = colors.HexColor('#CBD5E1')# Slate 300
CALLOUT_BG = colors.HexColor('#EFF6FF')  # Soft Blue Tint
RED_ACCENT = colors.HexColor('#DC2626')  # Soft Red

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas that adds running headers and 'Page X of Y' footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        
        # Header
        self.drawString(40, letter[1] - 30, "StockSense AI — Technical Platform & Interview Preparation Guide")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(40, letter[1] - 34, letter[0] - 40, letter[1] - 34)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 25, page_str)
        self.drawString(40, 25, "Confidential & Proprietary — For Candidate Technical Interview Preparation")
        self.line(40, 35, letter[0] - 40, 35)
        self.restoreState()


def get_custom_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=PRIMARY,
        alignment=0, # Left
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=BODY_TEXT
    ))
    styles.add(ParagraphStyle(
        'DocHeading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'DocHeading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'DocHeading3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=DARK_TEXT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=BODY_TEXT,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=BODY_TEXT,
        leftIndent=15,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderPadding=6,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=BODY_TEXT
    ))
    styles.add(ParagraphStyle(
        'QuestionText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'AnswerText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=BODY_TEXT,
        spaceAfter=6
    ))
    return styles

def create_callout(title, text, styles, border_color=SECONDARY, bg_color=CALLOUT_BG):
    content = [
        Paragraph(title, styles['CalloutTitle']),
        Paragraph(text, styles['CalloutBody'])
    ]
    t = Table([[content]], colWidths=[letter[0] - 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

print("PDF Helper initialized.")
