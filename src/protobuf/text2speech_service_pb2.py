# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: text2speech_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='text2speech_service.proto',
  package='Text2SpeechRPC',
  syntax='proto3',
  serialized_options=b'\242\002\003RTG',
  serialized_pb=b'\n\x19text2speech_service.proto\x12\x0eText2SpeechRPC\"&\n\x08TTSInput\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0c\n\x04lang\x18\x02 \x01(\t\"\x19\n\tTTSOutput\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32Y\n\x12Text2SpeechService\x12\x43\n\x0cTextToSpeech\x12\x18.Text2SpeechRPC.TTSInput\x1a\x19.Text2SpeechRPC.TTSOutputB\x06\xa2\x02\x03RTGb\x06proto3'
)




_TTSINPUT = _descriptor.Descriptor(
  name='TTSInput',
  full_name='Text2SpeechRPC.TTSInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='Text2SpeechRPC.TTSInput.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lang', full_name='Text2SpeechRPC.TTSInput.lang', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=83,
)


_TTSOUTPUT = _descriptor.Descriptor(
  name='TTSOutput',
  full_name='Text2SpeechRPC.TTSOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='Text2SpeechRPC.TTSOutput.data', index=0,
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
  serialized_start=85,
  serialized_end=110,
)

DESCRIPTOR.message_types_by_name['TTSInput'] = _TTSINPUT
DESCRIPTOR.message_types_by_name['TTSOutput'] = _TTSOUTPUT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TTSInput = _reflection.GeneratedProtocolMessageType('TTSInput', (_message.Message,), {
  'DESCRIPTOR' : _TTSINPUT,
  '__module__' : 'text2speech_service_pb2'
  # @@protoc_insertion_point(class_scope:Text2SpeechRPC.TTSInput)
  })
_sym_db.RegisterMessage(TTSInput)

TTSOutput = _reflection.GeneratedProtocolMessageType('TTSOutput', (_message.Message,), {
  'DESCRIPTOR' : _TTSOUTPUT,
  '__module__' : 'text2speech_service_pb2'
  # @@protoc_insertion_point(class_scope:Text2SpeechRPC.TTSOutput)
  })
_sym_db.RegisterMessage(TTSOutput)


DESCRIPTOR._options = None

_TEXT2SPEECHSERVICE = _descriptor.ServiceDescriptor(
  name='Text2SpeechService',
  full_name='Text2SpeechRPC.Text2SpeechService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=112,
  serialized_end=201,
  methods=[
  _descriptor.MethodDescriptor(
    name='TextToSpeech',
    full_name='Text2SpeechRPC.Text2SpeechService.TextToSpeech',
    index=0,
    containing_service=None,
    input_type=_TTSINPUT,
    output_type=_TTSOUTPUT,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TEXT2SPEECHSERVICE)

DESCRIPTOR.services_by_name['Text2SpeechService'] = _TEXT2SPEECHSERVICE

# @@protoc_insertion_point(module_scope)
