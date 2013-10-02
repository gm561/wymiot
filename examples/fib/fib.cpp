#include <iostream>

using namespace std;

void fib(int n) {
    int n0 = 0,n1 = 1, n2;
    for(int i = 1; i < n; ++i) {
	n2 = n1 + n0;
	n0 = n1;
	n1 = n2;
	cout << n2 << endl;
    }

    cout << n2 ;
}

int main() {
    int n,x;
    cin >> n ;
    while(n--) {
	cin >> x ;
	fib(x);
    }

    return 0;
}
