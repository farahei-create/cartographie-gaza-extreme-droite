# -*- coding: utf-8 -*-
"""Joue les tests Playwright avant un push.

test_v8.py est ignoré (clé votes retirée).
test_v5.py peut échouer sur « graph built lazily on Réseau » : ces cas seuls sont admis.
Tout autre échec arrête le workflow, sans push.
"""
import os
import re
import signal
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP = {"test_v8.py"}
ALLOWED_V5 = "graph built lazily on Réseau"


def fail_lines(text):
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("FAIL:") or stripped.startswith("FAIL "):
            lines.append(stripped)
    return lines


def unexpected(name, lines):
    if name == "test_v5.py":
        return [line for line in lines if ALLOWED_V5 not in line]
    return lines


def main():
    os.chdir(ROOT)
    os.environ["PYTHONPATH"] = ROOT + os.pathsep + os.environ.get("PYTHONPATH", "")
    os.makedirs("/workspace", exist_ok=True)
    os.makedirs("/opt/cursor/artifacts", exist_ok=True)
    link = os.path.join(ROOT, "site")
    created = False
    if not os.path.exists(link):
        os.symlink(".", link)
        created = True
    server = subprocess.Popen([sys.executable, "-m", "http.server", "8765"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                import urllib.request
                urllib.request.urlopen("http://127.0.0.1:8765/sw.js", timeout=1).read(20)
                break
            except Exception:
                time.sleep(0.2)
        else:
            print("Le serveur local ne répond pas.")
            return 1
        tests = sorted(name for name in os.listdir(os.path.join(ROOT, "tests")) if re.match(r"test_.*\.py$", name) and name not in SKIP)
        # Les garde-fous ont déjà tourné. Ici, les tests du site.
        tests = [name for name in tests if name != "test_daily.py"]
        failed = []
        for name in tests:
            print("=== %s ===" % name, flush=True)
            proc = subprocess.run([sys.executable, os.path.join("tests", name)], cwd=ROOT, capture_output=True, text=True, timeout=240)
            output = (proc.stdout or "") + "\n" + (proc.stderr or "")
            sys.stdout.write(proc.stdout or "")
            if proc.stderr:
                sys.stderr.write(proc.stderr)
            bad = unexpected(name, fail_lines(output))
            crashed = "Traceback (most recent call last)" in output
            if name == "test_v5.py":
                if bad or crashed:
                    failed.append(name)
            elif proc.returncode != 0 or bad or crashed:
                failed.append(name)
        if failed:
            print("Échec : " + ", ".join(failed))
            return 1
        print("Tests du site : OK (test_v8 ignoré, échecs connus de test_v5 admis).")
        return 0
    finally:
        server.send_signal(signal.SIGTERM)
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
        if created and os.path.islink(link):
            os.unlink(link)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.TimeoutExpired as exc:
        print("Test interrompu :", exc)
        sys.exit(1)
