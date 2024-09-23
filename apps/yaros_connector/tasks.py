from background_task import background

@background(schedule=5)  # Задача будет запускаться каждую минуту
def demo_task(message):
    print(f"Task running: {message}")