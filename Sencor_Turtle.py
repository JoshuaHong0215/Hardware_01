import turtle
import random
import serial
import time

# ==== 시리얼 센서 설정 ====
connection = None
current_distance = 0
DISTANCE_THRESHOLD = 5  # 예: 15cm 이하이면 멈춤


def connect_sensor(port='COM4'):
    global connection
    try:
        connection = serial.Serial(port, 9600)
        time.sleep(2)
        print("센서 연결 성공")
        return True
    except:
        print("센서 연결 실패")
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


# ==== 터틀 세팅 ====
s = turtle.getscreen()
t = turtle.Turtle()
t.shape("turtle")
t.shapesize(1.5, 1.5, 1.5)
t.pencolor("purple")
t.pensize(4)

# 장애물 (빨간 사각형)
t.penup()
t.goto(-50, 100)
t.setheading(0)
t.pendown()
t.fillcolor("red")
t.begin_fill()
for _ in range(2):
    t.forward(100)
    t.right(90)
    t.forward(100)
    t.right(90)
t.end_fill()

# 시작 위치
t.penup()
t.goto(-350, -300)
t.setheading(45)
t.pendown()


# === 거리 기록 ===
distance_list = []
avoid_positions = []

def custom_forward(turtle_obj, dist):
    turtle_obj.forward(dist)
    distance_list.append(dist)


def reached_destination(turtle_obj, goal_x, goal_y, tolerance=10):
    x, y = turtle_obj.pos()
    return abs(x - goal_x) <= tolerance and abs(y - goal_y) <= tolerance


def check_collision(turtle_obj, margin=10):
    x, y = turtle_obj.pos()
    return (-50 - margin) <= x <= (50 + margin) and (0 - margin) <= y <= (100 + margin)


def avoid_obstacle():
    print("장애물 감지! 회피 행동 시작!")
    turn_angle = random.randint(30, 150)
    direction = random.choice([1, -1])
    if direction == 1:
        t.left(turn_angle)
        print(f"좌회전 {turn_angle}도")
    else:
        t.right(turn_angle)
        print(f"우회전 {turn_angle}도")
    move_distance = random.randint(20, 50)
    t.forward(move_distance)
    print(f"{move_distance}픽셀 이동 완료")
    distance_list.append(move_distance)
    
# === 회피 좌표 저장 및 표시 ===
    pos = t.pos()
    avoid_positions.append(pos)
    t.dot(10, "red")  # 현재 위치에 빨간 점 찍기


# ==== 메인 실행 ====
def main():
    if not connect_sensor():
        return

    goal_x, goal_y = 250, 300
    step_size = 20
    max_steps = 1000

    for step in range(max_steps):
        # 목표 도달 여부
        if reached_destination(t, goal_x, goal_y):
            print("도착 지점에 도달했습니다.")
            break

        # 센서 거리 측정
        dist = read_distance()
        if dist is not None:
            print(f"센서 감지 거리: {dist:.1f}cm")
            if dist <= DISTANCE_THRESHOLD: 
                print("센서 거리 임계값 도달! 거북이 정지!")
                break

        # 무작위 이동
        angle_to_goal = t.towards(goal_x, goal_y)
        offset = random.randint(-30, 30)
        t.setheading(angle_to_goal + offset)
        t.forward(step_size)
        distance_list.append(step_size)

        # 충돌 → 회피
        if check_collision(t):
            print("충돌 감지! 되돌아갑니다.")
            t.backward(step_size)
            avoid_obstacle()

        time.sleep(0.1)  # 너무 빠르게 움직이지 않도록

    print(f"총 이동 거리: {sum(distance_list)} 픽셀")
    print(f"최종 거북이 위치: {t.pos()}")
    
# 결과 출력
    print(f"총 이동 거리: {sum(distance_list)} 픽셀")
    print(f"최종 거북이 위치: {t.pos()}")

# === 회피 좌표 출력 ===
    if avoid_positions:
        print("회피했던 좌표 목록:")
        for idx, pos in enumerate(avoid_positions, 1):
            print(f"{idx}. {pos}")
    else:
        print("회피한 장애물이 없었습니다.")


if __name__ == "__main__":
    main()
