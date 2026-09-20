#include <stdio.h>
#include <stdlib.h>

int main()
{
   float temperature,convertedTemp;
   int sourceUnit,targetUnit;
   int continueconv=1;

   while(continueconv){

        printf("enter the value of temperature");
   scanf("%f",&temperature);

    printf("enter the value of source unit");
    printf("\n1.celsius \n");
    printf("2.fahernheit \n");
    printf("3.kelvin \n");

    printf("---choose(1-3)---");
   scanf("%d",&sourceUnit);


    printf("enter the value of target unit");
    printf("1.celsius \n");
    printf("2.fahernheit \n");
    printf("3.kelvin \n");

    printf("choose(1-3)");
   scanf("%d",&targetUnit);

        if(sourceUnit==1&&targetUnit==2){
            convertedTemp=(temperature*9/5)+32;
        }
        else if(sourceUnit==1&&targetUnit==3){
            convertedTemp=temperature+273.15;
        }
        else if(sourceUnit==2&&targetUnit==1){
            convertedTemp=(temperature-32)*5/9;
        }
        else if(sourceUnit==2&&targetUnit==3){
            convertedTemp=(temperature-32)*5/9+273.15;
        }
        else if(sourceUnit==3&&targetUnit==1){
            convertedTemp=temperature-273.15;
        }
        else if(sourceUnit==3&&targetUnit==2){
            convertedTemp=(temperature-273.15)*9/5+32;
        }
        else if(sourceUnit==targetUnit){
            convertedTemp=temperature;
            printf("entered values both are same");
        }
        else{
            printf("invalid input");

        }
    printf("converted temperature is:%f",convertedTemp);
    printf("\n do you want to continue press 1 for yes 0 for no");
    scanf("%d",&continueconv);



   }

    printf("program has been terminated");



    return 0;
}
