# utils/pdf_report.py
from utils.reports.base_report import BaseReport
from datetime import datetime


class PDFReport(BaseReport):
    """
    Geração de relatório em formato PDF (simulado com texto formatado)
    """
    
    def _generate_header(self, start_date: datetime, end_date: datetime) -> str:
        return f"""================================================================================
                    RELATÓRIO DE ESTATÍSTICAS DE ACESSO
================================================================================

Período: {start_date.strftime('%d/%m/%Y %H:%M')} a {end_date.strftime('%d/%m/%Y %H:%M')}
Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

"""
    
    def _format_data(self, statistics: dict) -> str:
        # Extrair valores com fallback para 0 caso sejam None
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
        total_rooms = statistics.get('engagement', {}).get('total_rooms', 0) or 0
        total_participants = statistics.get('engagement', {}).get('total_participants', 0) or 0
        avg_participants = statistics.get('engagement', {}).get('avg_participants_per_room', 0) or 0
        
        pdf = ""
        
        # Resumo Geral
        pdf += """
┌─────────────────────────────────────────────────────────────────────────────┐
│                              RESUMO GERAL                                    │
├─────────────────────────────────────────────────────────────────────────────┤
"""
        pdf += f"""
│ Total de Acessos no período: {total_accesses:<45} │
│ Dias no período:              {days:<45} │
│                                                                               │
│ Usuários Únicos por Tipo de Ação:                                            │
│   • Submissões:  {unique_submissions:<44} │
│   • Problemas:   {unique_problems:<44} │
│   • Comentários: {unique_comments:<44} │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        
        # Estatísticas de Submissões
        pdf += """
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SUBMISSÕES                                        │
├─────────────────────────────────────────────────────────────────────────────┤
"""
        pdf += f"""
│ Total de Submissões:          {total_submissions:<45} │
│ Submissões Aceitas:           {accepted:<45} │
│ Taxa de Aceitação:            {acceptance_rate}%{' ' * (44 - len(str(acceptance_rate))) }│
│                                                                               │
│ Detalhamento de Erros:                                                       │
│   • Wrong Answer:             {wrong_answer:<45} │
│   • Time Limit Exceeded:      {tle:<45} │
│   • Compilation Error:        {compilation_error:<45} │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        
        # Estatísticas de Problemas
        pdf += """
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROBLEMAS CRIADOS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
"""
        pdf += f"""
│ Total de Problemas:           {total_problems:<45} │
│                                                                               │
│ Por Dificuldade:                                                             │
│   • Easy:                     {easy:<45} │
│   • Medium:                   {medium:<45} │
│   • Hard:                     {hard:<45} │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        
        # Engajamento
        pdf += """
┌─────────────────────────────────────────────────────────────────────────────┐
│                             ENGAJAMENTO                                      │
├─────────────────────────────────────────────────────────────────────────────┤
"""
        pdf += f"""
│ Total de Comentários:         {total_comments:<45} │
│ Total de Salas Criadas:       {total_rooms:<45} │
│ Total de Participantes:       {total_participants:<45} │
│ Média de Participantes/Sala:  {avg_participants:<45} │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        
        return pdf
    
    def _generate_footer(self) -> str:
        return """
================================================================================
                          FIM DO RELATÓRIO
================================================================================

Relatório gerado automaticamente pelo sistema RedBalloon

"""