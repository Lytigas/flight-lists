#!/usr/bin/env python3.7

import pathlib
import shutil

from jinja2 import Environment, PackageLoader, select_autoescape
JINJA_ENV = Environment(
    loader=PackageLoader('templates', ''),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_list_html(title, items):
    return JINJA_ENV.get_template("list_page.html").render(title=title, checklist=items)

def render_manifest_html(title, dirs, lists):
    return JINJA_ENV.get_template("dir_page.html").render(title=title, dirs=dirs, lists=lists)

def write_file(path, text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text)

def process_file(relative_path, in_root, out_root):
    infile = in_root / relative_path
    items = [l.strip() for l in infile.read_text().split('\n') if l.strip()]
    title = relative_path.name
    outfile = (out_root / relative_path).with_suffix('.html')
    write_file(outfile, render_list_html(title, items))


def process_dir(relative_path, in_root, out_root, render_up_dir=True):
    indir = in_root / relative_path
    dirs = [x.name for x in indir.iterdir() if x.is_dir()]
    if render_up_dir:
        dirs.append("..")
    lists = [x.name for x in indir.iterdir() if x.is_file()]
    dirs.sort()
    lists.sort()
    title = relative_path.name
    outfile = out_root / relative_path / 'index.html'
    write_file(outfile, render_manifest_html(title, dirs, lists))

def main():
    in_root_dir = pathlib.Path("lists")
    out_root_dir = pathlib.Path("public")
    assert in_root_dir.is_dir()
    if out_root_dir.exists():
        shutil.rmtree(out_root_dir)
    process_dir(pathlib.Path(''), in_root_dir, out_root_dir, render_up_dir=False)
    for p in in_root_dir.glob('**/*'):
        relative = p.relative_to(in_root_dir)
        if p.is_file():
            process_file(relative, in_root_dir, out_root_dir)
        elif p.is_dir():
            process_dir(relative, in_root_dir, out_root_dir)



if __name__ == "__main__":
    main()
