import re
from typing import List

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from sh import dot

DOT_START = re.compile(r"^```[\ \t]*dot[\ \t]*$")
DOT_END = re.compile(r"^```[\ \t]*$")


def generate_image(dot_code: str) -> str:
    """
    Converts Graphiz source code to SVG.
    :param dot_code: Dot input code as a string.
    :return: SVG code as a string.
    """

    return str(dot("-Tsvg", _in=dot_code))


class GraphvizProcessor(Preprocessor):
    def run(self, lines: List[str]) -> List[str]:
        def gen():
            looking_for_dots = True
            dot_code = ""

            for line in lines:
                if looking_for_dots:
                    if DOT_START.match(line):
                        looking_for_dots = False
                        continue
                    else:
                        yield line
                else:
                    if DOT_END.match(line):
                        yield generate_image(dot_code)
                        dot_code = ""
                        looking_for_dots = True
                        continue
                    else:
                        dot_code += line + "\n"
                        continue

        return list(gen())


class GraphvizExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(GraphvizProcessor(), "graphviz", 35)
        md.registerExtension(self)


def makeExtension(**kwargs):  # pragma: no cover
    return GraphvizExtension(**kwargs)
