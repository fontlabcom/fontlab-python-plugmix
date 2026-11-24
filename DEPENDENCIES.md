<!-- this_file: DEPENDENCIES.md -->
# Dependencies

| Package | Use |
| --- | --- |
| `fontlab-fontlabapp` | Runtime overlay lifecycle (`EditorPainters`), safe Qt menus (`OwnedMenus`) and native list conversion. Required inside FontLab. |
| `hatchling` and `hatch-vcs` | Build package and derive version from git tags. |
| `pytest` and `pytest-cov` | Offline tests and line-coverage reports. Test extra only. |

FontLab 9 provides `fontlab` and MeVisLab `PythonQt` at runtime; neither is a
PyPI dependency.

## Independent documentation environment

Python 3.13 and uv 0.13.7 build the site separately from the product runtime.
The hash-locked `src_docs/requirements.txt` installs fly-january 0.3.0 or later,
ProperDocs 1.6.7, MkDocs 1.6.1, MaterialX 10.1.8 and PyMdown Extensions
11.0.1. The theme provides the FontLab menu and footer.
