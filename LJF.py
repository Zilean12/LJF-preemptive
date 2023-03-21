import time
from typing import List
from tabulate import tabulate

class Process:
    def __init__(self, name: str, priority: int, burst_time: int) -> None:
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.wait_time = 0
        self.response_time = None
        self.response_deviation = None

    def __str__(self) -> str:
        return self.name

    def execute(self, current_time: int) -> None:
        self.start_time = current_time
        print(f"Executing {self.name} with priority {self.priority} for {self.remaining_time} seconds.")
        time.sleep(self.remaining_time)
        self.end_time = current_time + self.remaining_time

    def calculate_metrics(self) -> None:
        self.wait_time = self.end_time - self.start_time - self.burst_time
        self.response_time = self.start_time
        self.response_deviation = self.response_time - self.priority

def print_gantt_chart(processes: List[Process]) -> None:
    gantt_chart = ""
    for process in processes:
        gantt_chart += f"{process.name}|"
        for i in range(process.start_time, process.end_time):
            gantt_chart += "-"
        gantt_chart += f"{process.end_time}\n"
    print(gantt_chart)

def print_metrics_table(processes: List[Process]) -> None:
    metrics = []
    for process in processes:
        metrics.append([ 
            process.name, 
            process.priority, 
            process.burst_time, 
            process.start_time, 
            process.end_time, 
            process.end_time - process.start_time, 
            process.wait_time, 
            process.response_time, 
            process.response_deviation 
        ])
    headers = [ "Process", "Priority", "Burst Time", "Start Time", "End Time", "TAT", "WT", "RT", "RD" ]
    print(tabulate(metrics, headers=headers, tablefmt="grid"))

# define the list of processes to execute
processes = [
    Process("Process 1", 1, 3),
    Process("Process 2", 2, 2),
    Process("Process 3", 1, 1),
    Process("Process 4", 3, 4)
]

# sort the processes based on priority
processes.sort(key=lambda p: p.priority)

# execute the processes
current_time = 0
for process in processes:
    process.execute(current_time)
    current_time = process.end_time

# calculate metrics
total_tat = 0
total_wt = 0
total_rt = 0
total_rd = 0
for process in processes:
    process.calculate_metrics()
    total_tat += process.end_time - process.start_time
    total_wt += process.wait_time
    total_rt += process.response_time
    total_rd += process.response_deviation

# print metrics and Gantt chart
num_processes = len(processes)
avg_tat = total_tat / num_processes
avg_wt = total_wt / num_processes
avg_rt = total_rt / num_processes
avg_rd = total_rd / num_processes

print(f"Avg TAT: {avg_tat}")
print(f"Avg WT: {avg_wt}")
print(f"Avg RT: {avg_rt}")
print(f"Avg RD: {avg_rd}")

print("Gantt Chart:")
print_gantt_chart(processes)

print("Metrics Table:")
print_metrics_table(processes)
