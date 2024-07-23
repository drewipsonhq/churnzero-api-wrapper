from setuptools import setup, find_packages

setup(
    name="churnzero-api-wrapper",
    version="0.2.1",
    author="Drew Ipson",
    author_email="drewipson@gmail.com",
    description="A Python wrapper for the ChurnZero HTTP API",
    long_description="""This package provides a Python wrapper for the ChurnZero HTTP API. ChurnZero is a customer success platform that helps businesses reduce customer churn and increase customer engagement.

    With this wrapper, you can easily interact with the ChurnZero HTTP API to update account or contact attributes and track events.

    Features:
    - Set Account Attributes (Create or Update Account Records)
    - Set Contact Attributes (Create or Update Contact Record)
    - Track events: Record important events and actions performed by customers, such as product usage, feature adoption, and support interactions.
    """,
    url="https://github.com/drewipson/churnzero-python-api-wrapper",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=["requests>=2.32.3"],
)
