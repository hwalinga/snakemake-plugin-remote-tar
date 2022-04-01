from setuptools import setup
import meta as m

setup(
    name="snakemake-plugin-remote-tar",
    version=m.__version__,
    description="Use files in tar archives with Snakemake",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hielkewalinga/snakemake-plugin-remote-tar/",
    license=m.__license__,
    author=m.__author__,
    author_email=m.__email__,
    py_modules=["snakemake_plugin_remote_tar"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
