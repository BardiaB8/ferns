# Ferns

(Warning: This is a prototype. Do not use for sensitive communication.)

Ferns performs symmetric cryptography using Fernet. By placing accessible encryption into the hands of the user, Ferns attempts to address the issue of communicating over networks that may be watched by an adversary.

![Ferns demo](assets/ferns_test.mp4)

## Usage

Random keys can be created using `createKey.py`, but it is recommended to use `keyExchange.py` instead, which can perform a key exchange using the SPAKE2 algorithm. To use SPAKE2 you need to have agreed upon a shared password ahead of time.

To use `ferns.py`, you first need a key, which must be securely exchanged with the person you're communicating with. Anyone with a key can decrypt messages encrypted with it. To decrypt messages, select a message and press `Ctrl+.`.

## Dependencies

`pip install cryptography pynput spake2`
