import zmq
import json # Importe a biblioteca JSON
from const import PORT
from time import sleep

def send_request(socket, request_dict):
  request_string = json.dumps(request_dict)
  print(f"Sending: {request_string}")
  
  socket.send_string(request_string)
  
  reply_string = socket.recv_string()
  reply_data = json.loads(reply_string)
  
  print(f"Received: {reply_data}")
  sleep(0.1)
  return reply_data


def client():
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  
  socket.connect("tcp://127.0.0.1:" + PORT)
  print("Client (ZMQ) connected...")
  
  print("-" * 20)
  print("--- Teste de VALUE (lista vazia) ---")
  send_request(socket, {"comando": "VALUE"})
  
  print("\n--- Teste de APPEND (20, 5, 10) ---")
  send_request(socket, {"comando": "APPEND", "valor": 20})
  send_request(socket, {"comando": "APPEND", "valor": 5})
  send_request(socket, {"comando": "APPEND", "valor": 10})
  
  print("\n--- Teste de SEARCH (procurando 5) ---")
  send_request(socket, {"comando": "SEARCH", "valor": 5})

  print("\n--- Teste de SEARCH (procurando 99) ---")
  send_request(socket, {"comando": "SEARCH", "valor": 99})
  
  print("\n--- Teste de SORT ---")
  send_request(socket, {"comando": "SORT"})

  print("\n--- Teste de REMOVE (removendo 10) ---")
  send_request(socket, {"comando": "REMOVE", "valor": 10})

  print("\n--- Teste de REMOVE (removendo 99) ---")
  send_request(socket, {"comando": "REMOVE", "valor": 99})

  print("\n--- Teste de INSERT (99 na posição 0) ---")
  send_request(socket, {"comando": "INSERT", "indice": 0, "valor": 99})
  
  print("\n--- Teste de STOP ---")
  send_request(socket, {"comando": "STOP"})
  
  print("-" * 20)
  
  socket.close()
  context.term()
  print("Client terminated.")

if __name__ == "__main__":
  client()