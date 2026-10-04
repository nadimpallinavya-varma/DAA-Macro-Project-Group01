// Project 4: Greedy Job Sequencing with Deadlines
// Strategy: sort jobs by profit (descending); place each job in the latest free
// slot on or before its deadline. If no slot is free, reject the job.
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

    // Step 1: sort by profit, highest first
    sort(jobs.begin(), jobs.end(),
         [](const Job &a, const Job &b) { return a.profit > b.profit; });

    int maxDeadline = 0;
    for (const Job &j : jobs) maxDeadline = max(maxDeadline, j.deadline);

    vector<string> slot(maxDeadline + 1, "");  // slot[1..maxDeadline]
    int totalProfit = 0;

    cout << "Decision path:\n";
    for (const Job &j : jobs) {
        int t = min(j.deadline, maxDeadline);
        while (t >= 1 && !slot[t].empty()) t--;  // look for latest free slot
        if (t >= 1) {
            slot[t] = j.id;
            totalProfit += j.profit;
            cout << "  " << j.id << " (d=" << j.deadline << ", p=" << j.profit
                 << ") -> ACCEPTED in slot " << t << "\n";
        } else {
            cout << "  " << j.id << " (d=" << j.deadline << ", p=" << j.profit
                 << ") -> REJECTED (no free slot)\n";
        }
    }

    cout << "\nFinal schedule: ";
    for (int t = 1; t <= maxDeadline; t++)
        if (!slot[t].empty()) cout << slot[t] << " ";
    cout << "\nTotal profit = " << totalProfit << "\n";
    return 0;
}
