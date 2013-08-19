from distutils.core import setup

setup(
    name = "mpu_search",
    scripts = ["mpu_search.py"],
    requires = ["beautifulsoup4", "requests", "lxml", "re", "shelve", "sys"],
    version = "1.1",
    description = "Search Mac Power Users show notes",
    author = "Fernando Xavier de Freitas Crespo",
    author_email = "fernando@crespo.in",
    url = "https://github.com/fcrespo82/alfred2_workflows/tree/master/workflows/source/Search%20Mac%20Power%20Users",
    download_url = "https://github.com/fcrespo82/alfred2_workflows/tree/master/workflows/source/Search%20Mac%20Power%20Users",
    keywords = ["search", "mpu", "Mac Power Users"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        ],
    long_description = """\
"""
)