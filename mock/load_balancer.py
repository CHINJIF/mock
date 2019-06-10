
from threading import Thread
from mutex import mutex
# data = (seq, data)

class Service(object):
    
    def __init__(self, address, name):
        self.address = address
        self.name = name


class ServiceManager(object):

    def __init__(self):
        self.backends = []
        self.lock = mutex()

    def register_services(self, name, addresses):
        self.backends = addresses

    def register_backend(self, address):
        if address not in self.backends:
            with self.lock.lock():
                self.backends.append(address)

    def remove_backend(self, address):
        if address in self.backends:
            with self.lock.lock():
                del self.backends[self.backends.index(address)]

    def get_backend_addr(self, req_addr):
        seq = hash(req_addr)

        backend_num = seq % len(self.backends)
        return self.backends[backend_num]


def serve(service_manager):
    # listen to a port for incoming requests, and forward it to service manager
    port_number = 8080
    while True:
        request = get_request(port_number)
        return service.manager.get_backend_addr(
            request.get_address())



class HealthCheck(object):

    def __init__(self, service_manager):
        # can we retrieve backends from service_manager?
        # are master, slaves still needed?

        self.service_manager = service_manager


    def send_heartbeat(self):
        # one thread solution for now
        for service in self.service_manager.backends:
            resp = requests.get(service.address)

            if resp.status_code != 200:
                # slave offline
                self.service_manager.remove_backend(service.address)
        
        time.sleep(60)

if __name__ == "__main__":
    manager = ServiceManager()

    address_pool = [
        ("127.0.0.1", 5001),
        ("127.0.0.1", 5002)
        ("127.0.0.1", 5003)
    ]

    manager.register_services(address_pool)

    # get_backend_addr and remove_backend can happen concurrently
    # where should we put the mutex to protect backend list?
    # with backend list？
    health_checker = HealthCheck(manager)
    t_health_check = Thread(target=health_checker.send_heartbeat)
    t_health_check.start()

    serve(manager)

    # something like this ...
    # looks good.
    # will check more on mutex .. call it a day?
    # take a look at GSLB, it's very similiar to this.
    # cool， checking！thanks for the mock！！
    # Oyasumi nasai lol night
