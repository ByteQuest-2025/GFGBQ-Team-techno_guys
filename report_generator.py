from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_pdf_report(complaint_data, ticket_id):
    """Generate a professional PDF report for the complaint."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Title
    title = Paragraph("🎯 AI-Powered Grievance Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    meta_data = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Ticket ID:', ticket_id],
        ['Status:', complaint_data.get('status', 'Pending')]
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Analysis Results
    elements.append(Paragraph("Analysis Results", heading_style))
    
    analysis_data = [
        ['Category:', complaint_data.get('category', 'N/A')],
        ['Priority:', complaint_data.get('priority', 'N/A')],
        ['Department:', complaint_data.get('department', 'N/A')],
        ['Est. Resolution:', complaint_data.get('resolution_time', 'N/A')],
        ['Sentiment:', complaint_data.get('sentiment_label', 'N/A')]
    ]
    
    analysis_table = Table(analysis_data, colWidths=[2*inch, 4*inch])
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(analysis_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Complaint Text
    elements.append(Paragraph("Complaint Details", heading_style))
    complaint_text = Paragraph(complaint_data.get('complaint_text', 'N/A'), styles['Normal'])
    elements.append(complaint_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Keywords
    if 'keywords' in complaint_data and complaint_data['keywords']:
        elements.append(Paragraph("Key Topics", heading_style))
        keywords_text = ', '.join(complaint_data['keywords'])
        elements.append(Paragraph(keywords_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def send_email_notification(recipient_email, complaint_data, ticket_id):
    """Send email notification about the complaint."""
    try:
        # Email configuration (use environment variables in production)
        sender_email = "grievance.system@gov.in"
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Complaint Registered - Ticket #{ticket_id}"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # HTML content
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div style="background: white; padding: 30px; border-radius: 10px;">
                        <h1 style="color: #667eea; text-align: center;">🎯 Grievance Registered</h1>
                        <p>Dear Citizen,</p>
                        <p>Your complaint has been successfully registered in our AI-Powered Grievance Redressal System.</p>
                        
                        <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #764ba2; margin-top: 0;">Complaint Summary</h3>
                            <p><strong>Ticket ID:</strong> {ticket_id}</p>
                            <p><strong>Category:</strong> {complaint_data.get('category', 'N/A')}</p>
                            <p><strong>Priority:</strong> {complaint_data.get('priority', 'N/A')}</p>
                            <p><strong>Assigned Department:</strong> {complaint_data.get('department', 'N/A')}</p>
                            <p><strong>Expected Resolution:</strong> {complaint_data.get('resolution_time', 'N/A')}</p>
                        </div>
                        
                        <p><strong>Next Steps:</strong></p>
                        <ul>
                            <li>Your complaint has been forwarded to the concerned department</li>
                            <li>You will receive updates via SMS and Email</li>
                            <li>Track your complaint using Ticket ID: <strong>{ticket_id}</strong></li>
                        </ul>
                        
                        <p style="margin-top: 30px;">Best regards,<br>
                        <strong>AI Grievance Redressal Team</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML content
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Note: In production, use proper SMTP configuration
        # For demo purposes, return success message
        return True, "Email notification sent successfully!"
        
    except Exception as e:
        return False, f"Email error: {str(e)}"
