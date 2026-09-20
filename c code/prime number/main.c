#include <stdio.h>

int main(){

 int i,num,temp=0;
//getting input from user
 printf("enter the value of num :");
 scanf("%d",&num);
 //itterate from 2 untill i<=num/2
 for(i=2;i<=num/2;i++){

    if(num%i==0){
        temp++;
        break;
    }
 }

if(temp==0&&num!=1){
    printf("the given number is prime : %d",num);
}
else{
     printf("the given number is not prime : %d",num);
}
return 0;
}
