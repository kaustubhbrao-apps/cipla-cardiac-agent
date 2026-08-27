#!/usr/bin/env python3
"""
Run every build step, then mirror the data where the serverless function can
actually read it.

    python3 build/build_all.py

Why the mirror: Vercel serves public/ from the CDN but does NOT bundle it into
the function's filesystem, so api/ask.py cannot open public/data/*.json at
runtime — it fails with FileNotFoundError on /var/task/public/data/... Files
that sit alongside the function are bundled, so the same JSON is copied to
api/_data/. The duplication is deliberate and small (~160 KB); the alternative
is the function fetching its own CDN over HTTP on every cold start.
"""
import os, shutil, subprocess, sys

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
PUBLIC = os.path.join(ROOT, "public", "data")
FUNC   = os.path.join(ROOT, "api", "_data")

STEPS = ["build_data.py", "build_tools.py", "export_kb.py"]


def main():
    for s in STEPS:
        print("→ %s" % s)
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], cwd=ROOT)
        if r.returncode:
            sys.exit("build step failed: %s" % s)

    shutil.copyfile(os.path.join(HERE, "kb.json"), os.path.join(PUBLIC, "kb.json"))

    if os.path.isdir(FUNC):
        shutil.rmtree(FUNC)
    shutil.copytree(PUBLIC, FUNC)
    n = sum(os.path.getsize(os.path.join(FUNC, f)) for f in os.listdir(FUNC))
    print("\nmirrored %d files (%.0f KB) to api/_data/ so the function can read them"
          % (len(os.listdir(FUNC)), n / 1024))


if __name__ == "__main__":
    main()
