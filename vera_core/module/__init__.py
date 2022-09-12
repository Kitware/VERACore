from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__vera_core": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__vera_core/vue-vera_core.umd.min.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__vera_core/vue-vera_core.css"]

# List of Vue plugins to install/load
vue_use = ["vera_core"]
