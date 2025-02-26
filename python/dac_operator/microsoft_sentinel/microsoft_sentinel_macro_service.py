import re


class MicrosoftSentinelMacroService:
    def __init__(self):
        self.macro_pattern = r"`\$\{([a-zA-Z-0-9]+)\}`"

    def get_used_macros(self, query: str) -> list[str]:
        return re.findall(self.macro_pattern, query)

    def replace_macro(self, text: str, macro_name: str, replacement: str):
        return re.sub(rf"`\$\{{{macro_name}\}}`", replacement, text)
