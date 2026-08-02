import re
from dataclasses import dataclass

DISCLAIMER = (
    "This is general information, not legal advice or an official eligibility "
    "determination. Only the Maryland Department of Human Services can determine "
    "your eligibility. Please verify with the official sources linked above."
)

_PATTERNS = [
    (re.compile(r"\byou qualify\b", re.I), "you may be eligible"),
    (re.compile(r"\byou are eligible\b", re.I), "you may be eligible"),
    (re.compile(r"\byou don't qualify\b", re.I), "you may not be eligible"),
    (re.compile(r"\byou do not qualify\b", re.I), "you may not be eligible"),
    (re.compile(r"\byou are not eligible\b", re.I), "you may not be eligible"),
]

def soften_determinations(text: str) -> str:
    """
    Rewrite definitive eligibility language ("you qualify", "you are eligible")
    into non-binding language ("you may be eligible"), so the AI never appears
    to make an official determination.
    """
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text



@dataclass
class GuardrailResult:
    text: str
    blocked: bool


def enforce(draft: str, citations: list[dict]) -> GuardrailResult:
    """
    Final safety gate before an answer reaches the user.

    No citations -> block entirely and point the user to the real DHS
    contact info instead. We never let an answer through unsupported.
    Otherwise -> soften any definitive eligibility language and append
    the required disclaimer.
    """
     
    if not citations:
        return GuardrailResult(
            text=(
                "I don't have an official source that covers that, so I can't "
                "answer it reliably. You can check directly with the Maryland "
                "Department of Human Services at https://dhs.maryland.gov/ or "
                "call 1-800-332-6347."
            ),
            blocked=True,
        )

    softened = soften_determinations(draft)
    final_text = f"{softened.rstrip()}\n\n---\n{DISCLAIMER}"
    return GuardrailResult(text=final_text, blocked=False)
