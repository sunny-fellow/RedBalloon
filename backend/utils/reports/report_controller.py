# reports/controller.py
from flask_restx import Namespace, Resource
from flask import request, Response
from datetime import datetime
from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id
from utils.reports.report_factory import ReportFactory, ReportType
from flask import Response
from datetime import datetime
from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id
from utils.reports.html_report import HTMLReport
from utils.reports.pdf_report import PDFReport

api = Namespace("reports", description="Geração de Relatórios Estatísticos")

@api.route("/access-stats")
class AccessStatsReport(Resource):
    @handle_exceptions
    def get(self):
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")
        format_type = request.args.get("format", "html").lower()
        
        if not start_date_str or not end_date_str:
            return {"error": "start_date e end_date são obrigatórios"}, 400
        
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return {"error": "Formato de data inválido. Use YYYY-MM-DD"}, 400
        
        if format_type == "html":
            report = HTMLReport()
            content = report.generate(start_date, end_date)
            
            return Response(
                content,
                mimetype="text/html",
                headers={
                    "Content-Disposition": f"attachment; filename=relatorio_{start_date_str}_a_{end_date_str}.html"
                }
            )
        
        elif format_type == "pdf":
            report = PDFReport()
            pdf_bytes = report.generate(start_date, end_date)
            
            # Verificar se realmente é PDF (deve começar com %PDF)
            print(f"[DEBUG] PDF bytes preview: {pdf_bytes[:20]}")
            
            return Response(
                pdf_bytes,
                mimetype="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=relatorio_{start_date_str}_a_{end_date_str}.pdf"
                }
            )
        
        else:
            return {"error": "Formato inválido. Use 'html' ou 'pdf'"}, 400


@api.route("/formats")
class ReportFormats(Resource):
    @handle_exceptions
    @api.doc("Retorna os formatos de relatório disponíveis")
    def get(self):
        return {
            "formats": [
                {"type": "html", "description": "Relatório em HTML (visualização web)"},
                {"type": "pdf", "description": "Relatório em PDF (download)"}
            ]
        }, 200