#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import json
import base64
import jwt
import time
import random
from binascii import hexlify
from datetime import datetime, timezone

def base64url_decode(data: bytes) -> bytes:
    s = data.decode('utf-8')
    pad = 4 - (len(s) % 4)
    if pad != 4:
        s += '=' * pad
    return base64.urlsafe_b64decode(s)

def base64url_encode(data: bytes) -> bytes:
    s = base64.urlsafe_b64encode(data).rstrip(b'=')
    return s

def decode_jwt(token: str):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    header_b64, payload_b64, signature_b64 = parts
    header = json.loads(base64url_decode(header_b64.encode()))
    payload = json.loads(base64url_decode(payload_b64.encode()))
    signature = base64url_decode(signature_b64.encode())
    return header, payload, signature

def encode_jwt(header: dict, payload: dict, key: str, alg: str):
    return jwt.encode(payload=payload, key=key, algorithm=alg, headers=header)

def to_john(token: str):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    hp = parts[0] + '.' + parts[1]
    sig_hex = hexlify(base64url_decode(parts[2].encode())).decode()
    return f"{hp}#{sig_hex}"

def parse_jwt(token: str, human_time: bool = False):
    header, payload, signature = decode_jwt(token)
    print("Header:", json.dumps(header, indent=2))
    print("Payload:", json.dumps(payload, indent=2))
    if human_time:
        for tfield in ['iat','exp','nbf']:
            if tfield in payload:
                try:
                    val = int(payload[tfield])
                    dt = datetime.fromtimestamp(val, tz=timezone.utc)
                    print(f"{tfield} (UTC): {dt.isoformat()}")
                except:
                    pass
    print("Signature (hex):", hexlify(signature).decode())
    print("Algorithm:", header.get('alg','unknown'))

def resign_jwt(token: str, secret: str, alg: str, payload_update: str = None, payload_replace: str = None, header_update: str = None):
    h, p, _ = decode_jwt(token)
    if header_update:
        try:
            up = json.loads(header_update)
            for k,v in up.items():
                h[k] = v
        except:
            pass
    if payload_replace:
        try:
            p = json.loads(payload_replace)
        except:
            pass
    if payload_update:
        try:
            up = json.loads(payload_update)
            for k,v in up.items():
                p[k] = v
        except:
            pass
    if alg.lower() == 'none':
        h['alg'] = 'none'
        secret = ''
    try:
        new_token = encode_jwt(h, p, secret, alg)
        print("[New JWT]", new_token)
    except Exception as e:
        sys.stderr.write(f"[Error resigning] {str(e)}\n")

def bruteforce_jwt(token: str, wordlist: str, alg: str = "HS256"):
    try:
        h, p, sig = decode_jwt(token)
        sig_hex = hexlify(sig).decode()
        with open(wordlist, 'r', encoding='utf-8') as f:
            for line in f:
                candidate = line.strip()
                if not candidate:
                    continue
                try:
                    test_t = encode_jwt(h, p, candidate, alg)
                    t_parts = test_t.split('.')
                    if len(t_parts) == 3:
                        test_sig = t_parts[2]
                        test_sig_hex = hexlify(base64url_decode(test_sig.encode())).decode()
                        if test_sig_hex == sig_hex:
                            print(f"[+] Found secret: {candidate}")
                            return
                except:
                    pass
        print("[-] No matching secret found")
    except Exception as e:
        sys.stderr.write(f"[Error bruteforce] {str(e)}\n")

def fuzz_jwt(token: str, secret: str, alg: str, rounds: int = 5):
    try:
        h, p, _ = decode_jwt(token)
        for i in range(rounds):
            p_copy = dict(p)
            key_to_fuzz = random.choice(list(p_copy.keys())) if p_copy else None
            if key_to_fuzz:
                p_copy[key_to_fuzz] = "FUZZ_" + ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
            t = encode_jwt(h, p_copy, secret, alg)
            print(f"[Fuzz {i+1}] {t}")
    except Exception as e:
        sys.stderr.write(f"[Error fuzzing] {str(e)}\n")

def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="command", required=True)

    p_parse = subs.add_parser("parse")
    p_parse.add_argument("--jwt", required=True)
    p_parse.add_argument("--human-time", action="store_true")

    p_tojohn = subs.add_parser("tojohn")
    p_tojohn.add_argument("--jwt", required=True)

    p_resign = subs.add_parser("resign")
    p_resign.add_argument("--jwt", required=True)
    p_resign.add_argument("--secret", required=False, default="")
    p_resign.add_argument("--alg", required=True)
    p_resign.add_argument("--payload-update")
    p_resign.add_argument("--payload-replace")
    p_resign.add_argument("--header-update")

    p_brute = subs.add_parser("bruteforce")
    p_brute.add_argument("--jwt", required=True)
    p_brute.add_argument("--wordlist", required=True)
    p_brute.add_argument("--alg", default="HS256")

    p_fuzz = subs.add_parser("fuzz")
    p_fuzz.add_argument("--jwt", required=True)
    p_fuzz.add_argument("--secret", required=False, default="")
    p_fuzz.add_argument("--alg", default="HS256")
    p_fuzz.add_argument("--rounds", type=int, default=5)

    args = parser.parse_args()

    if args.command == "parse":
        parse_jwt(args.jwt, human_time=args.human_time)
    elif args.command == "tojohn":
        try:
            print(to_john(args.jwt))
        except Exception as e:
            sys.stderr.write(f"[Error tojohn] {str(e)}\n")
    elif args.command == "resign":
        resign_jwt(
            token=args.jwt,
            secret=args.secret,
            alg=args.alg,
            payload_update=args.payload_update,
            payload_replace=args.payload_replace,
            header_update=args.header_update
        )
    elif args.command == "bruteforce":
        bruteforce_jwt(
            token=args.jwt,
            wordlist=args.wordlist,
            alg=args.alg
        )
    elif args.command == "fuzz":
        fuzz_jwt(
            token=args.jwt,
            secret=args.secret,
            alg=args.alg,
            rounds=args.rounds
        )

if __name__ == "__main__":
    main()