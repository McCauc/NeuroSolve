from src.ui.app_metadata import APP_MILESTONE, APP_NAME, APP_VERSION, TEAM_MEMBERS


def test_app_identity_bundle_values():
    assert APP_NAME == "NeuroSolve"
    assert APP_VERSION == "v0.1.0"
    assert APP_MILESTONE == "Week 7 Midterm Build"


def test_team_members_are_complete_and_ordered():
    assert TEAM_MEMBERS == (
        "Rejay Buta",
        "John Cedrick Delgado",
        "Carlo Jose Anyayahan",
    )
