import subprocess as sp

sp.run(["python", "-m", "venv", "venv"])
sp.run([".\venv\Scripts\activate"])
sp.run(["pip", "install", "-r", "requirements,txt"])
