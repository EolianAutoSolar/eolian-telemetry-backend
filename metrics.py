import psutil
import datetime
import time

## SCRIPT SACADO DE CHATGPT

def log_usage():
    # Define the interval (0.2 seconds) and duration (10800 seconds for 3 hours)
    interval = 0.2
    duration = 60
    end_time = time.time() + duration

    while True:
        # Get the current time with microseconds
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
        # Get overall CPU usage
        cpu_usage = psutil.cpu_percent(interval=None)
        
        # Get usage per CPU core
        per_core_usage = psutil.cpu_percent(interval=None, percpu=True)
        
        # Get RAM usage
        ram_usage = psutil.virtual_memory().percent
        
        # Format the per core usage as a string
        per_core_usage_str = ', '.join(f'Core {i}: {usage}%' for i, usage in enumerate(per_core_usage))
        
        # Log the usage
        with open("system_usage.log", "a+") as log_file:
            log_file.write(f"{current_time}, CPU: {cpu_usage}%, RAM: {ram_usage}%, {per_core_usage_str}\n")
        
        # Sleep for the remainder of the interval
        time.sleep(interval)

if __name__ == "__main__":
    log_usage()
