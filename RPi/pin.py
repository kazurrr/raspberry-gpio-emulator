OUT = 0
IN = 1

PUD_OFF = 20
PUD_UP = 21
PUD_DOWN = 22

RISING = 31
FALLING = 32
BOTH = 33


class Pin:
    def __init__(self, channel, mode):
        # type: (int, int, int) -> None
        self.channel = channel
        self.mode = mode  # OUT/IN
        self.is_on = False
        self.pull_up_down = PUD_OFF  # PUD_OFF/PUD_UP/PUD_DOWN
        self.__event = []  # detected events (RISING/FALLING) queue
        self.__keep_event = False  # If it is true then PIN keep the event to __event queue.
        self.__event_callbacks = {RISING: [], FALLING: []}  # They are called when push_event() is called.
        self.__event_detected = False  # If it is true then callbacks are called.

    def has_event(self):
        # type: () -> bool
        return len(self.__event) > 0

    def pop_event(self):
        # type: () -> int
        return self.__event.pop(0)

    def push_event(self, event):
        # type: (int) -> None
        self.__call_event_callbacks(event)
        if self.__keep_event:
            self.__event.append(event)

    def start_monitor(self):
        # type: () -> None
        self.__keep_event = True

    def stop_monitor(self):
        # type: () -> None
        self.__keep_event = False
        self.__event.clear()

    def add_event_detect(self, event, callback):
        # type: (int) -> None
        if event == BOTH:
            self.__event_callbacks[RISING].append(callback)
            self.__event_callbacks[FALLING].append(callback)
        else:
            self.__event_callbacks[event].append(callback)

    def remove_event_detect(self):
        # type: () -> None
        self.__event_callbacks[RISING].clear()
        self.__event_callbacks[FALLING].clear()
        self.__event_detected = False

    def __call_event_callbacks(self, event):
        # type: (int) -> None
        for callback in self.__event_callbacks[event]:
            self.__event_detected = True
            if callback is not None:
                callback(self.channel)

    def event_detected(self):
        # type: () -> bool
        return self.__event_detected