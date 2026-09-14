from pathlib import Path
import re

HTML = Path("index.html").read_text(encoding="utf-8")
MANIFEST = Path("game.json").read_text(encoding="utf-8")


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


def test_random_events_have_first_event_path():
    assert "(Math.max(0,dt)/60)*0.05" in HTML or "(Math.max(0,dt)/60)*0.045" in HTML
    assert "s.meta.totalExperiments>0&&!s.meta.eventsSeen" in HTML
    assert "now-s.meta.tutorialStartedAt>=180000" in HTML


def test_no_eval_was_added_for_guided_navigation():
    assert "eval(" not in HTML


def test_yandex_and_mobile_shell_are_present():
    assert 'name="viewport"' in HTML
    assert 'https://sdk.games.s3.yandex.net/sdk.js' in HTML
    assert 'YaGames.init()' in HTML
    assert 'maximum-scale=1' in HTML
    assert '"orientation": "portrait"' in MANIFEST


def test_v19_save_schema_and_legacy_v18_key_are_present():
    assert "SAVE_SCHEMA_VERSION=19" in HTML
    assert "little_laboratory_v19" in HTML
    assert "little_laboratory_v18" in HTML
    assert "const base={version:SAVE_SCHEMA_VERSION," in HTML


def test_market_has_explicit_non_purchasable_items():
    assert "regen:null,matrix:null,mdna:null" in HTML
    assert "stableHeart:null,echoCore:null" in HTML
    assert "if(p==null)return null" in HTML
    assert "price==null" in HTML


def test_rewarded_ad_callback_is_single_shot():
    assert "let rewardedOnce=false" in HTML
    assert "if(rewardedOnce)return" in HTML


if __name__ == "__main__":
    tests = [v for n, v in globals().items() if n.startswith("test_")]
    for test in tests:
        test()
    print(f"Game integrity tests OK: {len(tests)}")

def test_runtime_stability_and_yandex_gameplay_markup():
    assert "function nowMs()" in HTML
    assert "ysdk?.serverTime" in HTML
    assert "if(s.event&&s.event.id&&num(s.event.expires)>now)return" in HTML
    assert "s.tasks.produce=(s.tasks.produce|0)+got" in HTML
    assert "await player.setData(s,false)" in HTML
    assert "GameplayAPI?.stop?.()" in HTML
    assert "LoadingAPI?.ready?.()" in HTML
    assert "game_api_pause" in HTML and "game_api_resume" in HTML
    assert "overscroll-behavior:none" in HTML


def test_reset_recreates_task_and_ad_state():
    assert "tech:clone(base.tech),tasks:clone(base.tasks),adCounts:clone(base.adCounts)" in HTML

