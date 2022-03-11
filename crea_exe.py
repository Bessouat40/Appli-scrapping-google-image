from cx_Freeze import setup, Executable
base = None

executables = [Executable("app.py", base=base)]

packages = ["dash", "dash_core_components", "dash_html_components", "webbrowser", "re", "pandas", "selenium", "time", "urllib.request", "os"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "scrappeur",
    options = options,
    version = "1.0",
    description = 'Voici mon programme',
    executables = executables
)