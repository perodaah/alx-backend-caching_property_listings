#!/usr/bin/env python3
import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

def send_order_reminders():
    # Calculate dates: last 7 days
    now = datetime.datetime.now()
    seven_days_ago = now - datetime.timedelta(days=7)
    
    # Format dates for GraphQL (ISO format)
    start_date = seven_days_ago.strftime("%Y-%m-%dT%H:%M:%S")
    end_date = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    # GraphQL query
    query = gql("""
        query GetRecentOrders($start: DateTime!, $end: DateTime!) {
            allOrders(filter: {orderDateGte: $start, orderDateLte: $end}) {
                edges {
                    node {
                        id
                        customer {
                            email
                        }
                    }
                }
            }
        }
    """)
    
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Execute query with variables
        result = client.execute(query, variable_values={"start": start_date, "end": end_date})
        
        # Log reminders
        timestamp = now.strftime("%d/%m/%Y-%H:%M:%S")
        with open("/tmp/order_reminders_log.txt", "a") as f:
            for edge in result["allOrders"]["edges"]:
                order = edge["node"]
                order_id = order["id"]
                customer_email = order["customer"]["email"]
                log_entry = f"{timestamp} Order ID: {order_id}, Customer Email: {customer_email}\n"
                f.write(log_entry)
        
        print("Order reminders processed!")
    
    except Exception as e:
        print(f"Error processing order reminders: {str(e)}")

if __name__ == "__main__":
    send_order_reminders()