import socket
import time


def send_move_command(ip, port, object_positions):
    """
    发送多个角色的目标坐标到Unity。
    object_positions: [(object_id, x, y), (object_id, x, y), ...]
    """
    try:
        # 创建 socket 客户端
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))

        # 构造移动命令，支持多个角色
        command = "MOVE:" + ";".join([f"{object_id},{x},{y}" for object_id, x, y in object_positions])
        client.sendall(command.encode('utf-8'))
        print(f"Sent: {command}")

        # 关闭连接
        client.close()
    except Exception as e:
        print(f"Error: {e}")


def send_speak_command(ip, port, object_id, message):
    """
    发送角色说话命令到Unity。
    """
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
        user_input = input("Enter command (e.g., objectID,x,y or 'speak objectID message') or 'exit' to quit: ").strip()

        if user_input.lower() == "exit":
            print("Exiting...")
            break  # 用户输入 "exit" 时退出循环

        elif user_input.lower().startswith("speak"):
            # 处理说话命令
            try:
                _, object_id, message = user_input.split(" ", 2)
                object_id = int(object_id)
                send_speak_command(unity_ip, unity_port, object_id, message)
            except ValueError:
                print("Invalid format for speak command. Use 'speak objectID message'.")

        else:
            # 处理多个角色移动命令
            try:
                object_positions = []
                commands = user_input.split(';')

                for command in commands:
                    object_id, x, y = command.split(',')
                    object_id = int(object_id)  # 转换物体ID为整数
                    x, y = float(x), float(y)  # 转换坐标为浮动类型
                    object_positions.append((object_id, x, y))

                send_move_command(unity_ip, unity_port, object_positions)

            except ValueError:
                print(
                    "Invalid input. Please enter coordinates in the format 'objectID,x,y' or multiple commands separated by ';'.")
