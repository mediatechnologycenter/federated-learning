from client_interface_helper import ClientInterface

server_port = '50050'
server_address = 'ip address of the host where you ran the client interface docker'
ClientInterfaceInstance = ClientInterface(server_address=server_address, server_port=server_port)

print(f"get_available_models returns a list of all available models and their meta data.")
models = ClientInterfaceInstance.get_available_models()

print(f"We pick one model and fetch it with get_model which returns the compiled keras model and its configuration.")
model_id = models[0]['_id']
model, config = ClientInterfaceInstance.get_model(model_id)

print(f"We tell the Node Worker to fetch the model, train it and return the loss:")
response = ClientInterfaceInstance.do_task("fetch_model", params={"model_id": model_id})
response = ClientInterfaceInstance.do_task("train_model", timeout=300)
response = ClientInterfaceInstance.do_task("send_loss", timeout=300)
