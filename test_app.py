from app import app

# Test Header
def test_header_present(dash_duo):
    dash_duo.start_server(app)
    
    header = dash_duo.wait_for_element("h1")
    assert "Impact of Pink Morsel Price Increase on Sales" in header.text


# Test Graph Presence
def test_graph_present(dash_duo):
    dash_duo.start_server(app)
    
    graph = dash_duo.wait_for_element("#sales-chart")
    assert graph is not None


# Test Region Picker Presence
def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    
    radio_buttons = dash_duo.wait_for_element("#region-filter")
    assert radio_buttons is not None