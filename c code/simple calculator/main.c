#include <stdio.h>
#include <stdlib.h>

int main()
{
    float num1,num2,result;
    char oper;
    int continueCalc=1;


    while(continueCalc)
    {

        printf("enter the value of first number");
        scanf("%f",&num1);
        printf("enter the value of second number");
        scanf("%f",&num2);


        printf("enter the value of operation");
        scanf(" %c",&oper);

        switch(oper)
        {

        case'+':
            result=num1+num2;
            printf("the value of result is %.2f \n",result);


            break;

        case'-':
            result=num1-num2;
            printf("the value of result is %.2f",result);


            break;

        case'*':
            result=num1*num2;
            printf("the value of result is %.2f",result);


            break;

        case'/':
            if(num2!=0)
            {
                result=num1/num2;
                printf("the value of result is %f",result);

            }
            else
            {
                printf("divisible by 0 is not valid");

            }

            break;

        default:
            printf("entered value is invalid");
            break;





        }

        printf(" \n if u want to continue calculation if press 1=Yes,0=No");
        scanf("%d",&continueCalc);


    }


    printf("the program is terminated");




    return 0;
}
