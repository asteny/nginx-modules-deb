import json
import logging
import os
import multiprocessing
from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path
from shutil import copy
from subprocess import check_call, Popen, check_output
from tempfile import TemporaryDirectory
from types import MappingProxyType
from typing import Dict

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


parser = ArgumentParser()
parser.add_argument("--nginx-src", required=True)
parser.add_argument("--module-map", required=True)
parser.add_argument("--nginx-depend", required=True)
parser.add_argument("--target", default="dist")
parser.add_argument("--deb-path", default="packages")
parser.add_argument("--deb-suffix", default="")
parser.add_argument("--deb-epoch", default=1, type=int)
parser.add_argument("--concurrent", default=multiprocessing.cpu_count(), type=int)


lsb_release = check_output(['lsb_release', '-sc']).decode().strip()


@contextmanager
def cd(path) -> Path:
    current = os.getcwd()

    os.chdir(str(path))
    try:
        log.info("Changing directory %s => %s", current, path)
        yield Path(os.getcwd())
    finally:
        os.chdir(current)


def build(modules, module_paths, concurrent) -> Dict[str, dict]:
    module_args = []

    for path in module_paths.values():
        module_args.append(f"--add-dynamic-module={path}")

    Popen(["make", "clean"]).wait()
    check_call(["/bin/bash", "./configure", "--with-compat"] + module_args)
    check_call(["make", f"-j{concurrent}", "modules"])

    cwd = Path(os.getcwd())

    results = {}
    for name, params in modules.items():
        results[name] = dict(params)
        results[name]['files'] = []
        results[name]['size'] = 0

        for fname in params['files']:
            fpath = cwd / 'objs' / fname

            assert fpath.exists(), f"File {fpath} doesn't exists"
            log.info("Found binary %s", fpath)

            check_call(["strip", "-s", str(fpath)])
            results[name]['size'] += fpath.stat().st_size

            results[name]['files'].append(fpath)
    return results


def prepare_modules(modules, build_path) -> Dict[str, Path]:
    module_paths = {}
    for name, params in modules.items():
        module_path = build_path / str(build_path / name)
        log.info("Cloning repo %s", params['repo'])
        check_call([
            'git', 'clone', '--recursive',
            params['repo'], module_path.resolve()
        ])
        with cd(module_path.resolve()):
            log.info("Fetching submodules for %s", params['repo'])
            check_call(['git', 'submodule', 'init'])
            check_call(['git', 'submodule', 'update'])
            if 'ref' in params:
                log.info(
                    "Switching to ref %r for %s",
                    params['ref'], params['repo']
                )
                check_call(['git', 'checkout', params["ref"]])
            if 'prefix' in params:
                module_path = module_path / params['prefix']

        module_paths[name] = module_path.resolve()
    return module_paths


def make_deb(path: Path, deb_path: Path, module: dict, nginx_version, deb_suffix, deb_epoch):
    with cd(path) as path:
        control_file = path / "DEBIAN" / "control"
        control_file.parent.mkdir(exist_ok=True, parents=True, mode=0o775)

        with open(control_file, "w") as fp:
            for line in module['debian']:
                fp.write(f"{line}\n")
            fp.write(f"Installed-Size: {module['size']}\n")
            fp.write(f"Version: {deb_epoch}:{module['version']}~nginx.{nginx_version}+{deb_suffix}{deb_epoch}\n")

            if "depends" in module:
                fp.write(f"Depends: {module['depends'] % nginx_version}\n")

        with cd(path.parent) as parent:
            check_call([
                'dpkg-deb', '--build',
                str(path.relative_to(parent)), str(deb_path)
            ])

def filter_releases(module_map):
    import lsb_release
    dist_info = lsb_release.get_distro_information()

    modules = dict(module_map['modules'])

    for name, module in modules.items():
        only_releases = module.get("only_releases", [])

        if only_releases and dist_info['RELEASE'] not in only_releases:
            log.info("Skipping module %s", name)
            module_map['modules'].pop(name)

    return module_map

def main():
    arguments = parser.parse_args()

    dist = Path(arguments.target).resolve()
    packages = Path(arguments.deb_path).resolve()
    packages.mkdir(exist_ok=True, parents=True, mode=0o775)

    with open(arguments.module_map, "r") as fp:
        module_map = MappingProxyType(filter_releases(json.load(fp)))

    with cd(arguments.nginx_src), TemporaryDirectory() as build_root:
        build_path = Path(build_root)
        modules = module_map['modules']
        module_paths = prepare_modules(modules, build_path)
        artifacts = build(modules, module_paths, arguments.concurrent)

        dist.mkdir(exist_ok=True, parents=True, mode=0o775)
        for name, module in artifacts.items():
            files = module['files']
            module_dir = dist / name
            module_target = (
                module_dir / 'usr' / 'lib' / 'nginx' / 'modules'
            )
            module_target.mkdir(exist_ok=True, parents=True, mode=0o775)

            if 'configs' in module:
                config_dir = module_dir / 'etc' / 'nginx'
                config_dir.mkdir(exist_ok=True, parents=True, mode=0o775)

                for fname, content in module['configs'].items():
                    fpath = config_dir / fname
                    fpath.parent.mkdir(exist_ok=True, parents=True, mode=0o775)
                    with open(fpath, "w") as fp:
                        fp.write(content)

            for file in files:
                copy(file, module_target / file.name)

            deb_suffix = f"{lsb_release}{arguments.deb_suffix}"

            deb_path = (
                packages / f"{name}_{module['version']}~{deb_suffix}.deb"
            )
            make_deb(
                module_dir,
                deb_path,
                module,
                arguments.nginx_depend,
                arguments.deb_suffix.strip("-"),
                arguments.deb_epoch
            )
            assert deb_path.exists(), f"File {deb_path} was not found"


if __name__ == '__main__':
    main()
