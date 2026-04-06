# reports/controller.py
from flask_restx import Namespace, Resource
from flask import request, Response
from datetime import datetime
from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id
from utils.reports.report_factory import ReportFactory, ReportType

api = Namespace("reports", description="Geração de Relatórios Estatísticos")

@api.route("/access-stats")
class AccessStatsReport(Resource):
    @handle_exceptions
    @api.doc("Gera relatório de estatísticas de acesso dos usuários")
    @api.param("start_date", "Data inicial (YYYY-MM-DD)")
    @api.param("end_date", "Data final (YYYY-MM-DD)")
    @api.param("format", "Formato do relatório: html ou pdf")
    def get(self):
        # Verificar permissão (apenas admin)
        user_id = get_user_id()
        # TODO: Verificar se user_id tem permissão de admin
        
        # Obter parâmetros
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
        
        # Criar relatório conforme formato
        if format_type == "html":
            report_type = ReportType.HTML
            content_type = "text/html"
            extension = "html"
        elif format_type == "pdf":
            report_type = ReportType.PDF
            content_type = "text/plain"  # Simulado - em produção use application/pdf
            extension = "txt"
        else:
            return {"error": "Formato inválido. Use 'html' ou 'pdf'"}, 400
        
        # Gerar relatório usando Template Method
        report = ReportFactory.create_report(report_type)
        report_content = report.generate(start_date, end_date)
        
        # Retornar como download
        return Response(
            report_content,
            mimetype=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=relatorio_acessos_{start_date_str}_a_{end_date_str}.{extension}"
            }
        )


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