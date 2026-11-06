from pathlib import Path
import subprocess, concurrent.futures, json, time, sys, tempfile, os, shutil

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
OUT = Path(tempfile.mkdtemp(prefix='teambook-audit-'))
CXX = os.environ.get('CXX') or shutil.which('g++-15') or shutil.which('g++')
if not CXX:
    raise SystemExit('GCC with C++20 support is required; set CXX to its executable path.')
PLATFORM_FLAGS = []
if sys.platform == 'darwin':
    sdk = subprocess.check_output(['xcrun', '--show-sdk-path'], text=True).strip()
    PLATFORM_FLAGS = ['-mmacosx-version-min=15.0', '-isysroot', sdk]
COMMON = r'''#include <bits/stdc++.h>
using namespace std;
using ll=long long; using ull=unsigned long long; using ld=long double; using vi=vector<int>;
#define all(v) begin(v),end(v)
#define pbc push_back
#define mp make_pair
#define sz(x) ((int)(x).size())
#define rep(i,a,b) for(int i=(a);i<(b);++i)
#define forn(i,n) for(int i=0;i<(n);++i)
mt19937 rnd(123456);
template<class A,class B> void chkmin(A &a,const B &b){if(b<a)a=b;}
template<class A,class B> void chkmax(A &a,const B &b){if(a<b)a=b;}
'''

def inc(*files):
    return ''.join('#include "'+str(ROOT/f)+'"\n' for f in files)

CASES=[]
def case(name, body, timeout=15, flags=None, stdin='', compile_only=False, expected=None):
    CASES.append(dict(name=name,body=body,timeout=timeout,flags=flags or [],stdin=stdin,compile_only=compile_only,expected=expected))

exec((SCRIPT_DIR/'cases.py').read_text())
exec((SCRIPT_DIR/'regressions.py').read_text())

def run(c):
    name=c['name']; source=OUT/(name+'.cpp'); exe=OUT/(name+'.bin')
    source.write_text(COMMON+c['body'])
    cmd=[CXX,'-std=c++20','-O1',*PLATFORM_FLAGS,'-Wno-cpp','-D_GLIBCXX_ASSERTIONS','-fsanitize=undefined','-fsanitize-undefined-trap-on-error','-Werror=return-type',*c['flags'],str(source)]
    cmd += ['-fsyntax-only'] if c['compile_only'] else ['-o',str(exe)]
    start=time.monotonic()
    try:p=subprocess.run(cmd,text=True,capture_output=True,timeout=60)
    except subprocess.TimeoutExpired:return dict(name=name,status='compile_timeout')
    r=dict(name=name,compile_seconds=round(time.monotonic()-start,3),compile_command=cmd,compile_stderr=p.stderr)
    if p.returncode:r.update(status='compile_error',returncode=p.returncode);return r
    if c['compile_only']:r.update(status='compile_ok');return r
    start=time.monotonic()
    try:
        p=subprocess.run([str(exe)],input=c['stdin'],text=True,capture_output=True,timeout=c['timeout'])
        status='pass' if p.returncode==0 else 'fail'
        if c['expected'] is not None and p.stdout!=c['expected']: status='wrong_output'
        r.update(status=status,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    except subprocess.TimeoutExpired as e:
        r.update(status='timeout',stdout=str(e.stdout or ''),stderr=str(e.stderr or ''))
    r['run_seconds']=round(time.monotonic()-start,3)
    return r

if __name__=='__main__':
    chosen=[c for c in CASES if len(sys.argv)==1 or any(s in c['name'] for s in sys.argv[1:])]
    if not chosen:
        raise SystemExit('No matching scenarios.')
    print('Working directory:', OUT, flush=True)
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(run,chosen):
            results.append(r)
            print(r['name'],r['status'],r.get('stdout','')[:800],r.get('stderr',r.get('compile_stderr',''))[:700],flush=True)
    path=OUT/'results.json'
    path.write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print('RESULTS',path,flush=True)

    sys.exit(any(r['status'] not in ('pass', 'compile_ok') for r in results))
