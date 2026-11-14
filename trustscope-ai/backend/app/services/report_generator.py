from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate(product, analysis, suspicious_reviews) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                 rightMargin=2*cm, leftMargin=2*cm,
                                 topMargin=2*cm, bottomMargin=2*cm)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle('Title', parent=styles['Title'], 
                                      fontSize=24, spaceAfter=6,
                                      textColor=colors.HexColor('#1e40af'))
        story.append(Paragraph("TrustScope AI", title_style))
        story.append(Paragraph("Fake Product Review Detection & Trust Report", styles['Heading2']))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3b82f6')))
        story.append(Spacer(1, 0.5*cm))
        
        # Product Info
        story.append(Paragraph("Product Information", styles['Heading2']))
        product_data = [
            ["Product Name", product.product_name or "N/A"],
            ["Platform", (product.platform or "Unknown").capitalize()],
            ["Original Rating", f"{product.average_rating or 'N/A'} / 5.0"],
            ["Analysis Date", datetime.now().strftime("%B %d, %Y %H:%M")],
            ["Data Source", "DEMONSTRATION DATA (Simulated)" if product.is_demo else "Live Review Source"],
        ]
        t = Table(product_data, colWidths=[5*cm, 12*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eff6ff')),
            ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1e40af')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*cm))
        
        # Trust Summary
        story.append(Paragraph("Analysis Summary & Risk Scores", styles['Heading2']))
        trust_color = colors.HexColor('#10b981') if analysis.trust_score >= 70 else (
            colors.HexColor('#f59e0b') if analysis.trust_score >= 40 else colors.HexColor('#ef4444')
        )
        trust_style = ParagraphStyle('Trust', parent=styles['Normal'], 
                                      fontSize=26, textColor=trust_color, 
                                      alignment=TA_CENTER, spaceAfter=12)
        story.append(Paragraph(f"Overall Product Trust Score: {analysis.trust_score:.1f}/100", trust_style))
        
        summary_data = [
            ["Metric", "Value"],
            ["Total Reviews Retrieved", str(analysis.total_retrieved)],
            ["Total Reviews Analysed", str(analysis.total_analysed)],
            ["Genuine-looking Reviews", f"{analysis.genuine_count} ({analysis.genuine_pct:.1f}%)"],
            ["Suspicious Reviews", f"{analysis.suspicious_count} ({analysis.suspicious_pct:.1f}%)"],
            ["Uncertain Reviews", f"{analysis.uncertain_count} ({analysis.uncertain_pct:.1f}%)"],
            ["Duplicate Reviews Detected", str(analysis.duplicate_count)],
            ["High-Risk Reviews (Score 61-100)", str(analysis.high_risk_count)],
            ["Medium-Risk Reviews (Score 31-60)", str(analysis.medium_risk_count)],
            ["Low-Risk Reviews (Score 0-30)", str(analysis.low_risk_count)],
            ["Risk-Adjusted Rating Estimate", f"{analysis.adjusted_rating or 'N/A'} / 5.0"],
        ]
        t2 = Table(summary_data, colWidths=[8*cm, 9*cm])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.5*cm))
        
        # Sample Suspicious Reviews
        if suspicious_reviews:
            story.append(Paragraph("Sample Suspicious Reviews & Explanations", styles['Heading2']))
            for i, (review, ra) in enumerate(suspicious_reviews[:5], 1):
                text = review.review_text[:280] + "..." if len(review.review_text) > 280 else review.review_text
                story.append(Paragraph(f"Review #{i} — Star Rating: {review.star_rating}★ | Risk Score: {ra.risk_score:.0f}/100", styles['Heading3']))
                story.append(Paragraph(f'"{text}"', styles['Normal']))
                if ra.detection_reasons:
                    story.append(Paragraph("Detection reasons:", styles['Normal']))
                    for reason in ra.detection_reasons[:3]:
                        story.append(Paragraph(f"• {reason}", styles['Normal']))
                story.append(Spacer(1, 0.3*cm))
        
        # Disclaimer
        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        disclaimer = ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
        story.append(Paragraph(
            "DISCLAIMER: This report is generated by TrustScope AI for informational and decision-support purposes. "
            "A suspicious review is not definitively a fake review. TrustScope AI evaluates stylistic anomalies, promotional markers, duplicate signatures, "
            "and ML predictions. Review trust does not establish overall product quality. "
            "TrustScope AI — College Hackathon Edition.",
            disclaimer
        ))
        
        doc.build(story)
        return buffer.getvalue()
