import socket
import time


def send_move_command(ip, port, object_id, x, y):
    try:
        # 创建 socket 客户端
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))

        # 构造移动命令
        command = f"MOVE:{object_id},{x},{y}"
        client.sendall(command.encode('utf-8'))
        print(f"Sent: {command}")

        # 关闭连接
        client.close()
    except Exception as e:
        print(f"Error: {e}")

def send_speak_command(ip, port, object_id, message):
    try:
        # 创建 socket 客户端
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))

        # 构造说话命令
        command = f"SPEAK:{object_id}:{message}"
        client.sendall(command.encode('utf-8'))
        print(f"Sent: {command}")

        # 关闭连接
        client.close()
    except Exception as e:
        print(f"Error: {e}")

# 示例调用
if __name__ == "__main__":
    unity_ip = "127.0.0.1"  # Unity 运行的 IP 地址
    unity_port = 12345  # Unity 使用的端口号

    while True:
        # 获取用户输入的物体ID、坐标或说话内容
        user_input = input("Enter object ID, coordinates (objectID,x,y), or 'speak objectID message' or type 'exit' to quit: ")

        if user_input.lower() == "exit":
            break  # 用户输入 "exit" 时退出循环

        if user_input.startswith("speak"):
            # 获取说话内容
            _, object_id, message = user_input.split(" ", 2)
            object_id = int(object_id)
            send_speak_command(unity_ip, unity_port, object_id, message)
        else:
            try:
                # 解析物体ID和坐标
                object_id, x, y = user_input.split(',')
                object_id = int(object_id)  # 转换物体ID为整数
                x, y = float(x), float(y)  # 转换坐标为浮动类型
                time.sleep(3)
                send_move_command(unity_ip, unity_port, object_id, x, y)
            except ValueError:
                print("Invalid input. Please enter coordinates in the correct format.")
