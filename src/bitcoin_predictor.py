import datetime
import numpy as np
import yfinance as yf
import dimod
from dwave.system import LeapHybridSampler

# Define the start and end dates
start_date = datetime.datetime(2010, 1, 1)
end_date = datetime.datetime.now()

df = yf.download('BTC-USD', start=start_date, end=end_date)
returns = df['Close'].pct_change().dropna().tolist()


# Define the optimization problem as a QUBO dictionary
def bitcoin_price_prediction_qubo(returns, window_size, future_window_size):
    qubo = {}
    n_variables = len(returns) - window_size - future_window_size

    # Define the variables and the linear coefficients
    for i in range(n_variables):
        for j in range(window_size):
            qubo[('x' + str(i * window_size + j), 'x' + str(i * window_size + j))] = -1

    # Define the quadratic coefficients
    for i in range(n_variables):
        for j in range(window_size):
            for k in range(window_size):
                if j != k:
                    qubo[('x' + str(i * window_size + j), 'x' + str(i * window_size + k))] = 2 * returns[i + j] * \
                                                                                             returns[i + k] / (
                                                                                                         window_size - 1)

    # Define the constraints
    for i in range(n_variables):
        for j in range(window_size):
            qubo[('x' + str(i * window_size + j), 'x' + str(i * window_size + j))] += 1

    return qubo


# Define the returns, window size, and future window size
window_size = 10
future_window_size = 5

# Convert the optimization problem to a binary quadratic model
qubo = bitcoin_price_prediction_qubo(returns, window_size, future_window_size)
bqm = dimod.as_bqm(qubo, dimod.BINARY)

# Run the quantum annealing sampler
sampler = LeapHybridSampler(token='YOUR-DWAVE-API-KEY')
sampleset = sampler.sample(bqm, time_limit=300)

# Print the results
sample = sampleset.first.sample
energy = sampleset.first.energy
prediction = sum(sample['x' + str(i)] * np.array(returns[i + window_size:i + window_size + future_window_size]) for i in
                 range(len(returns) - window_size - future_window_size)) / future_window_size
print("Sample:", sample)
print("Energy:", energy)
print("Predicted Future Price:", prediction)
