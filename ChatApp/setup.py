# setup.py
from setuptools import setup, find_packages

setup(
    name="OmegaChatApp",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "Flask-SocketIO>=5.0.0",
        "pyngrok>=5.0.0",
        "python-socketio>=5.0.0",
        "PyQt5>=5.15.0"  # (Not used in final code, but may be needed by some systems; our GUI is built with Tkinter.)
    ],
)
