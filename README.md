# Ferns

(Warning: This is a prototype. Do not use for sensitive communication.)

Ferns performs symmetric cryptography using Fernet. By placing accessible encryption into the hands of the user, Ferns attempts to address the issue of communicating over networks that may be watched by an adversary.

![Ferns demo](assets/ferns.gif)

## Usage

Keys can be created using `keyManage.py`. A secure key exchange algorithm has not been implemented yet.

To use `ferns.py`, you first need a key, which must be securely shared with the person you're communicating with. Anyone with a key can decrypt messages encrypted with it. To decrypt messages, select a message and press `Ctrl+.`.

## Dependencies

`pip install cryptography pynput`
