from setuptools import find_packages, setup  # type: ignore   ## required by github

setup(
    name="malcolm3utils",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "touch_latest = malcolm3utils.scripts.touch_latest:cli",
            "getcol = malcolm3utils.scripts.getcol:cli",
            "merge = malcolm3utils.scripts.merge:cli",
        ],
    },
)
