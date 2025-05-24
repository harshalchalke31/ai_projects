class MCPServer:
    def __init__(self, host):
        self.host = host
        self.context = {}  # Isolated per client

    def receive_query(self, client_id, query):
        print(f"[MCPServer] Received from {client_id}: {query}")
        result = self.host.run_agent_query(query)
        self.context[client_id] = {"query": query, "result": result}
        return result

    def save_output(self, client_id):
        data = self.context.get(client_id, {}).get("result")
        if not data or "error" in data:
            return f"Cannot save: Invalid or errored response for client '{client_id}'"
        return self.host.run_tool("SaveToDocx", data.json())
