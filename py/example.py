import modules.scripts as scripts
from .example2 import example2_func

def example_func():
    print(f"scripts.basedir(): {scripts.basedir()}")
    example2_func()
    #from ..py2.example3 import example3_func
    import pathlib
    p = pathlib.Path(__file__).parts[-4:-2]
    import importlib
    example3 = importlib.import_module(f"{p[0]}.{p[1]}.py2.example3")
    example3_func = getattr(example3, 'example3_func')
    example3_func()
