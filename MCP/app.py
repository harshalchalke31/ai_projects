from mcp_host import MCPHost
from mcp_server import MCPServer
from mcp_client import MCPClient

if __name__ == "__main__":
    host = MCPHost()
    server = MCPServer(host)
    client = MCPClient(server, client_id="user123")

    query = input("Enter your research question:\n> ")
    response = client.send_query(query)

    should_save = input("Do you want to save this to a .docx file? (y/n): ")
    if should_save.strip().lower() == 'y':
        client.save_result()
