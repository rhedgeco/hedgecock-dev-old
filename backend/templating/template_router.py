import os

from pathlib import Path
from typing import List
from jinja2 import Template
from sanic import Sanic, response


def define_frontend_routes_with_templates(
        app: Sanic,
        frontend_dir: Path,
        template_dir: Path):
    def _get_all_files_with_suffix_recursive(search_path: Path,
                                             suffix: str) -> List[Path]:
        files = []
        for f in os.listdir(str(search_path.absolute())):
            full_path = search_path / f
            if full_path.is_dir() and not full_path.is_symlink():
                files.extend(
                    _get_all_files_with_suffix_recursive(full_path,
                                                         suffix)
                )
            elif full_path.suffix.lower() == suffix.lower():
                files.append(full_path)
        return files

    template_dict = {}
    for path in _get_all_files_with_suffix_recursive(template_dir, '.html'):
        with open(str(path.absolute()), 'r') as f:
            template_dict[path.with_suffix('').name] = f.read()

    for path in _get_all_files_with_suffix_recursive(frontend_dir, '.html'):
        relative_path = path.relative_to(frontend_dir)
        uri = relative_path.with_suffix('')

        async def resource(request):
            with open(str(path.absolute()), 'r') as f:
                template = Template(f.read())
            return response.html(
                template.render(template_dict))

        app.add_route(resource, str(uri))

    def index(request):
        with open(str(frontend_dir / 'index.html')) as f:
            template = Template(f.read())
        return response.html(template.render(template_dict))

    app.static('/', str(frontend_dir))
    app.add_route(index, '/')
