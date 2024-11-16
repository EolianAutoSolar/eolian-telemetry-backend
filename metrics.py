import psutil
import datetime
import time
from multiprocessing import Event

# TODO: poder diferenciar la carga producida por la telemetria, es decir sin contar el feeder ni las metricas
def log_usage(stop_event):
    # Define the interval (0.2 seconds) and duration (10800 seconds for 3 hours)
    file_name = "system_usage.log"
    interval = 0.2
    duration = 60
    end_time = time.time() + duration
    # delete old file
    file_del = open(file_name, "w+")
    file_del.close()
    while not stop_event.is_set():
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
        with open(file_name, "a+") as log_file:
            log_file.write(f"{current_time}, CPU: {cpu_usage}%, RAM: {ram_usage}%, {per_core_usage_str}\n")
        
        # Sleep for the remainder of the interval
        time.sleep(interval)

if __name__ == "__main__":
    stop_event = Event()
    log_usage(stop_event)
