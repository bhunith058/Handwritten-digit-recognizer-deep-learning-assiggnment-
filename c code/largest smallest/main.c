#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,n;

    printf("enter how many terms need to insert");
    scanf("%d",&n);
     int arr[n];
    for(i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }
    int largest=arr[0];
    int smallest=arr[0];
    for(i=1;i<n;i++){
        if(arr[i]>largest){
           largest=arr[i];
        }
        if(arr[i]<smallest){
            smallest=arr[i];
        }
    }
    printf("the largest number is :%d\n",largest);
    printf("the smallest number is :%d\n",smallest);
    return 0;
}
