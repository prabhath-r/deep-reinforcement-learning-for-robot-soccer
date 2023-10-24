import functions
from functions import render_it

for i in range(10):
    score, s_list = render_it()
    print(f"Episode {i} has the score of: {score}")