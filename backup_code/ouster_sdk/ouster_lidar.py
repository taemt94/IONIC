import time
import pathlib
from contextlib import closing
import numpy as np
import cv2
import os

from ouster import client#, pcap

from config import ouster_config as os_cfg
from metadata import save_metadata
from stream_open3d import viewer_3d
from pcap_local import pcap

def receive_os1(name, stop_event=None):
    print(f"[INFO] pid[{os.getpid()}] '{name}' process is started.")
    
    hostname = os_cfg['hostname']
    udp_port_lidar = os_cfg['udp_port_lidar']
    udp_port_imu = os_cfg['udp_port_imu']
    n_seconds = os_cfg['n_seconds']
    if n_seconds is None:
        n_seconds = np.inf
        
    cfg = client.SensorConfig()
    cfg.udp_port_lidar =udp_port_lidar
    cfg.udp_port_imu = udp_port_imu
    cfg.operating_mode = client.OperatingMode.OPERATING_NORMAL
    client.set_config(hostname, cfg, persist=True, udp_dest_auto=True)
    
    lidar_st_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    save_metadata(client, hostname, lidar_st_time)
    
    from more_itertools import time_limited
    with closing(client.Sensor(hostname, udp_port_lidar, udp_port_imu, buf_size=640)) as source:
        lidar_path = pathlib.Path.cwd() / str(lidar_st_time + "_" + hostname.split(".")[0] + ".pcap")

        print(f"[INFO] Ouster OS1 writing to {lidar_path}")
        source_it = time_limited(n_seconds, source)
        n_packets = pcap.record(source_it, str(lidar_path), stop_event=stop_event)
    
        print(f"[INFO] {n_packets} packets were captured")
    
    print(f"[INFO] pid[{os.getpid()}] '{name}' process is terminated.")


def stream_live_os1():
    hostname = os_cfg['hostname']
    lidar_port = os_cfg['udp_port_lidar']
    
    with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
        show = True
        while show:
            for scan in stream:
                print(f"[INFO] Frame ID : {scan.frame_id}")
                reflectivity = client.destagger(stream.metadata,
                                                scan.field(client.ChanField.REFLECTIVITY))
                reflectivity = (reflectivity / np.max(reflectivity) * 255).astype(np.uint8)
                cv2.imshow("Scaled reflectivity", reflectivity)
                key = cv2.waitKey(1)


def stream_live_open3d(name, stop_event):
    print(f"[INFO] pid[{os.getpid()}] '{name}' process is started.")
    
    hostname = os_cfg['hostname']
    lidar_port = os_cfg['udp_port_lidar']
    
    with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
        viewer_3d(stream, stop_event)
        
    print(f"[INFO] pid[{os.getpid()}] '{name}' process is terminated.")