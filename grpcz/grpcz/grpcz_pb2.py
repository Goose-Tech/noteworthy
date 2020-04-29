# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpcz.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='grpcz.proto',
  package='grpcz',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0bgrpcz.proto\x12\x05grpcz\"\x14\n\x03\x41ny\x12\r\n\x05value\x18\x01 \x01(\x0c\"@\n\x0cGRPCZRequest\x12\x13\n\x0bmodule_path\x18\x01 \x01(\t\x12\x1b\n\x07request\x18\x02 \x01(\x0b\x32\n.grpcz.Any\"I\n\rGRPCZResponse\x12\n\n\x02ok\x18\x01 \x01(\x08\x12\x0e\n\x06result\x18\x02 \x01(\t\x12\x1c\n\x08response\x18\x03 \x01(\x0b\x32\n.grpcz.Any2=\n\x08\x44ispatch\x12\x31\n\x04\x63\x61ll\x12\x13.grpcz.GRPCZRequest\x1a\x14.grpcz.GRPCZResponseb\x06proto3'
)




_ANY = _descriptor.Descriptor(
  name='Any',
  full_name='grpcz.Any',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='grpcz.Any.value', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=42,
)


_GRPCZREQUEST = _descriptor.Descriptor(
  name='GRPCZRequest',
  full_name='grpcz.GRPCZRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='module_path', full_name='grpcz.GRPCZRequest.module_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='request', full_name='grpcz.GRPCZRequest.request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=108,
)


_GRPCZRESPONSE = _descriptor.Descriptor(
  name='GRPCZResponse',
  full_name='grpcz.GRPCZResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ok', full_name='grpcz.GRPCZResponse.ok', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='grpcz.GRPCZResponse.result', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='grpcz.GRPCZResponse.response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=110,
  serialized_end=183,
)

_GRPCZREQUEST.fields_by_name['request'].message_type = _ANY
_GRPCZRESPONSE.fields_by_name['response'].message_type = _ANY
DESCRIPTOR.message_types_by_name['Any'] = _ANY
DESCRIPTOR.message_types_by_name['GRPCZRequest'] = _GRPCZREQUEST
DESCRIPTOR.message_types_by_name['GRPCZResponse'] = _GRPCZRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Any = _reflection.GeneratedProtocolMessageType('Any', (_message.Message,), {
  'DESCRIPTOR' : _ANY,
  '__module__' : 'grpcz_pb2'
  # @@protoc_insertion_point(class_scope:grpcz.Any)
  })
_sym_db.RegisterMessage(Any)

GRPCZRequest = _reflection.GeneratedProtocolMessageType('GRPCZRequest', (_message.Message,), {
  'DESCRIPTOR' : _GRPCZREQUEST,
  '__module__' : 'grpcz_pb2'
  # @@protoc_insertion_point(class_scope:grpcz.GRPCZRequest)
  })
_sym_db.RegisterMessage(GRPCZRequest)

GRPCZResponse = _reflection.GeneratedProtocolMessageType('GRPCZResponse', (_message.Message,), {
  'DESCRIPTOR' : _GRPCZRESPONSE,
  '__module__' : 'grpcz_pb2'
  # @@protoc_insertion_point(class_scope:grpcz.GRPCZResponse)
  })
_sym_db.RegisterMessage(GRPCZResponse)



_DISPATCH = _descriptor.ServiceDescriptor(
  name='Dispatch',
  full_name='grpcz.Dispatch',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=185,
  serialized_end=246,
  methods=[
  _descriptor.MethodDescriptor(
    name='call',
    full_name='grpcz.Dispatch.call',
    index=0,
    containing_service=None,
    input_type=_GRPCZREQUEST,
    output_type=_GRPCZRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DISPATCH)

DESCRIPTOR.services_by_name['Dispatch'] = _DISPATCH

# @@protoc_insertion_point(module_scope)