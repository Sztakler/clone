import os

def read_last_lines(file_path: str, num_lines: int = 50) -> list[str]:
    """Efficiently read the last `num_lines` lines of a file."""
    with open(file_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        position = f.tell()
        buffer = bytearray()
        lines_found = 0

        while position >= 0 and lines_found <= num_lines:
            f.seek(position)
            byte = f.read(1)
            if byte == b"\n":
                lines_found += 1
            buffer.extend(byte)
            position -= 1

        # reverse the buffer to get the correct line order
        buffer.reverse()
        return buffer.decode("utf-8", errors="replace").splitlines()[-num_lines:]

