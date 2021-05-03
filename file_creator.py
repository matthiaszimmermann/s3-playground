import os
import sys

CMD_LINE_ARGS = "file-to-create [line-size lines]"

LINE_SIZE = 512
LINES = 10000

def _parse_command_line():
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("usage: {cmd} {args} {len}".format(cmd=sys.argv[0], args=CMD_LINE_ARGS, len=len(sys.argv)))
        sys.exit(1)
    else:
        file_name = sys.argv[1]

    if len(sys.argv) == 4:
        (line_size, lines) = (int(sys.argv[2]), int(sys.argv[3]))
    else:
        (line_size, lines) = (LINE_SIZE, LINES)

    return (file_name, line_size, lines)

def main():
    (file_name, line_size, lines) = _parse_command_line()

    with open(file_name, 'w') as f:
        for i in range(lines):
            f.write(os.urandom(line_size).hex())
            f.write('\n')

if __name__ == "__main__":
    main()
