from bson import ObjectId
from bson.errors import InvalidId
from tornado.escape import json_encode, json_decode
from tornado.web import RequestHandler, Finish


class BodyExtractor:
    def __init__(self, handler: RequestHandler):
        self.handler = handler

    def body(self) -> dict:
        try:
            return json_decode(self.handler.request.body)
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid body,body=%s" % self.handler.request.body
                    }
                )
            )
            raise Finish()

    def context(self) -> dict:
        try:
            return self.body()["context"] if "context" in self.body() else None
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "body [context]"
                    }
                )
            )
            raise Finish()


class ParamExtractor:
    def __init__(self, handler: RequestHandler):
        self.handler = handler
        pass

    def session_id(self):
        raw_session_id = self.handler.get_argument("session_id", None)
        if raw_session_id is None:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param(s) session_id"
                    }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_session_id)
        except InvalidId:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=session_id,session_id=%s" % raw_session_id
                    }
                )
            )
            raise Finish()

    def application_id(self):
        raw_application_id = self.handler.get_argument("application_id", None)
        if raw_application_id is None:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param(s) application_id"
                    }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_application_id)
        except InvalidId:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=application_id,application_id=%s" % raw_application_id
                    }
                )
            )
            raise Finish()

    def user_id(self) -> ObjectId:
        raw_user_id = self.handler.get_argument("user_id", None)
        try:
            return ObjectId(raw_user_id) if raw_user_id is not None else None
        except InvalidId:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=user_id,user_id=%s" % raw_user_id
                    }
                )
            )
            raise Finish()

    def locale(self):
        locale = self.handler.get_argument("locale", None)
        if locale is None:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=locale"
                    }
                )
            )
            raise Finish()
        else:
            return locale
