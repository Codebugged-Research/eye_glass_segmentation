import setuptools

# Read the requirements.txt file
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="eye_glass_segmentation",
    version="0.0.1",
    author="Codebugged-Research",
    author_email="thecodebugged@gmail.com",
    description="A package for spectacles segmentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Codebugged-Research/eye_glass_segmentation",
    package_dir={'': "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=requirements,  # Use the list from requirements.txt
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
    ]
)
