  
import socket
import sprint4_getData
import sprint4_sort

PORT = 5000
HOST = 'localhost'

# gets the data once to improve performance
data = sprint4_getData.getData()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  # the microserver location that all other services will connect to
  s.bind((HOST, PORT))
  # enable a server to accept connections
  s.listen(5)
  flag = 1
  while flag: # run the server until told to disconnect.
    client_socket = None
    try:
      (client_socket, addr) = s.accept()
      with client_socket: 
        
        # CLEANING
        '''
        Converts the rcvd byte string to a list of params for the 
        existing life gen getDat and sorting functions.
        Removes all unneeded quotes and spaces, cleaning the 
        command line request data sent by the client to the server
        '''
        client_req_raw = client_socket.recv(4096)
        req = list(client_req_raw.decode('ASCII').split(','))

        req[0] = req[0][1:]
        req[len(req) - 1] = req[len(req)-1][:-1]
        for i in range(len(req)):
          req[i] = req[i].replace("'","")
          req[i] = req[i].replace(" ","")
        # END CLEANING 

        print("Params requested by client: ", req)

        if not req:
          flag = 0 

        '''
        Reason for DONE is the SIGINT is not working with either
        ctrl + c     or ctrl + break
        on windows.
        '''
        if "['DONE']" == str(req):
            print("client initiated DC")
            flag = 0

        # Retrieve the data requested by the client
        sorting = sprint4_sort
        uniqId = sorting.byUniqId(req, data)
        numReviews = sorting.byNumOfReviews(req, data)
        avgRating = sorting.byAvgRevRating(req, data)

        # works for all sorting methods needed
        #res_data = uniqId 
        #res_data = numReviews 
        res_data = avgRating

        res = bytes(str(res_data), encoding="utf-8")
 
        client_socket.sendall(res)

      client_socket.close()
    # i think ctrl + c will work on anything other than windows
    except KeyboardInterrupt:
      if client_socket:
        client_socket.close()
      break

  print('client disconnected')