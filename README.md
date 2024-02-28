# sdn-mininet-backend

## get started
```c
python3 -m venv myenv
source myenv/bin/activate

install -r requirements.txt

python3 manage.py runserver 0.0.0.0:8000
```

## mininet test command
```
mn --switch ovs --controller ovsc --topo tree,depth=2,fanout=1 --test pingall
```

## GET command
```
http://ec2-3-21-206-55.us-east-2.compute.amazonaws.com:8000/mininet/depth_2/fanout_1/
```