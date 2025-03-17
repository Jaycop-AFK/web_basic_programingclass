import asyncio
import websockets
# import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BCM)

servo_pin = 17

# GPIO.setup(servo_pin, GPIO.OUT)

# pwm = GPIO.PWM(servo_pin, 50)
# pwm.start(0)


def set_angle(angle):
    print(f"Angle set to {angle}")
    duty = angle / 18 + 2
    # GPIO.output(servo_pin, True)
    # pwm.ChangeDutyCycle(duty)
    # time.sleep(1)
    # GPIO.output(servo_pin, False)
    # pwm.ChangeDutyCycle(0)

angle = 90

set_angle(angle)


class MotorControl:
    def move_forward(self, speed):
        print(f"Motor moving forward at speed {speed}")
        # mortor_pin.move_forward(speed)
        
    def move_backward(self, speed):
        print(f"Motor moving backward at speed {speed}")
        # mortor_pin.move_backward(speed)

    def turn_left(self, speed):
        print(f"Motor turning left at speed {speed}")
        # mortor_pin.turn_left(speed)

    def turn_right(self, speed):
        print(f"Motor turning right at speed {speed}")
        
        # mortor_pin.turn_right(speed)

    def stop(self):
        print("Motor stopped")
        # mortor_pin.stop()
motor_control = MotorControl()
current_speed = 100

async def handle_client(websocket):
    global current_speed, angle
    
    print(f"Client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received from client: {message}")

            if isinstance(message, bytes): 
                payload = message
                if len(payload) == 1:
                    command = payload[0]
                    if command == 0x04: 
                        current_speed = min(current_speed + 100, 255)
                        print(f"Speed increased to {current_speed}")
                    elif command == 0x05: 
                        current_speed = max(current_speed - 100, 100)
                        print(f"Speed decreased to {current_speed}")
                    elif command == 0x06: 
                        print(f"Rotate up of server")
                        angle += 10
                        if angle > 180:
                            angle = 180
                        set_angle(angle)
                    elif command == 0x07: 
                        print(f"Rotate down of server")
                        angle -= 10
                        if angle < 0:
                            angle = 0
                        set_angle(angle)
                    elif command == 0x08:
                        motor_control.turn_left(current_speed)
                    elif command == 0x09:
                        motor_control.turn_right(current_speed)
                    else:
                        motor_control.stop()
                elif len(payload) == 4:
                    direction = payload[0]
                    joystick_x = payload[2]
                    joystick_y = payload[3]
                    
                    if direction == 0x01: 
                        if joystick_y > 135: 
                            motor_control.move_forward(current_speed)
                        elif joystick_y < 120:
                            motor_control.move_backward(current_speed)
                        else:
                            motor_control.stop()
                            
                    elif direction == 0x02:
                        if joystick_y > 135: 
                              motor_control.move_backward(current_speed)
                           
                        elif joystick_y < 120:
                           motor_control.move_forward(current_speed)
                        elif joystick_x > 135: 
                            motor_control.turn_right(current_speed)
                        elif joystick_x < 120:
                            motor_control.turn_left(current_speed)
                        else:
                            motor_control.stop()
                    
                else:
                    motor_control.stop() 
            else:
                response = f"Server received your message: {message}"
                await websocket.send(response)

    except websockets.ConnectionClosed:
        print(f"Connection with client {websocket.remote_address} closed")
        motor_control.stop()

    except Exception as e:
        print(f"Error: {e}")
        motor_control.stop()

    finally:
        set_angle(90)   
        # pwm.stop()
        # GPIO.cleanup()

async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8003)
    print("WebSocket server started at ws://0.0.0.0:8003")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
