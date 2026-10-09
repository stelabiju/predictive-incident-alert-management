from fastapi import FastAPI
app = FastAPI()
memory_leak_storage = []

@app.get("/")
def read_root():
    return {"status": "healthy"}

@app.get("/leak")
def simulate_leak():
    # Adds ~10MB per call to simulate a memory leak
    memory_leak_storage.append(" " * 1024 * 1024 * 10)
    return {"allocated_blocks": len(memory_leak_storage)}