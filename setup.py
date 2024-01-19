from setuptools import find_packages, setup

setup(
    name="medutils",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "types-Pygments",
        "types-colorama",
        "types-setuptools",
    ],
    entry_points={
        "console_scripts": [
            "touch_latest = medutils.scripts.touch_latest:cli",
        ],
    },
)
