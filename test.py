import logging

def truncate_text(text: str, max_length: int, max_lines: int) -> str:
    lines = text.split('\n')
    if len(lines) > max_lines:
        text = '\n'.join(lines[:max_lines]) + '...'
        lines = text.split('\n')
    for i, line in enumerate(lines):
        if len(line) > max_length:
            lines[i] = line[:max_length-3] + '...'
    return '\n'.join(lines)
