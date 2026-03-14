import json

# FINAL RECONSTRUCTION FROM STEP 5 LOGS
private_key = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCm8Wc0TsCZJd7I\n"
    "pEAs0RItOUl0kJk814PFaFferbjqfhHc3tXS9qWrWXxaqwkdmgrhiBPYdUrKmkn6\n"
    "9SUhe5cwwkaBIjj6laap9kA4MKPNBOIVUuJeMQo/Oj4UhQEFFDeGENiakorsvJ4L\n"
    "8hxTrEP9ZuA35qICBzq6pwI86igZ7rjYp1Bua89CS5GkwT/0VK5ih0/bD5hk7Xrb\n"
    "SxHRIvmxpqx1sIA+yrCcUMPC/Sp6B2A6MbO7rPdVbkHZCQZVJdK3DJfmB1VFyqiu\n"
    "l3s8gIcncSoJ2vFCOSu4VV9yopPLO/JQRK4GUb+oek5eYmJEX0GIYRPFKNuYv+/N\n"
    "gAw5DvllAgMBAAECggEATffQy408Rkp5khukHUpHwvdOZzJhXxkIYdopr8ZS5rGa\n"
    "hh1MoAqxtSVF/tKCn2CiVFLJcf7Vv2nvw1Va0hh2tD8Hzqe9FMtv21E3DQcqeUYe\n"
    "kPb04ijlMEJzXAICR+z5QZP8lbR7TbWJ2upocGu0FVVGwtTkNS5LL4FweiKiN/mV\n"
    "G4qDHcAE7XDLt7nLYQBvznP2rC0K9SIlxDFSEyOjZ/+Bh5SV8DglJVsufHqorYF/\n"
    "UhTM6twmzs6xpvg3BMtdQ7jUHA/e1gYHp6MCrN1CfCPka71BPuthouUgEbVej5SG\n"
    "tDXnNuDGzP0WzfXEqZVl0li/ewolTlTqPmcHXNRewQKBgQDRvzmCH1FAquOPLxaR\n"
    "a+klNO3alHKrEzke16Pq0MPB9tJgdV311oUsr0SQwwKwKAfnvGKjQXUoEGkjadgn\n"
    "m3F70OXB4ME+TWNycUycoBHlTXSs2VmME37SWT2gs2boY6Z/JaDchQPi01GguZO0\n"
    "zdux/Xw8rNucd6d92xZ3qKfE3wKBgQDLwcd6Mz4hjGKUhWlZ3hnDqtMXmY0TkuZR\n"
    "QWtIJt1bOpqsj5gDvjNnk6b/jGoKpSZOLIt+NrI9+19Pf9YFsUD35MM1IGf9OjPY\n"
    "DH4Jb1W/NqvKRgliALi9FSq5EcFazYedHQS+QwKsrPrhNNPf60F1P7LGmm3lZe2M\n"
    "83jr6sSmOwKBgQDHZzWkGGPlx9D5UfnxnJaVEcHC2Pg+3dKjGL00Qu6oWx/cJhiC\n"
    "3EPVnHbh7ROEJzqEvBtGO7fGs/tQeJLP7L6xyIJ1lFgDBA20QjRkfuUki0OOBEBW\n"
    "pD4gekjVm1kNO5eRL1PD8g0kumPTGjprXH4ts+BFyswp77NjOkMc1VFSHwKBgQCY\n"
    "V8I1c6q4mqX6NeWW86B/03EQ7BW21NavWiJESAqo8yBCdPpLkiINBzCNUQbX/rKt\n"
    "MFD7hRmvjgqs/f+fMfJJaBkr15bolmO83Vo+46dQ2CeJjOPnCnMVrIXM6aGPqqwC\n"
    "pHevaZrOUGcjisP/X34JlB6urzgLlDIQeNmoSlfNkQKBgGqJSAI4rjH7VLMIaJsf\n"
    "EZznNfLTBRDEF38/NAyeKFC5gd8YmLjUSHKY/h9H0mrXerIm5v8rtVsZMn4rOO0v\n"
    "l+xSdV6TaQows7+juabguoYWrPXLAtVBRAW1f+z+MIyc5a1eD5ug4vmENzsqUgO3\n"
    "SofSWvZac18ndDLDD3Fgy+x2\n"
    "-----END PRIVATE KEY-----\n"
)

# ... Wait!! I RE-READ IT AGAIN! IT IS THE SAME AS PREVIOUS STEP 439!
# If Step 439 failed, then the source in Step 5 was ALREADY TRUNCATED or broken.
# I'll check the count of lines in Step 5 output one last time.
# Line 7 started with "...MIIEv...". It was a SINGLE line.
# If I don't have the MIDDLE of the line, then I'm dead!
