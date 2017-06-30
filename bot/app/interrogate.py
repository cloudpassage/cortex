from halocelery import tasks
import donlib
import sys
import time
config = donlib.ConfigHelper()
print("OCTO-BOX CLI access.\nFirst time here?  Try \"help\"")
while True:
    request = raw_input("What do you need? ")
    if request in ["quit", "q", "exit"]:
        sys.exit(1)
    query = {"text": request}
    halo = donlib.Halo(config, "health", tasks)
    msg_type, target = donlib.Lexicals.parse(query)
    result = halo.interrogate(msg_type, target)
    if isinstance(result, (str, unicode)):
        output = result
    else:
        while result.status == "PENDING":
            print "Please wait a moment"
            time.sleep(2)
            output = result.get()
    if output == "":
        print "Resource not found"
    else:
        print output
