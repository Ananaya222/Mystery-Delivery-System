import json
import math


def calculate_distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance


with open("base_case.json", "r") as file:
    data = json.load(file)


warehouses = {}

for warehouse in data["warehouses"]:

    warehouse_id = warehouse["id"]
    warehouse_location = warehouse["location"]

    warehouses[warehouse_id] = warehouse_location


agents = {}

for agent in data["agents"]:

    agent_id = agent["id"]
    agent_location = agent["location"]

    agents[agent_id] = agent_location


packages = data["packages"]


report = {}

for agent_id in agents:

    report[agent_id] = {
        "packages_delivered": 0,
        "total_distance": 0
    }


for package in packages:

    warehouse_id = package["warehouse_id"]

    warehouse_location = warehouses[warehouse_id]

    destination = package["destination"]

    nearest_agent = None

    minimum_distance = float("inf")


    for agent_id, agent_location in agents.items():

        distance_to_warehouse = calculate_distance(
            agent_location,
            warehouse_location
        )

        if distance_to_warehouse < minimum_distance:

            minimum_distance = distance_to_warehouse

            nearest_agent = agent_id


    warehouse_to_destination = calculate_distance(
        warehouse_location,
        destination
    )


    total_trip_distance = (
        minimum_distance +
        warehouse_to_destination
    )


    report[nearest_agent]["packages_delivered"] += 1


    report[nearest_agent]["total_distance"] = round(
        report[nearest_agent]["total_distance"] +
        total_trip_distance,
        2
    )


for agent_id in report:

    delivered_packages = report[agent_id]["packages_delivered"]

    total_distance = report[agent_id]["total_distance"]


    if delivered_packages > 0:

        efficiency = total_distance / delivered_packages

    else:

        efficiency = 0


    report[agent_id]["efficiency"] = round(
        efficiency,
        2
    )


best_agent = None

best_efficiency = float("inf")


for agent_id in report:

    delivered_packages = report[agent_id]["packages_delivered"]

    efficiency = report[agent_id]["efficiency"]


    if delivered_packages > 0:

        if efficiency < best_efficiency:

            best_efficiency = efficiency

            best_agent = agent_id


report["best_agent"] = best_agent


with open("report.json", "w") as file:

    json.dump(report, file, indent=4)


print("Report Generated Successfully")

print(json.dumps(report, indent=4))
