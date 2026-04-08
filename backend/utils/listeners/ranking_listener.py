from event_bus import EventListener, Event, EventType
from room.gateway.service import RoomGatewayService

class RankingUpdateListener(EventListener):
    def __init__(self):
        self.room_service = RoomGatewayService()
    
    def handle(self, event: Event):
        if event.type == EventType.SUBMISSION_ACCEPTED:
            room_id = event.payload.get("room_id")
            if room_id:
                # Atualiza ranking via WebSocket
                self.room_service.update_ranking(room_id)