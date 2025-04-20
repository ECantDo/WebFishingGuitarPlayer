import keyboard
import time

file_name = "WetHands.txt"
keys: list[str] = ['y', 't', 'r', 'e', 'w', 'q']


def main(file: str):
    tab_data = read_in_file(file)
    # for l in tab_data:
    #     print(l)

    time.sleep(3)
    print("Playing")
    play(tab_data, 350)
    pass


def play(tab_data: list[list[int]], bpm: int):
    delay: float = 60 / bpm
    for i in range(len(tab_data[0])):
        # print(f"Measure {i}\r", end="")
        hold_delay = 0
        for j in range(6):
            note: int = tab_data[j][i]
            if note == -1:
                continue
            note += 1
            keyboard.press(str(note))
            keyboard.press(keys[j])
            time.sleep(0.05)
            hold_delay += 0.05
            keyboard.release(str(note))
            keyboard.release(keys[j])
            # print(f"{note} {keys[j]}")
            pass

        t_delay = delay - hold_delay
        if t_delay > 0:
            time.sleep(t_delay)
    pass


def read_in_file(file_name: str) -> list[list[int]]:
    file = open(file_name, 'r')
    nulls = ['-', 'x', '/', '\\', 'p', 'h']
    output: list[list[int]] = [[], [], [], [], [], []]
    last_lines: list[str] = []
    line: str = ""
    capo: int = 0
    for line in file:
        line = line.strip()
        print(line)

        if line.startswith('Capo'):
            capo = int(line.split(" ")[1])
            continue

        if line == "END":
            break

        if line.startswith('e'):
            last_lines = []
            numbers: str = "".join(line.split("|")[1:])
            last_lines.append(numbers)
            for c in numbers:
                if c in nulls:
                    output[0].append(-1)
                else:
                    output[0].append(int(c) + capo)
            continue

        if line.startswith('B'):
            numbers: str = "".join(line.split("|")[1:])
            last_lines.append(numbers)
            for c in numbers:
                if c in nulls:
                    output[1].append(-1)
                else:
                    output[1].append(int(c) + capo)
            continue

        if line.startswith('G'):
            numbers: str = "".join(line.split("|")[1:])
            last_lines.append(numbers)
            for c in numbers:
                if c in nulls:
                    output[2].append(-1)
                else:
                    output[2].append(int(c) + capo)
            continue

        if line.startswith('D'):
            numbers: str = "".join(line.split("|")[1:])
            last_lines.append(numbers)
            for c in numbers:
                if c in nulls:
                    output[3].append(-1)
                else:
                    output[3].append(int(c) + capo)
            continue

        if line.startswith('A'):
            numbers: str = "".join(line.split("|")[1:])
            last_lines.append(numbers)
            for c in numbers:
                if c in nulls:
                    output[4].append(-1)
                else:
                    output[4].append(int(c) + capo)
            continue

        if line.startswith('E'):
            numbers: str = "".join(line.split("|")[1:])
            last_lines.append(numbers)
            for c in numbers:
                if c in nulls:
                    output[5].append(-1)
                else:
                    output[5].append(int(c) + capo)
            continue

        pass
    file.close()

    for L in output:
        for N in L:
            if N > 9:
                print("Note fret > 9")
                exit(1)

    return output
    pass


if __name__ == "__main__":
    main(file_name)
