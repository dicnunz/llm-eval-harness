from harness.summary import render_summary


def test_render_summary_includes_latest_best_and_average():
    runs = [
        {
            "run_id": "20260418-210101",
            "model": "model-a",
            "pack_name": "release-gate",
            "passed": 5,
            "total": 5,
            "score": 1.0,
        },
        {
            "run_id": "20260418-210422",
            "model": "model-b",
            "pack_name": "release-gate",
            "passed": 4,
            "total": 5,
            "score": 0.8,
        },
    ]

    output = render_summary(runs)

    assert "Recent runs (most recent last):" in output
    assert "pack=release-gate" in output
    assert "Latest: 20260418-210422  score=4/5 (80.0%)" in output
    assert "Best (last 2): 20260418-210101  score=5/5 (100.0%)" in output
    assert "Avg (last 2): 0.900" in output
