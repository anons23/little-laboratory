from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = s.replace("assets/'+encodeURIComponent('Эхо.gif')+'", 'assets/echo.gif')
old = """host.querySelectorAll('[data-echo]').forEach(b=>b.onclick=()=>{const k=b.dataset.echo;if(!(s.tech&&s.tech.echo))return toast('🔒 Сначала изучи «Протокол Эхо» в Тех');if(s.installed[k])return toast('Уже установлено');if((s[k]|0)<1)return toast('❌ Нет на складе: '+label(k));s[k]--;s.installed[k]=1;save();renderEcho();toast('✓ '+label(k))});
const fin=document.getElementById('echoFinishSlot');if(fin)fin.onclick=()=>{if(!(s.tech&&s.tech.echo)||!req.every(k=>s.installed[k]||(s[k]|0)>=1))return toast('Не все компоненты');for(const k of req){if(!s.installed[k]&&(s[k]|0)>=1){s[k]--;s.installed[k]=1}}s.echoDone=true;s.echoCore=1;s.money=(s.money|0)+5000;s.research=(s.research|0)+1000;discover('echoCore');save();if(typeof playEchoCinematic==='function')playEchoCinematic(()=>{renderEcho();toast('🔆 Ядро Эхо собрано')});else{renderEcho();toast('🔆 Ядро Эхо собрано')}}}"""
new = """const finishEcho=()=>{if(!(s.tech&&s.tech.echo)||!req.every(k=>s.installed[k]))return false;s.echoDone=true;s.echoCore=1;s.money=(s.money|0)+5000;s.research=(s.research|0)+1000;discover('echoCore');save();if(typeof playEchoCinematic==='function')playEchoCinematic(()=>{renderEcho();toast('🔆 Ядро Эхо собрано')});else{renderEcho();toast('🔆 Ядро Эхо собрано')}return true};
host.querySelectorAll('[data-echo]').forEach(b=>b.onclick=()=>{const k=b.dataset.echo;if(!(s.tech&&s.tech.echo))return toast('🔒 Сначала изучи «Протокол Эхо» в Тех');if(s.installed[k])return toast('Уже установлено');if((s[k]|0)<1)return toast('❌ Нет на складе: '+label(k));s[k]--;s.installed[k]=1;save();if(!finishEcho()){renderEcho();toast('✓ '+label(k))}});
const fin=document.getElementById('echoFinishSlot');if(fin)fin.onclick=()=>{if(!(s.tech&&s.tech.echo))return toast('🔒 Сначала изучи «Протокол Эхо» в Тех');for(const k of req){if(!s.installed[k]&&(s[k]|0)>=1){s[k]--;s.installed[k]=1}}if(!finishEcho())toast('Не все компоненты') };}"""
if old not in s:
    raise SystemExit('Expected Echo block not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Echo patch applied')
