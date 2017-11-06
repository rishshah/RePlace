#include <iostream>
#include <algorithm>
using namespace std;

struct skill{
	int s1,s2,s3;
	bool operator< (const skill other){
		if(s1!=other.s1)
			return s1<other.s1;
		else if(s2!=other.s2)
			return s2<other.s2;
		else
			return s3<other.s3;
	}
} s[3];

int main(){
	int t;
	cin >> t;
	for(int i=0; i<t; i++){
		for(int j=0; j<3; j++){
			cin >> s[j].s1 >> s[j].s2 >> s[j].s3; 
		}
		sort(s,s+3);
		if(s[0].s2<=s[1].s2 and s[0].s3<=s[1].s3 and (s[0].s2<s[1].s2 or s[0].s3<s[1].s3 or s[0].s1<s[1].s1) and
		s[1].s2<=s[2].s2 and s[1].s3<=s[2].s3 and (s[1].s2<s[2].s2 or s[1].s3<s[2].s3 or s[1].s1<s[2].s1))
			cout << "yes" << endl;
		else
			cout << "no" << endl;
	}
}