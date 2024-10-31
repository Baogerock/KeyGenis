import time
import pydirectinput
from pynput import keyboard

running = True


def on_press(key):
    global running
    try:
        if key == keyboard.Key.f12:
            running = False  # 当按下F12时停止循环
    except Exception as e:
        print(f"Error: {e}")


listener = keyboard.Listener(on_press=on_press)
listener.start()


def process_instructions(script_path, loop_amount, loop_gap_time, time_speed):
    with open(script_path, 'r') as f:
        scripts = f.readlines()
    number_lines = len(scripts)

    for _ in range(loop_amount):
        if not running:  # 检查是否需要停止
            print("\n循环已被停止")
            break
        i = 0
        for line in scripts:
            # 跳过第一行的等待和最后一行的额外录制
            if i == number_lines - 1:
                break
            i += 1

            words = line.split(' ')
            if words[0] == 'mouse':
                pos_down = [int(words[2].replace('(', '').replace(',', '')),
                            int(words[3].replace(')', ''))]
                pos_up = [int(words[4].replace('(', '').replace(',', '')),
                          int(words[5].replace(')', ''))]
                duration = float(words[6])
                side = words[1].replace('Button.', '')
                mouse_action(pos_down, pos_up, duration, side=side, time_speed=time_speed)
            elif words[0] == 'keyboard':
                key = words[1].replace('Key.', '').replace('\'', '')
                duration = float(words[2])
                key_action(key, duration, time_speed=time_speed)
            elif words[0] == 'wait':
                duration = float(words[1])
                time.sleep(duration / time_speed)
        time.sleep(loop_gap_time)


def key_action(key, duration, time_speed):
    pydirectinput.keyDown(key)
    time.sleep(duration / time_speed)
    pydirectinput.keyUp(key)


def mouse_action(pos_down, pos_up, duration, side, time_speed):
    pydirectinput.moveTo(pos_down[0], pos_down[1])  # 移动到当前鼠标位置
    pydirectinput.mouseDown(button=side)
    time.sleep(duration / time_speed)
    pydirectinput.moveTo(pos_up[0], pos_up[1])  # 移动到当前鼠标位置
    pydirectinput.mouseUp(button=side)


def simulate_key_and_mouse_operations():
    # 等待几秒钟，给你时间准备
    print("将在 5 秒后开始模拟操作...")
    time.sleep(5)

    # 模拟按下并松开某个键（例如 'a'）
    print("按下 'a' 键...")
    pydirectinput.keyDown('tab')  # 按下 'a'
    time.sleep(1)  # 持续按下 1 秒
    pydirectinput.keyUp('tab')  # 松开 'a'
    print("'a' 键已松开")

    # 获取当前鼠标位置
    x, y = pydirectinput.position()
    print(f"当前鼠标位置: ({x}, {y})")

    # 模拟点击鼠标
    print("将鼠标移动到当前位置并点击...")
    pydirectinput.moveTo(1000, 800)  # 移动到当前鼠标位置
    pydirectinput.mouseDown()  # 按下鼠标
    time.sleep(0.5)  # 按住 0.5 秒
    pydirectinput.mouseUp()  # 松开鼠标
    print("鼠标已点击")
