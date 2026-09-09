from pathlib import Path
import re

HTML = Path("index.html").read_text(encoding="utf-8")


def test_required_onboarding_and_guidance_are_present():
    assert 'id="onboarding"' in HTML
    assert 'id="onboardingSkip"' in HTML
    assert 'id="guidedGoal"' in HTML
    assert "function renderGuidedGoal()" in HTML
    assert "function openLabTab(tab)" in HTML
    assert "СИГНАЛ ИЗ ЭХА" in HTML


def test_wheel_has_exactly_ten_percent_empty_sector():
    m = re.search(r"function wheelPool\(\)\{return\[(.*?)\];?\}", HTML)
    if not m:
        m = re.search(r"function weightedWheel\(\)\{const pool=\[(.*?)\];", HTML)
    assert m, "wheel pool not found"
    weights = [float(x) for x in re.findall(r"\['[^']+',([0-9.]+)\]", m.group(1))]
    assert len(weights) == 11, weights
    assert abs(sum(weights) - 100.0) < 1e-9
    nothing = float(re.search(r"\['nothing',([0-9.]+)\]", m.group(1)).group(1))
    assert abs(nothing - 10.0) < 1e-9
    assert "#293552 327.27deg 360deg" in HTML


def test_reset_and_prestige_do_not_refresh_daily_ad_or_wheel_limits():
    assert "adCounts:clone(s.adCounts||base.adCounts)" in HTML
    assert "fortuneFree:s.fortuneFree" in HTML
    assert "fortuneAds:s.fortuneAds" in HTML
    assert "adWarehouseUntil:s.adWarehouseUntil" in HTML
    assert "adDiscountUntil:s.adDiscountUntil" in HTML
    assert "adProductionUntil:s.adProductionUntil" in HTML


def test_random_events_are_not_too_rare_and_have_first_event_path():
    assert "(Math.max(0,dt)/60)*0.05" in HTML
    assert "s.meta.totalExperiments>0&&!s.meta.eventsSeen" in HTML
    assert "now-s.meta.tutorialStartedAt>=180000" in HTML


def test_no_eval_was_added_for_guided_navigation():
    assert "eval(" not in HTML


if __name__ == "__main__":
    tests = [v for n, v in globals().items() if n.startswith("test_")]
    for test in tests:
        test()
    print(f"Game integrity tests OK: {len(tests)}")
