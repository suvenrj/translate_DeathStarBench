# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: recommend.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0frecommend.proto\"4\n\x07Request\x12\x0f\n\x07require\x18\x01 \x01(\t\x12\x0b\n\x03lat\x18\x02 \x01(\x01\x12\x0b\n\x03lon\x18\x03 \x01(\x01\"\x1a\n\x06Result\x12\x10\n\x08HotelIds\x18\x01 \x03(\t29\n\x0eRecommendation\x12\'\n\x12GetRecommendations\x12\x08.Request\x1a\x07.Resultb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'recommend_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=19
  _REQUEST._serialized_end=71
  _RESULT._serialized_start=73
  _RESULT._serialized_end=99
  _RECOMMENDATION._serialized_start=101
  _RECOMMENDATION._serialized_end=158
# @@protoc_insertion_point(module_scope)
