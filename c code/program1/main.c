#include<stdio.h>

int main()

{
    int array[10], n,i, item;

    printf("Enter the size of array: ");

    scanf("%d", &n);

    printf("\nEnter Elements in array: ");

    for(i=0; i<n; i++)
    {
        scanf("%d", &array[i]);

    }

    printf("\n enter the element at the beginning");

    scanf("%d", &item);

    n++;

    for(i=n; i>1; i--)

    {

        array[i-1]=array[i-2];

    }

    array[0]=item;

    printf("resultant array element");

    for(i=0; i<n; i++)

    {

        printf("\n%d", array[i]);

    }
    return 0;

}
