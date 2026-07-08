import os
import paramiko

HOST = os.environ["EC2_HOST"]
USERNAME = os.environ["EC2_USERNAME"]
PRIVATE_KEY = os.environ["PRIVATE_KEY"]

with open("key.pem", "w") as f:
    f.write(PRIVATE_KEY)

os.chmod("key.pem", 0o600)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(
    hostname=HOST,
    username=USERNAME,
    key_filename="key.pem"
)

command = """
cd /home/ec2-user/aws-python-deployment-demo &&
git pull &&
python3 app.py
"""

stdin, stdout, stderr = client.exec_command(command)

print(stdout.read().decode())
print(stderr.read().decode())

client.close()

print("Deployment Completed")