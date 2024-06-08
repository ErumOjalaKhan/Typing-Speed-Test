import time
import keyboard
import os
import sys

def clear_screen():
    """Clears the terminal screen."""
    if os.name == 'posix':  # Unix/Linux/MacOS
        _ = os.system('clear')
    elif os.name == 'nt':  # Windows
        _ = os.system('cls')
    else:
        print("Unsupported operating system. Cannot clear screen.")
        sys.exit(1)

def display_text_with_colors(reference_text, typed_text):
    """Displays the reference text with typed characters color-coded."""
    colored_text = ""
    for i, char in enumerate(reference_text):
        if i < len(typed_text):
            if char == typed_text[i]:
                # colored_text += colored(char, 'white', 'green', attrs=['reverse'])
                colored_text += f"\033[42m{char}\033[0m"  # Green background
            else:
                # colored_text += colored(char, 'white', 'red', attrs=['reverse'])
                colored_text += f"\033[41m{char}\033[0m"  # Red background
        else:
            colored_text += char

    # Print all lines, clearing previous content and ensuring cursor is at the start
    sys.stdout.write("\033[0;0H")  # Move cursor to top-left corner
    print("\r" + colored_text, end="")

def typing_speed_test(reference_text):
    """Runs the typing speed test with the provided reference text."""
    clear_screen()
    print("Type the displayed text as quickly and accurately as possible:")
    input("Press Enter when you're ready to start... ('esc' to abort)")
    clear_screen()
    print(reference_text)

    start_time = time.time()
    typed_text = ""

    test_aborted = False
    
    while len(typed_text) < len(reference_text):
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':  # Exit on Esc key
                print("\n\nTest aborted.")
                test_aborted = True
                break
            elif len(event.name) == 1 or event.name == "space":  # Only process single character keys, and space key
                if event.name == "space":
                    typed_text += " "
                    # display_text_with_colors(reference_text, typed_text)
                else:
                    typed_text += event.name
                display_text_with_colors(reference_text, typed_text)
        

    end_time = time.time()
    time_taken = end_time - start_time

    # Calculate typing speed (words per minute)
    words_typed = len(typed_text.split())
    words_per_minute = (words_typed / time_taken) * 60

    # Calculate accuracy
    correct_chars = sum(1 for i in range(min(len(typed_text), len(reference_text))) if typed_text[i] == reference_text[i])
    accuracy = (correct_chars / len(typed_text)) * 100

    if not test_aborted:
        print("\n\nTest complete!")
    print(f"Time taken: {time_taken:.2f} seconds")
    print(f"Typing speed: {words_per_minute:.2f} words per minute")
    print(f"Accuracy: {accuracy:.2f}%")

def read_text_from_file(filename):
    """Reads and returns the text from a file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

if __name__ == "__main__":
    reference_text = read_text_from_file('typing_text.txt')
    typing_speed_test(reference_text)

