#!/usr/bin/env python3
from flask import Flask, make_response, request, send_from_directory, abort
from flask_ipban import IpBan
from string import Template
import os, time 
import subprocess
import importlib
import shlex
import yaml

ip_ban = IpBan()
app = Flask(__name__)
ip_ban.init_app(app)
# ufw allow 6768/tcp


@app.route("/task/<taskid>", methods=["GET"])
def run_task(taskid):
  T= time.strftime("%Y-%m-%dT%H:%M:%S")
  ip= request.remote_addr
  print(request.user_agent)

  if taskid in TASKS.keys():
    print("OK")
    response_tmp=""

    for i in range(len(TASKS[taskid]['commands'])):

      if 'env' in TASKS[taskid]['commands'][i]:
        source_env(TASKS[taskid]['commands'][i]['env'])

      if 'python' in TASKS[taskid]['commands'][i]:
        penv= importlib.import_module(TASKS[taskid]['commands'][i]['python'])

      cmd_txt= TASKS[taskid]['commands'][i]['comm'] ;
      cmd_txt= Template(cmd_txt).substitute(ip=ip)
      cmd=shlex.split(cmd_txt)
      print(">>> cmd: " + cmd_txt)
      proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = proc.communicate()
      print(stdout.decode())
      print(stderr.decode())

      with open("flask-server.log", 'a') as fo:
        fo.write(str(time.time()) + ip + " " + taskid + " "+ T+"\n")
      fo.close()
      
      response_tmp= response_tmp + Template(TASKS[taskid]['commands'][i]['response']).substitute(ip=ip, stdout=stdout.decode(), stderr=stderr.decode)

    response= make_response(response_tmp, 200)
  else:
    print("Wrong")
    response= make_response('Wrong', 404)
    abort(404)

  response.mimetype = "text/plain"
  return response

# =============================================================================================================

def source_env(filename):
  cmd_txt=f'env -i bash -c "source {filename} && env"' ; cmd=shlex.split(cmd_txt)
  print(">>> env: "+cmd_txt)
  proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for line in proc.stdout:
    (key, _, value) = line.decode().partition("=")
    os.environ[key] = value.rstrip()
  proc.communicate()

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
  return True

# =============================================================================================================

if __name__ == '__main__':

  with open('flask-server-tasks.yaml','r') as f:     
    TASKS=yaml.load(f, yaml.FullLoader)    

  app.run(host="0.0.0.0", port=5000, debug=True)
