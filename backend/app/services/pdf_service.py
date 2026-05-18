import qrcode

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER

# =========================
# GENERATE PDF REPORT
# =========================

def generate_pdf_report(

    report_id,

    file,

    document_category,

    verification_status,

    fraud_risk,

    confidence_score,

    document_hash,

    name,

    pan_number,

    aadhaar_number,

    dob,

    gender,

    invoice_number,

    total_amount,

    verification_url
):

    pdf_file = f"reports/report_{report_id}.pdf"

    # QR
    qr = qrcode.make(
        verification_url
    )

    qr_path = f"qr_codes/qr_{report_id}.png"

    qr.save(qr_path)

    # PDF DOC
    doc = SimpleDocTemplate(
        pdf_file,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # TITLE STYLE
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2563EB")
    )

    # HEADER
    elements.append(

        Paragraph(
            "TrustChain AI Report",
            title_style
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    # SUMMARY TABLE
    summary_data = [

        ["Field", "Value"],

        ["Filename", file.filename],

        ["Document Category", document_category],

        ["Verification Status", verification_status],

        ["Fraud Risk", fraud_risk],

        ["Confidence Score", f"{confidence_score}%"],

        ["Document Hash", document_hash[:40] + "..."]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[180, 300]
    )

    summary_table.setStyle(

        TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563EB")),

            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('FONTSIZE', (0, 0), (-1, -1), 11),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),

            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ])
    )

    elements.append(summary_table)

    elements.append(
        Spacer(1, 30)
    )

    # QR SECTION
    elements.append(

        Paragraph(
            "Verification QR",
            styles['Heading2']
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    qr_image = RLImage(
        qr_path,
        width=140,
        height=140
    )

    elements.append(qr_image)

    elements.append(
        Spacer(1, 12)
    )

    elements.append(

        Paragraph(
            verification_url,
            styles['BodyText']
        )
    )

    doc.build(elements)

    return pdf_file