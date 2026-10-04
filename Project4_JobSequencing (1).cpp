// Project 4: Greedy Job Sequencing with Deadlines
// Sort jobs by profit (highest first); put each job in the latest free slot on or
// before its deadline. If no slot is free, the job is rejected.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Job {
    string id;
    int deadline;
    int profit;
};

int main() {
    vector<Job> jobs = {{"J1", 2, 100}, {"J2", 1, 19}, {"J3", 2, 27},
                        {"J4", 1, 25},  {"J5", 3, 15}};

    // Step 1: sort by profit in descending order
    sort(jobs.begin(), jobs.end(),
         [](const Job &a, const Job &b) { return a.profit > b.profit; });

    // Step 2: create slots 1..maxDeadline (all free)
    int maxD = 0;
    for (const Job &j : jobs) maxD = max(maxD, j.deadline);
    vector<string> slot(maxD + 1, "");
    int totalProfit = 0;

    // Step 3: process each job and record the decision path
    cout << "Decision path:\n";
    for (const Job &j : jobs) {
        int t = min(j.deadline, maxD);
        string checks;
        while (t >= 1 && !slot[t].empty()) {  // slot taken, move to an earlier one
            checks += "slot " + to_string(t) + " taken (" + slot[t] + "); ";
            t--;
        }
        cout << "  " << j.id << " (d=" << j.deadline << ", p=" << j.profit << "): "
             << checks;
        if (t >= 1) {
            slot[t] = j.id;
            totalProfit += j.profit;
            cout << "slot " << t << " free -> ACCEPT in slot " << t << "\n";
        } else {
            cout << "no free slot -> REJECT\n";
        }
    }

    cout << "\nFinal schedule: ";
    for (int t = 1; t <= maxD; t++)
        if (!slot[t].empty()) cout << slot[t] << " ";
    cout << "\nTotal profit = " << totalProfit << "\n";
    return 0;
}
