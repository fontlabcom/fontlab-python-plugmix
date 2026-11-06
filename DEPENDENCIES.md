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
`src_docs/requirements.txt` retains all 31 exact hash-locked dependencies from
the qualified ProperDocs pipeline: ProperDocs 1.6.7, MkDocs 1.6.1, MaterialX
10.1.8 and PyMdown Extensions 11.0.1. Runtime dependencies and locks are unchanged.
The fltheme26 1.0.0 light components and FontLab menu load as frontend assets;
the generated MaterialX assets retain their own vendor licence notices.
