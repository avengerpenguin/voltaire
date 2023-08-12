from xmldiff import main

from voltaire import graphviz


def test_generate_image():
    dot = """
    digraph g {
        A -> B;
    }
    """
    svg = graphviz.generate_image(dot)
    assert "DOCTYPE" not in svg
    expected = '<svg xmlns="http://www.w3.org/2000/svg" width="62pt" height="116pt" viewBox="0 0 62 116"><g class="graph" transform="translate(4 112)"><path fill="#fff" stroke="transparent" d="M-4 4v-116h62V4H-4z"/><g class="node"><ellipse cx="27" cy="-90" fill="none" stroke="#000" rx="27" ry="18"/><text x="27" y="-86.3" font-family="Times,serif" font-size="14" text-anchor="middle">A</text></g><g class="node"><ellipse cx="27" cy="-18" fill="none" stroke="#000" rx="27" ry="18"/><text x="27" y="-14.3" font-family="Times,serif" font-size="14" text-anchor="middle">B</text></g><g class="edge"><path fill="none" stroke="#000" d="M27-71.7v25.59"/><path stroke="#000" d="m30.5-46.1-3.5 10-3.5-10h7z"/></g></g></svg>'
    print(svg)
    diff = main.diff_texts(svg.encode("utf8"), expected.encode("utf8"))
    assert diff == []
