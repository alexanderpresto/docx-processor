from setuptools import setup, find_packages

setup(
    name="docx-processor",
    version="0.1.0",
    package_dir={"": "src"},
    packages=["docx_processor"],
    install_requires=[
        "mammoth>=1.5.0",
        "beautifulsoup4>=4.11.0",
        "Pillow>=9.0.0",
        "lxml>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "docx-processor=docx_processor.cli:main",
        ],
    },
)
