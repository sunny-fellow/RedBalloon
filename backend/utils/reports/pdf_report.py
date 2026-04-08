from utils.reports.base_report import BaseReport
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

class PDFReport(BaseReport):
    """
    Geração de relatório em formato PDF verdadeiro usando reportlab
    """
    def generate(self, start_date: datetime, end_date: datetime) -> bytes:
        """
        Gera o relatório e retorna como bytes (PDF)
        """
        self._validate_dates(start_date, end_date)
        access_data = self._collect_access_data(start_date, end_date)
        statistics = self._calculate_statistics(access_data)
        
        # Criar buffer para o PDF
        buffer = BytesIO()
        
        # Criar o documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=2*cm,
            bottomMargin=2*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            alignment=1,
            spaceAfter=30
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=20
        )
        normal_style = styles['Normal']
        
        # Elementos do PDF
        elements = []
        
        # Título
        elements.append(Paragraph("Relatório de Estatísticas de Acesso", title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Período
        period_text = f"Período: {start_date.strftime('%d/%m/%Y %H:%M')} a {end_date.strftime('%d/%m/%Y %H:%M')}"
        elements.append(Paragraph(period_text, normal_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # Data de geração
        gen_text = f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        elements.append(Paragraph(gen_text, normal_style))
        elements.append(Spacer(1, 1*cm))
        
        # Extrair valores
        total_accesses = statistics.get('summary', {}).get('total_accesses', 0) or 0
        days = statistics.get('summary', {}).get('period', {}).get('days', 0) or 0
        
        unique_submissions = statistics.get('summary', {}).get('unique_users', {}).get('submissions', 0) or 0
        unique_problems = statistics.get('summary', {}).get('unique_users', {}).get('problems', 0) or 0
        unique_comments = statistics.get('summary', {}).get('unique_users', {}).get('comments', 0) or 0
        
        total_submissions = statistics.get('submissions', {}).get('total', 0) or 0
        accepted = statistics.get('submissions', {}).get('accepted', 0) or 0
        acceptance_rate = statistics.get('submissions', {}).get('acceptance_rate', 0) or 0
        wrong_answer = statistics.get('submissions', {}).get('wrong_answer', 0) or 0
        tle = statistics.get('submissions', {}).get('time_limit_exceeded', 0) or 0
        compilation_error = statistics.get('submissions', {}).get('compilation_error', 0) or 0
        
        total_problems = statistics.get('problems', {}).get('total', 0) or 0
        easy = statistics.get('problems', {}).get('by_difficulty', {}).get('easy', 0) or 0
        medium = statistics.get('problems', {}).get('by_difficulty', {}).get('medium', 0) or 0
        hard = statistics.get('problems', {}).get('by_difficulty', {}).get('hard', 0) or 0
        
        total_comments = statistics.get('engagement', {}).get('total_comments', 0) or 0
        
        # ===== RESUMO GERAL =====
        elements.append(Paragraph("Resumo Geral", heading_style))
        
        summary_data = [
            ["Total de Acessos no período:", str(total_accesses)],
            ["Dias no período:", str(days)],
            ["", ""],
            ["Usuários Únicos por Tipo de Ação:", ""],
            [f"  • Submissões: {unique_submissions}", ""],
            [f"  • Problemas: {unique_problems}", ""],
            [f"  • Comentários: {unique_comments}", ""],
        ]
        
        summary_table = Table(summary_data, colWidths=[10*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # ===== SUBMISSÕES =====
        elements.append(Paragraph("Submissões", heading_style))
        
        submissions_data = [
            ["Total de Submissões:", str(total_submissions)],
            ["Submissões Aceitas:", str(accepted)],
            ["Taxa de Aceitação:", f"{acceptance_rate}%"],
            ["Wrong Answer:", str(wrong_answer)],
            ["Time Limit Exceeded:", str(tle)],
            ["Compilation Error:", str(compilation_error)],
        ]
        
        submissions_table = Table(submissions_data, colWidths=[10*cm, 4*cm])
        submissions_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        elements.append(submissions_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # ===== PROBLEMAS =====
        elements.append(Paragraph("Problemas Criados", heading_style))
        
        problems_data = [
            ["Total de Problemas:", str(total_problems)],
            ["", ""],
            ["Por Dificuldade:", ""],
            [f"  • Easy: {easy}", ""],
            [f"  • Medium: {medium}", ""],
            [f"  • Hard: {hard}", ""],
        ]
        
        problems_table = Table(problems_data, colWidths=[10*cm, 4*cm])
        problems_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(problems_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # ===== ENGAJAMENTO =====
        elements.append(Paragraph("Engajamento", heading_style))
        
        engagement_data = [
            ["Total de Comentários:", str(total_comments)],
        ]
        
        engagement_table = Table(engagement_data, colWidths=[10*cm, 4*cm])
        engagement_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(engagement_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Rodapé
        elements.append(Spacer(1, 1*cm))
        footer_text = "Relatório gerado automaticamente pelo sistema RedBalloon"
        elements.append(Paragraph(footer_text, normal_style))
        
        # Gerar PDF
        doc.build(elements)
        
        # Retornar bytes do PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        # Log da geração
        self._log_generation(start_date, end_date, access_data)
        
        return pdf_bytes
    
    def _format_data(self, statistics: dict) -> str:
        """Método abstrato - não usado"""
        return ""
    
    def _generate_header(self, start_date: datetime, end_date: datetime) -> str:
        """Método abstrato - não usado"""
        return ""
    
    def _generate_footer(self) -> str:
        """Método abstrato - não usado"""
        return ""