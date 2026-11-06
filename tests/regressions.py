# Turn the old audit probes into assertions; retain the exhaustive/differential
# tests. Seed searches are replaced by their two known counterexamples below.
CASES[:] = [c for c in CASES if c['name'] not in ('factorize_search', 'factorize_fixedpoint_search')]
expected = {
    'eertree': '29\n',
    'lcp_same': 'got=1 expected=1\n',
    'mcmf_reinit': '3\n1000000000\n',
    'mcmffast_reinit': '3\n4000000000000000000\n',
    'crt_overflow': '8000000000 expected 8000000000\n',
    'primality_overflow': '0 expected 0\n',
    'fastio_eof': '-1\n',
    'suffix_empty': '0\n',
    'z_empty': '0\n',
    'berlekamp_zero': 'order=0\n0\n',
    'berlekamp_zero_term': '0 expected 0\n',
    'ntt_capacity_scaled': 'MAXLOG=3, vectors of length 4 need only an 8-point NTT\n1 2 3 4 3 2 1 \n',
}
for c in CASES:
    if c['name'] in expected: c['expected'] = expected[c['name']]

case('factorization_regression',inc('content/math/Factorization.cpp')+r'''
int main(){
 for(auto [seed,n]:vector<pair<int,ll>>{{14377,1000007},{89725,85682793}}){rnd.seed(seed);auto f=factorize(n);__int128 product=1;for(ll p:f){if(!isprime(p))return 1;product*=p;}if(product!=n)return 2;}
 vector<bool> prime(200001,true);prime[0]=prime[1]=false;
 for(int i=2;i<sz(prime);i++)if(prime[i])for(int j=i+i;j<sz(prime);j+=i)prime[j]=false;
 for(int i=0;i<sz(prime);i++)if(isprime(i)!=prime[i])return 3;
 for(ll n:{341550071728321LL,3825123056546413051LL,LLONG_MAX,1000000016000000063LL}){auto f=factorize(n);__int128 product=1;for(ll p:f){if(!isprime(p))return 4;product*=p;}if(product!=n)return 5;}
 if(!isprime(2305843009213693951LL)||!isprime(9223372036854775783LL))return 6;
 for(int t=0;t<2000;t++){ll n=1+(ll)(rnd()%100000)* (1+rnd()%100000);auto f=factorize(n);ll product=1;for(ll p:f){for(ll d=2;d*d<=p;d++)if(p%d==0)return 7;product*=p;}if(product!=n)return 8;}
 cout<<"factorization and primality passed"<<endl;
}''',timeout=30)
case('closest_fuzz',GEO+inc('content/geometry/ClosestPair.cpp')+r'''
int main(){for(int t=0;t<10000;t++){int n=2+rnd()%30;vector<point>p(n);for(auto&a:p)a={(ld)(int(rnd()%501)-250)/13,(ld)(int(rnd()%501)-250)/17};ld want=1e100;for(int i=0;i<n;i++)for(int j=0;j<i;j++)want=min(want,len2(p[i]-p[j]));auto[a,b]=closest(p);if(abs(len2(a-b)-want)>1e-9)return 1;}cout<<"10000 closest pairs passed"<<endl;}
''')
case('polygon_fuzz',GEO+r'''
int main(){for(int t=0;t<5000;t++){vector<point>p;for(int i=0;i<12;i++)p.push_back({(ld)(int(rnd()%31)-15),(ld)(int(rnd()%31)-15)});auto h=hull(p);if(h.size()<3)continue;vector<point>q;for(int i=0;i<sz(h);i++){q.push_back(h[i]);q.push_back((h[i]+h[(i+1)%sz(h)])/2);}rotate(q.begin(),q.begin()+rnd()%q.size(),q.end());for(int k=0;k<30;k++){point a{(ld)(int(rnd()%81)-40)/2,(ld)(int(rnd()%81)-40)/2};bool want=1;for(int i=0;i<sz(h);i++)if(sign((h[(i+1)%sz(h)]-h[i])%(a-h[i]))<0)want=0;if(isInConvex(q,a)!=want||bool(isIn(q,a))!=want){cout<<"polygon fail "<<t<<" point="<<a.x<<","<<a.y<<" convex="<<isInConvex(q,a)<<" general="<<isIn(q,a)<<" expected="<<want<<endl;for(auto v:q)cout<<v.x<<","<<v.y<<" ";cout<<endl;return 1;}}}cout<<"5000 convex polygons with collinear vertices passed"<<endl;}
''')
case('string_edges_fuzz','const int MAXN=256,lgg=10;\n'+inc('content/strings/Manacher.cpp','content/strings/Eertree.cpp','content/strings/SuffixArray.cpp','content/strings/Lcp.cpp')+r'''
int main(){for(int t=0;t<3000;t++){int n=1+rnd()%60;string s(n,'a');for(char&c:s)c+=rnd()%3;auto odd=manacherOdd(s),even=manacherEven(s);eertree e;e.init(MAXN);e.init();set<string>pal;for(int i=0;i<n;i++){e.addLetter(i,s);int a=0,b=0;while(i-a>=0&&i+a<n&&s[i-a]==s[i+a])a++;while(i-b-1>=0&&i+b<n&&s[i-b-1]==s[i+b])b++;if(odd[i]!=a||even[i]!=b)return 1;for(int j=0;j<=i;j++){auto v=s.substr(j,i-j+1),r=v;reverse(all(r));if(v==r)pal.insert(v);}}int longer=0;for(auto v:pal)longer+=v.size()>1;if(e.numV!=28+longer)return 2;auto sa=buildSuffixArray(s);auto lcp=buildLCP(s,sa);build(lcp);for(int i=0;i<n;i++)for(int j=0;j<n;j++){int w=0;while(i+w<n&&j+w<n&&s[i+w]==s[j+w])w++;if(getLCP(i,j)!=w)return 3;}}cout<<"3000 palindrome trees, Manacher and LCP cases passed"<<endl;}
''')
case('crt_fuzz',inc('content/math/CRT.cpp')+r'''
int main(){for(ll a=1;a<=60;a++)for(ll b=1;b<=60;b++)for(int t=0;t<10;t++){ll r=int(rnd()%201)-100,s=int(rnd()%201)-100,w=-1;for(ll x=0;x<a*b;x++)if((x-r)%a==0&&(x-s)%b==0){w=x;break;}if(crt(a,b,r,s)!=w)return 1;}if(crt(LLONG_MAX,LLONG_MAX,LLONG_MAX-1,-1)!=LLONG_MAX-1)return 2;bool caught=0;try{crt(LLONG_MAX,2,0,0);}catch(const overflow_error&){caught=1;}if(!caught)return 3;cout<<"36000 CRT cases and overflow contract passed"<<endl;}
''')
case('tridiag_fuzz',inc('content/math/TridiagSLE.cpp')+r'''
int main(){for(int t=0;t<5000;t++){int n=rnd()%40;vector<ld>a(n),b(n),c(n),x(n),f(n);for(int i=0;i<n;i++){a[i]=i?int(rnd()%21)-10:0;b[i]=i+1<n?int(rnd()%21)-10:0;c[i]=abs(a[i])+abs(b[i])+1;x[i]=int(rnd()%201)-100;}for(int i=0;i<n;i++)f[i]=c[i]*x[i]+(i?a[i]*x[i-1]:0)+(i+1<n?b[i]*x[i+1]:0);auto y=trisle(a,b,c,f);for(int i=0;i<n;i++)if(abs(x[i]-y[i])>1e-8)return 1;}bool caught=0;try{trisle({0},{0},{0},{1});}catch(const domain_error&){caught=1;}return !caught;}
''')
case('berlekamp_fuzz',inc('content/math/NTT.cpp')+'int powmod(int a,int n){return power(a,n);}\n'+inc('content/math/BerlekampMassey.cpp')+r'''
int main(){for(int t=0;t<2000;t++){int d=1+rnd()%8;vector<int>c(d),v(80);for(int&i:c)i=rnd()%4;for(int i=0;i<d;i++)v[i]=rnd()%4;for(int i=d;i<80;i++)for(int j=0;j<d;j++)v[i]=add(v[i],mul(c[j],v[i-j-1]));vector<int>prefix(v.begin(),v.begin()+2*d+4);auto rec=berlekamp(prefix);for(int k=0;k<80;k++)if(getk(prefix,rec,k)!=v[k])return 1;}cout<<"2000 recurrences passed"<<endl;}
''',timeout=30)
case('pointlocation_fuzz',GEO+inc('content/geometry/PointLocation.cpp')+r'''
int main(){for(int t=0;t<1000;t++){
 vector<array<ld,4>> boxes{{-1000,-1000,1000,1000},{-600,-200,-200,200},{200,-200,600,200},{-500,-100,-300,100},{-500,2500,500,3500}};
 ld scale=(1+rnd()%8)/4.L,dx=int(rnd()%101)-50,dy=int(rnd()%101)-50;
 vector<point>pts;for(auto &b:boxes){b[0]=b[0]*scale+dx;b[2]=b[2]*scale+dx;b[1]=b[1]*scale+dy;b[3]=b[3]*scale+dy;pts.insert(pts.end(),{{b[0],b[1]},{b[2],b[1]},{b[2],b[3]},{b[0],b[3]}});}
 vector<vector<int>>g(pts.size());for(int z=0;z<sz(pts);z+=4)for(int i=0;i<4;i++){int a=z+i,b=z+(i+1)%4;g[a].push_back(b);g[b].push_back(a);}
 auto d=buildDCEL(pts,g);vector<int>face(boxes.size(),-1);
 for(int k=0;k<sz(boxes);k++)for(auto e:d.body)if(e.origin==pts[4*k]&&d.body[e.twin].origin==pts[4*k+1])face[k]=e.face;
 vector<point>q;for(int k=0;k<100;k++)q.push_back({(int(rnd()%6001)-3000+.37L)*scale+dx,(int(rnd()%8001)-3000+.23L)*scale+dy});
 for(auto b:boxes){q.push_back({b[0],(b[1]+b[3])/2});q.push_back({(b[0]+b[2])/2,b[3]});q.push_back({b[0],b[1]});}
 auto ans=point_location(d,q);for(int j=0;j<sz(q);j++){int want=-1;ld area=1e100;bool boundary=0;for(int k=0;k<sz(boxes);k++){auto b=boxes[k];for(int i=0;i<4;i++)boundary|=isOnSegment(pts[4*k+i],pts[4*k+(i+1)%4],q[j]);if(b[0]<q[j].x&&q[j].x<b[2]&&b[1]<q[j].y&&q[j].y<b[3]){ld a=(b[2]-b[0])*(b[3]-b[1]);if(a<area)area=a,want=face[k];}}
 if(boundary){if(ans[j].first!=0)return 1;auto e=d.body.at(ans[j].second);if(!isOnSegment(e.origin,d.body[e.twin].origin,q[j]))return 2;}
 else if(ans[j]!=make_pair(1,want)){cout<<"location mismatch t="<<t<<" query="<<q[j].x<<","<<q[j].y<<" got="<<ans[j].second<<" want="<<want<<endl;return 3;}}
 }cout<<"1000 disconnected/nested embeddings passed"<<endl;}
''',timeout=30)
case('delaunay_fuzz',GEO+inc('content/geometry/Delauney.cpp')+r'''
int main(){for(int t=0;t<1000;t++){int n=rnd()%22;set<pair<int,int>>s;while(sz(s)<n)s.insert({int(rnd()%101)-50,int(rnd()%101)-50});vector<point>p;for(auto[x,y]:s)p.push_back({(ld)x,(ld)y});auto tri=triangulate(p);auto h=hull(p);ld want=0,got=0;if(sz(h)>=3)for(int i=0;i<sz(h);i++)want+=h[i]%h[(i+1)%sz(h)];if(tri.size()%3)return 1;for(int i=0;i<sz(tri);i+=3){auto a=tri[i],b=tri[i+1],c=tri[i+2];ld area=(b-a)%(c-a);if(area<=0)return 2;got+=area;for(auto q:p){auto x=a-q,y=b-q,z=c-q;ld det=len2(x)*(y%z)-len2(y)*(x%z)+len2(z)*(x%y);if(det>1e-6){cout<<"circumcircle mismatch"<<endl;return 3;}}}if(abs(got-want)>1e-7){cout<<"triangulation area "<<got<<" vs "<<want<<endl;return 4;}}cout<<"1000 Delaunay triangulations passed"<<endl;}
''',timeout=30)
case('math_repaired_snippets',inc('content/math/PolyInter.cpp','content/math/DeterminantInt.cpp','content/math/DiscreteLog.cpp')+r'''
int main(){for(int t=0;t<2000;t++){int n=1+rnd()%6;vector<double>coef(n),x(n),y(n);for(auto &v:coef)v=int(rnd()%21)-10;for(int i=0;i<n;i++){x[i]=i-2;for(int j=n-1;j>=0;j--)y[i]=y[i]*x[i]+coef[j];}auto r=interpolate(x,y,n);for(int i=0;i<n;i++)if(abs(r[i]-coef[i])>1e-7)return 1;
 vector<vector<ll>>a(n,vector<ll>(n));for(auto&r:a)for(auto &v:r)v=int(rnd()%21)-10;vi p(n);iota(all(p),0);ll want=0;do{ll v=1;for(int i=0;i<n;i++){v*=a[i][p[i]];for(int j=0;j<i;j++)if(p[j]>p[i])v=-v;}want=(want+v)%mod;}while(next_permutation(all(p)));want=(want+mod)%mod;if(det(a)!=want)return 2;}
 for(int m=1;m<=80;m++)for(int a=0;a<m;a++){vector<int>w(m,-1);int v=1%m;for(int k=1;k<=m+1;k++){v=v*a%m;if(w[v]==-1)w[v]=k;}for(int b=0;b<m;b++)if(modLog(a,b,m)!=w[b]){cout<<"discrete log "<<a<<","<<b<<","<<m<<endl;return 3;}}
 cout<<"interpolation, modular determinant and discrete logs passed"<<endl;}
''',timeout=30)
case('kinetic_fuzz','const ll INF=4000000000000000000LL;\n'+inc('content/geometry/Kinetic.cpp')+r'''
int main(){for(int t=0;t<1000;t++){int n=1+rnd()%30;vector<line>a(n);for(auto &l:a)l={int(rnd()%21)-10,int(rnd()%101)-50,0};kinetic_segtree s(a);for(int it=0;it<200;it++){int l=rnd()%n,r=rnd()%n;if(l>r)swap(l,r);int op=rnd()%3;if(op==0){ll db=int(rnd()%31)-15,dt=rnd()%10;s.add(l,r,db,dt);for(int i=l;i<=r;i++)a[i].b+=db,a[i].temp+=dt;}else if(op==1){line v{int(rnd()%21)-10,int(rnd()%101)-50,(ll)(rnd()%100)};s.change_line(l,v);a[l]=v;}else{ll w=INF;for(int i=l;i<=r;i++)w=min(w,a[i].eval());if(s.query(l,r)!=w)return 1;}}}cout<<"1000 kinetic trees passed"<<endl;}
''',timeout=30)
for name,source in [('arena','content/cpp/alloc.cpp'),('template_arena','content/templates/fast_mem.cpp')]:
 case(name+'_bounds',inc(source)+r'''
int main(){auto p=::operator new(1);auto q=::operator new(64,align_val_t(64));if((uintptr_t)q%64||p==q)return 1;bool caught=0;try{::operator new(MAX_MEM+1);}catch(const bad_alloc&){caught=1;}if(!caught)return 2;auto r=::operator new(0);auto s=::operator new(0);if(r==s)return 3;::operator delete(q,align_val_t(64));return 0;}
''',flags=['-DNDEBUG'])
case('ntt_bounds',ntt_small+r'''
int main(){bool caught=0;try{conv(vector<int>(5,1),vector<int>(5,1));}catch(const length_error&){caught=1;}if(!caught)return 1;if(conv({}, {1})!=vector<int>{0})return 2;auto a=conv({3},{4});if(a!=vector<int>{12})return 3;}
''',flags=['-DNDEBUG'])
case('pointlocation_grid',GEO+inc('content/geometry/PointLocation.cpp')+r'''
int main(){vector<point>p;for(int y=0;y<4;y++)for(int x=0;x<4;x++)p.push_back({(ld)x,(ld)y});p.insert(p.end(),{{1.2L,1.2L},{1.8L,1.2L},{1.8L,1.8L},{1.2L,1.8L},{-2,-2},{-2,-1},{-1,-1}});vector<vector<int>>g(p.size());auto edge=[&](int a,int b){g[a].push_back(b);g[b].push_back(a);};for(int y=0;y<4;y++)for(int x=0;x<4;x++){if(x<3)edge(4*y+x,4*y+x+1);if(y<3)edge(4*y+x,4*(y+1)+x);}for(int i=0;i<4;i++)edge(16+i,16+(i+1)%4);edge(20,21);edge(21,22);auto d=buildDCEL(p,g);auto face=[&](int a,int b){for(auto e:d.body)if(e.origin==p[a]&&d.body[e.twin].origin==p[b])return e.face;return -999;};vector<point>q;for(int i=0;i<10000;i++)q.push_back({(int(rnd()%6001)-2500+.13L)/1000,(int(rnd()%6001)-2500+.17L)/1000});auto got=point_location(d,q);for(int i=0;i<sz(q);i++){auto v=q[i];int want=-1;if(0<v.x&&v.x<3&&0<v.y&&v.y<3)want=face(4*(int)v.y+(int)v.x,4*(int)v.y+(int)v.x+1);if(1.2L<v.x&&v.x<1.8L&&1.2L<v.y&&v.y<1.8L)want=face(16,17);if(got[i]!=make_pair(1,want)){cout<<"grid mismatch "<<v.x<<","<<v.y<<endl;return 1;}}cout<<"grid, bridges and nested component passed"<<endl;}
''')
case('fft_signed_fuzz',inc('content/math/FFT.cpp')+r'''
int main(){for(int t=0;t<3000;t++){int n=1+rnd()%50,m=1+rnd()%50;vector<ll>a(n),b(m),w(n+m-1);for(auto&v:a)v=int(rnd()%2001)-1000;for(auto&v:b)v=int(rnd()%2001)-1000;for(int i=0;i<n;i++)for(int j=0;j<m;j++)w[i+j]+=a[i]*b[j];auto r=mul(a,b);w.resize(r.size());if(w!=r)return 1;}cout<<"3000 signed FFT convolutions passed"<<endl;}
''')
case('ndhull_regression',inc('content/geometry/NDHull.cpp')+r'''
int main(){Face f{};__int128 expected=1;for(int i=0;i<DIM;i++)f[i][i]=65000,expected*=65000;if(V(f,pt{})!=expected)return 1;swap(f[0],f[1]);if(V(f,pt{})!=-expected)return 2;vector<pt>p(5);for(int i=0;i<DIM;i++)p[i+1][i]=65000;init(p);add(pt{100,100,100,100});if(faces.size()!=5)return 3;p.push_back(pt{65000,65000,65000,65000});add(p.back());for(auto face:faces)for(auto v:p)if(V(face,v)<0)return 4;}
''')
# Exercise the sparse-table upper bound with exactly enough columns.
case('lcp_capacity','const int MAXN=128,lgg=7;\n'+inc('content/strings/SuffixArray.cpp','content/strings/Lcp.cpp')+r'''
int main(){string s(128,'a');auto sa=buildSuffixArray(s);auto a=buildLCP(s,sa);build(a);for(int i=0;i<128;i++)for(int j=0;j<128;j++)if(getLCP(i,j)!=128-max(i,j))return 1;}
''')
