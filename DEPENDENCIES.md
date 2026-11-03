<!-- this_file: DEPENDENCIES.md -->
# Dependencies

| Package | Use |
| --- | --- |
| `fontlab-fontlabapp` | Runtime overlay lifecycle (`EditorPainters`), safe Qt menus (`OwnedMenus`) and native list conversion. Required inside FontLab. |
| `hatchling` and `hatch-vcs` | Build package and derive version from git tags. |
| `pytest` and `pytest-cov` | Offline tests and line-coverage reports. Test extra only. |

FontLab 9 provides `fontlab` and MeVisLab `PythonQt` at runtime; neither is a
PyPI dependency.
