Push unresolved issues count to telegraf

Example telegrafd input config:
```
# Generic socket listener capable of handling multiple socket types.
[[inputs.socket_listener]]
  ## URL to listen on
  service_address = "udp://127.0.0.1:8094"
```
