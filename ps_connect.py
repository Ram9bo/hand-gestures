import time

def send_command(speed, angle, ssh, command):
    # start = time.time()
    command += f' --speed {speed} --angle {angle}'

    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        # print("second try: ", time.time()-start)
        # start = time.time()
        # print(stdout)
    except Exception as e:
        print("problem")
        # print(e.message)

    # err = ''.join(stderr.readlines())
    # out = ''.join(stdout.readlines())
    # final_output = str(out)+str(err)
    # print(final_output)




# forward_command = command + 'forward.py'
# backwards_command = command + 'backwards.py'
# left_backwards_command = command + 'left_backwards.py'
# right_backwards_command = command + 'right_backwards.py'
# left_forward_command = command + 'left_forward.py'
# right_forward_command = command + 'right_forward.py'
# left_in_place_command = command + 'left_in_place.py'
# right_in_place_command = command + 'right_in_place.py'
# stop_command = command + 'stop.py'

