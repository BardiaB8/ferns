# Ferns

(Warning: This is a prototype. Do not use for sensitive communication.)

Ferns performs symmetric cryptography using Fernet. By placing accessible encryption into the hands of the user, Ferns attempts to address the issue of communicating over networks that may be watched by an adversary.

![avif](assets/fernstest.avif)

## Usage

Random keys can be created using `createKey.py`, but it is recommended to use `keyExchange.py` instead, which can perform a key exchange using the SPAKE2 algorithm. To use SPAKE2 you need to have agreed upon a shared password ahead of time.

To use `ferns.py`, you first need a key, which must be securely exchanged with the person you're communicating with. Anyone with a key can decrypt messages encrypted with it. To decrypt messages, select a message and press `Ctrl+.`.

### Secondary actions

This is called the Jot window: ![](assets/jot_window.png)

To change the width of the Jot window, right-click and hold the drag icon. The width of the window will change with the movement of the mouse.

To clear the message entry, right-click the message icon.

Clicking on the attack button allows you to encrypt a file. To decrypt a file, right-click the attach button.

## Dependencies

`pip install cryptography pynput spake2`
