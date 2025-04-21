import keyboard
import pyautogui
import time
import re

# Name of the file containing the guitar tab
file_name = "Waltz2.txt"

# Sets the rough BPM of the song (not all that accurate), if the file has "BPM 500" in it
#  the BPM here will be over-written
BPM = 360

# Button locations, first coordinates for the first chord shape having the first 9 layers
# second coordinates is for the second chord shape having from 10 to 15
positions = [(94, 245), (145, 248)]

keys: list[str] = ['y', 't', 'r', 'e', 'w', 'q']


def main(file: str):
    tab_data = read_in_file(file)
    # for l in tab_data:
    #     print(l)

    time.sleep(3)
    print("Playing")
    play(tab_data, BPM)
    pass


def play(tab_data: list[list[int]], bpm: int):
    delay: float = 60 / bpm
    delay_time = 0.02
    shapes = 1
    pyautogui.click(*positions[0])
    play_count = min([len(tab_data[0]), len(tab_data[1]), len(tab_data[2]), len(tab_data[3]),
                      len(tab_data[4]), len(tab_data[5])])
    for i in range(play_count):
        if keyboard.is_pressed('esc'):
            print("Escape key pressed.")
            break
        # print(f"Measure {i}\r", end="")
        hold_delay = 0
        notes = []
        notes = [(tab_data[j][i], j) for j in range(6) if tab_data[j][i] != -1]
        notes.sort(reverse=shapes == 2)
        for note_pair in notes:
            note = note_pair[0]
            j = note_pair[1]
            if note >= 9 and shapes != 2:
                pyautogui.click(*positions[1], _pause=False)
                shapes = 2

            if note < 9 and shapes != 1:
                pyautogui.click(*positions[0], _pause=False)
                shapes = 1

            if shapes == 2:
                note -= 8
            else:
                note += 1

            keyboard.press(str(note))
            keyboard.press(keys[j])
            time.sleep(delay_time)
            hold_delay += delay_time
            keyboard.release(str(note))
            keyboard.release(keys[j])
            # print(f"{note} {keys[j]}")
            pass

        t_delay = delay - hold_delay
        if t_delay > 0:
            time.sleep(t_delay)
    pass


def parse_tab_line(line: str, capo: int, nulls: list[str]) -> list[int]:
    frets = []
    tokens = re.findall(r'[\d]+|[^0-9]', line)
    for token in tokens:
        if token in nulls:
            frets.append(-1)
        elif token.isdigit():
            fret = int(token) + capo
            frets.append(fret)
        else:
            frets.append(-1)
    return frets


def read_in_file(file_name: str) -> list[list[int]]:
    file = open(file_name, 'r')
    nulls = ['-', 'x', '/', '\\', 'p', 'h', 't', 'b', '=']
    line_start = ['e', 'B', 'G', 'D', 'A', 'E']
    output: list[list[int]] = [[], [], [], [], [], []]
    last_lines: list[str] = []
    line: str = ""
    capo: int = 0
    for line in file:
        line = line.strip()
        print(line)

        if len(line) == 0:
            continue

        if line.startswith('Capo'):
            capo = int(line.split(" ")[1])
            continue

        if line.startswith("BPM"):
            global BPM
            BPM = int(line.split(" ")[1])
            continue

        if line == "END":
            break

        start_line = line[0]

        if start_line in line_start:
            index = line_start.index(start_line)
            numbers: str = "".join(line.split("|")[1:])
            output[index].extend(parse_tab_line(numbers, capo, nulls))
            continue

        pass
    file.close()

    for L in output:
        for N in L:
            if N > 15:
                print(f"Note fret > 15 ({N})")
                exit(1)

    return output
    pass


if __name__ == "__main__":
    main(file_name)
    pass
