#!/usr/bin/env python3
"""Build the formal research-internship CV. Requires ReportLab and PyYAML."""
from pathlib import Path
import argparse
import re
from xml.sax.saxutils import escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font-dir', default='/System/Library/Fonts/Supplemental')
args = parser.parse_args()
for name, file in [('CV', 'Times New Roman.ttf'), ('CV-Bold', 'Times New Roman Bold.ttf'), ('CV-Italic', 'Times New Roman Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path(args.font_dir) / file)))
pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV-Italic', boldItalic='CV-Bold')

INK = colors.HexColor('#111111')
MUTED = colors.HexColor('#333333')
WIDTH = 508
styles = {
    'body': ParagraphStyle('body', fontName='CV', fontSize=11, leading=14.2, textColor=INK),
    'small': ParagraphStyle('small', fontName='CV', fontSize=10.3, leading=13, textColor=MUTED),
    'paper': ParagraphStyle('paper', fontName='CV-Bold', fontSize=10.8, leading=13.8, textColor=INK),
    'section': ParagraphStyle('section', fontName='CV-Bold', fontSize=11.5, leading=15, spaceBefore=12, spaceAfter=2, textColor=INK),
    'subsection': ParagraphStyle('subsection', fontName='CV-Italic', fontSize=10.3, leading=13, spaceBefore=4, spaceAfter=5, textColor=MUTED),
    'name': ParagraphStyle('name', fontName='CV-Bold', fontSize=26, leading=30, alignment=TA_CENTER, textColor=INK),
    'contact': ParagraphStyle('contact', fontName='CV', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=INK),
    'date': ParagraphStyle('date', fontName='CV', fontSize=10.5, leading=14.2, alignment=TA_RIGHT, textColor=INK),
    'bullet': ParagraphStyle('bullet', fontName='CV', fontSize=11, leading=14.2, leftIndent=10, firstLineIndent=-10, spaceAfter=3, textColor=INK),
}

def p(text, style='body'):
    return Paragraph(text, styles[style])

def link(label, url):
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#111111">{escape(label)}</link>'

def heading(title):
    return KeepTogether([p(title.upper(), 'section'), HRFlowable(width='100%', thickness=.5, color=INK, spaceAfter=6)], maxHeight=35)

def row(left, right):
    t = Table([[p(left), p(right, 'date')]], colWidths=[WIDTH-132,132])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return t

def experience(institution, dates, role, details):
    return KeepTogether([row(f'<b>{institution}</b>',dates),p('<i>'+role+'</i>','small'),Spacer(1,4),*[p('- '+x,'bullet') for x in details],Spacer(1,6)])

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
    canvas.setStrokeColor(colors.HexColor('#aaaaaa'))
    canvas.setLineWidth(.5)
    canvas.line(46,37,566,37)
    canvas.setFont('CV',8)
    canvas.setFillColor(MUTED)
    canvas.drawString(46,24,'Keru Chen | Curriculum Vitae | Updated September 2026')
    canvas.drawRightString(566,24,f'{doc.page} / 2')

story = [p('Keru Chen','name'),Spacer(1,4),
    p('PhD Student, Electrical Engineering, Arizona State University','contact'),
    p(' | '.join([link('kchen234@asu.edu','mailto:kchen234@asu.edu'),link('cliverchen.github.io','https://cliverchen.github.io/'),link('Google Scholar','https://scholar.google.com/citations?user=W0LexmIAAAAJ'),link('GitHub','https://github.com/CLIVERCHEN')]),'contact'),
    Spacer(1,9),
    p('<b>Research focus:</b> Reinforcement learning, LLM post-training, and AI agents, including multi-agent systems; safety, alignment, and constrained decision-making, with interest in healthcare applications.'),
    heading('Education'),
    row('<b>Arizona State University</b>','Aug 2025 - Present'),
    row('PhD in Electrical Engineering','GPA: 3.89 / 4.00'),
    p('Advisor: '+link('Prof. Shaofeng Zou','https://sites.google.com/view/szou/home'),'small'),Spacer(1,7),
    row("<b>Xi'an Jiaotong University</b>",'2021 - 2025'),
    row('BEng in Automation','GPA: 3.5 / 4.3'),
    heading('Research Experience'),
    experience('Arizona State University','Aug 2025 - Present','Doctoral Research | Prof. Shaofeng Zou',[
        'Formulated instruction hierarchy in LLMs as constrained RL (<b>HIPO; EMNLP&nbsp;2026</b>).',
        'Developed information-directed exploration for offline-to-online RL (<b>NeurIPS&nbsp;2026</b>).',
        'Studied peer review and two-timescale monitoring to detect unreliable outputs and guide recovery in decentralized LLM agent networks (<b>MeshHeal; preprint</b>).',
        'Work closely with '+link('Prof. Sen Lin','https://slin70.github.io/')+' and '+link('Prof. Yingbin Liang','https://sites.google.com/view/yingbinliang/home')+'.']),
    experience('University of Houston','Sep 2023 - Jul 2025','Research Intern | Prof. Sen Lin',[
        'Studied value alignment and adaptive constraint penalties for safe online fine-tuning of offline RL policies (<b>first-author paper, TMLR 2026</b>).']),
    experience('Westlake University','Summer 2024','Research Intern | Prof. Donglin Wang',[
        'Applied reinforcement learning to fine-tune vision-language-action models for robotic manipulation.']),
    experience('University of North Carolina at Chapel Hill','Jan 2024 - May 2024','Research Intern | Prof. Tianlong Chen',[
        'Worked on time-series forecasting and security analysis of LLM and retrieval-augmented generation systems; contributed to research published at EMNLP 2024.']),
    heading('Technical Skills'),
    p('<b>Programming:</b> Python, C/C++, MATLAB. &nbsp; <b>Deep learning:</b> PyTorch.'),
    p('<b>Tools:</b> Git/GitHub, Linux, LaTeX.'),
    PageBreak(),heading('Publications')]
publications = yaml.safe_load((ROOT/'data/publications.yaml').read_text())
story += [paper(x) for x in publications if x['id']!='meshheal']
story += [p('Preprint','subsection'),paper(next(x for x in publications if x['id']=='meshheal')),
    heading('Additional Research Experience'),
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
]
output = ROOT/'output/pdf/Keru_Chen_CV.pdf'
output.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(output),pagesize=letter,rightMargin=46,leftMargin=46,topMargin=39,bottomMargin=48,title='Keru Chen - Curriculum Vitae',author='Keru Chen',subject='Academic curriculum vitae',pageCompression=1).build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
