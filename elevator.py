UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.destination_floor = None
        self.callbacks = None
        self.call_dict = {UP: [], DOWN: []}

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """

        if self.is_idle(): # Base case
            self.destination_floor = floor
            self.callbacks.motor_direction = UP if floor >= self.callbacks.current_floor else DOWN
        elif self.is_on_path(floor, direction):
            self.call_dict[self.callbacks.motor_direction].append(self.destination_floor)
            self.destination_floor = floor
        else:
            self.call_dict[direction].append(floor)

    def is_on_path(self, floor, direction):
        if self.callbacks.motor_direction == direction:
            return self.destination_floor > floor if direction == UP else self.destination_floor < floor
        return False

    def is_idle(self):
        return all([True if not self.call_dict[key] else False for key in self.call_dict]) and \
               not self.destination_floor and not self.callbacks.motor_direction

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        pass

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        if self.destination_floor == self.callbacks.current_floor:
            self.callbacks.motor_direction = None

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        if self.destination_floor > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
        elif self.destination_floor < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN


class TestElevator:

    def setup(self):
        class EmptyCallback:
            def __init__(self, direction=None, current_floor=None):
                self.motor_direction = direction
                self.current_floor = current_floor
        self.empty_callback = EmptyCallback()
        self.callback = EmptyCallback(direction=UP)

    def test_is_idle(self):
        elevator_logic = ElevatorLogic()
        elevator_logic.callbacks = self.empty_callback
        assert elevator_logic.is_idle() # Should be idle
        elevator_logic.callbacks = self.callback
        assert not elevator_logic.is_idle() # Should not be idle

    def test_is_on_path(self):
        elevator_logic = ElevatorLogic()
        elevator_logic.callbacks = self.callback
        elevator_logic.destination_floor = 5
        assert elevator_logic.is_on_path(4, UP) # Should be on path
        assert not elevator_logic.is_on_path(4, DOWN) # Should not be on path
        elevator_logic.callbacks.current_floor = 5
        assert not elevator_logic.is_on_path(5, UP) # Should not be on path
