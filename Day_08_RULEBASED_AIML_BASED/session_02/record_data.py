import socket
import argparse


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def record_data(signals, csv_file):
    with open(csv_file, "a") as f:
        string = ""
        for signal in signals["dependent_var"]:
            string += f"{signal},"
        string += f"{signals['target']}\n"
        f.writelines(string)

def rule_based_module(gravity_data, csv):
    g_x, g_y, g_z = gravity_data

    print(f"current state: {g_x}, {g_y}, {g_z}")
    # halt 
    if (-3 < g_x < 3) and (-3 < g_y < 3):
        print("HALT")
        signals = {"dependent_var": gravity_data[:-1], 
        "target": "0"}
        record_data(signals, csv_file=csv)

    # forward
    elif (-3 > g_x) and (-3 < g_y < 3):
        print("FORWARD")
        signals = {"dependent_var": gravity_data[:-1], 
        "target": "1"}
        record_data(signals, csv_file=csv)

    # retreat
    elif (3 < g_x) and (-3 < g_y < 3):
        print("RETREAT")
        signals = {"dependent_var": gravity_data[:-1], 
        "target": "2"}
        record_data(signals, csv_file=csv)

    # left
    elif (-3 < g_x < 3) and (-3 > g_y):
        print("LEFT TURN")
        signals = {"dependent_var": gravity_data[:-1], 
        "target": "3"}
        record_data(signals, csv_file=csv)

    # right
    elif (-3 < g_x < 3) and (3 < g_y):
        print("RIGHT TURN")
        signals = {"dependent_var": gravity_data[:-1], 
        "target": "4"}
        record_data(signals, csv_file=csv)

def init_csv_file(csv_file):
    with open(csv_file, "a") as f:
        string = "g_x,g_y,TARGET\n"
        f.writelines(string)


def main(host, port, csv):
    print(f"host: {host}, port: {port}")

    s.bind((host, int(port)))

    init_csv_file(csv)

    while True:
        try:
            BYTE = 8192
            message, address = s.recvfrom(BYTE)
            LIST_DATA = str(message).split(",")
            rcvd_length = len(LIST_DATA)
            EXPECTED_LEN = 17
            if rcvd_length == EXPECTED_LEN:
                gravity_data = LIST_DATA[-3:]
                for idx, gravity in enumerate(gravity_data):
                    gravity_data[idx] = float(gravity.strip()[:-1])

                rule_based_module(gravity_data, csv)


        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            raise e


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--port',  default=5555)
    args.add_argument('--host', default="192.168.0.6")
    args.add_argument('--csv', default="data.csv")
    parsed_args = args.parse_args()
    main(parsed_args.host, parsed_args.port, parsed_args.csv)
