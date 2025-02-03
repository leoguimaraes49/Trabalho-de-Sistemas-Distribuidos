from setuptools import setup, find_packages

setup(
    name="projeto_cafe",
    version="0.1",
    packages=find_packages(),  # Encontra automaticamente "agents", "api", etc.
    install_requires=[
        "fastapi",
        "uvicorn",
        "sounddevice",
        "whisper-openai",
        "numpy",
        "torch",
        "torchaudio",
        "soundfile",
        "git+https://github.com/facebookresearch/audiocraft.git"
    ],
)