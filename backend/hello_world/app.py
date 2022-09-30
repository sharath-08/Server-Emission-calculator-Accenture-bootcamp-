
import json
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig

cors_config = CORSConfig()
app = APIGatewayRestResolver(cors=cors_config)

def build_model(req,task_duration):
    import math
        # here we will implement the calculations
    # were waiting for sharath to send his algorithm plan

    # simple input validation. We cant have negatice requests or duration
    # input sanitation occurs during form uptake so we dont worry about it too much
    if req <= 0 or task_duration <= 0:
        print("must be positive")
        return -1

    # cores are calculated by Number of cores required = Requests Per Second (RPS) * task duration

    cores = req * task_duration

    # we need to calculate numbeer of processors. formula is processor = (number of cores / cores per processor)
    # 20 cores per processor

    processor = math.ceil(cores / 20)

    # need to get # of servers as wekk. Formular  is servers - processoors / proc per server
    # we use 2 per server
    servers = math.ceil(processor / 2)

    # get number of racks
    # assume 15 servers per rack
    racks = servers/15

    # rack volume (m^3) = number of racks * vol of one 42U rack
    rack_volume = racks * (2.10 * 0.7 * 0.9)
    # floor_area (m^2) = no. of racks * (2D area of one rack) * space multiplier
    floor_area = racks * (0.7*0.9) * 1.75

    # Multiply number of servers * avg power consumption per server
    # 𝐴𝑣𝑒𝑟𝑎𝑔𝑒 𝑃𝑜𝑤𝑒𝑟 𝐷𝑟𝑎𝑤 𝑝𝑒𝑟 𝑠𝑒𝑟𝑣𝑒𝑟(𝑊) = (𝑃𝑚𝑎𝑥 − 𝑃𝑖𝑑𝑙𝑒) × ( 𝑛 ) + 𝑃𝑖𝑑𝑙𝑒 where n is server utilization
    # converted to kwh
    # calculated prior. This is for on premise
    # multiply it by number of servers to get power rewuirements
    premise_power = servers * 4.944 * 1.69

    # get power cost of servers
    # using nsw average power cost at 28.54 c/kwh
    # cost is in cents
    cost = premise_power * 28.54

    # getttting emissions output
    emission = premise_power * 656.4

    # AWS energy savings = premise_power/2.5
    AWS_power = premise_power/2.5

    # emissions from aws
    AWS_emission = AWS_power * 656.4    

    #floor-space heat production (BTU)
    floor_space_heat = floor_area*20

    #Computer-heat generation: Total-Wattage * 1.5 (BTU). Estimated 400 wattage * number of servers
    Computer_heat = (400*servers) * 1.5

    #Lighting-heat production. AUS OSHA calls for 160 lux for large spaces. We assume use of fluorescent light bars
    Power_lights = (0.093*160*(floor_area/60))
    Power_heat = 4.25

    #Total cooling reqd. Takes into account server heat production, floor-space area and lighting in server room. 
    cooling_energy = ((Power_heat+Computer_heat+floor_space_heat)/3412)*24

    #cooling emissions: energy used by cooling (kWh) * gCO2/kWh
    cooling_emission = cooling_energy * 656.4

    #AWS cooling is on average 88% more efficient
    aws_cooling_energy = cooling_energy - (cooling_energy*0.84)
    aws_cooling_emission = aws_cooling_energy * 656.4

    ret = {
        "power": math.ceil(premise_power),
        "emissions": math.ceil(emission),
        "cost": math.ceil(cost),
        "aws_power": math.ceil(AWS_power),
        "aws_emission": math.ceil(AWS_emission),
        "aws_cost": math.ceil(AWS_power * 28.54),
        "difference": math.ceil(emission - AWS_emission),
        "floor_space" : math.ceil(floor_area),
        "server_numbers":servers,
        "rack_numbers":racks,
        "cooling_energy":math.ceil(cooling_energy),
        "cooling_emission":math.ceil(cooling_emission),
        "aws_cooling_energy":math.ceil(aws_cooling_energy),
        "aws_cooling_emission":math.ceil(aws_cooling_emission)
    }
    AWS_cost = AWS_power * 28.54
    difference = emission - AWS_emission

    return json.dumps(ret)

@app.post("/simulation")
def Simulate():

    body = app.current_event.json_body
    req = body.get("rps")
    task_duration = body.get("duration")
    # region = body.get("region")

    model = build_model(req,task_duration)
    model_values = json.loads(model)

    # if statuscode == []:
    return {
            "statusCode": 200,
            "body": {
                "server_number": model_values["server_numbers"],
                "power": model_values["power"],
                "cost": model_values["cost"],
                "aws_power": model_values["aws_power"],
                "aws_cost":model_values["aws_cost"],
                "emissions": model_values["emissions"],
                "aws_emission": model_values["aws_emission"],
                "difference": model_values["difference"],
                "cooling_energy":model_values["cooling_energy"],
                "cooling_emission":model_values["cooling_emission"],
                "aws_cooling_energy":model_values["aws_cooling_energy"],
                "aws_cooling_emission":model_values["aws_cooling_emission"]

            }
        }
    # else:
    #     return {
    #         "statusCode": 200,
    #         "body": {
    #             "isValid": False,
    #             "errors": [{
    #                 "error": str(e),
    #                 "validatorValue": str(e.validator_value),
    #                 "message": str(e.message),
    #                 "jsonPath": str(e.json_path),
    #                 "path": str(e.path.popleft()) if e.path else None
    #             }
    #             for e in errors
    #             ]
    #         } 
    #     }

def lambda_handler(event, context):
    return app.resolve(event, context)
