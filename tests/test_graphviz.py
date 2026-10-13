from xml.etree import ElementTree

from voltaire import graphviz


def test_generate_image():
    dot = """
    digraph g {
        A -> B;
    }
    """
    svg = graphviz.generate_image(dot)

    # The returned markup must be directly embeddable in an HTML document.
    assert svg.startswith("<svg")
    assert "<?xml" not in svg
    assert "DOCTYPE" not in svg

    root = ElementTree.fromstring(svg)
    assert root.tag.rsplit("}", 1)[-1] == "svg"

    groups = [
        element for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "g"
    ]

    def titles_for(group_class):
        return {
            next(
                child.text for child in group if child.tag.rsplit("}", 1)[-1] == "title"
            )
            for group in groups
            if group_class in group.attrib.get("class", "").split()
        }

    # Assert the graph's meaning, rather than renderer-specific paths, dimensions,
    # IDs, colours, or number formatting that change between Graphviz releases.
    assert titles_for("graph") == {"g"}
    assert titles_for("node") == {"A", "B"}
    assert titles_for("edge") == {"A->B"}
