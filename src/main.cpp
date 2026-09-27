#include <iostream>
#include <vector>
#include "segment_tree.h"

void runScenario(const std::string& outFile, void (*fn)(StepLogger&)) {
    StepLogger logger(outFile);
    fn(logger);
}

int main() {
    // Escena 1: build + query + update sobre un arreglo normal
    {
        StepLogger logger("steps_main.json");
        std::vector<int> arr = {2, 4, 5, 7, 8, 9};
        SegmentTree st(arr, logger);

        long long r1 = st.query(1, 4);
        std::cout << "[main] query(1,4) = " << r1 << " (esperado 24)\n";

        st.update(3, 10); // arr[3]: 7 -> 10
        long long r2 = st.query(1, 4);
        std::cout << "[main] tras update(3,10), query(1,4) = " << r2 << " (esperado 27)\n";
    }

    // Escena 2: caso borde - arreglo de un solo elemento
    {
        StepLogger logger("steps_edge_single.json");
        std::vector<int> arr = {42};
        SegmentTree st(arr, logger);
        long long r = st.query(0, 0);
        std::cout << "[edge-single] query(0,0) = " << r << " (esperado 42)\n";
        st.update(0, 100);
        long long r2 = st.query(0, 0);
        std::cout << "[edge-single] tras update(0,100), query(0,0) = " << r2 << " (esperado 100)\n";
    }

    // Escena 3: caso borde - consulta sobre el rango completo
    {
        StepLogger logger("steps_edge_full_range.json");
        std::vector<int> arr = {1, 1, 1, 1, 1, 1, 1, 1};
        SegmentTree st(arr, logger);
        long long r = st.query(0, 7);
        std::cout << "[edge-full-range] query(0,7) = " << r << " (esperado 8)\n";
    }

    return 0;
}
