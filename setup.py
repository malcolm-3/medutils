from setuptools import find_packages, setup  # type: ignore

setup(
    name="medutils",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "touch_latest = medutils.scripts.touch_latest:cli",
            "getcol = medutils.scripts.getcol:cli",
        ],
    },
)
