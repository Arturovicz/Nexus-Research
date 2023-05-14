#include "BAPModels.h"
#include <algorithm>
#include <cmath>
#include <vector>
#include <iostream>

using namespace std;

namespace models
{
    float BTSlow(float K, float T, float S0, float r, int N, float u, float d, char opttype)
    {
        float dt = T / N;
        float q = (exp(r * dt) - d) / (u - d);
        float disc = exp(-r * dt);

        std::vector<float> S(N + 1);
        S[0] = S0 * pow(d, N);
        for (int j = 1; j <= N; j++)
        {
            S[j] = u * S[j - 1] / d;
        }

        std::vector<float> C(N + 1);
        for (int j = 0; j <= N; j++)
        {
            C[j] = fmax(0, S[j] - K);
        }

        for (int i = N; i > 0; i--)
        {
            for (int j = 0; j < i; j++)
            {
                C[j] = disc * (q * C[j + 1] + (1 - q) * C[j]);
            }
        }

        return C[0];
    }

    double CRR(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C')
    {
        double dt = T / N;
        double u = exp(sigma * sqrt(dt));
        double d = 1 / u;
        double q = (exp(r * dt) - d) / (u - d);
        double disc = exp(-r * dt);

        double S[N + 1];
        S[0] = S0 * pow(d, N);
        for (int j = 1; j < N + 1; j++)
        {
            S[j] = S[j - 1] * u / d;
        }

        double C[N + 1];
        for (int j = 0; j < N + 1; j++)
        {
            C[j] = max(0.0, S[j] - K);
        }

        for (int i = N; i > 0; i--)
        {
            for (int j = 0; j < i; j++)
            {
                C[j] = disc * (q * C[j + 1] + (1 - q) * C[j]);
            }
        }

        return C[0];
    }

    double JR(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C')
    {

        double dt = T / N;
        double u = exp((r - 0.5 * pow(sigma, 2)) * dt + sigma * sqrt(dt));
        double d = exp((r - 0.5 * pow(sigma, 2)) * dt - sigma * sqrt(dt));
        double q = 0.5;
        double disc = exp(-r * dt);

        double S[N + 1];
        S[0] = S0 * pow(d, N);
        for (int j = 1; j <= N; j++)
        {
            S[j] = u * S[j - 1] / d;
        }

        double C[N + 1];
        for (int j = 0; j <= N; j++)
        {
            C[j] = max(0.0, S[j] - K);
        }

        for (int i = N; i >= 1; i--)
        {
            for (int j = 0; j <= i - 1; j++)
            {
                C[j] = disc * (q * C[j + 1] + (1 - q) * C[j]);
            }
        }

        return C[0];
    }

    double EQP(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C')
    {

        double dt = T / N;
        double nu = r - 0.5 * sigma * sigma;
        double sqrted = sqrt(4 * (sigma * sigma) * dt - 3 * (nu * dt) * (nu * dt));
        double dxu = 0.5 * nu * dt + 0.5 * sqrted;
        double dxd = 1.5 * nu * dt - 0.5 * sqrted;
        double pu = 0.5, pd = 0.5;
        double disc = exp(-r * dt);

        double *S = new double[N + 1];
        S[0] = S0 * exp(N * dxd);
        for (int j = 1; j <= N; j++)
        {
            S[j] = S[j - 1] * exp(dxu - dxd);
        }

        double *C = new double[N + 1];
        for (int j = 0; j <= N; j++)
        {
            C[j] = std::max(0.0, S[j] - K);
        }

        for (int i = N; i >= 1; i--)
        {
            for (int j = 0; j < i; j++)
            {
                C[j] = disc * (pu * C[j + 1] + pd * C[j]);
            }
        }

        double result = C[0];
        delete[] S;
        delete[] C;
        return result;
    }

    double TRG(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C')
    {

        double dt = T / N;
        double nu = r - 0.5 * sigma * sigma;
        double dxu = sqrt((sigma * sigma) * dt + (nu * dt) * (nu * dt));
        double dxd = -dxu;
        double pu = 0.5 * (1 + (nu * dt) / dxu);
        double pd = 1 - pu;
        double disc = exp(-r * dt);

        double *S = new double[N + 1];
        S[0] = S0 * exp(N * dxd); // worst case scenario
        for (int j = 1; j <= N; j++)
        {
            S[j] = S[j - 1] * exp(dxu - dxd);
        }

        double *C = new double[N + 1];
        for (int j = 0; j <= N; j++)
        {
            C[j] = std::max(0.0, S[j] - K);
        }

        for (int i = N; i >= 1; i--)
        {
            for (int j = 0; j < i; j++)
            {
                C[j] = disc * (pu * C[j + 1] + pd * C[j]);
            }
        }

        double result = C[0];
        delete[] S;
        delete[] C;
        return result;
    }

}
