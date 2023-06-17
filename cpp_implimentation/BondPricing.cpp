#include <cmath>
#include <vector>
#include <iostream>

using namespace std;

double PVB(double Face, double cr, double r, int m, double T)
{

    double BV = 0.;
    int TNC = T * m;
    double cpn = (cr / m) * Face;

    for (int i = 1; i <= TNC; i++)
    {
        double ti = double(i) / double(m);
        BV = BV + cpn * pow((1 + r / m), -ti * m);
    }

    BV = BV + Face * pow((1 + r / m), -T * m);
    return BV;
}

double PVBVectorized(vector<double> bp_period, vector<double> bp_amount, double bp_r)
{
    double PV = 0.0;
    for (int i = 0; i < bp_period.size(); i++)
    {
        PV += bp_amount[i] / pow(1.0 + bp_r, bp_period[i]);
    };
    return PV;
};

int main(int argc, char const *argv[])
{
    double Face = 100;
    double cr = 0.1;
    double rate = 0.1;
    int m = 2;
    double T = 3;

    vector<double> amount;
    amount.push_back(10);
    amount.push_back(10);
    amount.push_back(110);
    vector<double> period;
    period.push_back(1);
    period.push_back(2);
    period.push_back(3);

    cout.setf(ios::fixed);
    cout.precision(2);

    cout << " The Present Value of the Discrete bond is " << PVB(Face, cr, rate, m, T) << '\n';
    cout << " Bond Price is " << PVBVectorized(period, amount, rate) << '\n';
    return 0;
}
