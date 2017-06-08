# timeout_subprocess
## 使Python2的subprocess能够设置timeout

## API
* check_call()
* checkout_output()
* call()
* popen()

## usage
``` python
# 正常情况
print check_call("pwd; sleep 3; pwd;", shell=True)
print check_call("pwd; sleep 3; pwd;", shell=True, timeout=4)
# 超时情况，抛出异常
print check_call("pwd; sleep 3; pwd;", shell=True, timeout=2)
```
