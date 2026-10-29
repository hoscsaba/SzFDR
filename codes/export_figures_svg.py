#!/usr/bin/env python3
"""Export all figures used by the v3 textbook. Requires latex, dvisvgm, NumPy and Matplotlib."""
import argparse, base64, hashlib, json, re, shutil, struct, subprocess, tempfile, sys
from pathlib import Path
from xml.sax.saxutils import escape

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode:
        raise RuntimeError(' '.join(map(str, cmd)) + '\n' + p.stdout[-6000:])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output or root / 'graphics_svg'
    out.mkdir(parents=True, exist_ok=True)
    chapters = '\n'.join(p.read_text() for p in sorted((root/'chapters_v3').glob('*.tex')))
    refs = set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', chapters))
    refs.update(re.findall(r'\\input\{(graphics_v3/[^}]+\.tikz\.tex)\}', chapters))
    generated = {'stick_slip_cycle', 'zeno_ball', 'border_collision',
                 'friction_regularization', 'sliding_birth'}
    if any(Path(ref).stem in generated for ref in refs):
        run([sys.executable, str(root/'codes/practical_figures_v3.py')], root)
    equilibrium = {'phase_saddle', 'phase_nodes', 'phase_foci'}
    if any(Path(ref).stem in equilibrium for ref in refs):
        run([sys.executable, str(root/'codes/equilibrium_figures_v3.py')], root)
    generated |= equilibrium
    biftypes = {'equilibrium_bifurcations', 'cycle_bifurcations'}
    if any(Path(ref).stem in biftypes for ref in refs):
        run([sys.executable, str(root/'codes/bifurcation_types_v3.py')], root)
    generated |= biftypes
    if any(Path(ref).stem == 'circle_switch_fields' for ref in refs):
        run([sys.executable, str(root/'codes/circle_switch_figure_v3.py')], root)
    generated.add('circle_switch_fields')
    if any(Path(ref).stem == 'circle_sliding_fields' for ref in refs):
        run([sys.executable, str(root/'codes/circle_sliding_figure_v3.py')], root)
    generated.add('circle_sliding_fields')
    impact = {'impact_phase', 'impact_time'}
    if any(Path(ref).stem in impact for ref in refs):
        run([sys.executable, str(root/'codes/impact_figures_v3.py')], root)
    generated |= impact
    if any(Path(ref).stem == 'mass_spring_bvp' for ref in refs):
        matlab = shutil.which('matlab') or '/Applications/MATLAB_R2026a.app/bin/matlab'
        run([matlab, '-batch', "addpath('codes'); mass_spring_bvp_v3;"], root)
    generated.add('mass_spring_bvp')
    examples = {'spring_k', 'spring_m', 'bilinear_bvp'}
    if any(Path(ref).stem in examples for ref in refs):
        matlab = shutil.which('matlab') or '/Applications/MATLAB_R2026a.app/bin/matlab'
        run([matlab, '-batch', "addpath('codes'); spring_continuation_v3; bilinear_bvp_v3;"], root)
    generated |= examples
    regularization = {'regularization_braking', 'regularization_creep'}
    if any(Path(ref).stem in regularization for ref in refs):
        matlab = shutil.which('matlab') or '/Applications/MATLAB_R2026a.app/bin/matlab'
        run([matlab, '-batch', "addpath('codes'); friction_regularization_v3;"], root)
    generated |= regularization
    extensions = {'boundary_equilibria', 'sliding_geometries', 'continuous_grazing'}
    if any(Path(ref).stem in extensions for ref in refs):
        matlab = shutil.which('matlab') or '/Applications/MATLAB_R2026a.app/bin/matlab'
        run([matlab, '-batch', "addpath('codes'); boundary_equilibria_v3; sliding_geometries_v3; continuous_grazing_v3;"], root)
    generated |= extensions
    manifest = []
    for ref in sorted(refs):
        src = root/ref
        if not src.exists():
            src = next(p for p in src.parent.iterdir() if p.name.lower() == src.name.lower())
        name = src.name.removesuffix('.tikz.tex') if ref.endswith('.tikz.tex') else src.stem
        target = out/(name+'.svg')
        if name in generated:
            native = root/'graphics_svg'/(name+'.svg')
            if native.resolve() != target.resolve():
                shutil.copy2(native, target)
            kind = 'vector'
        elif src.suffix.lower() == '.png':
            data = src.read_bytes()
            width, height = struct.unpack('>II', data[16:24])
            uri = base64.b64encode(data).decode('ascii')
            target.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><title>{escape(name)}</title><desc>Original PNG embedded without resampling; raster content, not vectorized. Full source image, without LaTeX placement cropping.</desc><image width="{width}" height="{height}" href="data:image/png;base64,{uri}"/></svg>\n')
            kind = 'embedded_png'
        else:
            with tempfile.TemporaryDirectory(prefix='szfdr-svg-') as temp:
                work = Path(temp)
                if ref.endswith('.tikz.tex'):
                    tex = (r'\documentclass[border=5pt]{standalone}' '\n'
                           r'\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}' '\n'
                           r'\usepackage[magyar]{babel}\usepackage{lmodern,amsmath,tikz}' '\n'
                           r'\usetikzlibrary{arrows.meta,calc}\begin{document}' '\n'
                           + src.read_text() + '\n' + r'\end{document}')
                else:
                    tex = src.with_suffix('.tex').read_text()
                    for dat in src.parent.glob('*.dat'):
                        shutil.copy2(dat, work/dat.name)
                (work/'figure.tex').write_text(r'\def\pgfsysdriver{pgfsys-dvisvgm.def}' + '\n' + tex)
                run(['latex', '--cnf-line=extra_mem_top=20000000', '--cnf-line=extra_mem_bot=20000000', '-interaction=nonstopmode', '-halt-on-error', 'figure.tex'], work)
                run(['dvisvgm', '--no-fonts', '--exact-bbox', '--output='+str(target.resolve()), 'figure.dvi'], work)
            kind = 'vector'
        manifest.append({'source':str(src.relative_to(root)), 'svg':target.name, 'type':kind, 'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
        print(target.name, kind, flush=True)
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    vectors=sum(item['type']=='vector' for item in manifest)
    rasters=len(manifest)-vectors
    (out/'README.txt').write_text(
        f'A v3 jegyzet használt ábráinak SVG-változatai\n\n'
        f'{vectors} valódi vektoros SVG; {rasters} beágyazott PNG-t tartalmazó SVG.\n'
        'A vektoros ábrák többsége körvonalazott szöveget használ; a mass_spring_bvp.svg szerkeszthető Times New Roman feliratokat tartalmaz.\n'
        'A raszteres eredetik beágyazása nem jelent vektorizálást.\n'
        'Újragenerálás: python3 codes/export_figures_svg.py\n'
        'Szükséges: latex, dvisvgm, NumPy, Matplotlib.\n'
        'Az új 6. fejezet ábrái külön: python3 codes/practical_figures_v3.py\n'
        'Az 1.1. szakasz ábrái külön: python3 codes/equilibrium_figures_v3.py\n'
        'A manifest.json a használt forrásokat és SVG-ellenőrzőösszegeket sorolja fel.\n'
        'Korábbi, már nem hivatkozott ábrák is maradhatnak ebben a könyvtárban.\n')
    print(f'Exported {len(manifest)} figures.')
if __name__ == '__main__':
    main()
