#include<iostream.h>
#include<conio.h>
#include<string.h>
#include<cstdlib>
class ISPYTANIE
{
 public:

// конструктор класса с одним параметром, который по умолчанию равен пустой строке
 ISPYTANIE(const char * NAME = "")
 {
 // выделение памяти для name. размер выделяемой памяти = длина строки NAME
 //(возвращает ф-ция strlen)
 name = new char [strlen(NAME) + 1];
 strcpy(name,NAME);
 }
 virtual ~ISPYTANIE()
 {
     delete [] name;
 }
 virtual void show()=0;
  virtual void input()=0;
  friend class list;
  protected:
  char* name;
  ISPYTANIE* next;
};
class EXAMEN:public ISPYTANIE
 {
  public:
  EXAMEN() {st=0;}
  EXAMEN(int ST) {st=ST;}
  EXAMEN(char*NAME,int ST):ISPYTANIE(NAME)
  {
      st=ST;
      }
      void show()
      {
      cout<<"\n        Examen po: "<<name;
      cout<<"\n            Ozenka:"<<st;
      cout<<"\n";
  }
  void input()
  {
  cout<<"        Examen po: ";cin>>name;
cout<<"         Ozenka: ";cin>>st;
cout<<"\n";
}
protected:
int st;
};

class VYPUSK:public ISPYTANIE
{
    public:
    VYPUSK() {st=0;}
    VYPUSK(int ST){st=ST;}
    VYPUSK(char *NAME,int ST):ISPYTANIE(NAME)
    {
        st=ST;
    }
    void show()
    {
        cout<<"\n  Vypusknoi Examen "<<name;
        cout<<"  Srednyaya ozenka: "<<st;
        cout<<"\n";
    }
    void input()
    {
      cout<<"\n      Vypusknoi Examen : ";cin>>name;
        cout<<"  Srednyaya ozenka: ";cin>>st;
        cout<<"\n";
        }


    protected:
    int st;
};

class TEST:public ISPYTANIE
{
    public:
    TEST() {st=0;}
    TEST(int ST){st=ST;}
    TEST(char* NAME,int ST):ISPYTANIE(NAME)
    {
        st=ST;
    }

    void show()
    {
        cout<<"\n      Testirovanie po: "<<name;
        cout<<"\n  Kolichestvo nabrannyh ballov: "<<st;
        cout<<"\n";
    }
    void input()
    {
        cout<<"     Testirovanie po: "; cin>>name;

cout<<"   Kolichestvo nabrannyh ballov:";cin>>st;
cout<<"\n";
}
protected:
int st;
};

class list
{private:
    ISPYTANIE* begin;
    public:
    list(){begin=0;}
    ~list();
    void insert(ISPYTANIE*);
    void show();
    };
    list::~list()
    {ISPYTANIE* A;
    while(begin!=0)
    {A=begin;
    begin=begin->next;
    delete A;
    }
    }
void list::insert(ISPYTANIE* B)
{
ISPYTANIE* A;
A=begin;
begin=B;
B->next=A;
}
void list::show()
{
ISPYTANIE *A;
A=begin;
while(A!=0)
{
    A->show();
    A=A->next;
    }
    }
 int main()
 {
 //clrscr();
 list list;
 TEST *x1;
 EXAMEN *x2;
VYPUSK *x3;
x1= new TEST;
x2=new EXAMEN;
x3=new VYPUSK;
x1->input();
x2->input();
x3->input();
cout<<"---------------------------------";
list.insert(x3);
list.insert(x2);
list.insert(x1);
list.show();
getch();
}
