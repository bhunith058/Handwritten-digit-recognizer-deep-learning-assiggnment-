#include <stdio.h>
#include <stdlib.h>

int main()
{
        int i,n;
        printf("enter the number of elements need to insert");
        scanf("%d",&n);
        int arr[n];
        int sum=0;
        printf("enter the elements to array");
        for(i=0;i<n;i++){
            scanf("%d",&arr[i]);
            sum+=arr[i];
        }
        double average=(double)sum/n;

        printf("the sum of the array is :%d",sum);
        printf("\n the average of array is :%lf",average);


    return 0;
}
