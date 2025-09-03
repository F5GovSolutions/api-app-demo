import requests
import json
from datetime import date


class GraphQLClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.graphql_url = f"{base_url}/graphql"

    def execute_query(self, query, variables=None):
        """Execute a GraphQL query or mutation"""
        payload = {"query": query, "variables": variables or {}}

        response = requests.post(
            self.graphql_url, json=payload, headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status {response.status_code}")
            print(response.text)
            return None

    def get_all_inventory(self):
        """Get all inventory items"""
        query = """
        query {
          inventoryItems {
            id
            name
            ipAddress
            location
            state
            deviceType
            make
            model
            osVersion
            endOfSupport
          }
        }
        """
        return self.execute_query(query)

    def get_inventory_by_id(self, item_id):
        """Get a specific inventory item by ID"""
        query = """
        query GetInventoryItem($id: UUID!) {
          inventoryItem(id: $id) {
            id
            name
            ipAddress
            location
            state
            deviceType
            make
            model
            osVersion
            endOfSupport
          }
        }
        """
        variables = {"id": str(item_id)}
        return self.execute_query(query, variables)

    def get_inventory_by_location(self, location):
        """Get inventory items by location"""
        query = """
        query GetInventoryByLocation($location: String!) {
          inventoryByLocation(location: $location) {
            id
            name
            ipAddress
            state
            deviceType
            make
            model
          }
        }
        """
        variables = {"location": location}
        return self.execute_query(query, variables)

    def create_inventory_item(self, **kwargs):
        """Create a new inventory item"""
        mutation = """
        mutation CreateInventoryItem($inventory: InventoryInput!) {
          createInventoryItem(inventory: $inventory) {
            id
            name
            ipAddress
            location
            state
            deviceType
            make
            model
            osVersion
            endOfSupport
          }
        }
        """

        # Convert end_of_support date to string if provided
        if "endOfSupport" in kwargs and isinstance(kwargs["endOfSupport"], date):
            kwargs["endOfSupport"] = kwargs["endOfSupport"].isoformat()

        variables = {"inventory": kwargs}
        return self.execute_query(mutation, variables)

    def update_inventory_item(self, item_id, **kwargs):
        """Update an inventory item"""
        mutation = """
        mutation UpdateInventoryItem($inventory: InventoryUpdateInput!) {
          updateInventoryItem(inventory: $inventory) {
            id
            name
            ipAddress
            location
            state
            deviceType
            make
            model
            osVersion
            endOfSupport
          }
        }
        """

        # Convert end_of_support date to string if provided
        if "endOfSupport" in kwargs and isinstance(kwargs["endOfSupport"], date):
            kwargs["endOfSupport"] = kwargs["endOfSupport"].isoformat()

        kwargs["id"] = str(item_id)
        variables = {"inventory": kwargs}
        return self.execute_query(mutation, variables)

    def delete_inventory_item(self, item_id):
        """Delete an inventory item"""
        mutation = """
        mutation DeleteInventoryItem($id: UUID!) {
          deleteInventoryItem(id: $id)
        }
        """
        variables = {"id": str(item_id)}
        return self.execute_query(mutation, variables)


def main():
    """Example usage of the GraphQL client"""
    client = GraphQLClient()

    print("=== GraphQL Inventory API Test ===\n")

    # Test 1: Get all inventory items
    print("1. Getting all inventory items...")
    result = client.get_all_inventory()
    if result and "data" in result:
        items = result["data"]["inventoryItems"]
        print(f"Found {len(items)} inventory items")
        for item in items[:3]:  # Show first 3 items
            print(f"  - {item['name']}: {item['ipAddress']} ({item['state']})")
    else:
        print("No items found or error occurred")
    print()

    # Test 2: Create a new item
    print("2. Creating new inventory item...")
    new_item_data = {
        "name": "test-server.example.com",
        "ipAddress": "192.168.1.200",  # Changed from ip_address to ipAddress
        "location": "Test Lab",
        "state": "ONLINE",
        "deviceType": "Server",  # Changed from device_type to deviceType
        "make": "HP",
        "model": "ProLiant DL380",
        "osVersion": "Windows Server 2022",  # Changed from os_version to osVersion
        "endOfSupport": "2025-12-31",  # Changed from end_of_support to endOfSupport
    }

    result = client.create_inventory_item(**new_item_data)
    print(f"GraphQL Response: {json.dumps(result, indent=2)}")  # Debug output

    if result and "data" in result and result["data"]["createInventoryItem"]:
        created_item = result["data"]["createInventoryItem"]
        print(f"Created item: {created_item['name']} with ID: {created_item['id']}")

        # Test 3: Update the created item
        print("3. Updating the created item...")
        update_result = client.update_inventory_item(
            created_item["id"],
            state="OFFLINE",
            osVersion="Windows Server 2022 Updated",
            endOfSupport="2026-06-30",  # Add date update
        )
        print(
            f"Update GraphQL Response: {json.dumps(update_result, indent=2)}"
        )  # Debug output

        if (
            update_result
            and "data" in update_result
            and update_result["data"]["updateInventoryItem"]
        ):
            updated_item = update_result["data"]["updateInventoryItem"]
            print(f"Updated item state to: {updated_item['state']}")
        else:
            print("Failed to update item")
            if update_result and "errors" in update_result:
                print(f"Update Errors: {json.dumps(update_result['errors'], indent=2)}")

        # Test 4: Delete the created item (only if update succeeded)
        if (
            update_result
            and "data" in update_result
            and update_result["data"]["updateInventoryItem"]
        ):
            print("4. Deleting the created item...")
            delete_result = client.delete_inventory_item(created_item["id"])
            print(
                f"Delete GraphQL Response: {json.dumps(delete_result, indent=2)}"
            )  # Debug output

            if (
                delete_result
                and "data" in delete_result
                and delete_result["data"]["deleteInventoryItem"]
            ):
                print("Item deleted successfully")
            else:
                print("Failed to delete item")
                if delete_result and "errors" in delete_result:
                    print(
                        f"Delete Errors: {json.dumps(delete_result['errors'], indent=2)}"
                    )
        else:
            print("4. Skipping delete test due to update failure")
    else:
        print("Failed to create item")
        if result:
            if "errors" in result:
                print(f"GraphQL Errors: {json.dumps(result['errors'], indent=2)}")
            if "data" in result:
                print(f"Data returned: {result['data']}")
        else:
            print("No response received")

    # Test 5: Query by location
    print("5. Getting items by location...")
    location_result = client.get_inventory_by_location("Virginia DC1")
    if location_result and "data" in location_result:
        items = location_result["data"]["inventoryByLocation"]
        print(f"Found {len(items)} items in Virginia DC1")
        for item in items:
            print(f"  - {item['name']}: {item['make']} {item['model']}")


if __name__ == "__main__":
    main()
