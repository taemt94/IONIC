ouster_config = dict(hostname="os-122211003068.local",
                     udp_port_lidar=7502,
                     udp_port_imu=7503,
                     n_seconds=None, ## Max seconds of time to record. 
                                     ##If n_seconds == None, it will record data until interrupt
                     )