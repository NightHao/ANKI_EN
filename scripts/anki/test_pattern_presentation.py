"""Render templates through the installed Anki reviewer, including its body-class reset.

Run with Anki's Python environment (PyQt6 WebEngine and _aqt are required):
    python scripts/anki/test_pattern_presentation.py
This never opens or writes an Anki collection.
"""
from pathlib import Path
import csv,inspect,json,sys
from PyQt6.QtCore import QTimer,QUrl
from PyQt6.QtWidgets import QApplication,QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import _aqt.colors

ROOT=Path(__file__).resolve().parents[2]
REVIEWER=Path(inspect.getfile(_aqt.colors)).with_name('data')/'web/js/reviewer.js'

def run():
    template=ROOT/'cards/patterns/anki'
    front=(template/'front.html').read_text(encoding='utf-8')
    back=(template/'back.html').read_text(encoding='utf-8')
    css=(template/'styling.css').read_text(encoding='utf-8')
    with (ROOT/'cards/patterns/anki-import.tsv').open(encoding='utf-8',newline='') as f:
        patterns=list(csv.reader((line for line in f if not line.startswith('#')),delimiter='\t'))
    with (ROOT/'cards/connections/anki-import.tsv').open(encoding='utf-8',newline='') as f:
        connections=list(csv.reader((line for line in f if not line.startswith('#')),delimiter='\t'))
    reason=next(r for r in patterns if 'Just because' in r[1])
    contrast=next(r for r in patterns if 'Despite/In spite of' in r[1])
    single=next(r for r in patterns if r[1]=='If anything, + clause')
    grammar=next(r for r in patterns if r[1].startswith('... + (that/'))
    location=next(r for r in patterns if r[1].startswith('to the left/right of'))
    cases=[('reason-front',reason,'question',760,False,3),
           ('reason-phone',reason,'question',390,False,3),
           ('reason-dark',reason,'question',390,True,3),
           ('contrast-front',contrast,'question',760,False,5),
           ('contrast-back',contrast,'answer',760,False,0),
           ('contrast-back-phone',contrast,'answer',390,False,0),
           ('reason-back',reason,'answer',760,False,0),
           ('reason-back-dark',reason,'answer',390,True,0),
           ('single-back',single,'answer',390,False,0),
           ('grammar-back',grammar,'answer',390,False,0),
           ('location-back',location,'answer',390,True,0),
           ('connection-back',connections[0],'answer',760,False,0),
           ('connection-after-pattern',connections[0],'question',760,False,0),
           ('pattern-again',reason,'question',760,False,3)]
    app=QApplication([str(__file__)])
    host=QWidget();host.resize(800,750)
    view=QWebEngineView(host)
    failures=[];results=[];state={'position':0}
    page='''<!doctype html><html><head><script>
window.bridgeCommand=function(){};
window.MathJax={startup:{promise:Promise.resolve()},typesetClear:function(){},typesetPromise:function(){return Promise.resolve()}};
</script><script src="'''+QUrl.fromLocalFile(str(REVIEWER)).toString()+'''\"></script></head>
<body class="card card1"><div id="qa"></div></body></html>'''
    def html_for(row):
        def fill(s):
            return s.replace('{{Front}}',row[1]).replace('{{Back}}',row[2]).replace('{{Deck}}',row[0])
        q=fill(front);a=fill(back.replace('{{FrontSide}}',q))
        return '<style>'+css+'</style>'+q,'<style>'+css+'</style>'+a
    def next_case():
        index=state['position']
        if index==len(cases):app.quit();return
        name,row,side,width,dark,_=cases[index]
        view.resize(width,700)
        question,answer=html_for(row)
        bodyclass='card card1'+(' nightMode night_mode' if dark else '')
        view.page().runJavaScript('_showQuestion('+json.dumps(question)+','+json.dumps(answer)+','+json.dumps(bodyclass)+');')
        if side=='answer':QTimer.singleShot(200,lambda:view.page().runJavaScript('_showAnswer('+json.dumps(answer)+');'))
        QTimer.singleShot(500,measure)
    def measure():
        view.page().runJavaScript('''JSON.stringify({classes:document.body.className,align:getComputedStyle(document.body).textAlign,width:innerWidth,scroll:document.documentElement.scrollWidth,hooks:onUpdateHook.length,answerVisible:!!document.getElementById('answer')&&!document.getElementById('answer').hidden,titles:Array.from(document.querySelectorAll('.en-pattern-section-title')).map(e=>({size:getComputedStyle(e).fontSize,text:e.textContent})),sections:document.querySelectorAll('.en-pattern-section').length,examples:document.querySelectorAll('.en-pattern-example').length,patterns:Array.from(document.querySelectorAll('.en-pattern-line')).filter(e=>e.getClientRects().length).map(p=>({size:getComputedStyle(p).fontSize,panel:getComputedStyle(p).backgroundColor,slots:Array.from(p.querySelectorAll('.en-pattern-slot')).map(s=>getComputedStyle(s).fontSize)}))})''',checked)
    def checked(raw):
        data=json.loads(raw);name,row,side,width,dark,count=cases[state['position']]
        data['case']=name;results.append(data)
        active='en-pattern-layout' in data['classes']
        expected_active=row[0].startswith('EN::01 Patterns')
        if expected_active:
            if not active or data['align']!='left':failures.append(name+': scoped styling was reset by Anki')
            if len(data['patterns'])!=count:failures.append(name+': pattern groups lost')
            expected='24px' if width<480 else '26px'
            if side=='answer':
                if data['answerVisible'] or not data['sections']:failures.append(name+': repeated header or missing answer blocks')
                if any(t['size']!='21px' for t in data['titles']):failures.append(name+': mixed answer heading size')
            for item in data['patterns']:
                if item['size']!=expected or any(size!=expected for size in item['slots']):failures.append(name+': wrong or mixed font size')
                if item['panel']=='rgba(0, 0, 0, 0)':failures.append(name+': pattern panel disappeared')
        elif active or data['align']!='center':failures.append(name+': styles leaked to Connection Patterns')
        if data['scroll']>data['width']:failures.append(name+': horizontal overflow')
        if data['hooks']>3:failures.append(name+': update hooks accumulated across cards')
        if name.startswith('contrast-back') and (data['sections']!=5 or data['examples']!=11):failures.append(name+': contrast content lost')
        if name.startswith('reason-back') and (data['sections']!=3 or data['examples']!=3):failures.append(name+': inference comparison lost')
        if name=='single-back' and (data['sections']!=1 or data['examples']!=3):failures.append(name+': single-pattern content lost')
        if name=='location-back' and data['sections']!=11:failures.append(name+': location blocks lost')
        print(name+': '+('styled' if active else 'unstyled')+', '+str(data['patterns'][0]['size'] if data['patterns'] else 'no grouped patterns'),flush=True)
        state['position']+=1;QTimer.singleShot(20,next_case)
    view.loadFinished.connect(lambda ok:QTimer.singleShot(50,next_case) if ok else failures.append('Reviewer failed to load'))
    host.show();view.show();view.setHtml(page,QUrl.fromLocalFile(str(REVIEWER.parent)+'\\'))
    QTimer.singleShot(25000,app.quit);app.exec()
    if len(results)!=len(cases):failures.append('Not all reviewer cases ran')
    if failures:raise AssertionError('\n'.join(failures))
    print('Actual Anki reviewer regression passed: Front, Back, repeated cards, phone widths, dark mode, and connection isolation.')

if __name__=='__main__':run()
