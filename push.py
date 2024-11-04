import subprocess as sp
import shlex


sp.run(["python", "-m", "venv", "venv"])
sp.run(shlex.split(".\\venv\\Scripts\\activate && pip install -r requirements.txt"))
# sp.run([".\\venv\\Scripts\\activate", "&&", ""])
# sp.run(["pip", "install", "-r", "requirements,txt"])
