# reports/report_factory.py
from enum import Enum
from utils.reports.base_report import BaseReport
from utils.reports.html_report import HTMLReport
from utils.reports.pdf_report import PDFReport

class ReportType(Enum):
    HTML = "html"
    PDF = "pdf"

class ReportFactory:
    """
    Fábrica para criação de relatórios
    """
    @staticmethod
    def create_report(report_type: ReportType) -> BaseReport:
        if report_type == ReportType.HTML:
            return HTMLReport()
        
        elif report_type == ReportType.PDF:
            return PDFReport()
        
        else:
            raise ValueError(f"Tipo de relatório não suportado: {report_type}")