import os
import re
import tempfile
from subprocess import PIPE
from subprocess import Popen
from typing import Iterable
from typing import List
from typing import Text

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

MERMAID_START = re.compile(r"^```[\ \t]*[Mm]ermaid[\ \t]*$")
MERMAID_END = re.compile(r"^```[\ \t]*$")
CONF_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "mermaid.json"
)


def generate_image(mermaid_code: str) -> str:
    """
    Converts Mermaid source code to SVG.
    :param mermaid_code: Mermaid input code as a string.
    :return: SVG code as a string.
    """
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(mermaid_code.encode("utf8"))
    tf.flush()

    name = tf.name + ".svg"
    cmdline = [
        "mmdc",
        "-i",
        tf.name,
        "-o",
        name,
        "-c",
        CONF_FILE,
    ]

    try:
        p = Popen(cmdline, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
    except Exception as exc:
        raise Exception("Failed to run mermaid: %s" % exc)
    else:
        if p.returncode == 0:
            os.remove(tf.name)
            with open(name) as f:
                svg_string = f.read()
            os.remove(name)
            return svg_string
        else:
            raise RuntimeError(
                f"Error calling mermaid: {str(err)}\nTemp files: {tf.name} and {name}"
            )


class MermaidProcessor(Preprocessor):
    def run(self, lines: List[str]) -> Iterable[str]:
        looking_for_mermaids = True
        mermaid_code = ""

        for line in lines:
            # Ad hoc state machine to the rescue! (We only have two states:
            # either we're waiting for a potential Mermaid block or we're in
            # the middle of processing one).
            if looking_for_mermaids:
                if MERMAID_START.match(line):
                    # Caught a Mermaid! Switch state so the other other state
                    # can start slurping the Mermaid code.
                    looking_for_mermaids = False
                    continue
                else:
                    # No mermaids sighted yet. Leave alone what's not ours
                    # to touch.
                    yield line
            else:
                if MERMAID_END.match(line):
                    # Finished gobbling code. Convert to SVG, yield the SVG code
                    # instead of the Mermaid source we've been gobbling.
                    yield generate_image(mermaid_code)
                    # Reset the Mermaid code buffer and start looking for
                    # more mermaids in the same document...
                    mermaid_code = ""
                    looking_for_mermaids = True
                    continue
                else:
                    # Slurp up that Mermaid code and gobble[1] the lines so they
                    # get removed from the source Markdown.
                    # [1] i.e. don't yield the lines
                    mermaid_code += line + "\n"
                    continue


class MermaidExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(MermaidProcessor(), "mermaid", 35)
        md.registerExtension(self)


def makeExtension(**kwargs):  # pragma: no cover
    os.system(
        "which mmdc 2>/dev/null || npm install -g @mermaid-js/mermaid-cli"
    )
    return MermaidExtension(**kwargs)
