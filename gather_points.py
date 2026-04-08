import socket
import struct
import time
UDP_IP = "0.0.0.0"
UDP_PORT = 56301
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
points = []
START_TIME = time.time()
COLLECT_TIME = 15.0  # sec
def save_pcd(filename, points):
    with open(filename, 'w') as f:
        f.write("# .PCD v0.7\n")
        f.write("VERSION 0.7\n")
        f.write("FIELDS x y z intensity time\n")
        f.write("SIZE 4 4 4 4 4\n")
        f.write("TYPE F F F F F\n")
        f.write("COUNT 1 1 1 1 1\n")
        f.write(f"WIDTH {len(points)}\n")
        f.write("HEIGHT 1\n")
        f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        f.write(f"POINTS {len(points)}\n")
        f.write("DATA ascii\n")

        for p in points:
            f.write(f"{p[0]} {p[1]} {p[2]} {p[3]} {p[4]}\n")
while True:
    data, _ = sock.recvfrom(65535)
    if len(data) < 36:
        continue
    dot_num = struct.unpack_from("<H", data, 5)[0]
    data_type = struct.unpack_from("<B", data, 10)[0]
    if data_type != 1:
        continue
    offset = 36
    timestamp = time.time() - START_TIME 

    for i in range(dot_num):
        try:
            x, y, z, reflectivity = struct.unpack_from("<iiiB", data, offset)
        except:
            break
        offset += 14
        x /= 1000.0
        y /= 1000.0
        z /= 1000.0
        if x == 0 and y == 0 and z == 0:
            continue
        points.append([x, y, z, float(reflectivity), timestamp])
    if time.time() - START_TIME > COLLECT_TIME:
        print(f"Saving {len(points)} points...")
        save_pcd("cloud.pcd", points)
        print("Saved cloud.pcd")
        break