import pathlib
from contextlib import closing

def save_metadata(client, hostname, st_time):
    metadata_path = pathlib.Path.cwd() / str(st_time + "_" + hostname.split(".")[0] + ".json")
    with closing(client.Sensor(hostname)) as source:
        # print some useful info from
        print("Retrieved metadata:")
        print(f"  serial no:        {source.metadata.sn}")
        print(f"  firmware version: {source.metadata.fw_rev}")
        print(f"  product line:     {source.metadata.prod_line}")
        print(f"  lidar mode:       {source.metadata.mode}")
        print(f"Writing to: {hostname}.json")

        # write metadata to disk
        source.write_metadata(metadata_path)