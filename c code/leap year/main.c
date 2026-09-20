#include <stdio.h>
#include <stdlib.h>

int main()
{
   int year;
   printf("enter the value of year");
   scanf("%d",&year);
   if( (year%4==0&&year%100!=0)||(year%400==0)){
    printf("the entered year is leap year");
   }
   else{
     printf("the entered year is not a leap year");
   }

    return 0;
}
