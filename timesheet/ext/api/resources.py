from typing import List

from flask import request
from flask_restful import Api, Resource

from timesheet.ext.db.models import Register

api = Api()


@api.resource("/api/register")
class ResourceRegisterPoint(Resource):
    def post(self) -> dict:
        data = request.json

        if data is None:
            response = {"success": False, "message": "Informe os dados da requisição"}

        else:
            id = data.get("id")  # Trocar para puxar pelo ID do usuário atual
            pause = data.get("pause")
            event = data.get("event")

            register = Register.create(
                user_id=id,
                pause=pause,
                event=event,
            )
            response = register.save()

        return response


@api.resource("/api/consult/<string:date>")
class ResourceConsultPoint(Resource):
    def get(self, date: str) -> List[dict]:
        user_id = 1
        response = [
            register.to_dict() for register in Register.get_by_date(user_id, date)
        ]

        return response
