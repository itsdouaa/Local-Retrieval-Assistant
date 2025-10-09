import subprocess

def read():
    try:
        result = subprocess.run(
            ["sudo", "cat", "/etc/groq_API.txt"],
            check=True,
            text=True,
            capture_output=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Impossible de lire la clé API") from e
