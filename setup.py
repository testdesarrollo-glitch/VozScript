from setuptools import setup, find_packages

setup(
    name="stt_formatter",
    version="0.1.0",
    description="Librería para formateo de Speech-to-Text y captura de audio",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "ollama",
        "SpeechRecognition"
    ],
)