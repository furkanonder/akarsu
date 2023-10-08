import argparse
import io
from collections import Counter

from akarsu.akarsu import Akarsu


def main() -> None:
    parser = argparse.ArgumentParser(
        description="New Generation Profiler based on PEP 669"
    )
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    parser.add_argument("-f", "--file", type=str, help="Path to the file")
    args = parser.parse_args()

    if file := args.file:
        with io.open(file) as fp:
            source = fp.read()
        events = Akarsu(source, args.file).profile()
        counter: Counter = Counter()

        print(f"{'Count':>10}{'Event Type':^20}{'Filename(function)':<50}")
        for event, count in Counter(events).most_common():
            event_type, file_name, func_name = event
            counter[event_type] += 1
            print(f"{count:>10}{event_type:^20}{f'{file_name}({func_name})':<50}")

        print(f"\nTotal number of events: {counter.total()}")
        for event_type, count in counter.most_common():
            print(f"  {event_type} = {count}")


if __name__ == "__main__":
    main()
