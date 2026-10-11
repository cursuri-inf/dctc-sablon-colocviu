# Colocviu DCTC: proba practică individuală

Disciplina *Dezvoltare colaborativă și tehnologii cloud* (DCTC), UTCN, Centrul Universitar Nord din Baia Mare.

Lucrați individual, 50 de minute. Documentația, materialele disciplinei și notițele proprii sunt permise; asistenții AI sunt permiși pentru explicații, nu pentru a face sarcinile în locul dumneavoastră; ajutorul de la colegi nu este permis. După fiecare `push`, fila *Actions* > „Verificarea colocviului” > *Summary* vă arată punctele; puteți corecta până la închiderea probei. Nota se stabilește pe starea ramurii dumneavoastră la închidere.

## Înainte de sarcini

1. Acest depozit l-ați creat din `cursuri-inf/dctc-sablon-colocviu`, în contul dumneavoastră, privat, cu numele exact: `dctc-colocviu-proba` la simulare, `dctc-colocviu` la colocviu, `dctc-restanta` la restanță. După nume, verificarea știe ce variante vă sunt permise.
2. La colocviu și la restanță: *Settings > Collaborators* > `cosminsabo`, iar link-ul depozitului este predat în activitatea probei de pe Campus Virtual. La simulare, nu.
3. Clonați depozitul: *Code* > *HTTPS* > adresa; în terminal, `git clone <adresa>`, apoi `cd` în folderul lui.

## Varianta dumneavoastră

| Prima literă a numelui dumneavoastră de utilizator GitHub | Colocviul | Restanța |
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

Ordinea recomandată: sarcina 1, apoi 4 (dă valoarea `N`), 3 și 2. Deschideți pull request-ul imediat după primul `push`.

## Sarcina 1 (4 puncte): Git și GitHub

1. Creați ramura `colocviu/<utilizator>`, cu numele dumneavoastră de utilizator GitHub (de exemplu `git switch -c colocviu/ana-pop`).
2. În secțiunea „Linia mea” de mai jos, adăugați un rând nou de forma `Varianta X: utilizator, zz.ll.aaaa`: varianta dumneavoastră, numele dumneavoastră de utilizator, data de azi.
3. Commit cu un mesaj clar (cel puțin două cuvinte și 10 caractere, de exemplu `Add my colocviu line`), apoi `git push -u origin colocviu/<utilizator>`.
4. Pe GitHub, *Compare & pull request*: din ramura dumneavoastră spre `main`, cu o descriere de cel puțin o propoziție. *Create pull request*. Nu îl îmbinați.

## Sarcina 2 (2 puncte): document partajat

1. Creați un document nou, cu titlul `Colocviu <utilizator>`, în Word online (OneDrive-ul dumneavoastră UTCN) sau în Google Docs, cu o propoziție: varianta dumneavoastră și data.
2. Creați un **link de vizualizare**: în Word online, *Share > Copy link*, apoi setările link-ului (rotița): *People in* organizația UTCN și rolul *Can view*; *Apply*, apoi *Copy*. În Google Docs, *Share* > *General access* > *Anyone with the link*, rolul *Viewer*, apoi *Copy link*.
3. Adăugați link-ul în secțiunea „Linkuri” de mai jos, pe ramura dumneavoastră, cu un commit și un `push`: ajunge în același pull request.

Titularul deschide link-ul: se deschide fără cerere de acces (1 punct) și doar pentru citire, cu titlul cerut (1 punct).

## Sarcina 3 (2 puncte): LaTeX

1. În Overleaf, *New Project* > *Blank Project*; înlocuiți tot textul din `main.tex` cu cel din `report/colocviu.tex`.
2. Adăugați secțiunea cu titlul exact numele dumneavoastră de utilizator, cu formula variantei dumneavoastră într-un mediu `equation` (copiată din tabelul de mai sus), și rândul dumneavoastră în tabel: numele de utilizator și valoarea `N` din sarcina 4.
3. *Recompile*, fără erori. Descărcați PDF-ul (butonul de descărcare de lângă *Recompile*) și salvați-l ca `report/colocviu.pdf`.
4. Copiați textul modificat înapoi în `report/colocviu.tex`. Commit cu ambele fișiere, apoi `push`.

## Sarcina 4 (2 puncte): notebook

1. În Colab, *File > Open notebook* > *GitHub*: bifați *Include private repos* (și autorizați accesul, dacă vi se cere), alegeți depozitul dumneavoastră și ramura `colocviu/<utilizator>`, apoi `notebooks/colocviu.ipynb`.
2. În prima celulă de cod: `USER` = numele dumneavoastră de utilizator, `VARIANTA` = varianta dumneavoastră. *Runtime > Run all*.
3. *File > Save a copy in GitHub*: depozitul dumneavoastră, ramura `colocviu/<utilizator>`, calea `notebooks/colocviu.ipynb`, un mesaj de commit clar. *OK*.
4. Pe calculatorul dumneavoastră, `git pull`, ca să aveți și commit-ul din Colab înainte de următorul `push`.

## Linia mea

<!-- Adăugați aici, pe un rând nou: Varianta X: utilizator, zz.ll.aaaa -->

## Linkuri

- Documentul partajat:
