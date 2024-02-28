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

## set up screen
```
sudo apt-get install screen  # Debian/Ubuntu

screen # Start a new screen session

python3 manage.py runserver 0.0.0.0:8000

// Detach from the screen session by pressing Ctrl-A then D

screen -r # You can reattach to the session later with
```

## return JSON format looks like
``` json
{
    "depth": 3,
    "fanout": 1,
    "structured_output": {
        "network_setup": {
            "controllers": [],
            "hosts": [
                "h1"
            ],
            "switches": [
                "s1",
                "s2",
                "s3"
            ],
            "links": [
                "(s1, s2)",
                "(s2, s3)",
                "(s3, h1)"
            ]
        },
        "execution_details": {
            "ping_test": "h1 ->",
            "warnings": [
                "No packets sent"
            ],
            "performance": "5.672 seconds"
        }
    }
}
