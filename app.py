"""
calculate the emission amount for on premise and cloud

Create a function that takes as an input the amount of requests (either per day or year or second) and retruns a tuple of
the co2 output of each.
furhter improvements may be creating and returning graphs based on calculation

In order to run the code, type "python app.py" into the terminal


"""
import math

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

    print(processor)

    # need to get # of servers as wekk. Formular  is servers - processoors / proc per server
    # we use 2 per server
    servers = math.ceil(processor / 2)

    print(servers)

    # Multiply number of servers * avg power consumption per server
    # 𝐴𝑣𝑒𝑟𝑎𝑔𝑒 𝑃𝑜𝑤𝑒𝑟 𝐷𝑟𝑎𝑤 𝑝𝑒𝑟 𝑠𝑒𝑟𝑣𝑒𝑟(𝑊) = (𝑃𝑚𝑎𝑥 − 𝑃𝑖𝑑𝑙𝑒) × ( 𝑛 ) + 𝑃𝑖𝑑𝑙𝑒 where n is server utilization
    # converted to kwh
    # calculated prior. This is for on premise
    # multiply it by number of servers to get power rewuirements
    premise_power = servers * 4.944 * 1.69

    # getttting emissions output
    emission = premise_power * 656.4

    return emission


# main function will call the calculate function while we do the testing
def main():
    # prints the output from calculate on to the rermical
    print(calculate(100, 5), "per gram")
    pass


if __name__ == "__main__":
    main()
