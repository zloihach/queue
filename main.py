import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
import math

class ProducerConsumerGUI:
    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.producer_active = False
        self.consumer_active = False
        self.circles = []
        self.circle_ids = {}

        self.root.title("Producer Consumer Simulation")
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas = tk.Canvas(self.frame, height=300, width=300)
        self.canvas.grid(column=0, row=2, columnspan=4, pady=10)

        self.start_producer_button = ttk.Button(self.frame, text="Start Producer", command=self.start_producer)
        self.start_producer_button.grid(column=0, row=0, sticky=tk.W)

        self.stop_producer_button = ttk.Button(self.frame, text="Stop Producer", command=self.stop_producer)
        self.stop_producer_button.grid(column=1, row=0, sticky=tk.W)

        self.start_consumer_button = ttk.Button(self.frame, text="Start Consumer", command=self.start_consumer)
        self.start_consumer_button.grid(column=2, row=0, sticky=tk.W)

        self.stop_consumer_button = ttk.Button(self.frame, text="Stop Consumer", command=self.stop_consumer)
        self.stop_consumer_button.grid(column=3, row=0, sticky=tk.W)

        self.status_label = ttk.Label(self.frame, text="Queue Size: 0")
        self.status_label.grid(column=0, row=1, columnspan=4)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def start_producer(self):
        self.producer_active = True
        threading.Thread(target=self.producer).start()

    def stop_producer(self):
        self.producer_active = False

    def start_consumer(self):
        self.consumer_active = True
        threading.Thread(target=self.consumer).start()

    def stop_consumer(self):
        self.consumer_active = False

    def producer(self):
        while self.producer_active:
            time.sleep(1)
            self.queue.put("Product")
            self.root.after(0, self.add_circle)

    def consumer(self):
        while self.consumer_active:
            time.sleep(2)
            if not self.queue.empty():
                product = self.queue.get()
                self.root.after(0, lambda p=product: self.consume_circle(p))

    def add_circle(self):
        num_circles = len(self.circles)
        radius = 100
        center_x, center_y = 150, 150
        angle = (2 * math.pi / 20) * num_circles  # Distribute circles evenly on the circle path
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        circle_id = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
        self.circles.append(circle_id)
        self.circle_ids[circle_id] = "Product"
        self.update_status_label()

    def consume_circle(self, product):
        if self.circles:
            circle_id = self.circles.pop(0)
            self.canvas.itemconfig(circle_id, fill="green")
        self.update_status_label()

    def update_status_label(self):
        size = self.queue.qsize()
        self.status_label.config(text=f"Queue Size: {size}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProducerConsumerGUI(root)
    root.mainloop()
