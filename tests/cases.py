GEO=inc('content/geometry/Point.cpp','content/geometry/Line.cpp','content/geometry/Intersections.cpp','content/geometry/Hull.cpp','content/geometry/IsInPolygon.cpp')

case('compile_manacher',inc('content/strings/Manacher.cpp')+'int main(){}',compile_only=True)
for name in ['PolyInter','DeterminantInt','DiscreteLog']:
    case('compile_'+name,inc('content/math/'+name+'.cpp')+'int main(){}',compile_only=True)
case('compile_tridiag',inc('content/math/TridiagSLE.cpp')+'int main(){}',compile_only=True)
case('compile_kinetic','const ll INF=4e18;\n'+inc('content/geometry/Kinetic.cpp')+'int main(){}',compile_only=True)
case('compile_delaunay','using lll=__int128_t;\n'+GEO+inc('content/geometry/Delauney.cpp')+'int main(){}',compile_only=True)
case('compile_pointlocation',GEO+'ld get_area(const vector<point>&p){ld a=0;for(int i=0;i<sz(p);i++)a+=p[i]%p[(i+1)%sz(p)];return a/2;}\n'+inc('content/geometry/PointLocation.cpp')+'int main(){}',compile_only=True)
case('closest',GEO+inc('content/geometry/ClosestPair.cpp')+r'''
int main(){for(auto p:vector<vector<point>>{{{0,0},{0,1}},{{0,0},{0.5,0},{0.7,0}}}){
 auto [a,b]=closest(p);ld got=len(a-b),want=1e30;
 for(int i=0;i<sz(p);i++)for(int j=0;j<i;j++)want=min(want,len(p[i]-p[j]));
 cout<<"got="<<got<<" expected="<<want<<endl;
}}
''')
case('point_order',GEO+r'''
int main(){point a{2,0},b{1,0.75e-7L},c{0,1.5e-7L};cout<<"a<c "<<(a<c)<<" c<b "<<(c<b)<<" b<a "<<(b<a)<<endl;}
''')
case('fft_negative',inc('content/math/FFT.cpp')+r'''
int main(){auto a=mul(vector<ll>{-1},vector<ll>{1});cout<<"got="<<a[0]<<" expected=-1"<<endl;return a[0]!=-1;}
''')
case('eertree', 'const int MAXN=100;\n'+inc('content/strings/Eertree.cpp')+r'''
int main(){eertree e;e.init(MAXN);e.init();string s="aa";for(int i=0;i<sz(s);i++)e.addLetter(i,s);cout<<e.numV<<endl;}
''')
case('lcp_same','const int MAXN=100,lgg=10;\n'+inc('content/strings/SuffixArray.cpp','content/strings/Lcp.cpp')+r'''
int main(){string s="banana";auto sa=buildSuffixArray(s);auto lcp=buildLCP(s,sa);build(lcp);cout<<"got="<<getLCP(5,5)<<" expected=1"<<endl;}
''')
case('strings_fuzz',inc('content/strings/PrefixZ.cpp','content/strings/SuffixArray.cpp','content/strings/SA-IS.cpp','content/strings/MinShift.cpp')+r'''
int main(){int count=0;for(int n=1;n<=9;n++){int lim=pow(3,n);for(int mask=0;mask<lim;mask++){
 string s(n,'a');int m=mask;for(char &c:s)c+=m%3,m/=3;
 vector<int> want(n);iota(all(want),0);sort(all(want),[&](int i,int j){return s.substr(i)<s.substr(j);});
 auto sa=buildSuffixArray(s),sb=suffix_array(s);if(sa!=want||sb!=want){cout<<"suffix fail "<<s<<endl;return 1;}
 string shift=s;for(int i=0;i<n;i++)shift=min(shift,s.substr(i)+s.substr(0,i));if(minshift(s)!=shift){cout<<"shift fail "<<s<<endl;return 1;}
 auto z=zf(s),p=pf(s);for(int i=0;i<n;i++){int k=0;while(i+k<n&&s[k]==s[i+k])k++;if(z[i]!=k)return 2;
 int q=0;for(int k=1;k<=i;k++)if(s.substr(0,k)==s.substr(i-k+1,k))q=k;if(p[i]!=q)return 3;}count++;
 }}cout<<"passed strings="<<count<<endl;}
''',timeout=30)
case('factorize_search',inc('content/math/Factorization.cpp')+r'''
bool prime(ll n){for(ll p=2;p*p<=n;p++)if(n%p==0)return false;return n>=2;}
int main(){for(int seed=0;seed<30000;seed++){rnd.seed(seed);auto f=factorize(1000003LL*1000003);for(ll p:f)if(!prime(p)){cout<<"seed="<<seed<<" n=1000006000009 returned composite="<<p<<endl;return 1;}}cout<<"no failure"<<endl;}
''',timeout=30)
case('mcmf_reinit','const int INF=1000000000;\n'+inc('content/graph/MCMF.cpp')+r'''
int main(){MCMF m;m.init(2,0,1);m.addedge(0,1,1,3);cout<<m.getcost(1)<<endl;m.init(2,0,1);cout<<m.getcost(1)<<endl;}
''')
case('mcmffast_reinit','const ll INF=4000000000000000000LL;\n'+inc('content/graph/MCMFfast.cpp')+r'''
int main(){MCMF m;m.init(2,0,1);m.addedge(0,1,1,3);cout<<m.getcost(1)<<endl;m.init(2,0,1);cout<<m.getcost(1)<<endl;}
''')
case('dinic_reinit',inc('content/graph/MaxFlow.cpp')+r'''
int main(){MaxFlow f;f.init(2,0,1);f.addedge(0,1,7);f.init(2,0,1);cout<<"empty graph flow="<<f.dinic()<<" expected=0"<<endl;}
''')
case('global_mincut_limit',inc('content/graph/GlobalMincut.cpp')+r'''
int main(){n=2;g[0][1]=g[1][0]=1000000001;mincut();cout<<"got="<<best_cost<<" expected=1000000001 cut_size="<<best_cut.size()<<endl;}
''')
case('allocator_ndebug',inc('content/cpp/alloc.cpp')+r'''
int main(){void *a=::operator new(8);void *b=::operator new(8);printf("same pointer=%d\n",a==b);return a==b || mpos<16;}
''',flags=['-DNDEBUG'])
case('allocator_alignment',inc('content/cpp/alloc.cpp')+r'''
int main(){::operator new(1);auto p=::operator new(sizeof(long double));printf("alignment remainder=%zu expected=0\n",(uintptr_t)p%alignof(long double));}
''')

case('geometry_boundary',GEO+r'''
int main(){
 point a{0,0},b{0.0001L,0},x{0.00005L,0};cout<<"short segment midpoint: "<<isOnSegment(a,b,x)<<" expected 1"<<endl;
 vector<point> p{{-1,-1},{1,1.0L/(2e9L+228)},{-1,1}};point q{0,0};cout<<"ray hits vertex: "<<isIn(p,q)<<" expected 2"<<endl;
 vector<point> c{{0,0},{1,0},{2,0},{2,2},{0,2}};point z{3,0};cout<<"convex collinear: "<<isInConvex(c,z)<<" expected 0"<<endl;
}
''')
case('geometry_fuzz',GEO+inc('content/geometry/Diameter.cpp','content/geometry/MinDisk.cpp','content/geometry/TangentsAlex.cpp')+r'''
int main(){for(int t=0;t<10000;t++){
 int n=1+rnd()%12;vector<point> p(n);for(auto &a:p)a={(ld)(int(rnd()%31)-15),(ld)(int(rnd()%31)-15)};
 ld want=0;for(auto a:p)for(auto b:p)want=max(want,len(a-b));auto got=diameter(p);
 if(abs(want-got)>1e-6){cout<<"diameter fail"<<endl;return 1;}
 auto [o,r]=mindisk(p);for(auto a:p)if(len(a-o)>r+1e-6){cout<<"mindisk containment fail"<<endl;return 2;}
 ld br=1e30;auto check=[&](point c,ld rad){for(auto a:p)if(len(a-c)>rad+1e-7)return;br=min(br,rad);};
 for(auto a:p)check(a,0);for(int i=0;i<n;i++)for(int j=0;j<i;j++)check((p[i]+p[j])/2,len(p[i]-p[j])/2);
 for(int i=0;i<n;i++)for(int j=0;j<i;j++)for(int k=0;k<j;k++)if(abs((p[i]-p[k])%(p[j]-p[k]))>1e-8){auto c=circumcenter(p[i],p[j],p[k]);check(c,len(c-p[i]));}
 if(abs(br-r)>1e-6){cout<<"mindisk optimum fail"<<endl;return 3;}
 auto h=hull(p);point q{40,40};auto [i,j]=tangents_alex(h,q);for(auto a:h)if(sign((h[i]-q)%(a-q))<0||sign((h[j]-q)%(a-q))>0){cout<<"tangent fail t="<<t<<endl;return 4;}
 }cout<<"10000 integer geometry cases passed"<<endl;}
''',timeout=30)
case('hpi_fuzz',GEO+inc('content/geometry/IsHpiEmpty.cpp','content/geometry/HalfPlaneIntersection.cpp')+r'''
bool feasible(vector<line> a){vector<point> box{{-1000,-1000},{1000,-1000},{1000,1000},{-1000,1000}};for(int i=0;i<4;i++)a.push_back(getln(box[i],box[(i+1)%4]));
 for(int i=0;i<sz(a);i++)for(int j=0;j<i;j++){ld d=a[i].a*a[j].b-a[j].a*a[i].b;if(abs(d)<1e-12)continue;point p{(a[i].b*a[j].c-a[j].b*a[i].c)/d,(a[i].c*a[j].a-a[j].c*a[i].a)/d};bool ok=1;for(auto l:a)if(l.eval(p)<-1e-6)ok=0;if(ok)return true;}return false;}
int main(){for(int t=0;t<30000;t++){int n=1+rnd()%8;vector<line>a;for(int i=0;i<n;i++){int x=int(rnd()%11)-5,y=int(rnd()%11)-5;if(!x&&!y){i--;continue;}line l{(ld)x,(ld)y,(ld)(int(rnd()%21)-10)+0.137L};l.norm();a.push_back(l);}auto before=rnd;bool want=!feasible(a),got=isHpiEmpty(a);if(want!=got){cout<<setprecision(18)<<"t="<<t<<" empty got="<<got<<" expected="<<want<<"\n";for(auto l:a)cout<<l.a<<" "<<l.b<<" "<<l.c<<"\n";cout<<"rng "<<before<<endl;return 1;}
 }cout<<"30000 half-plane feasibility cases passed"<<endl;}
''',timeout=30)

dinic_src=(ROOT/'content/graph/MaxFlow.cpp').read_text().replace('bool bfs() {','bool bfs() { ++audit_bfs;').replace('for (int i : g[v]) {','for (int i : g[v]) { ++audit_scans;')
case('dinic_complexity','ll audit_bfs=0,audit_scans=0;\n'+dinic_src+r'''
int main(){for(int k:{100,1000,4000}){audit_bfs=audit_scans=0;MaxFlow f;f.init(3,0,2);for(int i=0;i<k;i++)f.addedge(0,1,1);f.addedge(1,2,k);cout<<"k="<<k<<" flow="<<f.dinic()<<" BFS="<<audit_bfs<<" scans="<<audit_scans<<endl;if(audit_scans>8LL*(k+1))return 1;}}
''')
mcmf_src=(ROOT/'content/graph/MCMF.cpp').read_text().replace('for (int i : g[v]) {','for (int i : g[v]) { ++audit_scans;')
case('mcmf_complexity','const int INF=1000000000; ll audit_scans=0;\n'+mcmf_src+r'''
int main(){for(int k:{100,1000,4000}){audit_scans=0;MCMF f;f.init(3,0,2);for(int i=k;i>0;i--)f.addedge(0,1,1,i);for(int i=0;i<k;i++)f.addedge(1,2,1,0);cout<<"k="<<k<<" cost="<<f.getcost(1)<<" scans="<<audit_scans<<endl;if(audit_scans>8LL*(k+1))return 1;}}
''')
case('dinic_fuzz',inc('content/graph/MaxFlow.cpp')+r'''
int main(){for(int t=0;t<10000;t++){int n=2+rnd()%7;MaxFlow f;f.init(n,0,n-1);vector<tuple<int,int,int>>es;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j&&rnd()%3==0){int c=rnd()%30;es.emplace_back(i,j,c);f.addedge(i,j,c);}int want=INT_MAX;for(int mask=1;mask<(1<<n);mask+=2)if(!(mask>>(n-1)&1)){int v=0;for(auto[a,b,c]:es)if((mask>>a&1)&&!(mask>>b&1))v+=c;want=min(want,v);}int got=f.dinic();if(got!=want){cout<<t<<" "<<got<<" "<<want<<endl;return 1;}}cout<<"10000 flows passed against exhaustive cuts"<<endl;}
''')

case('ntt_fuzz',inc('content/math/NTT.cpp','content/math/SubsetConvolution.cpp','content/math/AndConvolution.cpp','content/math/XorConvolution.cpp','content/math/CharPoly.cpp')+r'''
int main(){for(int t=0;t<2000;t++){
 int n=1+rnd()%30,m=1+rnd()%30;vector<int>a(n),b(m);for(int&x:a)x=rnd()%MOD;for(int&x:b)x=rnd()%MOD;
 vector<int>w(n+m-1);for(int i=0;i<n;i++)for(int j=0;j<m;j++)w[i+j]=add(w[i+j],mul(a[i],b[j]));auto g=conv(a,b);w.resize(max(w.size(),g.size()));g.resize(w.size());if(w!=g){cout<<"NTT fail";return 1;}
 a[0]=1;int k=1+rnd()%30;auto ai=inv(a,k);auto product=conv(a,ai);product.resize(k);for(int i=0;i<k;i++)if(product[i]!=(i==0)){cout<<"FPS inverse fail";return 2;}
 auto lg=log(a,k),ex=exp(lg,k);a.resize(k);if(ex!=a){cout<<"FPS exp/log fail";return 3;}
 vector<int>xs(m);for(int &x:xs)x=rnd()%MOD;auto canonical=a;while(canonical.size()>1&&!canonical.back())canonical.pop_back();auto ev=multipoint(canonical,xs);for(int i=0;i<m;i++){int val=0;for(int j=k-1;j>=0;j--)val=add(mul(val,xs[i]),a[j]);if(ev[i]!=val){cout<<"multipoint fail";return 4;}}
 }cout<<"2000 NTT/FPS/multipoint cases passed\n";
 for(int t=0;t<1000;t++){int n=1<<(rnd()%7);vector<int>a(n),b(n);for(int &x:a)x=rnd()%MOD;for(int &x:b)x=rnd()%MOD;auto s=SubsetConvolution(a,b),x=xorconvo(a,b),d=andcon(a,b);vector<int>ws(n),wx(n),wd(n);for(int i=0;i<n;i++)for(int j=0;j<n;j++){int v=mul(a[i],b[j]);wx[i^j]=add(wx[i^j],v);wd[i&j]=add(wd[i&j],v);if(!(i&j))ws[i|j]=add(ws[i|j],v);}if(s!=ws||x!=wx||d!=wd){cout<<"convolution fail t="<<t<<" subset="<<(s==ws)<<" xor="<<(x==wx)<<" and="<<(d==wd)<<endl;return 5;}}
 cout<<"1000 subset/AND/XOR cases passed"<<endl;
}
''',timeout=60)
case('math_small',inc('content/math/PrimeCount.cpp','content/math/GoncharFedor.cpp')+r'''
int main(){int pi=0;for(int n=1;n<=100000;n++){bool prime=n>=2;for(int d=2;d*d<=n;d++)if(n%d==0){prime=0;break;}pi+=prime;if(prime_pi(n)!=pi){cout<<"pi fail "<<n<<endl;return 1;}}
 for(int a=1;a<=30;a++)for(int b=1;b<=30;b++)for(int c=0;c<=200;c++){ll want=0;for(int x=0;a*x<=c;x++)want+=(c-a*x)/b+1;if(solve_triangle(a,b,c)!=want){cout<<"triangle fail";return 2;}}cout<<"100000 prime counts and 180900 lattice counts passed"<<endl;}
''',timeout=30)

case('crt_overflow','#define int ll\n'+inc('content/math/CRT.cpp')+'\n#undef int\n'+r'''
int main(){cout<<crt(4000000000LL,6000000000LL,0,2000000000LL)<<" expected 8000000000"<<endl;}
''')
case('primality_overflow',r'''
ll binpow(ll a,ll b,ll m){ll r=1;for(;b;b>>=1,a=(__int128)a*a%m)if(b&1)r=(__int128)r*a%m;return r;}
'''+inc('content/math/PrimalityTest.cpp')+r'''
int main(){cout<<isprime(6000000000000000000LL)<<" expected 0"<<endl;}
''')
case('fastio_eof',inc('content/cpp/fastio.cpp')+'int main(){cout<<readChar()<<endl;}',timeout=1)
case('suffix_empty',inc('content/strings/SA-IS.cpp')+'int main(){string s;auto a=suffix_array(s);cout<<a.size()<<endl;}')
case('z_empty',inc('content/strings/PrefixZ.cpp')+'int main(){cout<<zf("").size()<<endl;}')
case('berlekamp_zero',inc('content/math/NTT.cpp')+'int powmod(int a,int n){return power(a,n);}\n'+inc('content/math/BerlekampMassey.cpp')+r'''
int main(){vector<int> x(10,0);auto c=berlekamp(x);cout<<"order="<<c.size()<<endl;cout<<getk(x,c,20)<<endl;}
''')

push_src=(ROOT/'content/graph/Pushrelabel.cpp').read_text().split('\nint main()')[0]
case('pushrelabel_fuzz',push_src+r'''
int main(){for(int t=0;t<10000;t++){int n=2+rnd()%7;MaxFlow f(n);vector<tuple<int,int,int>>es;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j&&rnd()%3==0){int c=rnd()%30;es.emplace_back(i,j,c);f.add_edge(i,j,c);}int want=INT_MAX;for(int mask=1;mask<(1<<n);mask+=2)if(!(mask>>(n-1)&1)){int v=0;for(auto[a,b,c]:es)if((mask>>a&1)&&!(mask>>b&1))v+=c;want=min(want,v);}auto got=f.run(0,n-1);if(got!=want){cout<<t<<" "<<got<<" "<<want<<endl;return 1;}}cout<<"10000 flows passed against exhaustive cuts"<<endl;}
''')
case('dominator_fuzz',inc('content/graph/DominatorTree.cpp')+r'''
int main(){for(int t=0;t<10000;t++){int n=1+rnd()%9,root=rnd()%n;DominatorTree d(n);vector<vector<int>>a(n);for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(rnd()%4==0){d.add_edge(i,j);a[i].push_back(j);}auto reach=[&](int skip){vector<int>v(n);auto dfs=[&](auto&&self,int x)->void{if(x==skip||v[x])return;v[x]=1;for(int y:a[x])self(self,y);};dfs(dfs,root);return v;};auto base=reach(-1);vector<vector<int>>dom(n,vector<int>(n));for(int x=0;x<n;x++){auto r=reach(x);for(int v=0;v<n;v++)dom[v][x]=base[v]&&!r[v];}auto got=d.run(root);for(int v=0;v<n;v++){int want=-1;if(base[v]&&v!=root)for(int x=0;x<n;x++)if(x!=v&&dom[v][x]){bool closest=1;for(int y=0;y<n;y++)if(y!=v&&y!=x&&dom[v][y]&&dom[y][x])closest=0;if(closest)want=x;}if(got[v]!=want){cout<<"dominator fail t="<<t<<" v="<<v<<" got="<<got[v]<<" expected="<<want<<endl;return 1;}}}cout<<"10000 dominator graphs passed"<<endl;}
''')
case('weighted_matching_fuzz',inc('content/graph/WeightedMatching.cpp')+r'''
int main(){for(int t=0;t<2000;t++){n=1+rnd()%9;for(int i=1;i<=n;i++)for(int j=1;j<=n;j++)g[i][j]={i,j,0};for(int i=1;i<=n;i++)for(int j=1;j<i;j++)g[i][j].w=g[j][i].w=rnd()%21;
 vector<int>dp(1<<n,-1);auto brute=[&](auto&&self,int mask)->int{if(!mask)return 0;int&r=dp[mask];if(r!=-1)return r;int i=__builtin_ctz(mask);r=self(self,mask^(1<<i));for(int j=i+1;j<n;j++)if(mask>>j&1)r=max(r,g[i+1][j+1].w+self(self,mask^(1<<i)^(1<<j)));return r;};ll want=brute(brute,(1<<n)-1),got=weight_blossom().first;if(got!=want){cout<<"weighted fail t="<<t<<" got="<<got<<" expected="<<want<<endl;return 1;}}
 cout<<"2000 weighted matching cases passed"<<endl;}
''',timeout=30)

case('factorize_fixedpoint_search',inc('content/math/Factorization.cpp')+r'''
bool iscomposite(ll n){for(ll d=2;d*d<=n;d++)if(n%d==0)return true;return false;}
int main(){for(int seed=0;seed<2000000;seed++){rnd.seed(seed);ll z=(ull)rnd()+1,x=sqrtl(z);if(x*x!=z||x<1001)continue;ll n=x*x-x+1;if(!iscomposite(n))continue;rnd.seed(seed);auto f=factorize(n);bool bad=false;for(ll a:f)bad|=iscomposite(a);if(!bad)continue;cout<<"seed="<<seed<<" initial_x="<<x<<" n="<<n<<" result:";for(ll a:f)cout<<" "<<a;cout<<endl;return 1;}cout<<"not found"<<endl;}
''',timeout=30)

case('hpi_ndebug',GEO+inc('content/geometry/HalfPlaneIntersection.cpp')+r'''
int main(){vector<point>q{{-1,-1},{1,-1},{1,1},{-1,1}};vector<line>ls;for(int i=0;i<4;i++)ls.push_back(getln(q[i],q[(i+1)%4]));auto p=hpi(ls);ld area=0;for(int i=0;i<sz(p);i++)area+=p[i]%p[(i+1)%sz(p)];cout<<"vertices="<<p.size()<<" area="<<abs(area)/2<<" expected=4"<<endl;return abs(abs(area)/2-4)>1e-6;}
''',flags=['-DNDEBUG'])
case('hpi_area_fuzz',GEO+inc('content/geometry/HalfPlaneIntersection.cpp')+r'''
int main(){for(int t=0;t<10000;t++){vector<point>p{{-50,-50},{50,-50},{50,50},{-50,50}},box=p;vector<line>ls;for(int i=0;i<4;i++)ls.push_back(getln(p[i],p[(i+1)%4]));int n=rnd()%9;for(int i=0;i<n;i++){int a=int(rnd()%11)-5,b=int(rnd()%11)-5;if(!a&&!b){i--;continue;}line l{(ld)a,(ld)b,(ld)(int(rnd()%21)-10)+.137L};l.norm();ls.push_back(l);vector<point>q;for(int j=0;j<sz(p);j++){auto a=p[j],b=p[(j+1)%sz(p)];ld fa=l.eval(a),fb=l.eval(b);if(fa>=0)q.push_back(a);if((fa>=0)!=(fb>=0))q.push_back(a+(b-a)*(fa/(fa-fb)));}p=q;}
 auto area=[](vector<point>p){ld r=0;for(int i=0;i<sz(p);i++)r+=p[i]%p[(i+1)%sz(p)];return abs(r)/2;};auto got=hpi(ls);ld x=area(got),y=area(p);if(abs(x-y)>1e-6){cout<<"hpi fail t="<<t<<" area="<<x<<" expected="<<y<<endl;return 1;}}
 cout<<"10000 HPI areas passed against polygon clipping"<<endl;}
''',timeout=30)
case('minplus_fuzz',inc('content/geometry/MinPlusConv.cpp')+r'''
int main(){for(int t=0;t<10000;t++){int n=1+rnd()%30,m=1+rnd()%30;vector<ll>a(n),b(m);ll d=-10;for(int i=1;i<n;i++){d+=rnd()%3;a[i]=a[i-1]+d;}for(auto &v:b)v=int(rnd()%101)-50;auto got=convex_arbitrary_min_plus_conv(a,b);vector<ll>w(n+m-1,LLONG_MAX);for(int i=0;i<n;i++)for(int j=0;j<m;j++)w[i+j]=min(w[i+j],a[i]+b[j]);if(w!=got){cout<<"minplus fail"<<endl;return 1;}}cout<<"10000 convex min-plus convolutions passed"<<endl;}
''')
case('mcmf_fuzz','const int INF=1000000000;\nnamespace slow {\n'+inc('content/graph/MCMF.cpp')+'}\nnamespace fast {\n'+inc('content/graph/MCMFfast.cpp')+'}\n'+r'''
int main(){for(int t=0;t<2000;t++){int n=2+rnd()%5,k=rnd()%4;slow::MCMF a;fast::MCMF b;a.init(n,0,n-1);b.init(n,0,n-1);vector<array<int,4>>es;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(rnd()%2&&es.size()<8){int cap=rnd()%3,cost=int(rnd()%15)-7;es.push_back({i,j,cap,cost});a.addedge(i,j,cap,cost);b.addedge(i,j,cap,cost);}vector<int>bal(n);int want=INF;auto rec=[&](auto&&self,int i,int cost)->void{if(i==sz(es)){if(bal[0]!=k||bal[n-1]!=-k)return;for(int j=1;j<n-1;j++)if(bal[j])return;want=min(want,cost);return;}auto[u,v,c,w]=es[i];for(int f=0;f<=c;f++){bal[u]+=f;bal[v]-=f;self(self,i+1,cost+w*f);bal[u]-=f;bal[v]+=f;}};rec(rec,0,0);auto x=a.getcost(k);auto y=b.getcost(k);if(x!=want||y!=want){cout<<"mincost fail t="<<t<<" got="<<x<<","<<y<<" expected="<<want<<endl;return 1;}}cout<<"2000 min-cost flows passed for both implementations"<<endl;}
''',timeout=30)

import random
rr=random.Random(12345)
n=25; adjacency=[set() for _ in range(n)];ops=[];answers=[]
def distance(s,t):
    q=[s];d={s:0}
    for x in q:
        for y in adjacency[x]:
            if y not in d:d[y]=d[x]+1;q.append(y)
    return d.get(t,-1)
for _ in range(20000):
    u,v=rr.randrange(n),rr.randrange(n);d=distance(u,v);op=rr.randrange(3)
    if op==0 and d==-1:
        adjacency[u].add(v);adjacency[v].add(u);ops.append(f'link {u+1} {v+1}')
    elif op==1 and adjacency[u]:
        v=rr.choice(sorted(adjacency[u]));adjacency[u].remove(v);adjacency[v].remove(u);ops.append(f'cut {u+1} {v+1}')
    else:ops.append(f'get {u+1} {v+1}');answers.append(str(d))
case('lct_driver',inc('content/graph/Lct.cpp'),stdin=f'{n}\n{len(ops)}\n'+'\n'.join(ops)+'\n',expected='\n'.join(answers)+'\n')

case('berlekamp_zero_term',inc('content/math/NTT.cpp')+'int powmod(int a,int n){return power(a,n);}\n'+inc('content/math/BerlekampMassey.cpp')+r'''
int main(){cout<<getk({1,0,1,0},{0,1},3)<<" expected 0"<<endl;}
''')
case('linear_charpoly_fuzz',inc('content/math/NTT.cpp','content/math/CharPoly.cpp','content/math/SolveLinear.cpp','content/math/DeterminantLd.cpp')+r'''
int determinant(vector<vector<int>> a){int n=sz(a),res=1;for(int i=0;i<n;i++){int p=i;while(p<n&&!a[p][i])p++;if(p==n)return 0;if(p!=i){swap(a[i],a[p]);res=sub(0,res);}res=mul(res,a[i][i]);int v=inv(a[i][i]);for(int j=i+1;j<n;j++){int c=mul(a[j][i],v);for(int k=i;k<n;k++)a[j][k]=sub(a[j][k],mul(c,a[i][k]));}}return res;}
int main(){for(int t=0;t<3000;t++){int n=1+rnd()%6;vector<vector<int>>a(n,vector<int>(n));for(auto&r:a)for(int&x:r)x=rnd()%MOD;auto p=CharacteristicPolynomial(a);for(int x=0;x<8;x++){int v=0;for(int j=n;j>=0;j--)v=add(mul(v,x),p[j]);auto b=a;for(int i=0;i<n;i++)b[i][i]=sub(b[i][i],x);if(v!=determinant(b)){cout<<"charpoly fail";return 1;}}
 vector<vector<double>> A(n,vector<double>(n));vector<double> x(n),want(n),b(n);for(auto&r:A)for(auto&v:r)v=int(rnd()%11)-5;for(auto&v:want)v=int(rnd()%11)-5;for(int i=0;i<n;i++)for(int j=0;j<n;j++)b[i]+=A[i][j]*want[j];auto old=A;auto bb=b;int rank=solveLinear(A,b,x);if(rank<0){cout<<"SLE unexpected inconsistency";return 2;}for(int i=0;i<n;i++){double s=0;for(int j=0;j<n;j++)s+=old[i][j]*x[j];if(abs(s-bb[i])>1e-6){cout<<"SLE fail";return 3;}}
 vi perm(n);iota(all(perm),0);double wd=0;do{double v=1;for(int i=0;i<n;i++){v*=old[i][perm[i]];for(int j=0;j<i;j++)if(perm[j]>perm[i])v=-v;}wd+=v;}while(next_permutation(all(perm)));double got=det(old);if(abs(got-wd)>1e-5){cout<<"det fail";return 4;}}
cout<<"3000 characteristic polynomials, linear systems and floating determinants passed"<<endl;}
''',timeout=30)
case('suffix_automaton_fuzz',inc('content/strings/SuffixAutomaton.cpp')+r'''
int main(){for(int t=0;t<2000;t++){for(auto &x:st)x.next.clear();sa_init();int n=rnd()%25;string s;for(int i=0;i<n;i++){char c='a'+rnd()%3;s+=c;sa_extend(c);}set<string>ss;for(int i=0;i<n;i++)for(int j=i+1;j<=n;j++)ss.insert(s.substr(i,j-i));ll count=0;for(int i=1;i<sz;i++)count+=st[i].len-st[st[i].link].len;if(count!=ss.size()){cout<<"SAM count fail";return 1;}for(auto s:ss){int v=0;for(char c:s){if(!st[v].next.count(c)){cout<<"SAM missing substring";return 2;}v=st[v].next[c];}}}cout<<"2000 suffix automata passed"<<endl;}
''',timeout=30)
blossom_src=(ROOT/'content/graph/BlossomShrinking.cpp').read_text().split('\nsigned main()')[0]
case('blossom_fuzz',blossom_src+r'''
int main(){for(int t=0;t<3000;t++){n=1+rnd()%10;for(int i=0;i<N;i++)g[i].clear();perfectMatching.clear();vector<vector<int>>a(n,vector<int>(n));for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(rnd()%2){a[i][j]=a[j][i]=1;g[i].push_back(j);g[j].push_back(i);}vector<int>dp(1<<n,-1);auto rec=[&](auto&&self,int mask)->int{if(!mask)return 0;int&r=dp[mask];if(r!=-1)return r;int i=__builtin_ctz(mask);r=self(self,mask^(1<<i));for(int j=i+1;j<n;j++)if((mask>>j&1)&&a[i][j])r=max(r,1+self(self,mask^(1<<i)^(1<<j)));return r;};int want=rec(rec,(1<<n)-1);blossomShrinking();if(sz(perfectMatching)!=want){cout<<"blossom fail";return 1;}}cout<<"3000 general matchings passed"<<endl;}
''')
case('matroid_fuzz',inc('content/graph/MatroidIntersection.cpp')+r'''
struct Elem{int id,a,b;};
struct Partition{bool second;vector<int>cnt;Partition(bool s,int k):second(s),cnt(k){} int color(Elem e)const{return second?e.b:e.a;}void add(Elem e){cnt[color(e)]++;}void add_extra(Elem e){add(e);}bool independed_with(Elem e){return cnt[color(e)]==0;}bool independed_without(Elem e){for(int i=0;i<sz(cnt);i++)if(cnt[i]-(i==color(e))>1)return false;return true;}};
int main(){for(int t=0;t<5000;t++){int n=rnd()%12,k=1+rnd()%5;vector<Elem>a;for(int i=0;i<n;i++)a.push_back({i,int(rnd()%k),int(rnd()%k)});auto got=matroid_intersection(a,Partition(false,k),Partition(true,k));int want=0;for(int mask=0;mask<(1<<n);mask++){vector<int>x(k),y(k);bool ok=1;for(int i=0;i<n;i++)if(mask>>i&1)if(++x[a[i].a]>1||++y[a[i].b]>1){ok=0;break;}if(ok)want=max(want,__builtin_popcount((unsigned)mask));}if(sz(got)!=want){cout<<"matroid fail";return 1;}}cout<<"5000 intersections of two partition matroids passed"<<endl;}
''',timeout=30)
case('simplex_fuzz',inc('content/math/Simplex.cpp')+r'''
int main(){for(int t=0;t<5000;t++){vector<vector<ld>>A{{-1,0},{0,-1},{1,0},{0,1}};vector<ld>b{0,0,10,10},c{(ld)(int(rnd()%11)-5),(ld)(int(rnd()%11)-5)};int n=rnd()%5;for(int i=0;i<n;i++){int x=int(rnd()%11)-5,y=int(rnd()%11)-5;A.push_back({(ld)x,(ld)y});b.push_back((ld)(int(rnd()%31)-10));}ld want=-numeric_limits<ld>::infinity();for(int i=0;i<sz(A);i++)for(int j=0;j<i;j++){ld d=A[i][0]*A[j][1]-A[j][0]*A[i][1];if(abs(d)<1e-12)continue;ld x=(b[i]*A[j][1]-b[j]*A[i][1])/d,y=(A[i][0]*b[j]-A[j][0]*b[i])/d;bool ok=1;for(int k=0;k<sz(A);k++)if(A[k][0]*x+A[k][1]*y>b[k]+1e-8)ok=0;if(ok)want=max(want,c[0]*x+c[1]*y);}Simplex_Steep<ld>s(A,b,c);vector<ld>x;ld got=s.Solve(x);if(isfinite(got)!=isfinite(want)||(isfinite(want)&&abs(got-want)>1e-6)){cout<<"simplex fail t="<<t<<" got="<<got<<" expected="<<want<<endl;return 1;}}cout<<"5000 bounded/infeasible 2D linear programs passed"<<endl;}
''',timeout=30)

case('pointlocation_nested',GEO+inc('content/geometry/PointLocation.cpp')+r'''
int main(){vector<vec>p{{-10,-10},{10,-10},{10,10},{-10,10},{-2,-2},{2,-2},{2,2},{-2,2}};vector<vector<int>>g(8);for(int z:{0,4})for(int i=0;i<4;i++){int a=z+i,b=z+(i+1)%4;g[a].push_back(b);g[b].push_back(a);}auto d=buildDCEL(p,g);auto r=point_location(d,{{9,0},{0,3},{0,0}});for(auto[a,b]:r)cout<<a<<" "<<b<<"\n";cout<<"first two queries must belong to the same bounded face"<<endl;return r[0]!=r[1];}
''')
ntt_small=(ROOT/'content/math/NTT.cpp').read_text().replace('const int MAXLOG = 23;','const int MAXLOG = 3;')
case('ntt_capacity_scaled',ntt_small+r'''
int main(){cout<<"MAXLOG=3, vectors of length 4 need only an 8-point NTT"<<endl;auto a=conv(vector<int>(4,1),vector<int>(4,1));for(int x:a)cout<<x<<" ";cout<<endl;}
''')
case('ndhull_overflow',inc('content/geometry/NDHull.cpp')+r'''
int main(){Face f{};for(int i=0;i<DIM;i++)f[i][i]=65000;cout<<"positive orientation="<<(V(f,pt{})>0)<<endl;return V(f,pt{})<=0;}
''')

vin=next(l for l in (ROOT/'content/contest/template.cpp').read_text().splitlines() if l.startswith('#define vin('))
case('compile_vin',vin+'\nint main(){vector<int> values(2);vin(values);}',compile_only=True)
case('compile_generator',GEO+'int randint(int l,int r){return l+rnd()%(r-l+1);}\nld area(vector<point>&p){ld a=0;for(int i=0;i<sz(p);i++)a+=p[i]%p[(i+1)%sz(p)];return a/2;}\n'+inc('content/geometry/GenerateNonConvex.cpp')+'int main(){}',compile_only=True)

expected_outputs={
 'closest':'got=1 expected=1\ngot=0.2 expected=0.2\n',
 'point_order':None,
 'dinic_reinit':'empty graph flow=0 expected=0\n',
 'global_mincut_limit':'got=1000000001 expected=1000000001 cut_size=1\n',
 'allocator_ndebug':'same pointer=0\n',
 'allocator_alignment':'alignment remainder=0 expected=0\n',
 'geometry_boundary':'short segment midpoint: 1 expected 1\nray hits vertex: 2 expected 2\nconvex collinear: 0 expected 0\n',
}
for c in CASES:
    if c['name'] in expected_outputs:c['expected']=expected_outputs[c['name']]
    if c['name']=='point_order':c['body']=c['body'].replace('<<endl;}','<<endl;return (a<c)&&(c<b)&&(b<a);}')
case('dmst_fuzz',inc('content/graph/OrientedSpanningTree.cpp')+r'''
int main(){for(int t=0;t<2000;t++){int n=2+rnd()%4,r=rnd()%n;vector<Edge>g;vector<vector<int>>in(n);for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j&&rnd()%2){in[j].push_back(sz(g));g.push_back({i,j,(ll)(int(rnd()%21)-10)});}vector<int>p(n,-1);ll want=LLONG_MAX;auto rec=[&](auto&&self,int v,ll cost)->void{if(v==n){for(int x=0;x<n;x++){int z=x;for(int k=0;k<n&&z!=r;k++)z=p[z];if(z!=r)return;}want=min(want,cost);return;}if(v==r){self(self,v+1,cost);return;}for(int i:in[v]){p[v]=g[i].a;self(self,v+1,cost+g[i].w);}};rec(rec,0,0);auto got=dmst(n,r,g);if((want==LLONG_MAX&&!got.second.empty())||(want!=LLONG_MAX&&got.first!=want)){cout<<"dmst fail t="<<t<<" got="<<got.first<<" expected="<<want<<endl;return 1;}}
cout<<"2000 directed MST cases passed"<<endl;}
''',timeout=30)
case('cht_fuzz','const int INF=1000000000;\n'+inc('content/geometry/CHT.cpp')+r'''
int main(){for(int t=0;t<3000;t++){ConvexHullMin h;vector<line>a;int k=50;for(int j=0;j<30;j++){k-=rnd()%3;line l{k,int(rnd()%1001)-500};a.push_back(l);h.add(l);for(int x=-100;x<=100;x++){int w=INT_MAX;for(auto l:a)w=min(w,l.eval(x));if(h.get_val(x)!=w){cout<<"cht fail";return 1;}}}}cout<<"3000 monotone CHT sequences passed"<<endl;}
''',timeout=30)
case('dynamic_cht_fuzz','bool Q=false;\n'+inc('content/geometry/DynamicCHT.cpp')+r'''
int main(){for(int t=0;t<3000;t++){LineContainer h;vector<pair<ll,ll>>a;for(int j=0;j<30;j++){ll k=int(rnd()%101)-50,b=int(rnd()%1001)-500;a.emplace_back(k,b);h.add(k,b);for(int x=-100;x<=100;x++){ll w=LLONG_MIN;for(auto[k,b]:a)w=max(w,k*x+b);if(h.query(x)!=w){cout<<"dynamic cht fail";return 1;}}}}cout<<"3000 dynamic CHT sequences passed"<<endl;}
''',timeout=30)

case('factorize_fixedpoint',inc('content/math/Factorization.cpp')+r'''
int main(){rnd.seed(89725);auto f=factorize(85682793LL);sort(all(f));vector<ll>w{3,7,4080133};cout<<"got:";for(ll p:f)cout<<" "<<p;cout<<" expected: 3 7 4080133"<<endl;return f!=w;}
''')
