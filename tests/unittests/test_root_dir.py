from musync import ROOT_DIR


def test_root_dir():
    musync_dir = ROOT_DIR / "musync"
    assert musync_dir.exists()
