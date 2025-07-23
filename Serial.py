import serial
import time

# 전역 변수
connection = None
current_distance = 0

def connect_sensor(port='COM4'):
    global connection
    try:
        connection = serial.Serial(port, 9600)
        time.sleep(2)
        print("연결 성공")
        return True
    except:
        print("연결 실패")
        return False

def read_distance():
    global connection, current_distance
    if connection and connection.in_waiting > 0:
        data = connection.readline().decode().strip()
        try:
            distance = float(data)
            current_distance = distance
            return distance
        except:
            pass
    return None

def main():
    if connect_sensor():
        for i in range(10):
            dist = read_distance()
            if dist:
                print(f"거리: {dist}cm")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
