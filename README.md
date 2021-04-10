# TruStar Challenge

### Reflection on the technical spec:
In particular, I'd say that a better approach would be to receive an array containing
each step of the property chain so I would just do something like:
```
path = ['path', 'to', 'my', 'array', 0]
for key in path:
    data = data[key]
```
and the code would be much simpler, at the expense of some tinkering on client
code probably :)

So, changing this in the spec the new call to the function would look like:
```
Path: https://github.com/mitre/cti/enterprise-attack/attack-pattern
Fields: [
    ["id"],
    ["objects", 0, 'name'],
    ["objects", 0, "kill_chain_phases"]
]
```
