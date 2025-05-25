def chunk_text(text, max_len=1000):
    lines = text.split('\n')
    chunks = []
    current = []
    current_len = 0

    for line in lines:
        if current_len + len(line) + 1 > max_len:
            if current:
                chunks.append('\n'.join(current))
                current = []
                current_len = 0
        current.append(line)
        current_len += len(line) + 1

    if current:
        chunks.append('\n'.join(current))
    return chunks
