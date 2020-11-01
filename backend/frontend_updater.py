import os
import zipfile
import aiofiles
import shutil

from pathlib import Path

from sanic.exceptions import InvalidUsage
from sanic.response import text


class FrontendUpdater:
    def __init__(self, main_dir: Path, frontend_dir: Path):
        self.main_dir = main_dir
        self.frontend_dir = frontend_dir

    async def update_frontend(self, request):
        files = request.files
        if 'file' not in files or len(files['file']) == 0:
            raise InvalidUsage('no file uploaded')

        if self.frontend_dir.exists():
            shutil.rmtree(str(self.frontend_dir.absolute()))

        self.frontend_dir.mkdir()

        upload_file = request.files['file'][0]
        upload_path = self.main_dir / upload_file.name
        async with aiofiles.open(upload_path, 'wb') as f:
            await f.write(request.files['file'][0].body)
            f.close()

        with zipfile.ZipFile(upload_path) as zf:
            zf.extractall(self.frontend_dir)

        os.remove(upload_path)

        return text('Update successful!')
