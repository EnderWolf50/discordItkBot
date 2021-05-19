import importlib
import inspect
import logging
import pkgutil
from typing import Iterator

from bot import exts

__all__ = [
    "EXTENSIONS",
]

logger = logging.getLogger(__name__)


def get_extensions() -> Iterator[str]:
    for module in pkgutil.walk_packages(exts.__path__, f"{exts.__name__}."):
        # 不載入名稱為 "_" 開頭的檔案
        if module.name.split(".")[-1].startswith("_"):
            continue

        imported = importlib.import_module(module.name)
        if not inspect.isfunction(getattr(imported, "setup", None)):
            # 為資料夾且有 __init__.py 才為 pkg，反之為 cog 檔案
            if not module.ispkg:
                # 如果不是 pkg (為 cog) 且沒有 setup() 則送出警告
                logger.error(
                    f"No `setup()` in {module.name}, the extension will not be loaded."
                )
            continue

        yield module.name


EXTENSIONS = frozenset(get_extensions())
