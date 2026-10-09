import time
import psutil
import csv
import os

def get_app_memory():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('app:app' in arg for arg in cmdline):
                mem_info = proc.memory_info()
                return mem_info.rss / (1024 * 1024) # Convert bytes to MB
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def main():
    csv_file = 'metrics.csv'
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'memory_usage_mb'])
        
        print("🔍 Starting telemetry collection... (Press Ctrl+C to stop)")
        while True:
            mem = get_app_memory()
            if mem is not None:
                timestamp = time.time()
                writer.writerow([timestamp, round(mem, 2)])
                f.flush()
                print(f"[Telemetry] Recorded Memory: {round(mem, 2)} MB")
            else:
                print("[Telemetry] Waiting for FastAPI app process to start...")
            time.sleep(2)

if __name__ == '__main__':
    main()