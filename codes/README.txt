SzFDR – MATLAB példaprogramok

A jegyzet összes MATLAB-példája ebben a könyvtárban érhető el.
A helyi és beágyazott segédfüggvények a hozzájuk tartozó főfüggvény
.m fájljában vannak; nem kell külön másolni vagy keresni őket.
A Contents.m a programok MATLAB-ból is olvasható tartalomjegyzéke.

INDÍTÁS
Nyisd meg ezt a könyvtárat a MATLAB Current Folder ablakában.
Alternatív megoldásként a projekt gyökérkönyvtárából:

    addpath(fullfile(pwd, 'codes'))

AZ EGYSZERŰ TANPÉLDÁK INDÍTÁSA
    apex_bvp_v3       – feldobás: ismeretlen kezdeti sebesség és idő;
    apex_shooting_v3  – ugyanaz a feladat eseményvezérelt belövéssel;
    fold_pal_v3       – mu=x^2 egyensúlyi ág követése a fordulóponton át;
    bilinear_bvp_v3   – kétmerevségű rugó két félperiódusának illesztése.
Az 5.1. kódlista most az apex_bvp_v3 teljes programja.
A fold_pal_v3 a pal_corrector_v3 függvényt hívja ugyanebből a könyvtárból.
A többi új példa minden szükséges függvényt a saját fájljában tartalmaz.
A mass_spring_bvp_v3 csak a kiszámított negyed periódust ábrázolja.
A bilinear_bvp_v3 dimenziótlan, egységnyi tömegű modell.

A V3 JEGYZET TOVÁBBI PÉLDÁI
    M = Monodromia_mx_pelda_v3
    [T, sol] = mass_spring_bvp_v3
    [yT, M, t, y, nImpact] = ...
        impact_monodromy_v3([1;0], 0, 2*pi/3, 0.05, 3, 0.8, 0)

A paraméterezett eszközök bemenetét a fájlok elején dokumentáljuk:
    [yn, info] = pal_corrector_v3(G, yi, yold, ds, scale)
    sol = slip_bvp_v3(mesh, guess, Tguess, p)

A pal_corrector_v3 egy összeállított reziduumot és két korábbi megoldást
vár. A slip_bvp_v3 kezdeti pályabecslést és fizikai paramétereket igényel;
ezek nem bemenet nélküli demóprogramok.

FELTÉTELEK
MATLAB szükséges. A peremérték-megoldókhoz bvp5c/bvpinit/deval kell;
a pal_corrector_v3 fsolve hívása Optimization
Toolboxot igényel. Az ode45, odeset és fzero a MATLAB alapfüggvényei.
A programok tényleges MATLAB-futtatását a célkörnyezetben külön is
ellenőrizni kell.

A square_root_figures_v3.py Python-program a négyzetgyökös modell
vektoros ábráit állítja elő, nem MATLAB-fájl.

KÓDSTÍLUS
A példák rövidek, a dokumentált bemeneteket adottnak tekintik.
Csak az algoritmus szempontjából szükséges konvergencia-, megoldáság-
és szingularitási ellenőrzések maradtak meg; általános bemenetvalidálás nincs.

6. FEJEZET – ESEMÉNYKEZELÉS ÉS MODELLVÁLASZTÁS
    bouncing_ball_v3           – nyolc ütközés; a Zeno-időn túl nem folytat;
    stick_slip_v3              – dimenziótlan, egzakt tapadási/csúszási ciklus;
    border_collision_v3        – kétszakaszos leképezés border-collision bifurcatione;
    friction_regularization_v3 – simított súrlódás, ode15s megoldóval.
Mind a négy program bemenet nélkül indítható, külön toolboxot nem igényel.
A practical_figures_v3.py NumPy és Matplotlib segítségével öt ábrát készít
PDF és valódi vektoros SVG formátumban. A referenciaábrák egzakt képletekből
készülnek; nem tekintendők a MATLAB-kódok futtatási eredményeinek.

1.1. SZAKASZ – FÁZISPORTRÉK
    phase_portraits_v3 – öt lineáris rendszer (nyereg, két csomó, két fókusz).
Az equilibrium_figures_v3.py NumPy és Matplotlib segítségével a jegyzet
három PDF/SVG ábráját rajzolja meg. Saját generált ábrák, nem könyvillusztrációk
másolatai. A MATLAB-változat ugyanazon mátrixokat használja.

2.1. ÁBRA – KONKRÉT KAPCSOLÓFELÜLET ÉS VEKTORMEZŐK
    circle_switch_fields_v3 – az egységkör két oldalán megadott mezők.
A nyilak csak az irányt jelzik, nem a sebesség nagyságát.
A jegyzet PDF/SVG ábrája: python3 codes/circle_switch_figure_v3.py

2.2. ábra: circle_sliding_fields_v3.m; azonos mezők a 2.1. ábrával, zöld vonzó csúszási körív és Filippov-mező. PDF/SVG: python3 codes/circle_sliding_figure_v3.py

4.1-4.2. ábra: impact_portraits_v3.m (impact_monodromy_v3.m szükséges). A nyomdai PDF/SVG-ábrák: python3 codes/impact_figures_v3.py; pontos szabad mozgás és eseménykeresés, NumPy és Matplotlib.

5.4. ábra: mass_spring_bvp_v3, MATLAB bvp5c; teljes periódus szimmetriával. 16 x 12 cm, 11 pt; vektoros PDF és SVG automatikus mentése.

5.5.1: spring_continuation_v3; 5.5.2: bilinear_bvp_v3. Önálló MATLAB-függvények minden segédfüggvénnyel, automatikus PDF/SVG-exporttal, 11 pontos feliratokkal.

Regularizációs összehasonlítások: friction_regularization_v3; ideális és simított sebesség, illetve helyzet, analitikus ellenőrzéssel. Két vektoros PDF/SVG, 11 pontos feliratok.

6.6–6.8. szakasz: boundary_equilibria_v3, sliding_geometries_v3,
continuous_grazing_v3. Önálló MATLAB-szkriptek egzakt helyi példákkal;
PDF/SVG-export 11 pontos feliratokkal. Futtatás: addpath('codes');
majd a kívánt program neve. Teljes kódjuk az A függelékben szerepel.

1.4.1–1.4.2: python3 codes/bifurcation_types_v3.py; normálalakok helyi ágdiagramjai, PDF és SVG, 11 pontos feliratok.
