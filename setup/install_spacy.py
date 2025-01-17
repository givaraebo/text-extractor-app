import subprocess
import platform
import sys


def run_command(command):
    """Führt einen Shell-Befehl aus."""
    try:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running: {command}\n{e}\n")
        sys.exit(1)


def install_spacy():
    """Installiert spaCy basierend auf dem Betriebssystem."""
    system = platform.system()
    machine = platform.machine()

    if system == "Darwin":
        if "arm" in machine.lower():  # Für M1/M2-Chips
            print("Detected macOS (Apple Silicon).")
            commands = [
                "pip install -U pip setuptools wheel",
                "pip install -U 'spacy[apple]'",
                "python -m spacy download en_core_web_sm",
                "python -m spacy download de_core_news_sm",
                "pip install spacy-lookups-data"
            ]
        else:
            print("Detected macOS (Intel).")
            commands = [
                "pip install -U pip setuptools wheel",
                "pip install -U spacy",
                "python -m spacy download en_core_web_sm",
                "python -m spacy download de_core_news_sm",
                "pip install spacy-lookups-data",
            ]
    elif system == "Linux":
        print("Detected Linux.")
        commands = [
            "pip install -U pip setuptools wheel",
            "pip install -U spacy",
            "python -m spacy download en_core_web_sm",
            "python -m spacy download de_core_news_sm",
            "pip install spacy-lookups-data",

        ]
    elif system == "Windows":
        print("Detected Windows.")
        commands = [
            "python -m pip install -U pip setuptools wheel",
            "python -m pip install -U spacy",
            "python -m spacy download en_core_web_sm",
            "python -m spacy download de_core_news_sm",
            "pip install spacy-lookups-data",

        ]
    else:
        print(f"Unsupported system: {system}")
        sys.exit(1)

    # Führe die entsprechenden Befehle aus
    for cmd in commands:
        run_command(cmd)


if __name__ == "__main__":
    install_spacy()
