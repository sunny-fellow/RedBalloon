# utils/base_report.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Union
from database.service import DatabaseService
from utils.adapter.logger_factory import LoggerFactory
from sqlalchemy import text

class BaseReport(ABC):
    """
    Template Method para geração de relatórios de estatísticas de acesso
    """
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.logger = LoggerFactory.create_logger()
    
    def generate(self, start_date: datetime, end_date: datetime) -> Union[str, bytes]:
        """
        Método template - pode retornar str (HTML/TXT) ou bytes (PDF)
        """
        self._validate_dates(start_date, end_date)
        access_data = self._collect_access_data(start_date, end_date)
        statistics = self._calculate_statistics(access_data)
        formatted_data = self._format_data(statistics)
        header = self._generate_header(start_date, end_date)
        footer = self._generate_footer()
        report = self._assemble_report(header, formatted_data, footer)
        self._log_generation(start_date, end_date, access_data)
        return report
    
    @abstractmethod
    def _format_data(self, statistics: Dict) -> str:
        pass
    
    @abstractmethod
    def _generate_header(self, start_date: datetime, end_date: datetime) -> str:
        pass
    
    @abstractmethod
    def _generate_footer(self) -> str:
        pass
    
    def _validate_dates(self, start_date: datetime, end_date: datetime) -> None:
        if start_date > end_date:
            raise ValueError("Data inicial não pode ser maior que data final")
        if end_date > datetime.now():
            raise ValueError("Data final não pode ser no futuro")
        if (end_date - start_date).days > 365:
            raise ValueError("Período máximo é de 365 dias")
    
    def _collect_access_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Coleta dados de acesso do banco de dados"""
        def func(session):
            # Converter datas para string ISO (formato das colunas String)
            start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
            end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')
            
            submissions = self._get_submissions_data(session, start_date, end_date)
            problems = self._get_problems_data(session, start_str, end_str)
            comments = self._get_comments_data(session, start_str, end_str)
            rooms = self._get_rooms_data(session, start_str, end_str)
            
            return {
                "submissions": submissions,
                "problems": problems,
                "comments": comments,
                "rooms": rooms,
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "days": (end_date - start_date).days
                }
            }
        
        return self.db_service.run(func)
    
    def _get_submissions_data(self, session, start_date: datetime, end_date: datetime) -> Dict:
        """Busca dados de submissões (submitted_at é DateTime)"""
        result = session.execute(
            text("""
                SELECT 
                    COUNT(*) as total_submissions,
                    COUNT(DISTINCT user_id) as unique_users,
                    SUM(CASE WHEN status = 'ACCEPTED' THEN 1 ELSE 0 END) as accepted,
                    SUM(CASE WHEN status = 'WRONG_ANSWER' THEN 1 ELSE 0 END) as wrong_answer,
                    SUM(CASE WHEN status = 'TIME_LIMIT_EXCEEDED' THEN 1 ELSE 0 END) as tle,
                    SUM(CASE WHEN status = 'COMPILATION_ERROR' THEN 1 ELSE 0 END) as compilation_error
                FROM submissions
                WHERE submitted_at >= :start AND submitted_at <= :end
            """),
            {"start": start_date, "end": end_date}
        )
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {
            "total_submissions": 0,
            "unique_users": 0,
            "accepted": 0,
            "wrong_answer": 0,
            "tle": 0,
            "compilation_error": 0
        }
    
    def _get_problems_data(self, session, start_date: str, end_date: str) -> Dict:
        """Busca dados de problemas criados (created_at é String)"""
        result = session.execute(
            text("""
                SELECT 
                    COUNT(*) as total_problems,
                    COUNT(DISTINCT creator_id) as unique_creators,
                    SUM(CASE WHEN difficulty = 'EASY' THEN 1 ELSE 0 END) as easy,
                    SUM(CASE WHEN difficulty = 'MEDIUM' THEN 1 ELSE 0 END) as medium,
                    SUM(CASE WHEN difficulty = 'HARD' THEN 1 ELSE 0 END) as hard
                FROM problems
                WHERE created_at >= :start AND created_at <= :end
                AND private = false
            """),
            {"start": start_date, "end": end_date}
        )
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {
            "total_problems": 0,
            "unique_creators": 0,
            "easy": 0,
            "medium": 0,
            "hard": 0
        }
    
    def _get_comments_data(self, session, start_date: str, end_date: str) -> Dict:
        """Busca dados de comentários (sent_at é String, tabela é message_contexts)"""
        result = session.execute(
            text("""
                SELECT 
                    COUNT(*) as total_comments,
                    COUNT(DISTINCT m.user_id) as unique_users,
                    COUNT(DISTINCT mc.context_type) as contexts_used
                FROM messages m
                JOIN message_contexts mc ON m.message_id = mc.message_id
                WHERE m.sent_at >= :start AND m.sent_at <= :end
            """),
            {"start": start_date, "end": end_date}
        )
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {
            "total_comments": 0,
            "unique_users": 0,
            "contexts_used": 0
        }
    
    # utils/base_report.py - método _get_rooms_data corrigido

    def _get_rooms_data(self, session, start_date: str, end_date: str) -> Dict:
        """Busca dados de salas de competição usando joined_at dos participantes"""
        result = session.execute(
            text("""
                SELECT 
                    COUNT(DISTINCT r.room_id) as total_rooms,
                    COUNT(DISTINCT rp.user_id) as unique_creators,
                    COUNT(DISTINCT rp.user_id) as total_participants,
                    0 as avg_participants
                FROM rooms r
                JOIN room_participants rp ON r.room_id = rp.room_id
                WHERE rp.joined_at >= :start AND rp.joined_at <= :end
            """),
            {"start": start_date, "end": end_date}
        )
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return {
            "total_rooms": 0,
            "unique_creators": 0,
            "total_participants": 0,
            "avg_participants": 0
        }
    
    def _calculate_statistics(self, access_data: Dict) -> Dict:
        submissions = access_data["submissions"]
        problems = access_data["problems"]
        comments = access_data["comments"]
        rooms = access_data["rooms"]
        
        total_accesses = (
            submissions.get("total_submissions", 0) +
            problems.get("total_problems", 0) +
            comments.get("total_comments", 0) +
            rooms.get("total_rooms", 0)
        )
        
        acceptance_rate = 0
        if submissions.get("total_submissions", 0) > 0:
            acceptance_rate = (submissions.get("accepted", 0) / 
                              submissions["total_submissions"] * 100)
        
        return {
            "summary": {
                "total_accesses": total_accesses,
                "unique_users": {
                    "submissions": submissions.get("unique_users", 0),
                    "problems": problems.get("unique_creators", 0),
                    "comments": comments.get("unique_users", 0),
                    "rooms": rooms.get("unique_creators", 0)
                },
                "period": access_data["period"]
            },
            "submissions": {
                "total": submissions.get("total_submissions", 0),
                "accepted": submissions.get("accepted", 0),
                "acceptance_rate": round(acceptance_rate, 2),
                "wrong_answer": submissions.get("wrong_answer", 0),
                "time_limit_exceeded": submissions.get("tle", 0),
                "compilation_error": submissions.get("compilation_error", 0)
            },
            "problems": {
                "total": problems.get("total_problems", 0),
                "by_difficulty": {
                    "easy": problems.get("easy", 0),
                    "medium": problems.get("medium", 0),
                    "hard": problems.get("hard", 0)
                }
            },
            "engagement": {
                "total_comments": comments.get("total_comments", 0),
                "total_rooms": rooms.get("total_rooms", 0),
                "total_participants": rooms.get("total_participants", 0),
                "avg_participants_per_room": round(rooms.get("avg_participants", 0), 2)
            }
        }
    
    def _assemble_report(self, header: str, body: str, footer: str) -> str:
        return f"{header}\n\n{body}\n\n{footer}"
    
    def _log_generation(self, start_date: datetime, end_date: datetime, access_data: Dict) -> None:
        records_count = (
            access_data.get("submissions", {}).get("total_submissions", 0) +
            access_data.get("problems", {}).get("total_problems", 0) +
            access_data.get("comments", {}).get("total_comments", 0) +
            access_data.get("rooms", {}).get("total_rooms", 0)
        )
        
        self.logger.info(
            f"Relatório gerado com sucesso",
            context={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "records_count": records_count,
                "report_type": self.__class__.__name__,
                "action": "generate_report"
            }
        )