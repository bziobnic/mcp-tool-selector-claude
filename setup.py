"""Setup script for the MCP Tool Selector package."""

from setuptools import setup, find_packages
import os

# Read the version from __init__.py
with open(os.path.join("mcp_tool_selector", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("'\"")
            break
    else:
        version = "0.1.0"

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mcp-tool-selector",
    version=version,
    description="A graphical tool for enabling and disabling MCP server tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MCP Tool Selector Team",
    author_email="example@example.com",
    url="https://github.com/example/mcp-tool-selector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mcp-tool-selector=mcp_tool_selector.app:main",
        ],
    },
)
