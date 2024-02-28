# sdn-mininet-backend

## activate env
```c
python3 -m venv myenv
source myenv/bin/activate
```

## mininet test command
```
mn --switch ovs --controller ovsc --topo tree,depth=2,fanout=1 --test pingall
```