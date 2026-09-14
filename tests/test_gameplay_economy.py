from pathlib import Path
HTML=Path('index.html').read_text(encoding='utf-8')
def test_offline_scenarios_are_capped():
    assert 'Math.min(10800,Math.max(0,(nowMs()-num(s.lastOffline))/1000))' in HTML
    assert 'Math.max(0,dt)' in HTML
def test_daily_limits_use_server_time(): assert 'function today(){const d=new Date(nowMs())' in HTML
def test_render_is_frame_coalesced():
    assert 'function renderNow(){' in HTML and 'window.__llRenderQueued' in HTML and 'requestAnimationFrame(flush)' in HTML
def test_echo_checklist_removed():
    assert 'function renderEchoProgress(){' not in HTML
    assert 'renderEchoProgress()' not in HTML
def test_reward_reset_persistence_markers_exist():
    assert 'adCounts:clone(s.adCounts||base.adCounts)' in HTML and 'fortuneFree:s.fortuneFree' in HTML and 'fortuneAds:s.fortuneAds' in HTML
def test_prestige_and_reset_preserve_meta():
    assert 'meta.resets=(meta.resets||0)+1' in HTML and 'meta.bestLevel=Math.max(meta.bestLevel||1,s.labLevel||1)' in HTML and 'await save(false,true)' in HTML
def test_no_unsafe_dynamic_code(): assert 'eval(' not in HTML and 'new Function(' not in HTML
def test_yandex_pause_resume_lifecycle_exists():
    assert 'game_api_pause' in HTML and 'game_api_resume' in HTML
    assert 'GameplayAPI?.stop?.()' in HTML and 'GameplayAPI?.start?.()' in HTML
if __name__=='__main__':
    tests=[v for n,v in globals().items() if n.startswith('test_')]
    for t in tests:t()
    print(f'Gameplay economy tests OK: {len(tests)}')
