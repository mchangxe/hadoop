struct Person
{
	char* name_p;
	int age;
	Person** friends;
}; typedef struct Person Person_t

Person_t* create(char* name, int age){
	Person_t* person = (Person_t*) malloc(sizeof(Person_t));
	person->name_p = strdup(name);
	person->age = age;
}

vod destroy(Person_t* person){
	free(person->name_p);
	memset(person, 0, sizeof(Person_t)); 
	free(person);
	person = NULL;
}

int main(void){
	Person_t *smith = (Person_t*) malloc(sizeof(Person_t));
	strcpy(smith->name_p, "Agent Smith");
	smith->age = 128;
	Person_t* sonny = (Person_t*) malloc(sizeof(Person_t));
	strcpy(sonny->name_p, "Sonny Moore");
	sonny->age = 256;
	smith->friends = &sonny;
	sonny->friends = &smith;
	return 0;
}