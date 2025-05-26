async def chunk_text(text, min_words=100, max_words=1000, max_len=1000):
    lines = text.split('\n')
    chunks = []
    current = []
    current_len = 0
    current_words = 0

    for line in lines:
        line_words = len(line.split())
        if current_words + line_words > max_words or current_len + len(line) + 1 > max_len:
            if current and current_words >= min_words:
                chunks.append('\n'.join(current))
                current = []
                current_len = 0
                current_words = 0
        current.append(line)
        current_len += len(line) + 1
        current_words += line_words

    if current and current_words >= min_words:
        chunks.append('\n'.join(current))
    elif current:
        if chunks:
            chunks[-1] += '\n' + '\n'.join(current)
        else:
            chunks.append('\n'.join(current))
    return chunks