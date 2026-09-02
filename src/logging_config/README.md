# logging_config (shared module)

## Role

`logging_config` is a **shared helper module** (not a deployable capacity) that configures the Python
logging system with coloured, developer-friendly log output. Every capacity and shared module calls
`setup_logging()` and then retrieves its logger through `logging_config.getLogger(__name__)`.

## How it works

* `setup_logging()` in `src/logging_config/logging_config.py`:
  * attaches a `colorlog.StreamHandler` to the root logger;
  * adds a `LevelPaddingFilter` that pads the level name so columns align;
  * formats each record as `LEVEL:  filename [timestamp] message`;
  * clears existing handlers, sets the root level to `DEBUG`.
* `LevelPaddingFilter` pads `record.levelname` to a fixed width.

## Usage

```python
import logging
from src.logging_config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
```

## Notes / known inconsistency

* The package `src/logging_config/__init__.py` is empty. Most modules import the package as
  `import logging_config` and use it as an alias of the standard `logging` module
  (`logging_config.getLogger`, `logging_config.Filter`, `logging_config.DEBUG`). Those attributes are
  **not** defined on the empty package, and no `logging_config` package is installed in the virtual
  environment, so `import logging_config` currently raises `ModuleNotFoundError` unless `src` is placed
  on `PYTHONPATH` and the module resolves appropriately.
* Because it is a shared module, it is not listed as a capacity and has no standalone `requirements.txt`;
  its dependency (`colorlog`) is declared in the capacity `requirements.txt` files.
