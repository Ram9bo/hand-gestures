from ps_connect import send_command


hostname = "192.168.101.252"
username = 'pi'
password = 'raspberry'
dir_path = '/home/pi/picar-4wd/final_project/control.py'
command = 'python3 ' + dir_path
send_command(-5, -5, hostname, username, password, command)