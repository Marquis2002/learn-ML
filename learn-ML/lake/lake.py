from tqdm import tqdm
import time

for episode in tqdm(range(100)):
    time.sleep(0.01*episode)
    pass