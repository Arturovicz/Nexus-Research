#include "Models.h"

#include <iostream>
#include <chrono>

using namespace std;
using namespace std::chrono;

int main()
{
    double K = 100;
    double T = 1;
    double S0 = 100;
    double r = 0.05;
    int N = 100;
    double sigma = 0.2;
    float u = 1.1;
    float d = 1 / u;
    char opttype = 'C';

    auto res = models::BTSlow(K, T, S0, r, N, u, d, opttype);

    double (*model_funcs[])(double, double, double, double, int, double, char) = {
        models::TRG,
        models::EQP,
        models::JR,
        models::CRR};

    auto start = high_resolution_clock::now();
    auto res = models::BTSlow(K, T, S0, r, N, u, d, opttype);
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << res << '\n';
    cout << "Time taken by function: " << duration.count() << " milliseconds" << endl;
    for (int i = 0; i < 4; i++)
    {
        auto start = high_resolution_clock::now();
        cout << "Result from model N" << i << ": " << model_funcs[i](K, T, S0, r, N, sigma, opttype) << '\n';
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(stop - start);
        cout << "Time taken by function: " << duration.count() << " milliseconds\n";
    }

    return 0;
}