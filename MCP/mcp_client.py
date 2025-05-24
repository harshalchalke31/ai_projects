class MCPClient:
    def __init__(self, server, client_id):
        self.server = server
        self.client_id = client_id

    def send_query(self, query):
        result = self.server.receive_query(self.client_id, query)
        print("Response:")
        print(result)
        return result

    def save_result(self):
        response = self.server.save_output(self.client_id)
        print(response)
        return response
