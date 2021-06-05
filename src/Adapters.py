# System Imports#
import base64
import six
import struct

# Cryptography Imports #
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


# Method maps a JWK to a PEM #
def jwk_to_pem(jwk):
    # Algorithm type casts #
    exponent = base64_to_long(jwk['e'])
    modulus = base64_to_long(jwk['n'])
    numbers = RSAPublicNumbers(exponent, modulus)
    # Getting public key #
    public_key = numbers.public_key(backend=default_backend())
    # Mapping to PEM #
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Returning decoded PEM #
    return pem.decode("utf-8")


# Method casts base64 data to long #
def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return int_array_to_long_array(struct.unpack('%sB' % len(_d), _d))


# Method converts an int array to a long array #
def int_array_to_long_array(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)
