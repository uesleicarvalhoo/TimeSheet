from datetime import datetime
from typing import List

from flask import request
from flask_login import current_user
from flask_pydantic import validate
from flask_restful import Api, Resource

from timesheet.ext.auth import check_api_auth
from timesheet.ext.db.models import Pauses, Register

from .schemas import Date, Pause

api = Api()


@api.resource("/api/register")
class ResourceRegisterPoint(Resource):
    @check_api_auth
    @validate(body=Pause)
    def post(self) -> dict:
        status = 201
        user_id = current_user.id
        pause_id = request.body_params.id
        event = request.body_params.event
        type = request.body_params.type
        hour = datetime.now().time()
        register = Register.get(user_id=user_id, date=datetime.now().date())

        if register is None:
            register = Register.create(user_id, date=datetime.now().date(), save=False)
            register.save()

        if type == "register":
            response = register.validate(event)
            if response["success"]:
                register.update(**{event: hour})
                response = register.save()
        else:
            if register.entry is None:
                response = {"success": False, "message": "Você precisa registrar a entrada primeiro"}

            else:
                pause = Pauses.get(register_id=register.id, pause_id=pause_id)
                if pause is None:
                    pause = Pauses.create(register.id, pause_id, save=False)

                response = pause.validate(event)
                if response["success"]:
                    pause.update(**{event: hour})
                    response = pause.save()

        if not response.get("success"):
            status = 400

        return response, status


@api.resource("/api/consult")
class ResourceConsultPoint(Resource):
    @check_api_auth
    @validate(query=Date)
    def get(self) -> List[dict]:
        register = Register.get_by_date(current_user.id, request.query_params.date)
        if register is None:
            return {}

        return register.to_json()
