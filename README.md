# Colocviu DCTC: proba practică individuală

Disciplina *Dezvoltare colaborativă și tehnologii cloud* (DCTC), UTCN, Centrul Universitar Nord din Baia Mare.

Lucrezi singur, 50 de minute. Documentația, materialele disciplinei și notițele tale sunt permise; asistenții AI sunt permiși pentru explicații, nu pentru a face sarcinile în locul tău; ajutorul de la colegi nu este permis. După fiecare `push`, fila *Actions* > „Verificarea colocviului” > *Summary* îți arată punctele; poți corecta până la închiderea probei. Nota se stabilește pe starea ramurii tale la închidere.

## Înainte de sarcini

1. Acest depozit l-ai creat din `cursuri-inf/dctc-sablon-colocviu`, în contul tău, privat, cu numele exact: `dctc-colocviu-proba` la simulare, `dctc-colocviu` la colocviu, `dctc-restanta` la restanță. După nume, verificarea știe ce variante îți sunt permise.
2. La colocviu și la restanță: *Settings > Collaborators* > `cosminsabo`, iar link-ul depozitului este predat în activitatea probei de pe Campus Virtual. La simulare, nu.
3. Clonează depozitul: *Code* > *HTTPS* > adresa; în terminal, `git clone <adresa>`, apoi `cd` în folderul lui.

## Varianta ta

| Prima literă a numelui tău de utilizator GitHub | Colocviul | Restanța |
| --- | --- | --- |
| a–h | A | D |
| i–q | B | E |
| r–z sau o cifră | C | F |

La simulare, varianta este **S**, pentru toți.

| Varianta | Formula pentru sarcina 3 |
| --- | --- |
| S | $A = \pi r^2$ |
| A | $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$ |
| B | $S = \sum_{i=1}^{n} (x_i - \bar{x})^2$ |
| C | $x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ |
| D | $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$ |
| E | $(a+b)^2 = a^2 + 2ab + b^2$ |
| F | $n! = \prod_{k=1}^{n} k$ |

Ordinea recomandată: sarcina 1, apoi 4 (dă valoarea `N`), 3 și 2. Deschide pull request-ul imediat după primul `push`.

## Sarcina 1 (4 puncte): Git și GitHub

1. Creează ramura `colocviu/<utilizator>`, cu numele tău de utilizator GitHub (de exemplu `git switch -c colocviu/ana-pop`).
2. În secțiunea „Linia mea” de mai jos, adaugă un rând nou de forma `Varianta X: utilizator, zz.ll.aaaa`: varianta ta, numele tău de utilizator, data de azi.
3. Commit cu un mesaj clar (cel puțin două cuvinte și 10 caractere, de exemplu `Add my colocviu line`), apoi `git push -u origin colocviu/<utilizator>`.
4. Pe GitHub, *Compare & pull request*: din ramura ta spre `main`, cu o descriere de cel puțin o propoziție. *Create pull request*. Nu îl îmbina.

## Sarcina 2 (2 puncte): document partajat

1. Creează un document nou, cu titlul `Colocviu <utilizator>`, în Word online (OneDrive-ul tău UTCN) sau în Google Docs, cu o propoziție: varianta ta și data.
2. Creează un **link de vizualizare**: în Word online, *Share > Copy link*, apoi setările link-ului (rotița): *People in* organizația UTCN și rolul *Can view*; *Apply*, apoi *Copy*. În Google Docs, *Share* > *General access* > *Anyone with the link*, rolul *Viewer*, apoi *Copy link*.
3. Pune link-ul în secțiunea „Linkuri” de mai jos, pe ramura ta, cu un commit și un `push`: ajunge în același pull request.

Titularul deschide link-ul: se deschide fără cerere de acces (1 punct) și doar pentru citire, cu titlul cerut (1 punct).

## Sarcina 3 (2 puncte): LaTeX

1. În Overleaf, *New Project* > *Blank Project*; înlocuiește tot textul din `main.tex` cu cel din `report/colocviu.tex`.
2. Adaugă secțiunea cu titlul exact numele tău de utilizator, cu formula variantei tale într-un mediu `equation` (copiată din tabelul de mai sus), și rândul tău în tabel: numele de utilizator și valoarea `N` din sarcina 4.
3. *Recompile*, fără erori. Descarcă PDF-ul (butonul de descărcare de lângă *Recompile*) și salvează-l ca `report/colocviu.pdf`.
4. Copiază textul modificat înapoi în `report/colocviu.tex`. Commit cu ambele fișiere, apoi `push`.

## Sarcina 4 (2 puncte): notebook

1. În Colab, *File > Open notebook* > *GitHub*: bifează *Include private repos* (și autorizează accesul, dacă ți se cere), alege depozitul tău și ramura `colocviu/<utilizator>`, apoi `notebooks/colocviu.ipynb`.
2. În prima celulă de cod: `USER` = numele tău de utilizator, `VARIANTA` = varianta ta. *Runtime > Run all*.
3. *File > Save a copy in GitHub*: depozitul tău, ramura `colocviu/<utilizator>`, calea `notebooks/colocviu.ipynb`, un mesaj de commit clar. *OK*.
4. Pe calculatorul tău, `git pull`, ca să ai și commit-ul din Colab înainte de următorul `push`.

## Linia mea

<!-- Adaugă aici, pe un rând nou: Varianta X: utilizator, zz.ll.aaaa -->

## Linkuri

- Documentul partajat:
