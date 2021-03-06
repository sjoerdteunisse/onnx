from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .onnx_pb import *  # noqa
from .version import version as __version__  # noqa

# Import common subpackages so they're available when you 'import onnx'
import onnx.helper  # noqa
import onnx.checker  # noqa
import onnx.defs  # noqa

import google.protobuf.message


def load(obj):
    '''
    Loads a binary protobuf that stores onnx model

    @params
    Takes a file-like object (has "read" function)
    or a string containing a file name
    @return ONNX ModelProto object
    '''
    if hasattr(obj, 'read') and callable(obj.read):
        s = obj.read()
    else:
        with open(obj, 'rb') as f:
            s = f.read()
    return load_from_string(s)


def load_from_string(s):
    '''
    Loads a binary string that stores onnx model

    @params
    Takes a string object containing protobuf
    @return ONNX ModelProto object
    '''
    model = ModelProto()
    decoded = model.ParseFromString(s)
    # in python implementation ParseFromString returns None
    if decoded is not None and decoded != len(s):
        raise google.protobuf.message.DecodeError(
            "Protobuf decoding consumed too few bytes: {} out of {}".format(
                decoded, len(s)))
    return model


def _save(model, writable):
    if isinstance(model, ModelProto):
        writable.write(model.SerializeToString())
    elif isinstance(model, str):
        writable.write(model)
    else:
        raise ValueError('Model is neither ModelProto nor str.\n{}'.format(model))


def save(model, f):
    '''
    Saves the model to the specified path.

    @params
    Takes an ONNX model (ModelProto or string) and a path (writable or string)
    '''
    if hasattr(f, 'write') and callable(f.write):
        _save(model, f)
    else:
        with open(f, 'wb') as writable:
            _save(model, writable)
