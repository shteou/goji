import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goji",
    version="0.0.3",
    author="Stewart Platt",
    author_email="shteou@gmail.com",
    description="A GitOps tool for running jobs on k8s",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shteou/goji",
    entry_points={"console_scripts": ["goji=goji.goji:main"]},
    packages=["goji","goji.commands"],
    install_requires=[
          'gitpython',
          'kubernetes',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

