from bson import ObjectId
from bson.errors import InvalidId
from tornado.escape import json_encode, json_decode
from tornado.web import RequestHandler, Finish


class PathExtractor:
    def __init__(self, handler: RequestHandler):
        self.handler = handler

    def suggestion_id(self, suggestion_id) -> ObjectId:
        try:
            return ObjectId(suggestion_id)
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=suggestion_id,suggestion_id=%s" % suggestion_id
                    }
                )
            )
            raise Finish()


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

    def offset(self) -> int:
        raw_offset = self.handler.get_argument("offset", None)
        try:
            return int(raw_offset) if raw_offset is not None else None
        except InvalidId:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=offset,offset=%s" % raw_offset
                    }
                )
            )
            raise Finish()

    def page_size(self) -> int:
        raw_page_size = self.handler.get_argument("page_size", None)
        try:
            return int(raw_page_size) if raw_page_size is not None else None
        except InvalidId:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=page_size,page_size=%s" % raw_page_size
                    }
                )
            )
            raise Finish()
