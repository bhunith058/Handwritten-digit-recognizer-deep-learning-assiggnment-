#include <stdio.h>
#include <math.h>

int main()
{
    double a,b,c;
    double root1,root2,realpart,imaginarypart,discriminant;


    printf("enter the value of coefficients a,b and c");
    scanf("%lf %lf %lf",&a,&b,&c);

    if(a==0){
        printf("the coefficirnt a cannot be 0 in quadratic equation");
        return 1;
    }


    discriminant=b*b-4*a*c;

    if(discriminant>0){

        root1=(-b+sqrt(discriminant))/2*a;
         root2=(-b-sqrt(discriminant))/2*a;
         printf("this equation has two real roots %lf %lf",root1,root2);
    }
    else if(discriminant==0){
      root1=-b/2*a;
      printf("this equation has two identical roots %lf",root1);

    }
    else{
        realpart=-b/2*a;
        imaginarypart=-sqrt(-discriminant)/2*a;

        printf("the equation has complex root: %lf+%lf and %lf-(%lf)",realpart,imaginarypart,realpart,imaginarypart);


    }
    return 0;


}
