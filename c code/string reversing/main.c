#include <stdio.h>
#include <string.h>




void reverseString(char str[]){
int length=strlen(str);
for(int i=0;i<length/2;i++){
    char temp=str[i];
    str[i]=str[length-i-1];
    str[length-i-1]=temp;
}
}

void reverseList(int arr[],int size){
for(int i=0;i<size/2;i++){
    int temp=arr[i];
    arr[i]=arr[size-i-1];
    arr[size-i-1]=temp;
}

}

int main()
{
    int choice;
    printf("do you want to reverse a string press 1 or reverse a list press 2:");
    scanf("%d",&choice);
    if(choice==1){
        char str[100];
        printf("enter the string");
        scanf("%s",&str);
        reverseString(str);
        printf("reversed string is:%s",str);
    }

  else if (choice==2){
       int n;
       printf("ENTER THE NUMBER OF ELEMENTS WANT TO BE INSERTED");
       scanf("%d",&n);
       int arr[n];
       printf("enter the elements to array");
       for (int i=0;i<n;i++){
        scanf("%d",&arr[i]);
       }
       reverseList(arr,n);
       printf("reversed list:");
       for(int i=0;i<n;i++){
        printf("%d \n",arr[i]);


       }

    }
    else{
        printf("invalid input");
    }

    return 0;
}
