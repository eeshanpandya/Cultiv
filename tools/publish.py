#!/usr/bin/env python3
"""Encrypt Cultiv editions for the public site.

Usage:
  CULTIV_PASSCODE='...' python3 tools/publish.py --site . \
      --edition path/to/2026-11-06.json [--edition ...] \
      --threads path/to/threads_dir_or_file \
      --index path/to/index.json

- Edition files are the plain edition documents (the "date" field names the file).
- --threads takes a folder of thread documents (file name = thread id) or one JSON
  file holding a list of threads that each carry an "id".
- --index is the meta/index document ({"dates": [...]}).
Everything is encrypted with AES-256-GCM using a key derived from the passcode
(PBKDF2-SHA256). data/meta.json holds the salt; it is created once and reused so
the passcode keeps working. Requires: pip install cryptography
"""
import argparse, base64, glob, json, os, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 310000
b64 = lambda b: base64.b64encode(b).decode()

def derive(passcode, salt, iters):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters).derive(passcode.encode())

def enc(key, obj):
    iv = secrets.token_bytes(12)
    ct = AESGCM(key).encrypt(iv, json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode(), None)
    return {"v": 1, "iv": b64(iv), "ct": b64(ct)}

def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=".")
    ap.add_argument("--edition", action="append", default=[])
    ap.add_argument("--threads")
    ap.add_argument("--index")
    a = ap.parse_args()
    pw = os.environ.get("CULTIV_PASSCODE", "")
    if not pw:
        sys.exit("Set CULTIV_PASSCODE")
    data = os.path.join(a.site, "data")
    meta_p = os.path.join(data, "meta.json")
    if os.path.exists(meta_p):
        meta = json.load(open(meta_p))
        key = derive(pw, base64.b64decode(meta["salt"]), meta["iter"])
        try:
            iv = base64.b64decode(meta["check"]["iv"]); ct = base64.b64decode(meta["check"]["ct"])
            if json.loads(AESGCM(key).decrypt(iv, ct, None)).get("ok") != "cultiv":
                raise ValueError
        except Exception:
            sys.exit("Passcode does not match the existing site. Nothing written.")
    else:
        salt = secrets.token_bytes(16)
        key = derive(pw, salt, ITER)
        meta = {"v": 1, "salt": b64(salt), "iter": ITER, "check": enc(key, {"ok": "cultiv"})}
        write(meta_p, meta)
    n = 0
    for p in a.edition:
        ed = json.load(open(p))
        d = ed.get("date") or os.path.splitext(os.path.basename(p))[0]
        write(os.path.join(data, "editions", d + ".json"), enc(key, ed)); n += 1
    if a.threads:
        if os.path.isdir(a.threads):
            ths = []
            for f in sorted(glob.glob(os.path.join(a.threads, "*.json"))):
                t = json.load(open(f)); t.setdefault("id", os.path.splitext(os.path.basename(f))[0]); ths.append(t)
        else:
            ths = json.load(open(a.threads))
        write(os.path.join(data, "threads.json"), enc(key, {"threads": ths}))
    if a.index:
        idx = json.load(open(a.index))
        write(os.path.join(data, "index.json"), enc(key, {"dates": idx.get("dates", [])}))
    print(f"Encrypted {n} edition(s){', threads' if a.threads else ''}{', index' if a.index else ''} into {data}")

if __name__ == "__main__":
    main()
