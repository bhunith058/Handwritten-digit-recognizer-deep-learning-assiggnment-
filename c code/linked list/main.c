#include <stdio.h>
#include <stdlib.h>
struct Node
{
    int data;
    struct Node*next;
};
void traverse(struct Node*ptr)
{
    while(ptr!=NULL)
    {
        printf("element is :%d \n",ptr->data);
        ptr=ptr->next;
    }


}
/*struct Node*atfirst(struct Node*head,int data)
{
    struct Node*ptr=(struct Node*)malloc(sizeof(struct Node));
    ptr->next=head;
    ptr->data=data;
    return ptr;

};
struct Node*atbetween(struct Node*head,int data,int index)
{
    struct Node*ptr=(struct Node*)malloc(sizeof(struct Node));
    struct Node*p=head;
    int i=0;
    while(i!=index-1)
    {
        p=p->next;
        i++;
    }
        ptr->data=data;
    ptr->next=p->next;
    p->next=ptr;


    return head;
};*/
struct Node*atend(struct Node*head,int data){
struct Node*ptr=(struct Node*)malloc(sizeof(struct Node));
ptr->data=data;
struct Node*p=head;
while(p->next!=NULL){
    p=p->next;

}
p->next=ptr;
ptr->next=NULL;
return head;

};



int main()
{
    struct Node*head;
    struct Node*first;
    struct Node*second;
    struct Node*third;

    head=(struct Node*)malloc(sizeof(struct Node));
    first=(struct Node*)malloc(sizeof(struct Node));
    second=(struct Node*)malloc(sizeof(struct Node));
    third=(struct Node*)malloc(sizeof(struct Node));

    head->data= 21;
    head->next=first;

    first->data=22;
    first->next=  second;

    second->data=24;
    second->next=third;

    third->data=25;
    third->next=NULL;
/*traverse(head);//
    head=atfirst(head,56);
//traverse(head);
   head=atbetween(head,30,1);*/
 head=atend(head,202);

    traverse(head);
    return 0;
}
