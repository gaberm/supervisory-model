import pkgutil
import importlib

from .base_adapter import BaseAdapter
from .adapter_worker import AdapterWorker

for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name not in ("base_adapter", "adapter_worker"):
        importlib.import_module(f".{module_name}", package=__name__)
