from pathlib import Path
import subprocess,concurrent.futures,json,tempfile,os,shutil,sys
root=Path(__file__).resolve().parents[1]; out=Path(tempfile.mkdtemp(prefix='teambook-existing-tests-'))
compiler=os.environ.get('CXX') or shutil.which('g++-15') or shutil.which('g++')
platform_flags=[]
if sys.platform=='darwin':
 sdk=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip()
 platform_flags=['-mmacosx-version-min=15.0','-isysroot',sdk]
files=sorted((root/'content/verify').rglob('*.cpp'))
def check(p):
 cmd=[compiler,'-std=c++20',*platform_flags,'-Wno-cpp','-fsyntax-only',str(p)]
 r=subprocess.run(cmd,text=True,capture_output=True,timeout=60)
 return {'file':str(p.relative_to(root)),'returncode':r.returncode,'diagnostics':r.stderr}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(check,files))
(out/'existing-test-compilation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('Existing test sources:',len(results),'compiled:',sum(r['returncode']==0 for r in results))
for r in results:
 if r['returncode']:print(r['file'], '\n'.join(x for x in r['diagnostics'].splitlines() if 'error:' in x)[:400])

print('Results:',out/'existing-test-compilation.json')
sys.exit(any(r['returncode'] for r in results))
