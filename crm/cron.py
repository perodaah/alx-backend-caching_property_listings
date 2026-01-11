import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)
    
    # Optionally, query the GraphQL hello field to verify the endpoint is responsive
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
            query {
                hello
            }
        """)
        result = client.execute(query)
        # If no errors, it's responsive
    except Exception as e:
        error_message = f"{timestamp} Error querying GraphQL: {str(e)}\n"
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(error_message)


def update_low_stock():
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    updatedProducts {
                        name
                        stock
                    }
                    message
                }
            }
        """)
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]
        
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for product in updated_products:
                log_entry = f"{timestamp} Product: {product['name']}, New Stock: {product['stock']}\n"
                f.write(log_entry)
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        error_message = f"{timestamp} Error updating low stock: {str(e)}\n"
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(error_message)
