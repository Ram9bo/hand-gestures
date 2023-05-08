import paramiko

hostname = "192.168.36.47"
username = 'pi'
password = 'raspberry'
dir_path = 'picar-x/final_project/'
command = 'python3 ' + dir_path

forward_command = command + 'forward.py'
backwards_command = command + 'backwards.py'
left_backwards_command = command + 'left_backwards.py'
right_backwards_command = command + 'right_backwards.py'
left_forward_command = command + 'left_forward.py'
right_forward_command = command + 'right_forward.py'
left_in_place_command = command + 'left_in_place.py'
right_in_place_command = command + 'right_in_place.py'
stop_command = command + 'stop.py'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname,username=username,password=password)
    print("Connected to %s" % hostname)
except paramiko.AuthenticationException:
    print("Failed to connect to %s due to wrong username/password" %hostname)
    exit(1)
except Exception as e:
    print(e.message)    
    exit(2)

move_command = left_forward_command
try:
    stdin, stdout, stderr = ssh.exec_command(move_command)
    print(stdout)
except Exception as e:
    print(e.message)

err = ''.join(stderr.readlines())
out = ''.join(stdout.readlines())
final_output = str(out)+str(err)
print(final_output)