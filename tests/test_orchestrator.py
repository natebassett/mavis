from app.core.orchestrator import Orchestrator

mavis = Orchestrator()

print(mavis.process("Hello MAVIS"))
print(mavis.process(""))
print(mavis.process("How are you?"))