# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: XiguaGift.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='XiguaGift.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x0fXiguaGift.proto\"\\\n\x04Gift\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x1a\n\x04gift\x18\x02 \x02(\x0b\x32\x0c.Gift.Detail\x1a,\n\x06\x44\x65tail\x12\x0f\n\x07gift_id\x18\x01 \x02(\t\x12\x11\n\tgift_name\x18\x02 \x02(\t'
)




_GIFT_DETAIL = _descriptor.Descriptor(
  name='Detail',
  full_name='Gift.Detail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gift_id', full_name='Gift.Detail.gift_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gift_name', full_name='Gift.Detail.gift_name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=67,
  serialized_end=111,
)

_GIFT = _descriptor.Descriptor(
  name='Gift',
  full_name='Gift',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Gift.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gift', full_name='Gift.gift', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GIFT_DETAIL, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=111,
)

_GIFT_DETAIL.containing_type = _GIFT
_GIFT.fields_by_name['gift'].message_type = _GIFT_DETAIL
DESCRIPTOR.message_types_by_name['Gift'] = _GIFT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Gift = _reflection.GeneratedProtocolMessageType('Gift', (_message.Message,), {

  'Detail' : _reflection.GeneratedProtocolMessageType('Detail', (_message.Message,), {
    'DESCRIPTOR' : _GIFT_DETAIL,
    '__module__' : 'XiguaGift_pb2'
    # @@protoc_insertion_point(class_scope:Gift.Detail)
    })
  ,
  'DESCRIPTOR' : _GIFT,
  '__module__' : 'XiguaGift_pb2'
  # @@protoc_insertion_point(class_scope:Gift)
  })
_sym_db.RegisterMessage(Gift)
_sym_db.RegisterMessage(Gift.Detail)


# @@protoc_insertion_point(module_scope)