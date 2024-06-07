from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PostViewRequest(_message.Message):
    __slots__ = ("post_id",)
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    def __init__(self, post_id: _Optional[int] = ...) -> None: ...

class PostViewResponse(_message.Message):
    __slots__ = ("post_id", "post_view_count")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    POST_VIEW_COUNT_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    post_view_count: int
    def __init__(self, post_id: _Optional[int] = ..., post_view_count: _Optional[int] = ...) -> None: ...
