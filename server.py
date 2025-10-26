import zmq
import json
from const import PORT

def server():  
  db_list = [] 
    
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://127.0.0.1:" + PORT)
  
  print(f"Server (ZMQ) listening on port {PORT}")

  try:
    while True:
      message = socket.recv_string()
      print(f"\nReceived request: {message}")

      try:
        data = json.loads(message)
        command = data.get("comando")
        
        reply_data = {"status": "OK"}

        if command == "APPEND":
          val = data.get("valor")
          db_list.append(val)
          reply_data["lista"] = db_list

        elif command == "REMOVE":
          val = data.get("valor")
          if val in db_list:
            db_list.remove(val)
            reply_data["lista"] = db_list
          else:
            reply_data = {"status": "ERROR", "message": "Valor não encontrado"}

        elif command == "SEARCH":
          val = data.get("valor")
          reply_data["encontrado"] = (val in db_list)

        elif command == "INSERT":
          idx = data.get("indice")
          val = data.get("valor")
          try:
            db_list.insert(idx, val)
            reply_data["lista"] = db_list
          except IndexError:
            reply_data = {"status": "ERROR", "message": "Índice inválido"}

        elif command == "SORT":
          db_list.sort()
          reply_data["lista"] = db_list

        elif command == "VALUE":
          reply_data["lista"] = db_list

        elif command == "STOP":
          print("Comando STOP recebido. Encerrando.")
          reply_data["message"] = "Servidor encerrando."
          socket.send_string(json.dumps(reply_data))
          break
        
        else:
          reply_data = {"status": "ERROR", "message": "Comando desconhecido"}

        reply_string = json.dumps(reply_data)
        socket.send_string(reply_string)
        print(f"Replied: {reply_string}")

      except (json.JSONDecodeError, TypeError, AttributeError):
        print("Erro: Mensagem inválida ou não-JSON recebida.")
        reply = {"status": "ERROR", "message": "Requisição inválida (não-JSON)."}
        socket.send_string(json.dumps(reply))

  except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")
  finally:
    socket.close()
    context.term()
    print("Server terminated.")

if __name__ == "__main__":
  server()