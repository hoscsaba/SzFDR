SzFDR – aktuális oktatási jegyzet

Főforrás: SzFDR_jegyzet_v3.tex
Kész dokumentum: SzFDR_jegyzet_v3.pdf
Fejezetek: chapters_v3/
MATLAB-példák és ábragenerátorok: codes/ (lásd README.txt és Contents.m)
Aktuális vektoros ábrák és ábraforrások: graphics_v3/
SVG-változatok: graphics_svg/ (manifest.json)
A jegyzetben még használt hat raszteres ábra: graphics/
Matematikai és forrásellenőrzések: checks/

Fordítás a projekt gyökeréből, külön kimeneti könyvtárba:
  mkdir -p build
  latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build SzFDR_jegyzet_v3.tex
  cp build/SzFDR_jegyzet_v3.pdf SzFDR_jegyzet_v3.pdf

Ellenőrzések (Python 3 és NumPy szükséges):
  python3 checks/verify_p1.py
  python3 checks/verify_p23.py
  python3 checks/verify_equilibria.py
  python3 checks/verify_practical_examples.py

A régi jegyzetverziók és a már nem használt ábrák a Git előzményeiből
visszakereshetők. Az aktuális gyökérkönyvtár csak a v3 változatot tartalmazza.
A graphics_v3 könyvtár .tex és .dat fájljai az ábrák reprodukálható
forrásai, nem törlendő fordítási segédfájlok.
