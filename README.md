# flask-tasks

## notes

```
# flask + 
python3 -m venv venv/flask_flask_openstack
source venv/flask_openstack/bin/activate
python3 -m pip install -U setuptools pip
python3 -m pip install flask flask-ipban python-openstackclient geoip2
```







## OpenStack
```
#https://docs.openstack.org/newton/user-guide/cli-nova-configure-access-security-for-instances.html
openstack security group rule list Rstudio
openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip 127.00.000.00/32
openstack security group rule show   490050ba-6576-4186-87b6-22ab5329c5d7
openstack security group rule delete 490050ba-6576-4186-87b6-22ab5329c5d7

nova list-secgroup NONMEM

```

## Example config files structure

flask-server-tasks.yaml
``` yaml
08447a4f-fe80-43da-a16c-e5a916c66fdb:
  comment: "Add single IP address to the the Rstudio security rule at region east-1"
  commands:
  - comm: "openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip ${ip}/32"
    env: SNIC_2020_20-??-east-1-openrc.sh
    python: OK
    response: "Your IP address: ${ip} is wite-listed for 24 hours on region east-1"
  pass: password
99783eb6-7dcd-4f3a-a4a1-8a44a7fb00e5:
  comment: "Add single IP address to the the Rstudio security rule at regions east-1 and C3SE"
  commands:
  - comm: "openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip ${ip}/32"
    env: SNIC_2020_20-??-east-1-openrc.sh
    python: OK
    response: "Your IP address: ${ip} is wite-listed for 24 hours on region east-1\n"
  - comm: "openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip ${ip}/32"
    env: SNIC_2020_20-??-C3SE-openrc.sh
    python: OK                                                                                                                                               
    response: "Your IP address: ${ip} is wite-listed for 24 hours on region C3SE\n"
  pass: password
ac08f7f9-cbed-42c7-9097-7135221e8318:
  comment: "Print witelisted IPs"
  commands:
  - comm: "openstack security group rule list --ingress Rstudio"
    env: SNIC_2020_20-??-east-1-openrc.sh
    python: OK
    response: "${stdout}"
  pass: password
```





monitor-tasks.yaml
``` yaml
SNIC_2020_20-17:
  ports:
  - '8787'
  regions:
  - east-1
  - C3SE
  rules:
  - Rstudio
```
