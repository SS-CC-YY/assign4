import socket
from population_generator import PopulationGenerator

if __name__ == '__main__':
    PORT = 5000
    host = 'localhost'
    test_data = ['one', 'two']
    population = PopulationGenerator()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, PORT))
    s.listen(5)
    while True:
        (client_socket, addr) = s.accept()
        with client_socket:
            print('addr:', addr)
            content = str(client_socket.recv(2048), 'utf-8')
            print('content:', content)
            a_list = content.split(',')
            if len(a_list) >= 2:
                value = population.getValue(a_list[0], a_list[1])
                print(value)
                client_socket.send(','.join([a_list[0], a_list[1], value]).encode('utf-8'))
        client_socket.close()

    s.close()

