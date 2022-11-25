# import pathlib

# from ouster import client, pcap


# def pcap_read_packet():
#     dataname = "OS-1-64-U02_122211003068_1024x10_20221114_103539"
#     metadata_path = pathlib.Path.cwd() / str(dataname + ".json")
#     pcap_path = pathlib.Path.cwd() / str(dataname + ".pcap")
    
#     with open(metadata_path, 'r') as f:
#         metadata = client.SensorInfo(f.read())
#     source = pcap.Pcap(str(pcap_path), metadata)
    
#     for packet in source:
#         if isinstance(packet, client.LidarPacket):
#             measurement_ids = packet.measurement_id
#             timestamps = packet.timestamp
#             ranges = packet.field(client.ChanField.RANGE)
#             print(f"Encoder counts : {measurement_ids.shape}")
#             print(f"timestamps     : {timestamps.shape}")
#             print(f"ranges         : {ranges.shape}")
        
#         elif isinstance(packet, client.ImuPacket):
#             print(f"Acceleration     : {packet.accel}")
#             print(f"Angular_velocity : {packet.angular_vel}")


# if __name__ == "__main__":
#     pcap_read_packet()