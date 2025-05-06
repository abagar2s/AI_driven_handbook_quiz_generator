import re

def clean_text(text: str) -> str:
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)  # replace multiple spaces/newlines with one space
    text = text.replace("•", "-")     # normalize bullet points
    text = re.sub(r"\n+", "\n", text) # collapse multiple newlines to one
    
    # Remove extra spaces around lines
    lines = [line.strip() for line in text.splitlines()]
    
    # Remove empty lines and very short lines (like page numbers or headers)
    lines = [line for line in lines if len(line) > 10]

    return "\n".join(lines)
