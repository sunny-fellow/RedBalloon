from utils.singleton import Singleton
from utils.adapter.json_logger_adapter import JsonLoggerAdapter
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Callable

class EventType(Enum):
    SUBMISSION_ACCEPTED = "submission.accepted"
    PROBLEM_CREATED = "problem.created"
    USER_FOLLOWED = "user.followed"
    ROOM_PARTICIPANT_JOINED = "room.joined"
    COMMENT_ADDED = "comment.added"

@dataclass
class Event:
    type: EventType
    payload: dict
    timestamp: datetime = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now()

class EventListener:
    def handle(self, event: Event) -> None:
        raise NotImplementedError

@Singleton
class EventBus:
    def __init__(self):
        self.listeners: Dict[EventType, List[EventListener]] = {}
        self.logger = JsonLoggerAdapter("logs", "events.json")
    
    def subscribe(self, event_type: EventType, listener: EventListener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        self.listeners[event_type].append(listener)
        self.logger.info(f"Listener subscribed", {
            "event_type": event_type.value,
            "listener": listener.__class__.__name__
        })
    
    def emit(self, event: Event):
        self.logger.debug(f"Event emitted", {
            "event_type": event.type.value,
            "payload": event.payload
        })
        
        for listener in self.listeners.get(event.type, []):
            try:
                listener.handle(event)
            
            except Exception as e:
                self.logger.error(f"Listener failed", {
                    "event_type": event.type.value,
                    "listener": listener.__class__.__name__,
                    "error": str(e)
                })