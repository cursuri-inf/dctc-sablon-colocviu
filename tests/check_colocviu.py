#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificarea automată a probei practice de la colocviu, DCTC (UTCN CUNBM).

Utilizare (din rădăcina depozitului): python3 tests/check_colocviu.py all [--json FISIER]   sau   python3 tests/check_colocviu.py <test>
    ramura     ramura colocviu/<utilizator>, cel puțin un commit propriu cu mesaj clar (1 p);
               linia „Varianta X: utilizator, zz.ll.aaaa” în README, cu varianta potrivită (1 p)          2 p
    pr         pull request din colocviu/<utilizator> spre main (1 p), cu descriere (1 p)                   2 p
    document   link-ul documentului partajat în secțiunea „Linkuri” din README;
               punctele (2) le dă titularul, după ce deschide link-ul                                     0 p automat
    latex      report/colocviu.tex: secțiunea cu numele de utilizator și formula variantei (1 p);
               report/colocviu.pdf: numele de utilizator și valoarea N (1 p)                               2 p
    notebook   notebooks/colocviu.ipynb salvat cu rezultate (1 p), cu N corect (1 p)                        2 p
    all        toate, cu tabelul punctelor (Markdown) pentru rezumatul din Actions                       8 p automat

Utilizatorul: variabila COLOCVIU_USER, altfel GITHUB_REPOSITORY_OWNER (în Actions), altfel proprietarul din
`git remote get-url origin`. Ramura: COLOCVIU_RAMURA, altfel GITHUB_HEAD_REF / GITHUB_REF_NAME, altfel ramura curentă.
Pull request-ul: prin API (`gh`, cu GH_TOKEN) sau, la titular, din fișierul JSON din COLOCVIU_PR_JSON.
Sesiunea (COLOCVIU_SESIUNE): „simulare” (S), „colocviu” (A–C), „restanta” (D–F) sau „orice” (implicit: toate).
În Actions, workflow-ul o alege după numele depozitului: dctc-colocviu-proba, dctc-colocviu, dctc-restanta.
Scriptul folosește doar biblioteca standard Python și, pentru PDF, `pdftotext` (pachetul poppler-utils).
Codul de ieșire 0 înseamnă că toate punctele automate sunt obținute.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

LINIE = re.compile(r"^\s*Varianta\s+([A-FS])\s*:\s*([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)\s*,\s*(\d{2})\.(\d{2})\.(\d{4})\s*$", re.M | re.I)
K = {"S": 2, "A": 3, "B": 5, "C": 7, "D": 11, "E": 13, "F": 17}
# Elementele formulei fiecărei variante, căutate în sursa LaTeX fără spații.
FORMULE = {
    "S": [r"\pi", "r^2"],
    "A": [r"\bar{x}", r"\frac{1}{n}", r"\sum"],
    "B": [r"\sum", r"(x_i-\bar{x})^2"],
    "C": [r"\pm", r"\sqrt{b^2-4ac}"],
    "D": [r"\sum", r"\frac{n(n+1)}{2}"],
    "E": ["(a+b)^2", "2ab"],
    "F": [r"\prod", "n!"],
}
GAZDE_DOCUMENT = ("docs.google.com", "sharepoint.com", "1drv.ms", "onedrive.live.com", "office.com")


def calculeaza_n(user: str, varianta: str) -> int:
    s = sum(ord(c) for c in user.strip().lower())
    return 1000 + (K[varianta.strip().upper()] * s) % 500


def grupa(user: str) -> int:
    c = user.strip().lower()[:1]
    if "a" <= c <= "h":
        return 0
    if "i" <= c <= "q":
        return 1
    return 2


def variante_permise(user: str) -> set:
    sesiune = os.environ.get("COLOCVIU_SESIUNE", "orice").lower()
    colocviu, restanta = "ABC"[grupa(user)], "DEF"[grupa(user)]
    if sesiune == "colocviu":
        return {colocviu}
    if sesiune == "restanta":
        return {restanta}
    if sesiune == "simulare":
        return {"S"}
    return {"S", colocviu, restanta}


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], capture_output=True, check=True).stdout.decode("utf-8", "replace").strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def utilizator() -> str:
    for var in ("COLOCVIU_USER", "GITHUB_REPOSITORY_OWNER"):
        if os.environ.get(var):
            return os.environ[var].strip().lower()
    m = re.search(r"github\.com[:/]+([^/]+)/", git("remote", "get-url", "origin"))
    return m.group(1).lower() if m else ""


def depozit() -> str:
    if os.environ.get("GITHUB_REPOSITORY"):
        return os.environ["GITHUB_REPOSITORY"]
    m = re.search(r"github\.com[:/]+([^/]+/[^/.]+)", git("remote", "get-url", "origin"))
    return m.group(1) if m else ""


def ramura_curenta() -> str:
    for var in ("COLOCVIU_RAMURA", "GITHUB_HEAD_REF", "GITHUB_REF_NAME"):
        if os.environ.get(var):
            return os.environ[var].strip()
    return git("rev-parse", "--abbrev-ref", "HEAD")


def readme() -> str:
    p = Path("README.md")
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def sectiune(text: str, titlu: str) -> str:
    m = re.search(r"^## +" + re.escape(titlu) + r"\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def linia_din_readme():
    m = LINIE.search(sectiune(readme(), "Linia mea"))
    if not m:
        return None
    return m.group(1).upper(), m.group(2).lower(), f"{m.group(3)}.{m.group(4)}.{m.group(5)}"


def varianta_declarata(user: str):
    """Varianta din linia README-ului, dacă este a utilizatorului; altfel, când sesiunea permite o singură variantă
    (la notarea titularului), aceea: o greșeală în linie se punctează doar la sarcina 1."""
    linie = linia_din_readme()
    permise = variante_permise(user)
    if linie and linie[1] == user and linie[0] in permise:
        return linie[0]
    return next(iter(permise)) if len(permise) == 1 else None


def commituri_proprii() -> list:
    """Commit-urile studentului: toate, în afara commit-ului inițial creat din șablon (și a celor automate).
    Se numără de la rădăcină, nu de la origin/main, ca un commit pus din greșeală pe main să nu dispară."""
    radacini = git("rev-list", "--max-parents=0", "HEAD").split()
    interval = ["HEAD"] + [f"^{r}" for r in radacini]
    linii = git("log", "--no-merges", "--format=%an%x09%ae%x09%s", *interval).splitlines()
    rezultat = []
    for linie in linii:
        nume, email, subiect = (linie.split("\t") + ["", ""])[:3]
        if "[bot]" in (nume + email).lower() or "noreply@github.com" == email.lower():
            continue
        rezultat.append(subiect)
    return rezultat


class Rezultat:
    def __init__(self, cheie, titlu, maxim):
        self.cheie, self.titlu, self.maxim, self.puncte, self.mesaje = cheie, titlu, maxim, 0, []

    def da(self, puncte, mesaj):
        self.puncte += puncte
        self.mesaje.append(("TRECUT: " if puncte else "INFO: ") + mesaj)

    def lipsa(self, mesaj):
        self.mesaje.append("LIPSEȘTE: " + mesaj)


def test_ramura() -> Rezultat:
    r = Rezultat("ramura", "Sarcina 1a: ramura, commit-ul, linia din README", 2)
    user, ramura = utilizator(), ramura_curenta()
    if not user:
        r.lipsa("nu pot afla numele de utilizator (rulați din depozitul clonat de pe GitHub).")
        return r
    commituri = commituri_proprii()
    clare = [s for s in commituri if len(s.strip()) >= 10 and len(s.split()) >= 2]
    if ramura.lower() != f"colocviu/{user}":
        r.lipsa(f"ramura este „{ramura}”; se așteaptă `colocviu/{user}`.")
    elif not commituri:
        r.lipsa("pe această ramură nu există niciun commit propriu (verificați `git config user.name` și `user.email`, apoi push).")
    elif not clare:
        r.lipsa("niciun commit cu mesaj clar (cel puțin două cuvinte și 10 caractere): " + "; ".join(f"„{s}”" for s in commituri[:3]))
    else:
        r.da(1, f"ramura `colocviu/{user}`; commit-uri proprii: {len(commituri)}, cu mesaj clar: {len(clare)}.")
    linie = linia_din_readme()
    permise = ", ".join(sorted(variante_permise(user)))
    if not linie:
        r.lipsa("în secțiunea „Linia mea” din README lipsește rândul `Varianta X: utilizator, zz.ll.aaaa`.")
    elif linie[1] != user:
        r.lipsa(f"în linia din README, numele de utilizator este „{linie[1]}”; contul dumneavoastră este „{user}”.")
    elif linie[0] not in variante_permise(user):
        r.lipsa(f"varianta {linie[0]} nu este a dumneavoastră; pentru {user}: {permise} (tabelul din README).")
    else:
        r.da(1, f"linia din README: varianta {linie[0]}, data {linie[2]}.")
    return r


def pull_requesturi(user: str) -> list:
    if os.environ.get("COLOCVIU_PR_JSON"):
        try:
            return json.loads(Path(os.environ["COLOCVIU_PR_JSON"]).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
    if not shutil.which("gh") or not (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")):
        return None
    env = dict(os.environ)
    env.setdefault("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    proc = subprocess.run(["gh", "api", f"repos/{depozit()}/pulls?state=all&base=main&per_page=100"], capture_output=True, env=env)
    if proc.returncode != 0:
        return None
    try:
        toate = json.loads(proc.stdout.decode("utf-8", "replace") or "[]")
    except json.JSONDecodeError:
        return None
    return [p for p in toate if ((p.get("head") or {}).get("ref") or "").lower() == f"colocviu/{user}"]


def test_pr() -> Rezultat:
    r = Rezultat("pr", "Sarcina 1b: pull request-ul spre main", 2)
    user = utilizator()
    pruri = pull_requesturi(user)
    if pruri is None:
        r.lipsa("nu pot interoga pull request-urile aici (verificarea rulează în Actions, cu GH_TOKEN).")
        return r
    if not pruri:
        r.lipsa(f"nu există un pull request din `colocviu/{user}` spre `main`; deschideți-l, apoi verificarea rulează din nou.")
        return r
    pr = pruri[0]
    r.da(1, f"pull request #{pr.get('number')} („{pr.get('title', '')}”).")
    if len((pr.get("body") or "").split()) >= 3:
        r.da(1, "pull request-ul are descriere.")
    else:
        r.lipsa("pull request-ul nu are descriere (cel puțin o propoziție); o adăugați cu *Edit*, pe pagina lui.")
    return r


def test_document() -> Rezultat:
    r = Rezultat("document", "Sarcina 2: documentul partajat (de verificat de titular)", 0)
    linkuri = re.findall(r"https?://[^\s)>\]]+", sectiune(readme(), "Linkuri"))
    bune = [l for l in linkuri if any(g in l.lower() for g in GAZDE_DOCUMENT)]
    if bune:
        r.da(0, f"link de document găsit; titularul îl deschide la notare: {bune[0]}")
    else:
        r.lipsa("în secțiunea „Linkuri” din README lipsește link-ul documentului (Word online sau Google Docs).")
    return r


def text_pdf(cale: Path) -> str:
    if not shutil.which("pdftotext"):
        return ""
    try:
        text = subprocess.run(["pdftotext", "-layout", str(cale), "-"], capture_output=True, check=True,
                              timeout=60).stdout.decode("utf-8", "replace")
        return "".join(c for c in unicodedata.normalize("NFKC", text) if c in "\n\t" or unicodedata.category(c)[0] != "C")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ""


def normalizeaza_latex(text: str) -> str:
    """Sursa fără spații și cu scrierile echivalente aduse la aceeași formă: r^{2} = r^2, \\overline{x} = \\bar{x}, fără \\left și \\right."""
    t = re.sub(r"\s+", "", text)
    t = re.sub(r"\\(left|right)(?=[()\[\]|.])", "", t)
    t = t.replace(r"\overline{", r"\bar{")
    t = re.sub(r"\^\{(\w)\}", r"^\1", t)
    t = re.sub(r"_\{(\w)\}", r"_\1", t)
    return t


def sectiunea_latex(sursa: str, user: str) -> str:
    m = re.search(r"^[ \t]*\\section\*?\{\s*" + re.escape(user) + r"\s*\}(.*?)(?=^[ \t]*\\section|\\end\{document\})", sursa, re.S | re.I | re.M)
    return m.group(1) if m else ""


def test_latex() -> Rezultat:
    r = Rezultat("latex", "Sarcina 3: LaTeX", 2)
    user = utilizator()
    varianta = varianta_declarata(user)
    if not varianta:
        r.lipsa("completați întâi linia din README (sarcina 1): de acolo se citește varianta.")
        return r
    tex, pdf = Path("report/colocviu.tex"), Path("report/colocviu.pdf")
    sursa = tex.read_text(encoding="utf-8", errors="replace") if tex.is_file() else ""
    sect = sectiunea_latex(sursa, user)
    compact = normalizeaza_latex(sect)
    if not sect:
        r.lipsa(f"în `report/colocviu.tex` lipsește `\\section{{{user}}}`.")
    elif "\\begin{equation" not in sect:
        r.lipsa("secțiunea dumneavoastră nu are formula într-un mediu `equation`.")
    elif not all(normalizeaza_latex(e) in compact for e in FORMULE[varianta]):
        r.lipsa(f"formula din secțiunea dumneavoastră nu este cea a variantei {varianta} (tabelul din README).")
    else:
        r.da(1, f"sursa: secțiunea `{user}`, cu formula variantei {varianta}.")
    if not pdf.is_file() or pdf.stat().st_size < 5 * 1024:
        r.lipsa("`report/colocviu.pdf` lipsește sau e gol; descărcați PDF-ul din Overleaf și adăugați-l pe ramura dumneavoastră.")
        return r
    text = text_pdf(pdf)
    n = calculeaza_n(user, varianta)
    if not text:
        r.lipsa("nu pot citi textul PDF-ului (pdftotext lipsește sau PDF-ul nu este valid).")
    elif text.lower().count(user) < 2:
        r.lipsa(f"în PDF, numele de utilizator „{user}” apare de mai puțin de două ori (titlul secțiunii și rândul din tabel); recompilați și descărcați PDF-ul nou.")
    elif str(n) not in text:
        r.lipsa(f"în PDF nu apare valoarea N corectă pentru {user}, varianta {varianta} (rândul din tabel).")
    else:
        r.da(1, f"PDF-ul: secțiunea și rândul din tabel, cu N={n}.")
    return r


def test_notebook() -> Rezultat:
    r = Rezultat("notebook", "Sarcina 4: notebook-ul", 2)
    user = utilizator()
    varianta = varianta_declarata(user)
    nb = Path("notebooks/colocviu.ipynb")
    try:
        date = json.loads(nb.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        r.lipsa("`notebooks/colocviu.ipynb` lipsește sau nu este un notebook valid.")
        return r
    iesiri = []
    for c in date.get("cells", []):
        for o in c.get("outputs", []) if c.get("cell_type") == "code" else []:
            iesiri.append("".join(o.get("text", "")))
            iesiri.append("".join(o.get("data", {}).get("text/plain", "")))
    m = re.search(r"REZULTAT:\s*N=(\d+)", "\n".join(iesiri))
    if not m:
        r.lipsa("notebook-ul nu are rezultatele salvate (`REZULTAT: N=...`); *Run all*, apoi *Save a copy in GitHub* pe ramura dumneavoastră.")
        return r
    r.da(1, "notebook-ul este salvat cu rezultate.")
    if not varianta:
        r.lipsa("completați linia din README (sarcina 1): de acolo se citește varianta.")
    elif int(m.group(1)) != calculeaza_n(user, varianta):
        r.lipsa(f"N={m.group(1)} nu corespunde utilizatorului {user} și variantei {varianta}; verificați `USER` și `VARIANTA` din prima celulă.")
    else:
        r.da(1, f"N={m.group(1)}, corect pentru {user}, varianta {varianta}.")
    return r


TESTE = {"ramura": test_ramura, "pr": test_pr, "document": test_document, "latex": test_latex, "notebook": test_notebook}


def toate(fisier_json=None) -> int:
    rez = [f() for f in TESTE.values()]
    total, maxim = sum(r.puncte for r in rez), sum(r.maxim for r in rez)
    print(f"## Verificarea colocviului: {total} din {maxim} puncte automate\n")
    print(f"Utilizatorul: `{utilizator()}` · ramura: `{ramura_curenta()}`\n")
    print("| Sarcina | Puncte | Ce s-a găsit |\n| --- | --- | --- |")
    for r in rez:
        puncte = "2 (titular)" if r.cheie == "document" else f"{r.puncte} / {r.maxim}"
        print(f"| {r.titlu} | {puncte} | " + "<br>".join(m.replace("|", "\\|") for m in r.mesaje) + " |")
    print("\nSarcina 2 o notează titularul, după ce deschide link-ul. Nota se stabilește pe starea ramurii la închiderea probei.")
    if fisier_json:
        Path(fisier_json).write_text(json.dumps({r.cheie: {"puncte": r.puncte, "maxim": r.maxim, "mesaje": r.mesaje}
                                                 for r in rez}, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if total == maxim else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "all":
        sys.exit(toate(args[2] if len(args) > 2 and args[1] == "--json" else None))
    if len(args) == 1 and args[0] in TESTE:
        r = TESTE[args[0]]()
        print("\n".join(r.mesaje))
        sys.exit(0 if r.puncte == r.maxim else 1)
    print(__doc__)
    sys.exit(2)
