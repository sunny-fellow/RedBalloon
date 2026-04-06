# reports/html_report.py
from utils.reports.base_report import BaseReport
from datetime import datetime


class HTMLReport(BaseReport):
    """
    Geração de relatório em formato HTML
    """
    
    def _generate_header(self, start_date: datetime, end_date: datetime) -> str:
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Estatísticas de Acesso</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .period {{
            margin-top: 10px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 20px;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background-color: #f8f9fa;
            color: #333;
            font-weight: 600;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📊 Relatório de Estatísticas de Acesso</h1>
        <div class="period">
            Período: {start_date.strftime('%d/%m/%Y %H:%M')} a {end_date.strftime('%d/%m/%Y %H:%M')}
        </div>
    </div>
    <div class="content">
"""
    
    def _format_data(self, statistics: dict) -> str:
        html = ""
        
        # Resumo geral
        html += """
        <div class="section">
            <h2>📈 Resumo Geral</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total de Acessos</h3>
                    <div class="value">{}</div>
                </div>
                <div class="stat-card">
                    <h3>Dias no Período</h3>
                    <div class="value">{}</div>
                </div>
            </div>
        </div>
        """.format(
            statistics["summary"]["total_accesses"],
            statistics["summary"]["period"]["days"]
        )
        
        # Estatísticas de Submissões
        html += """
        <div class="section">
            <h2>💻 Submissões</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total de Submissões</h3>
                    <div class="value">{}</div>
                </div>
                <div class="stat-card">
                    <h3>Submissões Aceitas</h3>
                    <div class="value">{}</div>
                </div>
                <div class="stat-card">
                    <h3>Taxa de Aceitação</h3>
                    <div class="value">{}%</div>
                </div>
            </div>
            <table>
                <tr><th>Tipo</th><th>Quantidade</th></tr>
                <tr><td>❌ Wrong Answer</td><td>{}</td></tr>
                <tr><td>⏱️ Time Limit Exceeded</td><td>{}</td></tr>
                <tr><td>🔧 Compilation Error</td><td>{}</td></tr>
            </table>
        </div>
        """.format(
            statistics["submissions"]["total"],
            statistics["submissions"]["accepted"],
            statistics["submissions"]["acceptance_rate"],
            statistics["submissions"]["wrong_answer"],
            statistics["submissions"]["time_limit_exceeded"],
            statistics["submissions"]["compilation_error"]
        )
        
        # Estatísticas de Problemas
        html += """
        <div class="section">
            <h2>📝 Problemas Criados</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total de Problemas</h3>
                    <div class="value">{}</div>
                </div>
            </div>
            <table>
                <tr><th>Dificuldade</th><th>Quantidade</th></tr>
                <tr><td>🟢 Easy</td><td>{}</td></tr>
                <tr><td>🟡 Medium</td><td>{}</td></tr>
                <tr><td>🔴 Hard</td><td>{}</td></tr>
            </table>
        </div>
        """.format(
            statistics["problems"]["total"],
            statistics["problems"]["by_difficulty"]["easy"],
            statistics["problems"]["by_difficulty"]["medium"],
            statistics["problems"]["by_difficulty"]["hard"]
        )
        
        # Engajamento
        html += """
        <div class="section">
            <h2>💬 Engajamento</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total de Comentários</h3>
                    <div class="value">{}</div>
                </div>
                <div class="stat-card">
                    <h3>Salas Criadas</h3>
                    <div class="value">{}</div>
                </div>
                <div class="stat-card">
                    <h3>Total de Participantes</h3>
                    <div class="value">{}</div>
                </div>
                <div class="stat-card">
                    <h3>Média por Sala</h3>
                    <div class="value">{}</div>
                </div>
            </div>
        </div>
        """.format(
            statistics["engagement"]["total_comments"],
            statistics["engagement"]["total_rooms"],
            statistics["engagement"]["total_participants"],
            statistics["engagement"]["avg_participants_per_room"]
        )
        
        return html
    
    def _generate_footer(self) -> str:
        return """
    </div>
    <div class="footer">
        <p>Relatório gerado automaticamente pelo sistema RedBalloon</p>
        <p>Data de geração: {}</p>
    </div>
</div>
</body>
</html>
        """.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))