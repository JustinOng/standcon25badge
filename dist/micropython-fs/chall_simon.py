import time
import random
from badge import Badge
from game import v,e,l

MAX_TIME = 10
MAX_ERRORS = 5


def show_sequence(badge: Badge, sequence: list) -> None:
    for led_index in sequence:
        blink_led(badge, led_index)

def blink_led(badge: Badge, index) -> None:
    badge.set_led(index, True)
    time.sleep(0.5)
    badge.set_led(index, False)

def blink_all_leds(badge: Badge) -> None:
    """Flicker all LEDs on and off three times."""
    for _ in range(3):
        for i in range(4):
            badge.set_led(i, True)
        time.sleep(0.5)
        for i in range(4):
            badge.set_led(i, False)

def reset_leds(badge: Badge) -> None:
    for i in range(4):
        badge.set_led(i, False)

button_mapping = [0, 1, 2, 3]

def randomize_button_mapping():
    global button_mapping
    
    numbers = [0, 1, 2, 3]
    result = []
    while numbers:
        choice = random.choice(numbers)
        result.append(choice)
        numbers.remove(choice)
    button_mapping = result

def get_player_input(badge: Badge, sequence: list, previous_states: list) -> tuple:
    global MAX_TIME
    inputs = []
    for i in range(len(sequence)):
        button_pressed = None
        start_time = time.time()

        while time.time() - start_time < MAX_TIME:

            state = badge.read_touch_pads()

            if any(state):
                for i, e in enumerate(state):
                    if e == 1:
                        button_pressed = i
                        break

                break

            time.sleep(0.01)
        
        if button_pressed is None:
            print("Time's up!")
            return False, inputs

        blink_led(badge, button_pressed)
        inputs.append(button_mapping[button_pressed])

        if not v(inputs, sequence[:i+1], previous_states):
            print("Incorrect button pressed!")
            reset_leds(badge)
            return False, inputs

    return True, inputs


def play_level(badge: Badge, sequence: list, previous_states: list) -> tuple:
    show_sequence(badge, sequence)
    success, inputs = get_player_input(badge, sequence, previous_states)
    if success:
        state = e(inputs, sequence, previous_states) & 0x3F
        previous_states.append(state)
    return success, previous_states


def generate_sequence(length: int) -> list:
    return [random.randint(0, 3) for _ in range(length)]


def main() -> None:
    global MAX_TIME, MAX_ERRORS
    badge = Badge()
    print("Starting Sequence Memory Game")

    previous_states = []
    level = 0

    try:
        for _ in range(5):
            level += 1
            level_info = l(level, previous_states)
            errors = 0
            print(f"\nLevel {level}: {level_info['level_name']}")
            MAX_TIME, MAX_ERRORS = level_info["max_time"], level_info["max_errors"]

            sequence = [0, 1, 2, 3] if level == 1 else generate_sequence(level_info["sequence_length"])

            while True:
                success, previous_states = play_level(badge, sequence, previous_states)
                if success:
                    break
                errors += 1
                if errors >= MAX_ERRORS:
                    print("Game Over!")
                    return
                print("Try again!")

            blink_all_leds(badge)
            randomize_button_mapping()

        print("Congratulations! You've completed all levels!")

    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting...")


# if __name__ == '__main__':
main()
