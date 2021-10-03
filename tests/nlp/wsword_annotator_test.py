from paukenator.nlp import WSWordAnnotator, WSWord


def test_text_has_correct_number_of_wswords(text_deu_1):
    wswords = text_deu_1.wswords()
    exp = 293  # counted using: wc -w
    assert exp == len(wswords), \
        f"Text must contain {exp} lines but got {len(wswords)}"


def test_has_property_type():
    assert hasattr(WSWordAnnotator, "type"), \
        ("WSWordAnnotator must have a property `type` that returns the type of"
         " created annotations.")

    exp, actual = WSWord, WSWordAnnotator().type
    assert exp == actual, \
        (f"WSWordAnnotator is expected to produce objects of type {exp} but"
         f" got {actual}")
