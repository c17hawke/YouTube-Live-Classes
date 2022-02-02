# Lecture 06: 
## How to use python plus your phone to control your system by Sunny | Day 6

<iframe width="560" height="315" src="https://www.youtube.com/embed/GpIBENNX1jU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Code used in the lecture

??? Notes "rx.py"
    ```python
    import socket
    import argparse
    from pynput.keyboard import Key, Controller

    keyboard = Controller()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def control(signals):
        for signal in signals["signal_release"]:
            keyboard.release(signal)

        keyboard.press(signals["signal_on"])

    def main(host, port):
        print(f"host: {host}, port: {port}")

        s.bind((host, int(port)))

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
                    g_x, g_y, g_z = gravity_data

                    print(f"current state: {g_x}, {g_y}, {g_z}")
                    # halt 
                    if (-3 < g_x < 3) and (-3 < g_y < 3):
                        print("HALT")
                        signals = {"signal_release": [Key.up, Key.down, Key.left, Key.right], 
                        "signal_on": Key.space}
                        control(signals)

                    # forward
                    elif (-3 > g_x) and (-3 < g_y < 3):
                        print("FORWARD")
                        signals = {"signal_release": [Key.space, Key.down, Key.left, Key.right], 
                        "signal_on": Key.up}
                        control(signals)

                    # retreat
                    elif (3 < g_x) and (-3 < g_y < 3):
                        print("RETREAT")
                        signals = {"signal_release": [Key.up, Key.space, Key.left, Key.right], 
                        "signal_on": Key.down}
                        control(signals)

                    # left
                    elif (-3 < g_x < 3) and (-3 > g_y):
                        print("LEFT TURN")
                        signals = {"signal_release": [Key.up, Key.down, Key.space, Key.right], 
                        "signal_on": Key.left}
                        control(signals)

                    # right
                    elif (-3 < g_x < 3) and (3 < g_y):
                        print("RIGHT TURN")
                        signals = {"signal_release": [Key.up, Key.down, Key.left, Key.space], 
                        "signal_on": Key.right}
                        control(signals)


            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                print(e)


    if __name__ == '__main__':
        args = argparse.ArgumentParser()
        args.add_argument('--port',  default=5555)
        args.add_argument('--host', default="192.168.0.6")
        parsed_args = args.parse_args()
        main(parsed_args.host, parsed_args.port)
    ```