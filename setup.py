import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jstream",
    version="0.5",
    author="yuanxb",
    author_email="",
    description="Simple stream tool like java",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/github-yxb/jstream",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    python_requires=">=3.10",
)
