"""Execute website notebooks in place, then refresh their download zips.

Usage: python3 tools/run_notebooks.py html/files/ToyModel/ToyModel.ipynb [more notebooks...]

The notebooks are executed in their own folder, with a kernel of the conda environment given by
$MABOSS_ENV (default: ~/.local/share/mamba/envs/profile), which must provide pyMaBoSS, the MaBoSS
executables (MaBoSS_128n and MaBoSS_256n are needed by Sizek and Prostate), pygraphviz and ipykernel.
nbconvert itself runs with the Python launching this script.

After execution:
- the "ipylab module is not installed" message printed by that environment is removed from the outputs;
- the notebook is replaced in the zip of its folder (if any), keeping the other files of the zip;
- the run folders created by UPMaBoSS (one per run) are deleted, as they are not part of the site.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

import nbformat

ENV = os.path.expanduser(os.environ.get("MABOSS_ENV", "~/.local/share/mamba/envs/profile"))


def execute(path, kernels_dir):
    folder, name = os.path.split(os.path.abspath(path))
    before = set(os.listdir(folder))
    env = dict(os.environ, JUPYTER_PATH=kernels_dir)
    proc = subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
                           "--inplace", "--ExecutePreprocessor.timeout=7200", name],
                          cwd=folder, env=env, capture_output=True, text=True)
    # UPMaBoSS writes one folder per run next to the notebook
    for new in set(os.listdir(folder)) - before:
        if os.path.isdir(os.path.join(folder, new)) and new != "figures":
            shutil.rmtree(os.path.join(folder, new))
    if proc.returncode != 0:
        print(proc.stderr[-3000:])
        return False
    return True


def strip_ipylab(path):
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = [o for o in cell.outputs if not (
                o.get("output_type") == "stream" and "ipylab module is not installed" in o.get("text", ""))]
    nbformat.write(nb, path)


def refresh_zip(path):
    folder = os.path.dirname(os.path.abspath(path))
    for zip_path in [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".zip")]:
        tmp = zip_path + ".tmp"
        with zipfile.ZipFile(zip_path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                local = os.path.join(folder, os.path.basename(info.filename))
                if info.filename.endswith(".ipynb") and os.path.exists(local):
                    dst.write(local, info.filename)
                else:
                    dst.writestr(info, src.read(info.filename))
        shutil.move(tmp, zip_path)


def main(paths):
    with tempfile.TemporaryDirectory() as kernels_dir:
        os.makedirs(os.path.join(kernels_dir, "kernels", "python3"))
        with open(os.path.join(kernels_dir, "kernels", "python3", "kernel.json"), "w") as f:
            json.dump({"argv": [os.path.join(ENV, "bin", "python"), "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                       "display_name": "Python 3", "language": "python",
                       "env": {"PATH": os.path.join(ENV, "bin") + ":/usr/bin:/bin"}}, f)
        failed = []
        for path in paths:
            print("Running", path, flush=True)
            if execute(path, kernels_dir):
                strip_ipylab(path)
                refresh_zip(path)
                print("OK:", path, flush=True)
            else:
                failed.append(path)
                print("FAILED:", path, flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
