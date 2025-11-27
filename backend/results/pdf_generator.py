from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.db.models import Sum, Avg
from .models import Result

def generate_report_card(student, term):
    """Generate PDF report card for a student"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1976d2'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
    )
    
    # Title
    title = Paragraph("STUDENT REPORT CARD", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Student Information
    student_info = [
        ['Student Name:', student.full_name],
        ['Student ID:', student.student_id],
        ['Class:', student.current_class.name if student.current_class else 'Not Assigned'],
        ['Academic Year:', term.academic_year.year],
        ['Term:', f"Term {term.term_number}"],
    ]
    
    student_table = Table(student_info, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(student_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Academic Performance
    heading = Paragraph("Academic Performance", heading_style)
    elements.append(heading)
    
    # Get results
    results = Result.objects.filter(student=student, term=term).select_related('subject')
    
    if results.exists():
        # Results table
        data = [['Subject', 'Marks Obtained', 'Total Marks', 'Percentage', 'Grade', 'Remarks']]
        
        for result in results:
            data.append([
                result.subject.name,
                str(result.marks_obtained),
                str(result.total_marks),
                f"{result.percentage:.2f}%",
                result.grade,
                result.remarks or '-'
            ])
        
        # Calculate totals
        total_marks_obtained = results.aggregate(Sum('marks_obtained'))['marks_obtained__sum']
        total_marks_possible = results.aggregate(Sum('total_marks'))['total_marks__sum']
        overall_percentage = (total_marks_obtained / total_marks_possible * 100) if total_marks_possible > 0 else 0
        
        # Calculate overall grade
        if overall_percentage >= 90:
            overall_grade = 'A+'
        elif overall_percentage >= 80:
            overall_grade = 'A'
        elif overall_percentage >= 70:
            overall_grade = 'B+'
        elif overall_percentage >= 60:
            overall_grade = 'B'
        elif overall_percentage >= 50:
            overall_grade = 'C'
        elif overall_percentage >= 40:
            overall_grade = 'D'
        else:
            overall_grade = 'F'
        
        # Add totals row
        data.append([
            'TOTAL/OVERALL',
            str(total_marks_obtained),
            str(total_marks_possible),
            f"{overall_percentage:.2f}%",
            overall_grade,
            ''
        ])
        
        results_table = Table(data, colWidths=[1.8*inch, 1*inch, 1*inch, 1*inch, 0.7*inch, 1.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e3f2fd')),
            ('FONTNAME', (0, -1), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        
        elements.append(results_table)
    else:
        no_results = Paragraph("No results available for this term.", styles['Normal'])
        elements.append(no_results)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Grading Scale
    heading = Paragraph("Grading Scale", heading_style)
    elements.append(heading)
    
    grading_data = [
        ['Grade', 'Percentage Range', 'Description'],
        ['A+', '90% - 100%', 'Excellent'],
        ['A', '80% - 89%', 'Very Good'],
        ['B+', '70% - 79%', 'Good'],
        ['B', '60% - 69%', 'Above Average'],
        ['C', '50% - 59%', 'Average'],
        ['D', '40% - 49%', 'Below Average'],
        ['F', 'Below 40%', 'Fail'],
    ]
    
    grading_table = Table(grading_data, colWidths=[1*inch, 2*inch, 2*inch])
    grading_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#424242')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    
    elements.append(grading_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = Paragraph(
        "This is a computer-generated report. No signature is required.",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    )
    elements.append(footer_text)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer