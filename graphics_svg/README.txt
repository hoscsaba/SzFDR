A v3 jegyzet használt ábráinak SVG-változatai

34 valódi vektoros SVG; 6 beágyazott PNG-t tartalmazó SVG.
A szövegek a vektoros ábrák többségén körvonalakká alakítva szerepelnek; a MATLAB-ból exportált mass_spring_bvp.svg, spring_k.svg, spring_m.svg és bilinear_bvp.svg szerkeszthető szöveget és Times New Roman betűtípust használ.
A raszteres eredetik beágyazása nem jelent vektorizálást.
Újragenerálás: python3 codes/export_figures_svg.py
Szükséges: latex, dvisvgm, NumPy, Matplotlib.
Az új 6. fejezet ábrái külön: python3 codes/practical_figures_v3.py
Az 1.1. szakasz ábrái külön: python3 codes/equilibrium_figures_v3.py
A manifest.json a használt forrásokat és SVG-ellenőrzőösszegeket sorolja fel.
Korábbi, már nem hivatkozott ábrák is maradhatnak ebben a könyvtárban.

A 2.1. ábra külön: python3 codes/circle_switch_figure_v3.py

A 2.2. ábra külön: python3 codes/circle_sliding_figure_v3.py

A 4.1-4.2. ábrák: python3 codes/impact_figures_v3.py

Az 5.4. ábra újragenerálása MATLAB-ban: addpath('codes'); mass_spring_bvp_v3;

5.5.1-5.5.2: MATLAB-ban spring_continuation_v3; bilinear_bvp_v3;

A regularization_braking.svg és regularization_creep.svg MATLAB-export, szerkeszthető Times New Roman szöveggel. Újragenerálás: friction_regularization_v3.

6.6–6.8: boundary_equilibria_v3; sliding_geometries_v3; continuous_grazing_v3. MATLAB-exportok, szerkeszthető Times New Roman szöveggel.

1.4.1–1.4.2: equilibrium_bifurcations.svg, cycle_bifurcations.svg; újragenerálás: python3 codes/bifurcation_types_v3.py.
