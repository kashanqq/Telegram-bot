import os
import asyncio
import shutil
import stat
from aiogram.types import CallbackQuery

async def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

async def delete_file_later(file_path, delay):
    await asyncio.sleep(delay)
    if os.path.exists(file_path):
        shutil.rmtree(file_path, onerror=remove_readonly)