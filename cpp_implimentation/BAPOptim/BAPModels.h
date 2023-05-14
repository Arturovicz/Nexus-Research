#pragma once

namespace models
{
    float BTSlow(float K, float T, float S0, float r, int N, float u, float d, char opttype);
    double CRR(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C');
    double JR(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C');
    double EQP(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C');
    double TRG(double K, double T, double S0, double r, int N, double sigma, char opttype = 'C');
}