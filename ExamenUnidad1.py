import os, sys
urls = []

def gevent():
    import gevent.monkey
    from urllib2 import urlopen
    gevent.monkey.patch_all()
    agregar = input("Cuantos trabajos habra en la pila?: ")
    print("")
    for i in range(agregar):
        elem = raw_input("Cual es el url del trabajo {0}: ".format(i+1))
        urls.append(elem)

    def print_head(url):
        print('Starting {}'.format(url))
        data = urlopen(url).read()
        print('{}: {} bytes: {}'.format(url, len(data), data))

    jobs = [gevent.spawn(print_head, _url) for _url in urls]
    gevent.wait(jobs)
    sys.exit()
        
def callback():
    import tornado.ioloop
    from tornado.httpclient import AsyncHTTPClient
    agregar = input("Cuantos trabajos habra en la pila?: ")
    print("")
    for i in range(agregar):
        elem = raw_input("Cual es el url del trabajo {0}: ".format(i+1))
        urls.append(elem)
        
    def handle_response(response):
        if response.error:
            print("error", response.error)
        else:
            url = response.request.url
            data = response.body
            print('{}: {} bytes: {}'.format(url, len(data), data))

    http_client = AsyncHTTPClient()
    for url in urls:
        http_client.fetch(url, handle_response)
       
    tornado.ioloop.IOLoop.instance().start()
    sys.exit()

def menu():
    os.system('clear')
    print("--------Menu--------")
    print("")
    print("\t 1- green thread")
    print("\t 2- callback")
    print("")

while True:   
    menu()
    opcionMenu = raw_input("ingrese una opcion: ")
    try:
        ({'1': gevent, '2': callback}[opcionMenu])()
    except KeyError:
        menu()