# Manual solution — no AI assistance.


def parse_mark(raw: str):
    text = raw.strip()
    if text == "":
        return None
    try:
        value = float(text)
    except ValueError:
        return None
  
    if value != value or value in (float("inf"), float("-inf")):
        return None
  
    if value != int(value):
        return None
    mark = int(value)
    if 0 <= mark <= 100:
        return mark
    return None


def read_marks():
    print("Enter marks one per line. Press Enter on an empty line to finish.")
    marks = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip() == "":
            break
        mark = parse_mark(line)
        if mark is not None:
            marks.append(mark)
    return marks


def compute_stats(marks):
    if not marks:
        print("No valid marks found. Nothing to compute.")
        return

    count = len(marks)
    average = sum(marks) / count
    highest = max(marks)
    lowest = min(marks)
    passing = 0
    for m in marks:
        if m >= 50:
            passing += 1
    pass_rate = passing / count * 100

    print(f"Valid marks : {count}")
    print(f"Average     : {average:.2f}")
    print(f"Highest     : {highest}")
    print(f"Lowest      : {lowest}")
    print(f"Pass rate   : {pass_rate:.1f}%")


def main():
    marks = read_marks()
    compute_stats(marks)


if __name__ == "__main__":
    main()