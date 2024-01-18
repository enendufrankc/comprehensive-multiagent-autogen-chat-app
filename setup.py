import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.1.0"  # Consider updating the version

REPO_NAME = "Multi Agent Chat Bot"
AUTHOR_USER_NAME = "enendufrankc"
SRC_REPO = "multi_agent_chat_bot"
AUTHOR_EMAIL = "enendufrankc@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A multi-agent chatbot implementation using AutoGen",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Correct the parameter name
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        # List of your dependencies, e.g.,
        # 'numpy',
        # 'pandas',
        # 'streamlit',
        # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Add more classifiers as appropriate
    ],
    python_requires='>=3.6',  # Specify your Python version requirement
    keywords='chatbot autogen multi-agent streamlit',  # Add relevant keywords
)
