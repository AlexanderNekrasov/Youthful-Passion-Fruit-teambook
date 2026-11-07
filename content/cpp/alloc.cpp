/**
 * Author: Iurii Pustovalov
 * Date: 2024-08-23
 * Description: fastalloc
 */
const int MAX_MEM = 1e8;
int mpos = 0;
char mem[MAX_MEM];
inline void *operator new(size_t n) {
  assert((mpos += n) <= MAX_MEM);
  return (void *)(mem + mpos - n);
}
void operator delete(void *) noexcept {
}  // must have!
void operator delete(void *, size_t) noexcept {
}  // must have!