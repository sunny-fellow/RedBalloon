from flask_restx import Namespace, Resource
from flask import request
from utils.handle_exceptions import handle_exceptions
from room.service import RoomService

service = RoomService()

api = Namespace("room", description="Endpoints iniciais sobre sala")

# Models
from room.models.create import CreateRoomModel
from room.models.enter import EnterRoomModel

# Commands
from room.commands.create import CreateRoomCommand
from room.commands.enter import EnterRoomCommand
from room.commands.list import ListRoomCommand

@api.route("/list")
class RoomList(Resource):

    @handle_exceptions
    @api.doc("Lista as salas criadas ativas")
    @api.param("query", "Query de busca de salas")
    def get(self):
        query = request.args.get("query", "")
        command = ListRoomCommand(service, query)
        return command.execute(), 200

@api.route("/create")
class CreateRoom(Resource):

    @handle_exceptions
    @api.doc("Endpoint para criação de uma sala")
    @api.expect(CreateRoomModel(api), validate = True)
    def post(self):
        data = api.payload
        command = CreateRoomCommand(service, data)
        return command.execute(), 201


@api.route("/enter")
class EnterRoom(Resource):

    @handle_exceptions
    @api.doc("Endpoint para entrar em uma sala existente")
    @api.expect(EnterRoomModel(api), validate = True)
    def post(self):
        data = api.payload
        command = EnterRoomCommand(service, data)
        return command.execute(), 200