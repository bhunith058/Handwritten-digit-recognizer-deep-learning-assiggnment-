#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n;
    printf("enter the size of array");
    scanf("%d",&n);
    int arr[n];
    int p = 0;
    int sum=0;
    printf("enter the numbers");

    while(p<n){
        scanf("%d",&arr[p]);
        sum+=arr[p];
        p++;


    }

    printf("the value of sum :%d",sum);
    return 0;

}
