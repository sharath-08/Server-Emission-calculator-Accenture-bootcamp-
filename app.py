"""
calculate the emission amount for on premise and cloud

Create a function that takes as an input the amount of requests (either per day or year or second) and retruns a tuple of
the co2 output of each.
furhter improvements may be creating and returning graphs based on calculation

In order to run the code, type "python app.py" into the terminal


"""
import math
import json

# req is requests per second, task duration is per request in miliseconds


def calculate(req, task_duration):
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

    ret = {
        "power": premise_power,
        "emissions": emission,
        "cost": cost,
        "aws_power": AWS_power,
        "aws_emission": AWS_emission,
        "aws_cost": AWS_power * 28.54,
        "difference": emission - AWS_emission
    }

    return json.dumps(ret)

# main function will call the calculate function while we do the testing


def main():
    # prints the output from calculate on to the rermical
    print(calculate(10000, 5))

    pass


if __name__ == "__main__":
    main()
