import datetime
from datetime import datetime
import requests
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
from .celery import app


@app.task
def generate_crm_report():
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
            query {
                allCustomers {
                    totalCount
                }
                allOrders {
                    totalCount
                }
                allOrders {
                    edges {
                        node {
                            totalAmount
                        }
                    }
                }
            }
        """)
        result = client.execute(query)
        
        total_customers = result["allCustomers"]["totalCount"]
        total_orders = result["allOrders"]["totalCount"]
        total_revenue = sum(edge["node"]["totalAmount"] for edge in result["allOrders"]["edges"])
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
        
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(report)
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"{timestamp} - Error generating CRM report: {str(e)}\n"
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(error_message)
