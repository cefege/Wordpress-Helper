import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='WPHelper',
    version='0.0.1',
    author='Mihai Mateias',
    author_email='mateiasmihaiandrei@gmail.com',
    description='Package to translate the webpages content while keeping the same page structure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['WPHelper'],
    install_requires=["playwright==1.20.1"],

)
