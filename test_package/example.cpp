#include <iostream>
#include <physfs.h>

int main()
{
    if (PHYSFS_init(NULL) != 0)
    {
        std::cout << "physfs successfully initialized!\n";
    }

    if (PHYSFS_deinit() != 0)
    {
        std::cout << "physfs successfully deinitialized!\n";
    }
}
