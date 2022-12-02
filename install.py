# This file is run during installation and startup
import pathlib
p = pathlib.Path(__file__).parts[-3:]
print(f"called {p[0]}/{p[1]}/{p[2]}")
