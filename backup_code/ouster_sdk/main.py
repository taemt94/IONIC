import multiprocessing
import time

from ouster_lidar import receive_os1, stream_live_os1, stream_live_open3d


def main():
    
    procs = []
    stop_event = multiprocessing.Event()
    
    # proc_functions = [('os1_record', receive_os1)]#, ('os1_stream', stream_live_open3d)]
    proc_functions = [('os1_stream', stream_live_open3d)]
    
    
    for name, proc_func in proc_functions:
        proc = multiprocessing.Process(target=proc_func, args=(name, stop_event))
        procs.append(proc)
    
    for proc in procs:
        proc.start()
    
    time.sleep(2)
    signal_input = input("[REQUEST] Press 'Enter' to terminate all processes. \n")
    while signal_input != '':
        signal_input = input()
    stop_event.set()
    
    for proc in procs:
        proc.join()
    
if __name__ == "__main__":
    main()