#!/usr/bin/env python3
"""Build the two-page CV. Requires ReportLab and PyYAML; use --font-dir for fonts."""
from pathlib import Path
import argparse
import re
from xml.sax.saxutils import escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font-dir', default='/System/Library/Fonts/Supplemental')
args = parser.parse_args()
for name, file in [('CV', 'Trebuchet MS.ttf'), ('CV-Bold', 'Trebuchet MS Bold.ttf'), ('CV-Italic', 'Trebuchet MS Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path(args.font_dir) / file)))
pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV-Italic', boldItalic='CV-Bold')

INK = colors.HexColor('#20282c')
MUTED = colors.HexColor('#58656c')
ACCENT = colors.HexColor('#32627a')
WIDTH = 508
styles = {
    'body': ParagraphStyle('body', fontName='CV', fontSize=10, leading=14, textColor=INK),
    'small': ParagraphStyle('small', fontName='CV', fontSize=9.2, leading=12.5, textColor=MUTED),
    'paper': ParagraphStyle('paper', fontName='CV-Bold', fontSize=10.2, leading=13.4, textColor=INK),
    'section': ParagraphStyle('section', fontName='CV-Bold', fontSize=11, leading=15, spaceBefore=14, spaceAfter=7, textColor=ACCENT),
    'subsection': ParagraphStyle('subsection', fontName='CV-Bold', fontSize=9.2, leading=13, spaceBefore=7, spaceAfter=5, textColor=MUTED),
    'name': ParagraphStyle('name', fontName='CV-Bold', fontSize=27, leading=32, textColor=INK),
    'date': ParagraphStyle('date', fontName='CV', fontSize=9.2, leading=13, alignment=TA_RIGHT, textColor=MUTED),
}

def p(text, style='body'):
    return Paragraph(text, styles[style])

def link(label, url):
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#32627a">{escape(label)}</link>'

def heading(title):
    return p(title.upper(), 'section')

def row(left, right):
    t = Table([[p(left), p(right, 'date')]], colWidths=[WIDTH-132,132])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return t

def experience(institution, dates, role, details):
    return KeepTogether([row(f'<b>{institution}</b>',dates),p(role,'small'),Spacer(1,4),*[p('- '+x) for x in details],Spacer(1,7)])

def paper(pub):
    authors = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escape(pub['authors']))
    venue = {
        'ids': 'NeurIPS 2026, Main Conference. Also at ICML 2026 DEMO Workshop.',
        'hipo': 'EMNLP 2026, Main Conference.',
        'marvel': 'Transactions on Machine Learning Research (TMLR), 2026.',
        'fpm': 'Cells, 13(4), 324, 2024.',
        'meshheal': 'arXiv:2609.29015, 2026.',
    }[pub['id']]
    return KeepTogether([p(link(pub['title'],pub['paper']),'paper'),Spacer(1,2),p(authors,'small'),p(venue,'small'),Spacer(1,9)])

def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#dce2e5'))
    canvas.setLineWidth(.5)
    canvas.line(46,37,566,37)
    canvas.setFont('CV',8)
    canvas.setFillColor(MUTED)
    canvas.drawString(46,24,'Keru Chen | Curriculum Vitae | Updated September 2026')
    canvas.drawRightString(566,24,f'{doc.page} / 2')

story = [p('Keru Chen','name'),Spacer(1,3),p('PhD Student in Electrical Engineering | Arizona State University'),Spacer(1,5),
    p(' &nbsp; | &nbsp; '.join([link('kchen234@asu.edu','mailto:kchen234@asu.edu'),link('Website','https://cliverchen.github.io/'),link('Google Scholar','https://scholar.google.com/citations?user=W0LexmIAAAAJ'),link('GitHub','https://github.com/CLIVERCHEN')]),'small'),
    heading('Research Interests'),
    p('Reinforcement learning, LLM post-training, and AI agents, including multi-agent systems. My interests center on safety, alignment, and decision-making under constraints, with applications to healthcare.'),
    heading('Education'),
    row('<b>Arizona State University</b>','Aug 2025 - Present'),
    row('PhD in Electrical Engineering','GPA: 3.89 / 4.00'),
    p('Advisor: '+link('Prof. Shaofeng Zou','https://sites.google.com/view/szou/home'),'small'),
    p('I also work closely with '+link('Prof. Sen Lin','https://slin70.github.io/')+' and '+link('Prof. Yingbin Liang','https://sites.google.com/view/yingbinliang/home')+'.','small'),Spacer(1,8),
    row("<b>Xi'an Jiaotong University</b>",'2021 - 2025'),
    row('BEng in Automation','GPA: 3.5 / 4.3'),
    heading('Publications')]
publications = yaml.safe_load((ROOT/'data/publications.yaml').read_text())
story += [paper(x) for x in publications if x['id']!='meshheal']
story += [p('PREPRINT','subsection'),paper(next(x for x in publications if x['id']=='meshheal')),PageBreak(),heading('Research Experience')]
story += [
    experience('Arizona State University','Aug 2025 - Present','Doctoral Research | Prof. Shaofeng Zou',[
        'Study safe and constrained reinforcement learning, instruction hierarchy in language models, and reliability in multi-agent systems.']),
    experience('Westlake University','Summer 2024','Research Intern | Prof. Donglin Wang',[
        'Worked on reinforcement learning for robotic manipulation and RL-based fine-tuning of vision-language-action models.']),
    experience('University of Houston','Sep 2023 - Jul 2025','Research Intern | Prof. Sen Lin',[
        'Studied safe offline-to-online reinforcement learning and constrained policy fine-tuning; first-author paper accepted to TMLR in 2026.']),
    experience('University of North Carolina at Chapel Hill','Jan 2024 - May 2024','Research Intern | Prof. Tianlong Chen',[
        'Worked on time-series forecasting and security analysis of LLM and retrieval-augmented generation systems.',
        'Contributed to research published at EMNLP 2024.']),
    experience('Chinese Academy of Sciences','Feb 2023 - Oct 2023',"Research Intern | Prof. An Pan | Xi'an, China",[
        'Worked on computational imaging and Fourier ptychographic microscopy; co-authored a review published in Cells.']),
    heading('Selected Projects'),
    experience('Biomedical Image Translation with GANs','2024','Research Project',[
        'Developed a multi-scale GAN for breast cancer cell image translation.',
        'National Second Prize, National Biomedical Engineering Innovation Design Competition.']),
    experience('Waveformer: EEG Sleep Stage Classification','2023','Research Project',[
        'Built a transformer-based model combining wavelet transforms and deep learning for EEG sleep stage classification; code available on GitHub.']),
    heading('Academic Service'),
    p('<b>Conference Reviewer:</b> NeurIPS 2026; ICLR 2027.'),
    p('<b>Journal Reviewer:</b> Scientific Reports; IEEE/ACM Transactions on Networking.'),
    heading('Skills'),
    p('<b>Programming:</b> Python (PyTorch), C/C++, MATLAB.'),
    p('<b>Tools:</b> Git/GitHub, Linux, LaTeX.'),
    p('<b>Languages:</b> Mandarin (native); English (IELTS 6.5).'),
]
output = ROOT/'output/pdf/Keru_Chen_CV.pdf'
output.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(output),pagesize=letter,rightMargin=46,leftMargin=46,topMargin=39,bottomMargin=48,title='Keru Chen - Curriculum Vitae',author='Keru Chen',subject='Academic curriculum vitae',pageCompression=1).build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
