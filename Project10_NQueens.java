/*
 * Project 10: N-Queens Problem using Backtracking (N = 4)
 * Unit IV - Backtracking
 *
 * Prints every placement, every conflict (pruned branch) and every
 * backtrack so the output can be matched with the state space tree.
 */
public class Project10_NQueens {

    static int N = 4;
    static int[] col = new int[N + 1];   // col[r] = column of queen in row r
    static int solutionCount = 0;

    // Check whether a queen can be placed at (row, c)
    static boolean isSafe(int row, int c) {
        for (int r = 1; r < row; r++) {
            if (col[r] == c || Math.abs(col[r] - c) == Math.abs(r - row)) {
                return false;   // same column or same diagonal
            }
        }
        return true;
    }

    static void solve(int row) {
        if (row == N + 1) {
            solutionCount++;
            System.out.println("\n*** Solution " + solutionCount + " found ***");
            printBoard();
            return;
        }
        for (int c = 1; c <= N; c++) {
            if (isSafe(row, c)) {
                col[row] = c;
                System.out.println(indent(row) + "Place queen at (" + row + "," + c + ")");
                solve(row + 1);
                System.out.println(indent(row) + "Backtrack: remove queen from (" + row + "," + c + ")");
                col[row] = 0;
            } else {
                System.out.println(indent(row) + "(" + row + "," + c + ") is NOT safe -> pruned (red node)");
            }
        }
    }

    static String indent(int row) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i < row; i++) sb.append("    ");
        return sb.toString();
    }

    static void printBoard() {
        for (int r = 1; r <= N; r++) {
            for (int c = 1; c <= N; c++) {
                System.out.print(col[r] == c ? " Q " : " . ");
            }
            System.out.println();
        }
        StringBuilder sb = new StringBuilder("Columns by row: (");
        for (int r = 1; r <= N; r++) {
            sb.append(col[r]);
            if (r < N) sb.append(", ");
        }
        System.out.println(sb.append(")"));
    }

    public static void main(String[] args) {
        System.out.println("N-Queens using Backtracking, N = " + N + "\n");
        solve(1);
        System.out.println("\nTotal solutions for N = " + N + ": " + solutionCount);
    }
}
