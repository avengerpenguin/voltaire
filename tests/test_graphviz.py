from textwrap import dedent

from xmldiff import main

from voltaire import graphviz


def test_generate_image():
    dot = """
    digraph g {
        A -> B;
    }
    """
    svg = graphviz.generate_image(dot)
    expected = dedent(
        """\
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
         "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <!-- Title: g Pages: 1 -->
        <svg width="62pt" height="116pt"
         viewBox="0.00 0.00 62.00 116.00" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 112)">
        <title>g</title>
        <polygon fill="white" stroke="transparent" points="-4,4 -4,-112 58,-112 58,4 -4,4"/>
        <!-- A -->
        <g id="node1" class="node">
        <title>A</title>
        <ellipse fill="none" stroke="black" cx="27" cy="-90" rx="27" ry="18"/>
        <text text-anchor="middle" x="27" y="-86.3" font-family="Times,serif" font-size="14.00">A</text>
        </g>
        <!-- B -->
        <g id="node2" class="node">
        <title>B</title>
        <ellipse fill="none" stroke="black" cx="27" cy="-18" rx="27" ry="18"/>
        <text text-anchor="middle" x="27" y="-14.3" font-family="Times,serif" font-size="14.00">B</text>
        </g>
        <!-- A&#45;&gt;B -->
        <g id="edge1" class="edge">
        <title>A&#45;&gt;B</title>
        <path fill="none" stroke="black" d="M27,-71.7C27,-63.98 27,-54.71 27,-46.11"/>
        <polygon fill="black" stroke="black" points="30.5,-46.1 27,-36.1 23.5,-46.1 30.5,-46.1"/>
        </g>
        </g>
        </svg>
    """
    )
    print(svg)
    diff = main.diff_texts(svg.encode("utf8"), expected.encode("utf8"))
    assert diff == []
