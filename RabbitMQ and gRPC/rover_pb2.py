# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rover.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0brover.proto\"\x0f\n\rgetMapRequest\">\n\x0egetMapResponse\x12\x0b\n\x03row\x18\x01 \x01(\x05\x12\x0b\n\x03\x63ol\x18\x02 \x01(\x05\x12\x12\n\nmoving_map\x18\x03 \x03(\x05\"#\n\x0fgetMovesRequest\x12\x10\n\x08roverNum\x18\x01 \x01(\x05\" \n\x10getMovesResponse\x12\x0c\n\x04move\x18\x01 \x01(\t\"\x15\n\x13getSerialNumRequest\";\n\x14getSerialNumResponse\x12\x12\n\nserial_num\x18\x01 \x03(\t\x12\x0f\n\x07pin_num\x18\x02 \x03(\t\"#\n\x10isSuccessRequest\x12\x0f\n\x07success\x18\x01 \x01(\t\"$\n\x11isSuccessResponse\x12\x0f\n\x07\x63onfirm\x18\x01 \x01(\t\"\x19\n\nPinRequest\x12\x0b\n\x03pin\x18\x01 \x01(\t\"\x1b\n\x0bPinResponse\x12\x0c\n\x04recv\x18\x01 \x01(\t2\x90\x02\n\x0cRoverService\x12\x31\n\x0c\x63reate_files\x12\x0e.getMapRequest\x1a\x0f.getMapResponse\"\x00\x12\x35\n\x0crover_scrape\x12\x10.getMovesRequest\x1a\x11.getMovesResponse\"\x00\x12:\n\tfarm_keys\x12\x14.getSerialNumRequest\x1a\x15.getSerialNumResponse\"\x00\x12\x32\n\x07isAlive\x12\x11.isSuccessRequest\x1a\x12.isSuccessResponse\"\x00\x12&\n\x07sendPin\x12\x0b.PinRequest\x1a\x0c.PinResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rover_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETMAPREQUEST._serialized_start=15
  _GETMAPREQUEST._serialized_end=30
  _GETMAPRESPONSE._serialized_start=32
  _GETMAPRESPONSE._serialized_end=94
  _GETMOVESREQUEST._serialized_start=96
  _GETMOVESREQUEST._serialized_end=131
  _GETMOVESRESPONSE._serialized_start=133
  _GETMOVESRESPONSE._serialized_end=165
  _GETSERIALNUMREQUEST._serialized_start=167
  _GETSERIALNUMREQUEST._serialized_end=188
  _GETSERIALNUMRESPONSE._serialized_start=190
  _GETSERIALNUMRESPONSE._serialized_end=249
  _ISSUCCESSREQUEST._serialized_start=251
  _ISSUCCESSREQUEST._serialized_end=286
  _ISSUCCESSRESPONSE._serialized_start=288
  _ISSUCCESSRESPONSE._serialized_end=324
  _PINREQUEST._serialized_start=326
  _PINREQUEST._serialized_end=351
  _PINRESPONSE._serialized_start=353
  _PINRESPONSE._serialized_end=380
  _ROVERSERVICE._serialized_start=383
  _ROVERSERVICE._serialized_end=655
# @@protoc_insertion_point(module_scope)