/**
 * Author: Iurii Pustovalov
 * Date: 2024-08-23
 * Description: Fast aligned arena allocator; requires C++17.
 */
#include <new>
#include <cstddef>
#include <cstdint>
const size_t MAX_MEM = 100000000;
size_t mpos = 0;
alignas(std::max_align_t) unsigned char mem[MAX_MEM];

// Arena: individual frees are intentionally no-ops. Not thread-safe.
void *arena_allocate(size_t n, size_t alignment) {
    if (n == 0) n = 1;
    size_t padding = (-(uintptr_t)(mem + mpos)) & (alignment - 1);
    if (padding > MAX_MEM - mpos || n > MAX_MEM - mpos - padding)
        throw std::bad_alloc();
    mpos += padding;
    void *res = mem + mpos;
    mpos += n;
    return res;
}
void *operator new(size_t n) { return arena_allocate(n, alignof(std::max_align_t)); }
void *operator new[](size_t n) { return ::operator new(n); }
void *operator new(size_t n, std::align_val_t a) { return arena_allocate(n, (size_t)a); }
void *operator new[](size_t n, std::align_val_t a) { return ::operator new(n, a); }
void operator delete(void *) noexcept {}
void operator delete[](void *) noexcept {}
void operator delete(void *, size_t) noexcept {}
void operator delete[](void *, size_t) noexcept {}
void operator delete(void *, std::align_val_t) noexcept {}
void operator delete[](void *, std::align_val_t) noexcept {}
void operator delete(void *, size_t, std::align_val_t) noexcept {}
void operator delete[](void *, size_t, std::align_val_t) noexcept {}
