#include <stdio.h>
#include <physfs.h>

int main()
{
    if (PHYSFS_init(NULL) != 0)
    {
        printf("physfs successfully initialized!\n");
    }

    if (PHYSFS_deinit() != 0)
    {
        printf("physfs successfully deinitialized!\n");
    }

    return 0;
}
