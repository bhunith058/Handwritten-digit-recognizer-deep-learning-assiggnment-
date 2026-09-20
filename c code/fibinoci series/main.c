#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,n,n1=0,n2=1,nextTerm=n1+n2;


    printf("enter how many term want to be print");
    scanf("%d",&n);
    printf(" the value of first two term %d %d",n1,n2);
    for(i=3;i<=n;++i){
        printf(" %d ",nextTerm);
        n1=n2;
        n2=nextTerm;
        nextTerm=n1+n2;
    }


    return 0;
}
