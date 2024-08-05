import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.paused_time = 0
        self.is_paused = False

    def start(self):
        self.start_time = time.time()
        self.paused_time = 0
        self.is_paused = False

    def pause(self):
        if not self.is_paused:
            self.paused_time = time.time() - self.start_time
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            self.start_time = time.time() - self.paused_time
            self.paused_time = 0
            self.is_paused = False

    def elapsed_time(self):
        if self.is_paused:
            return self.paused_time
        else:
            return time.time() - self.start_time

# Create and start the timer
timer = Timer()
timer.start()

# Simulate your game update loop
while True:
    elapsed = timer.elapsed_time()
    print(f"Elapsed Time: {elapsed:.2f} seconds")

    # Simulate some game condition to pause/resume the timer
    if elapsed > 2 and not timer.is_paused:
        print("Pausing timer...")
        timer.pause()
    elif elapsed > 4 and timer.is_paused:
        print("Resuming timer...")
        timer.resume()

    time.sleep(0.1)  # Sleep to simulate frame time
